import pandas as pd
from pandas import ExcelWriter
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
import time
import pymzml
import scipy.signal
from scipy.interpolate import interp1d
from scipy.spatial import KDTree
from scipy.stats import zscore
from numpy import where, argmin, zeros
from glob import glob
import numpy as np
from molmass import Formula
import os
import json
from tqdm.auto import tqdm
from multiprocessing import Pool, cpu_count
from scipy.stats import ttest_ind
from sklearn.decomposition import PCA
from sklearn import preprocessing
import scipy.stats as st
from scipy import integrate
import itertools
import bisect
import re
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import networkx as nx
import shutil
from datetime import datetime
import inspect
import traceback
from scipy.stats import pearsonr
import warnings
from fake_useragent import UserAgent  # 更新pyhrms的时候，记得安装fake_useragent
import math
import gc
from scipy.optimize import curve_fit, fsolve

warnings.filterwarnings("ignore")


"""
# 20250314
(1) 更新了one_step_process_DDA解决了一个引用错误，‘precursor’
(2) 更新了database match算法，如果processors=1，就不用并行，应为jupyter可能不兼容
(3) 增加了summarize_result_export
(4) 修复了summarize_rsult_concat里的bug，读取excel时候去掉了index_col = 'Unnamed: 0'
========================================================================================================
1. basic function
========================================================================================================
"""


atom_mass_table = pd.Series(
    data={'C': 12.000000, 'Ciso': 13.003355, 'N': 14.003074, 'Niso': 15.000109, 'O': 15.994915, 'H': 1.007825,
          'Oiso': 17.999159, 'F': 18.998403, 'K': 38.963708, 'P': 30.973763, 'Cl': 34.968853,
          'Cliso': 36.965903, 'S': 31.972072, 'Siso': 33.967868, 'Br': 78.918336, 'Na': 22.989770,
          'Si': 27.976928, 'Fe': 55.934939, 'Se': 79.916521, 'As': 74.921596, 'I': 126.904477, 'D': 2.014102,
          'Co': 58.933198, 'Au': 196.966560, 'B': 11.009305, 'e': 0.0005486, 'Cr': 51.996, 'Sn': 111.904826,
          'Ag': 106.905095, 'Hg': 195.965812, 'Li': 6.015123
          })


def adducts_type_converter(adduct_type):
    adducts_type_dict = {
        '[M+H]+': '+H',
        '[M+Na]+': '+Na',
        '[M+NH4]+': '+NH4',
        '[M+K]+': '+K',
        '[M-H2O+H]+': '-H2O+H',
        'M+H': '+H',
        '[M]+': '+',
        'M+Na': '+Na',
        '[M-H]-': '-H',
        '[M+H]-': '-H',
        '[M+FA-H]-': '+HCOO',
        '[M+CH3COO]-': '+CH3COO',
        '[M-H]1-': '-H',
        '[M+CH3COOH-H]-': '+CH3COO',
        '[M+HCOO]-': '+HCOO',
        '[M+Cl]-': '+Cl'
    }
    if adduct_type in adducts_type_dict.keys():
        new_adduct_type = adducts_type_dict[adduct_type]
    else:
        new_adduct_type = None
    return new_adduct_type


def isotope_score(iso_info, formula, mode='pos', i_threshold=2, error=0.015, adducts_type=None):
    """
    Calculate the isotope matching score by comparing observed isotope distributions
    with theoretically generated distributions for a given molecular formula and
    ionization mode/adduct.

    The function:
    1. Determines the appropriate ion adduct based on `mode` or `adducts_type`.
    2. Generates a theoretical isotope distribution for the modified formula.
    3. Filters out theoretical peaks below a given intensity threshold.
    4. Matches observed peaks to theoretical peaks within a specified mass error.
    5. Computes a score indicating how closely the observed distribution matches
       the theoretical one.

    Args:
        iso_info (dict): Observed isotope data, where keys are m/z values (float)
                         and values are intensities (float).
        formula (str): The molecular formula (e.g., 'C13H13N3').
        mode (str, optional): Ionization mode, 'pos' for positive or 'neg' for
                              negative. Determines the default adduct if `adducts_type`
                              is not provided. Defaults to 'pos'.
        i_threshold (float, optional): Minimum intensity threshold for including
                                       theoretical isotopes in the comparison.
                                       Defaults to 2(%).
        error (float, optional): Mass error tolerance (in Da) for peak matching.
                                 Defaults to 0.015.
        adducts_type (str, optional): Specifies the exact adduct type (e.g., '[M+H]+',
                                      '[M+Na]+', '[M+K]+', 'M+', 'M-', '[M-H]-', '[M+Cl]-').
                                      If not provided, defaults to '+H' for 'pos' and '-H'
                                      for 'neg'.

    Returns:
        float: The isotope matching score, rounded to three decimal places. A higher
               score (closer to 1.0) indicates a better match between observed and
               theoretical isotope distributions.
    """
    adduct = adducts_type_converter(adducts_type)
    if adduct is None:
        adduct = '+H' if mode == 'pos' else '-H'
    
    isotopes, distribution = formula_to_distribution(formula, adducts=adduct, num=5)
    
    # Filter isotopes and distribution based on the intensity threshold
    valid_indices = np.where(distribution > i_threshold)
    isotopes = isotopes[valid_indices]
    distribution = distribution[valid_indices]
    
    # Normalizing the distribution
    distribution_normalized = distribution / np.max(distribution)
    
    # Calculate target distribution
    target_distribution = np.zeros_like(distribution_normalized)
    for i, isotope in enumerate(isotopes):
        for k, v in iso_info.items():
            if (k < isotope + error) & (k > isotope - error):
                target_distribution[i] = v
                break
    
    # Calculate the score
    diff = target_distribution - distribution_normalized
    score = 1 - np.sum(np.abs(diff)) / sum(distribution_normalized)
    return round(score, 3)


def formula_to_distribution(formula, adducts='+H', num=5):
    """
    根据给定的分子式和离子加合物生成同位素分布。

    首先根据加合物修改分子式，然后计算电荷状态。

    参数:
        formula (str): 分子式，例如 'C13H13N3'。
        adducts (str): 离子加合物，支持以下选项：
            正离子模式:
                '+H'       : 增加一个H原子
                '+Na'      : 增加一个Na原子
                '+K'       : 增加一个K原子
                '+Cl'      : 增加一个Cl原子（带正电的复合离子情况较少见，此处按要求处理）
                '+NH4'     : 增加一个NH4基团
                '+HCOO'    : 增加一个HCOO基团
                '+CH3COO'  : 增加一个CH3COO基团
                '+'        : 不添加任何元素，仅带正电
            负离子模式:
                '-H'       : 减少一个H原子
                '-H2O+H'   : 减少一个H2O分子并增加一个H原子
                '-'        : 不添加任何元素，仅带负电
        num (int): 返回的同位素峰数量。

    返回:
        mz_iso (np.array): 同位素的质荷比 (m/z) 值。
        i_iso (np.array): 同位素的相对强度（归一化到最大强度为100）。
    """
    
    # 根据adduct修饰formula
    f = Formula(formula)
    # 定义电子质量
    electron_mass = 0.00054858
    comp = f.composition()
    comp_dict = {elem[0]: elem[1] for elem in comp}
    
    # 根据adduct对formula进行修正
    # 为简单起见，这里假设formula中有足够的H以支持'-H'操作。
    # 如果需要更严格的控制，需要先检查Formula中的H数量再进行减法。
    if adducts == '+H':
        f = f + Formula('H')
    elif adducts == '-H':
        # 确保有H可减
        if comp_dict.get('H', 0) > 0:
            f = f - Formula('H')
        else:
            raise ValueError("Not enough H in the original formula to remove.")
    elif adducts == '+Na':
        f = f + Formula('Na')
    elif adducts == '+Cl':
        f = f + Formula('Cl')
    elif adducts == '+K':
        f = f + Formula('K')
    elif adducts == '+NH4':
        f = f + Formula('NH4')
    elif adducts == '+HCOO':
        f = f + Formula('HCOO')
    elif adducts == '+CH3COO':
        f = f + Formula('CH3COO')
    elif adducts == '-H2O+H':
        f = f - Formula('H2O')
        f = f + Formula('H')
    # 如果是'+'或者'-'不对分子式进行变化
    
    # 计算同位素分布
    a = f.spectrum()
    mz_iso, i_iso = np.array([vals for vals in a.values()]).T
    
    # 强度归一化
    i_iso = i_iso / max(i_iso) * 100
    
    # 判断离子模式：正离子或负离子
    # 把正离子adduct放在一起判断，负离子adduct放在一起判断
    if adducts in ['+', '+H', '+Na', '+K', '+NH4', '-H2O+H']:
        # 正离子模式：mz_iso需要减去电子质量
        mz_iso -= electron_mass
    elif adducts in ['-', '-H', '+Cl', '+HCOO', '+CH3COO']:
        # 负离子模式：mz_iso需要加上电子质量
        mz_iso += electron_mass
    
    # 保留合理精度
    mz_iso = mz_iso.round(6)
    i_iso = i_iso.round(3)
    
    # 对同位素峰排序并取前num个最丰度的峰
    s1 = pd.Series(data=i_iso, index=mz_iso).sort_values(ascending=False)
    return s1.index.values[:num], s1.values[:num]


def suspect_screen(unique_cmps, database, mode, ms1_error=5, ms2_error=0.015, rt_error=0.1, iso_score=0.7,
                   precursor_window=2,
                   similarity_thresholod=0.8):
    """
    Perform suspect screening of compounds against a suspect database based on precursor m/z, RT, and MS/MS spectral similarity.

    This function iterates over each compound in `unique_cmps` and attempts to find a matching record in the `suspect_db`
    that falls within the specified mass (ms1_error), retention time (rt_error), and MS/MS similarity thresholds. For
    each matched suspect candidate, it compares the observed MS2 fragments to those in the database, selecting matches
    that exceed a certain similarity threshold. The best matching fragment information, including similarity score
    and fragment count, is recorded back into `unique_cmps`.

    Parameters
    ----------
    unique_cmps : pandas.DataFrame
        A DataFrame containing unique compounds with their m/z and RT, as well as MS2 spectra at different collision energies.
    suspect_db : pandas.DataFrame
        A suspect database DataFrame that includes precursor masses, compound names, CAS numbers, and associated MS2 spectra.
    ms1_error : float, optional
        The tolerance (in ppm) allowed for precursor mass matching. Default is 5.
    ms2_error : float, optional
        The m/z tolerance (in Da) for matching individual fragment ions between observed and database MS2 spectra. Default is 0.015.
    rt_error : float, optional
        The retention time tolerance allowed for matching compounds in suspect_db. Default is 0.1.
    iso_score : float, optional
        The isotope pattern score threshold. This parameter may be used upstream or downstream for filtering; its role
        is not fully illustrated here. Default is 0.7.
    score : float, optional
        The overall similarity score threshold for considering a match to be significant. Default is 0.8.

    Returns
    -------
    pandas.DataFrame
        The updated `unique_cmps` DataFrame with additional columns that record the best hit from the suspect database,
        including matched compound names, CAS numbers, similarity scores, fragment counts, and detailed matched results.
    """
    suspect_db = database[database['mode'] == mode].reset_index(drop=True)
    
    DDA_columns = [i for i in unique_cmps.columns if 'MS2_spec_DDA' in i]
    for i in tqdm(range(len(unique_cmps)), desc='Suspect_screening'):
        if 'collision energy' in unique_cmps.columns:
            DDA_CE = unique_cmps.loc[i, 'collision energy']
        else:
            DDA_CE = None
        
        # 1. 开始便利，每一个entry
        precursor = float(unique_cmps.loc[i, 'mz'])
        rt = float(unique_cmps.loc[i, 'rt'])
        # 2. 每一个都在suspect数据库中找一下
        matched_result = suspect_db[(suspect_db['Precursor'] >
                                     precursor * (1 - ms1_error * 1e-6)) & (
                                            suspect_db['Precursor'] < precursor * (
                                            1 + ms1_error * 1e-6))].copy().reset_index(drop=True)
        
        # 3. 如果匹配到了
        if len(matched_result) > 0:
            # 4. 针对每一个碰撞能的数据
            final_result = []
            for DDA_column in DDA_columns:  # 不同碰撞能
                measured_spec_dict = eval(unique_cmps.loc[i, DDA_column])
                if len(measured_spec_dict) > 0:  # 只有>0才需要继续下面的匹配
                    for j in range(len(matched_result)):  # 如果有多个结果，都要考虑到
                        db_ms2_spec_info = eval(matched_result.loc[j, 'ms2_spec'])
                        name = matched_result.loc[j, 'Name']
                        CAS = matched_result.loc[j, 'CAS']
                        ik = matched_result.loc[j, 'Inchikey']
                        db_rt = matched_result.loc[j, 'Retention Time']
                        if str(db_rt) == 'nan':
                            rt_error = np.nan
                        elif isinstance(db_rt, float) and db_rt > 0:
                            rt_error = rt - db_rt
                        else:
                            rt_error = np.nan
                        for ce, single_spec_info in db_ms2_spec_info.items():
                            single_match_info = {}
                            db_matched_spec_dict = eval(single_spec_info)
                            # 5. 开始比对质谱图
                            result = calculate_similarity_score(measured_spec_dict, db_matched_spec_dict, precursor,
                                                                ms2_error=ms2_error, precursor_window=precursor_window)
                            if result['similarity_score'] > similarity_thresholod:  # 只选择那些高分数的
                                single_match_info['name'] = name
                                single_match_info['CAS'] = CAS
                                single_match_info['ik'] = ik
                                single_match_info['Instrumental_CE'] = DDA_column.split('_')[
                                    -1] if DDA_CE is None else DDA_CE
                                single_match_info['Database_CE'] = ce
                                single_match_info['similarity_score'] = round(result['similarity_score'], 3)
                                single_match_info['frag_num'] = len(result['matched_fragments']['obs'])
                                single_match_info['Detailed_info'] = str(result['matched_fragments'])
                                single_match_info['raw_measured_spec_dict'] = str(measured_spec_dict)
                                single_match_info['raw_database_spec_dict'] = str(db_matched_spec_dict)
                                single_match_info['rt_error'] = rt_error
                                # 组装完成后添加到final_result中
                                final_result.append(single_match_info)
            if len(final_result) > 0:
                unique_cmps.loc[i, 'Matched_result'] = str(final_result)
                unique_cmps.loc[i, 'Matched_cmp_num'] = len(set([i['name'] for i in final_result]))
                best_hit = sorted(final_result, key=lambda x: x['frag_num'], reverse=True)[0]
                unique_cmps.loc[i, 'Best_hit_name'] = best_hit['name']
                unique_cmps.loc[i, 'CAS'] = best_hit['CAS']
                unique_cmps.loc[i, 'similarity_score'] = best_hit['similarity_score']
                unique_cmps.loc[i, 'frag_num'] = best_hit['frag_num']
                unique_cmps.loc[i, 'ik'] = best_hit['ik']
                unique_cmps.loc[i, 'Detailed_info'] = best_hit['Detailed_info']
                unique_cmps.loc[i, 'raw_measured_spec_dict'] = best_hit['raw_measured_spec_dict']
                unique_cmps.loc[i, 'raw_database_spec_dict'] = best_hit['raw_database_spec_dict']
                unique_cmps.loc[i, 'Instrumental_CE'] = best_hit['Instrumental_CE']
                unique_cmps.loc[i, 'Database_CE'] = best_hit['Database_CE']
                unique_cmps.loc[i, 'rt_error'] = best_hit['rt_error']
    
    return unique_cmps


def calculate_similarity_score(obs_spec, db_spec, precursor, ms2_error=0.015, precursor_window=2.0):
    """
    Calculate the similarity score between observed and database MS/MS spectra.

    This function compares an observed MS/MS spectrum (`obs_spec`) with a reference database spectrum (`db_spec`)
    to determine their similarity. It first filters out peaks above a specified precursor mass window, normalizes
    intensities, and then attempts to find the best matching observed fragments for each database fragment ion
    within a specified mass tolerance. If multiple observed peaks fall within the tolerance, the one with the
    highest intensity is chosen. A cosine similarity metric is used to compute the final similarity score.

    Parameters
    ----------
    obs_spec : dict
        The observed MS/MS spectrum, given as a dictionary {mz: intensity, ...}.
    db_spec : dict
        The database MS/MS spectrum, given as a dictionary {mz: intensity, ...}.
    precursor : float
        The precursor m/z value for the spectra.
    ms2_error : float, optional
        The mass tolerance (in Da) for matching fragment ions. Default is 0.015.
    precursor_window : float, optional
        The window (in Da) below the precursor mass within which peaks are retained. Any peak
        >= (precursor - precursor_window) is discarded before similarity calculation. Default is 2.0.

    Returns
    -------
    dict
        A dictionary with:
        - "similarity_score" : float
          The calculated similarity score between the two spectra (0 to 1).
        - "matched_fragments" : dict
          A dictionary containing matched fragment information:
          {
            "obs": {mz: intensity, ...} of matched observed fragments,
            "db" : {mz: intensity, ...} of matched database fragments
          }
    """
    
    # 将字典转换为列表并按m/z排序
    obs_list = sorted(obs_spec.items(), key=lambda x: x[0])  # [(mz, intensity), ...]
    db_list = sorted(db_spec.items(), key=lambda x: x[0])
    
    # 过滤掉 >= precursor - precursor_window 的峰
    obs_list = [(m, i) for (m, i) in obs_list if m < (precursor - precursor_window)]
    db_list = [(m, i) for (m, i) in db_list if m < (precursor - precursor_window)]
    
    if not obs_list or not db_list:
        return {
            "similarity_score": 0.0,
            "matched_fragments": {
                "obs": {},
                "db": {}
            }
        }
    
    # 归一化函数
    def normalize_spectrum(spec_list):
        if not spec_list:
            return spec_list
        max_intensity = max(i for _, i in spec_list)
        return [(m, i / max_intensity) for m, i in spec_list]
    
    obs_norm = normalize_spectrum(obs_list)
    db_norm = normalize_spectrum(db_list)
    
    # 为了在obs_norm中快速找到候选峰，我们创建一个单独的m/z列表以供查找
    obs_mzs = [p[0] for p in obs_norm]
    
    matched_obs_ints = []
    matched_db_ints = []
    matched_obs_indices = []
    matched_db_indices = []
    
    # 对于每个db峰，在obs中寻找所有候选峰并挑选强度最高的进行匹配
    for db_idx, (mz_db, int_db) in enumerate(db_norm):
        # 使用bisect在obs_mzs中找到mz_db应插入的位置
        pos = bisect.bisect_left(obs_mzs, mz_db)
        
        # 在pos附近搜索满足 |mz_obs - mz_db| <= ms2_error 的峰
        candidates = []
        
        # 向左扩展
        l = pos - 1
        while l >= 0 and (mz_db - obs_mzs[l]) <= ms2_error:
            if abs(obs_mzs[l] - mz_db) <= ms2_error:
                candidates.append((l, obs_norm[l]))
            l -= 1
        
        # 向右扩展
        r = pos
        while r < len(obs_norm) and (obs_mzs[r] - mz_db) <= ms2_error:
            if abs(obs_mzs[r] - mz_db) <= ms2_error:
                candidates.append((r, obs_norm[r]))
            r += 1
        
        # 如果没有候选则继续下一个db峰
        if not candidates:
            continue
        
        # 从候选中找到强度最高的obs峰
        # candidates中元素形式 (index_in_obs_norm, (mz_obs, int_obs_normalized))
        best_candidate = max(candidates, key=lambda x: x[1][1])  # 按强度排序
        best_obs_idx, (best_mz_obs, best_int_obs) = best_candidate
        
        # 匹配成功，记录
        matched_obs_ints.append(best_int_obs)
        matched_db_ints.append(int_db)
        matched_obs_indices.append(best_obs_idx)
        matched_db_indices.append(db_idx)
    
    if not matched_obs_ints or not matched_db_ints:
        return {
            "similarity_score": 0.0,
            "matched_fragments": {
                "obs": {},
                "db": {}
            }
        }
    
    # 计算余弦相似度
    dot_product = sum(o * d for o, d in zip(matched_obs_ints, matched_db_ints))
    obs_mag = (sum(o ** 2 for o in matched_obs_ints)) ** 0.5
    db_mag = (sum(d ** 2 for d in matched_db_ints)) ** 0.5
    similarity = dot_product / (obs_mag * db_mag) if (obs_mag > 0 and db_mag > 0) else 0.0
    
    # 将匹配结果还原为原始值（未归一化前）
    # matched_obs_indices 和 matched_db_indices 对应 obs_list, db_list
    matched_obs_dict = {obs_list[idx][0]: obs_list[idx][1] for idx in matched_obs_indices}
    matched_db_dict = {db_list[idx][0]: db_list[idx][1] for idx in matched_db_indices}
    
    result = {
        "similarity_score": similarity,
        "matched_fragments": {
            "obs": matched_obs_dict,
            "db": matched_db_dict
        }
    }
    return result


def one_step_process(path, company, profile=True, control_group=['lab_blank', 'methanol'], filter_type=1, threshold=10,
                     i_threshold=200, SN_threshold=3, peak_width=1, area_threshold=500, height_threshold=500,
                     rt_error_alignment=0.05,
                     mz_error_alignment=0.015, mz_overlap=1, ms2_analysis=True, frag_rt_error=0.02, split_n=20,
                     rt_overlap=1,
                     sat_intensity=False, long_rt_split_n=1, step_size=0.02, orbi=False, max_frag_num=50):
    """
    This function uses one processor to process mzML data and perform a comparison between the sample set and the control set. The resulting data will be used to generate an Excel file that summarizes the differences between the two sets.

    Args:
        path (str): The file path for the mzML files that will be processed. For example, '../Users/Desktop/my_HRMS_files'.
        company (str): The type of mass spectrometer used to acquire the data. Valid options are 'Waters', 'Thermo', 'Sciex', and 'Agilent'.
        profile (bool): Indicates whether the data is in profile or centroid mode. True for profile mode, False for centroid mode.
        control_group (List[str]): A list of labels representing the control group. These labels are used in the search for relevant file names.
        filter_type (int): Determines the mode of operation.
            - 1: For data without triplicates; fold change is computed as the ratio of the sample area to the maximum control area.
            - 2: For data with triplicates; the function will calculate p-values, and fold change is computed as the ratio of the mean sample area to the mean control area.
        threshold (int): The threshold value for peak detection.
        i_threshold (int): The intensity threshold for peak detection.
        SN_threshold (int): The signal-to-noise threshold for peak detection.
        peak_width (float): The peak width for chromatographic peak detection.
        area_threshold (float): The minimum peak area threshold. Peaks with an area below this threshold will be excluded from analysis.
        height_threshold (float): The minimum peak height threshold. Peaks with a height below this threshold will be excluded from analysis.
        rt_error_alignment (float): The retention time error tolerance for alignment.
        mz_error_alignment (float): The m/z error tolerance for alignment.
        mz_overlap (float): The m/z overlap threshold.
        ms2_analysis (bool): Indicates whether to perform DIA fragment analysis. True to enable DIA fragment analysis, False to disable it.
        frag_rt_error (float): The retention time error tolerance for fragment MS2 analysis.
        split_n (int): The number of pieces to split the large dataframe.
        rt_overlap (float): The retention time overlap threshold.
        sat_intensity (bool): Indicates whether to consider saturation intensity. False to disable.
        long_rt_split_n (int): The number of pieces to split the MS1 data.
        step_size (float): Step size for data processing.
        orbi (bool): Indicates whether the data is in orbitrap data (True) or TOF-MS data (False).
        max_frag_num (int): Maximum number of fragments to consider in MS2 analysis.

    Returns:
        None. Generates Excel files that summarize the differences between the control sets and sample sets.
    """
    
    print('                                                                            ')
    print('============================================================================')
    print('First process...')
    print('============================================================================')
    print('                                                                            ')
    
    move_files(path)
    # Log function details
    func_name = inspect.currentframe().f_code.co_name
    func_params = inspect.getargvalues(inspect.currentframe()).locals
    log_function_details(path, func_name, func_params)
    
    files_mzml = glob(os.path.join(path, '*.mzML'))
    files_mzml_DDA = [file for file in files_mzml if 'DDA' in os.path.basename(file)]
    files_mzml = [file for file in files_mzml if 'DDA' not in os.path.basename(file)]
    for j, file in enumerate(files_mzml):
        first_process(file, company=company, profile=profile, control_group=control_group, threshold=threshold,
                      i_threshold=i_threshold,
                      SN_threshold=SN_threshold, peak_width=peak_width, area_threshold=area_threshold,
                      height_threshold=height_threshold,
                      rt_error_alignment=rt_error_alignment, mz_error_alignment=mz_error_alignment,
                      mz_overlap=mz_overlap,
                      ms2_analysis=ms2_analysis, frag_rt_error=frag_rt_error, split_n=split_n,
                      sat_intensity=sat_intensity,
                      long_rt_split_n=long_rt_split_n, rt_overlap=rt_overlap, step_size=step_size, orbi=orbi,
                      message=f'No. {j + 1} : ', max_frag_num=max_frag_num)
    
    # 检查是否有遗漏的
    files_excel_temp = glob(os.path.join(path, '*.xlsx'))
    files_excel_names = [os.path.basename(i)[:-5] for i in files_excel_temp]
    path_omitted = []
    if len(files_mzml) > len(files_excel_names):
        # 检查是哪个文件漏掉了
        for path1 in files_mzml:
            if os.path.basename(path1)[:-5] in files_excel_names:
                pass
            else:
                path_omitted.append(path1)
    if len(path_omitted) == 0:
        pass
    else:
        for file in path_omitted:
            first_process(file, company=company, profile=profile, control_group=control_group, threshold=threshold,
                          i_threshold=i_threshold,
                          SN_threshold=SN_threshold, peak_width=peak_width, area_threshold=area_threshold,
                          height_threshold=height_threshold,
                          rt_error_alignment=rt_error_alignment, mz_error_alignment=mz_error_alignment,
                          mz_overlap=mz_overlap,
                          ms2_analysis=ms2_analysis, frag_rt_error=frag_rt_error, split_n=split_n,
                          sat_intensity=sat_intensity,
                          long_rt_split_n=long_rt_split_n, rt_overlap=rt_overlap, step_size=step_size, orbi=orbi,
                          max_frag_num=max_frag_num)
    
    # 中间过程
    files_excel = glob(os.path.join(path, '*.xlsx'))
    peak_alignment(files_excel, rt_error=rt_error_alignment, mz_error=mz_error_alignment)
    ref_all = pd.read_excel(os.path.join(path, 'peak_ref.xlsx'), index_col='Unnamed: 0')
    
    # 第二个过程
    print('                                                                            ')
    print('============================================================================')
    print('Second process...')
    print('============================================================================')
    print('                                                                            ')
    for j, file in enumerate(files_mzml):
        second_process(file, ref_all, company, profile=profile, long_rt_split_n=long_rt_split_n, orbi=orbi,
                       message=f'No. {j + 1} ')
    
    # 第三个过程, 做fold change filter
    print('                                                                            ')
    print('============================================================================')
    print('Third process...')
    print('============================================================================')
    print('                                                                            ')
    
    fold_change_filter(path, control_group=control_group, filter_type=filter_type)
    
    # 如果有DDA，将DDA数据加入到excel里
    DDA_to_DIA_result(path, company, profile)


def one_step_process_DDA(path, company, profile=True, i_threshold=200, orbi=False, control_group=['methanol'],
                         filter_type=1):
    """
    Only process DDA data. This function using one processor to process mzML data and perform a comparison between the sample set and the control set. The resulting data will be used to generate an Excel file that summarizes the differences between the two sets.
    Args:
       - path: The file path for the mzML files that will be processed. For example, '../Users/Desktop/my_HRMS_files'.
       - company: The type of mass spectrometer used to acquire the data. Valid options are 'Waters', 'Thermo', 'Sciex', and 'Agilent'.
       - profile: A Boolean value that indicates whether the data is in profile or centroid mode. True for profile mode, False for centroid mode.
       - control_group (List[str]): A list of labels representing the control group.These labels are used in the search for relevant file names.
       - i_threshold (int): Threshold for mass peak intensity.
       - filter_type (int): Determines the mode of operation.
                           Set to 1 for data without triplicates; fold change is computed
                           as the ratio of the sample area to the maximum control area.
                           Set to 2 for data with triplicates; the function will calculate p-values,
                           and fold change is computed as the ratio of the mean sample area
                           to the mean control area.
       - orbi: A boolean indicating whether the data is in orbitrap data (True) or TOF-MS data (False)
    returns:
        None.Generate Excel files that summarizes the differences between the control sets and sample sets.

    """
    move_files(path)
    # Log function details
    func_name = inspect.currentframe().f_code.co_name
    func_params = inspect.getargvalues(inspect.currentframe()).locals
    log_function_details(path, func_name, func_params)
    files_mzml = glob(os.path.join(path, '*.mzML'))
    
    # 第一步，生成文件
    for i, file in enumerate(files_mzml):
        message = f'No. {i + 1}: '
        ms1, ms2 = sep_scans(file, company, message=message)
        DDA_df = gen_DDA_ms2_df(ms1, ms2, i_threshold=i_threshold, profile=profile, opt=False, more_info=True,
                                message=message)
        DDA_df.loc[:, 'mz'] = DDA_df['precursor']
        DDA_df = DDA_df.drop(columns='precursor')
        DDA_df.loc[:, 'iso_distribution'] = DDA_df.loc[:, 'iso_distribution'].astype(str)
        DDA_df = DDA_df[DDA_df['frag'].apply(len) != 0].reset_index(drop=True)
        DDA_df.loc[:, 'frag'] = DDA_df.loc[:, 'frag'].astype(str)
        DDA_df.to_excel(file.replace('.mzML', '.xlsx'))
    
    # 做alignment
    files_excel = glob(os.path.join(path, '*.xlsx'))
    peak_alignment(files_excel, rt_error=0.1, mz_error=0.015)
    ref_all = pd.read_excel(os.path.join(path, r'peak_ref.xlsx'))
    # 第二步骤
    for i, file in enumerate(files_mzml):
        message = f'No. {i + 1}: '
        second_process(file, ref_all, company, profile=profile, orbi=orbi, message=message)
    
    # 第三步
    fold_change_filter(path, control_group=control_group, filter_type=filter_type)
    
    # 解决删除相同alignment数据的问题
    unique_files = [i for i in glob(os.path.join(path, '*.xlsx')) if 'unique_cmps' in os.path.basename(i)]
    for unique_file in unique_files:
        unique = pd.read_excel(unique_file)
        first_file = unique_file.replace('_unique_cmps.xlsx', '.xlsx')
        if os.path.exists(first_file):
            first = pd.read_excel(first_file)
            data_all = []
            for i in range(len(unique)):
                # precursor = unique.loc[i, 'precursor']
                # rt = first.loc[i, 'rt']
                new_index = unique.loc[i, 'new_index']
                rt1 = eval(new_index.split('_')[0])
                mz1 = eval(new_index.split('_')[1])
                
                fold_change_names = [j for j in unique.loc[i].index if 'old_change' in j]
                fold_change_values = [unique.loc[i, j] for j in fold_change_names]
                first1 = first[(first['rt'] >= rt1 - 0.1) & (first['rt'] <= rt1 + 0.1
                                                             ) & (first['mz'] >= mz1 - 0.015) & (
                                       first['mz'] <= mz1 + 0.015)].copy()
                first1.loc[:, 'new_index'] = new_index
                for n, fold_change_name in enumerate(fold_change_names):
                    first1.loc[:, fold_change_name] = fold_change_values[n]
                
                # 存起来
                data_all.append(first1)
            final_unique_DDA = pd.concat(data_all, axis=0)
            final_unique_DDA = remove_unnamed_columns(final_unique_DDA.drop_duplicates(subset='rt')).reset_index(
                drop=True)
            final_unique_DDA.to_excel(unique_file)


def ultimate_peak_picking(ms1, profile=True, split_n=20, threshold=10, i_threshold=500, SN_threshold=3, peak_width=1,
                          area_threshold=500,
                          height_threshold=500, noise_threshold=0, rt_error_alignment=0.05, mz_error_alignment=0.015,
                          mz_overlap=1,
                          sat_intensity=False, long_rt_split_n=1, rt_overlap=1, orbi=False, step_size=0.02, message='',
                          isotope_analysis=True):
    """
    Find peaks in the original ms1 list, analyze isotope and adduct information, and return a dataframe with
    information on the peaks including retention time, m/z value, intensity, and area.

    Args:
        ms1 (scan list): List of MS1 scans generated from sep_scans(file.mzML).
        profile (bool): Indicates whether the data is in profile mode (True) or centroid mode (False).
        split_n (int): The number of pieces to split the large dataframe.
        threshold (int): Threshold for finding peaks.
        i_threshold (int): Threshold for peak intensity.
        SN_threshold (float): Signal-to-noise threshold.
        peak_width (float): The peak width for chromatographic peak detection.
        area_threshold (float): The minimum peak area threshold. Peaks with an area below this threshold will be excluded from analysis.
        height_threshold (float): The minimum peak height threshold. Peaks with a height below this threshold will be excluded from analysis.
        noise_threshold (float): The noise threshold for peak detection.
        rt_error_alignment (float): Retention time error alignment threshold.
        mz_error_alignment (float): m/z error alignment threshold.
        mz_overlap (float): The m/z overlap (Da) between adjacent sections of data when splitting it.
        sat_intensity (bool): Indicates whether to consider saturation intensity. False to disable.
        long_rt_split_n (int): The number of pieces to split the ms1 data.
        rt_overlap (float): The retention time overlap (min) between adjacent sections of data when splitting it.
        orbi (bool): Indicates whether the data is in orbitrap data (True) or TOF-MS data (False).
        step_size (float): Step size for data processing.
        message (str): A message to display during processing.

    Returns:
        pandas.DataFrame: A dataframe with information on the peaks including retention time, m/z value, intensity, and area.
    """
    
    if long_rt_split_n == 1:
        peak_all = split_peak_picking(ms1, profile=profile, split_n=split_n, threshold=threshold, peak_width=peak_width,
                                      i_threshold=i_threshold, SN_threshold=SN_threshold,
                                      noise_threshold=noise_threshold,
                                      rt_error_alignment=rt_error_alignment, mz_error_alignment=mz_error_alignment,
                                      mz_overlap=mz_overlap, sat_intensity=sat_intensity, orbi=orbi,
                                      message=message, isotope_analysis=isotope_analysis)
    else:
        # Calculate the length of each part
        total_spectra = len(ms1)
        part_length = total_spectra // long_rt_split_n
        overlap_spectra = int(rt_overlap / (ms1[1].scan_time[0] - ms1[0].scan_time[
            0]))  # calculate the number of spectra in 1 minute of retention time
        
        # Split the list into parts
        parts = []
        for i in range(long_rt_split_n):
            start_index = i * part_length - overlap_spectra
            start_index = max(start_index, 0)  # set start index to 0 if it is less than 0
            end_index = (i + 1) * part_length + overlap_spectra
            part = ms1[start_index:end_index]
            parts.append(part)
        
        # Add any remaining spectra to the last part
        if end_index < total_spectra:
            last_part = ms1[end_index:]
            parts[-1] += last_part
        
        # just get the split time point
        parts1 = [ms1[i * part_length:(i + 1) * part_length] for i in range(long_rt_split_n)]
        ranges = []
        for i, part in enumerate(parts1):
            rt_start = part[0].scan_time[0]
            rt_end = part[-1].scan_time[0]
            range1 = [rt_start, rt_end]
            ranges.append(range1)
        
        # to make sure there is no gap between each list.
        my_list = ranges
        ranges = [[my_list[i][0], my_list[i + 1][0]] for i in range(len(my_list) - 1)] + [my_list[-1]]
        
        # start to do peak picking for each part
        peak_list_all = []
        for n, part in enumerate(parts):
            peak_all = split_peak_picking(part, profile=profile, split_n=split_n, threshold=threshold,
                                          i_threshold=i_threshold,
                                          peak_width=peak_width, SN_threshold=SN_threshold,
                                          area_threshold=area_threshold,
                                          height_threshold=height_threshold,
                                          rt_error_alignment=rt_error_alignment, mz_error_alignment=mz_error_alignment,
                                          mz_overlap=mz_overlap, sat_intensity=sat_intensity, step_size=step_size,
                                          orbi=orbi, message=message, isotope_analysis=isotope_analysis)
            peak_all = peak_all[(peak_all['rt'] > ranges[n][0]) & (peak_all['rt'] <= ranges[n][1])]
            peak_list_all.append(peak_all)
        
        peak_all = pd.concat(peak_list_all).reset_index(drop=True)
    return peak_all


def first_process(file, company, profile=True, control_group=['methanol_blank', 'control', 'lab_blank'], threshold=10,
                  i_threshold=200, SN_threshold=3, peak_width=1, area_threshold=500, height_threshold=500,
                  rt_error_alignment=0.05,
                  mz_error_alignment=0.015, mz_overlap=1, ms2_analysis=True, frag_rt_error=0.02, split_n=20,
                  sat_intensity=False,
                  long_rt_split_n=1, rt_overlap=1, step_size=0.02, orbi=False, message='', max_frag_num=50):
    """
    Processes HRMS data by performing peak picking and generating a result file.

    Args:
        file (str): Path to the input file to be processed.
        company (str): The manufacturer of the instrument used to generate the data (e.g., 'Waters', 'Agilent', etc.).
        profile (bool): Indicates whether the data is in profile or centroid mode. True for profile mode, False for centroid mode.
        control_group (List[str]): A list of labels representing the control group. These labels are used in the search for relevant file names.
        threshold (int): The threshold value for peak detection.
        i_threshold (int): The intensity threshold for peak detection.
        SN_threshold (int): The signal-to-noise threshold for peak detection.
        peak_width (float): The peak width for chromatographic peak detection.
        area_threshold (float): The minimum peak area threshold. Peaks with an area below this threshold will be excluded from analysis.
        height_threshold (float): The minimum peak height threshold. Peaks with a height below this threshold will be excluded from analysis.
        rt_error_alignment (float): The retention time error tolerance for alignment.
        mz_error_alignment (float): The m/z error tolerance for alignment.
        mz_overlap (float): The m/z overlap threshold.
        ms2_analysis (bool): Indicates whether to perform DIA fragment analysis. True to enable DIA fragment analysis, False to disable it.
        frag_rt_error (float): The retention time error tolerance for fragment MS2 analysis.
        split_n (int): The number of pieces to split the large dataframe.
        sat_intensity (bool): Indicates whether to consider saturation intensity. False to disable.
        long_rt_split_n (int): The number of pieces to split the MS1 data.
        rt_overlap (float): The retention time overlap threshold.
        step_size (float): Step size for data processing.
        orbi (bool): Indicates whether the data is in orbitrap data (True) or TOF-MS data (False).
        message (str): A message to display during processing.
        max_frag_num (int): Maximum number of fragments to consider in MS2 analysis.

    Returns:
        None. Instead, the function exports an Excel file with the result information.
    """
    try:
        mz_round = 4
        ms1, ms2 = sep_scans(file, company, message=message)
        peak_all = ultimate_peak_picking(ms1, profile=profile, split_n=split_n, threshold=threshold,
                                         i_threshold=i_threshold,
                                         SN_threshold=SN_threshold, peak_width=peak_width,
                                         area_threshold=area_threshold,
                                         height_threshold=height_threshold, rt_error_alignment=rt_error_alignment,
                                         mz_error_alignment=mz_error_alignment, mz_overlap=mz_overlap,
                                         sat_intensity=sat_intensity,
                                         long_rt_split_n=long_rt_split_n, rt_overlap=rt_overlap, step_size=step_size,
                                         orbi=orbi, message=message)
        # 是否分析ms2
        if len(ms2) == 0:
            pass
        else:
            if ms2_analysis is True:
                basename_file = os.path.basename(file)
                if any(item.lower() in basename_file.lower() for item in control_group):
                    pass
                else:
                    
                    peak_all2 = ultimate_peak_picking(ms2, profile=profile, split_n=split_n, threshold=threshold,
                                                      i_threshold=i_threshold,
                                                      SN_threshold=SN_threshold, peak_width=peak_width,
                                                      area_threshold=area_threshold,
                                                      height_threshold=height_threshold,
                                                      rt_error_alignment=rt_error_alignment,
                                                      mz_error_alignment=mz_error_alignment, mz_overlap=mz_overlap,
                                                      sat_intensity=sat_intensity,
                                                      long_rt_split_n=long_rt_split_n, rt_overlap=rt_overlap,
                                                      step_size=step_size,
                                                      orbi=orbi, message=message, isotope_analysis=False)
                    
                    frag_all = []
                    spec_all = []
                    for i in tqdm(range(len(peak_all)), desc=f'{message}Assign DIA MS2 spectrum', leave=False,
                                  colour='Green', ncols=100):
                        rt = peak_all.loc[i, 'rt']
                        df_DIA = peak_all2[(peak_all2['rt'] > rt - frag_rt_error)
                                           & (peak_all2['rt'] < rt + frag_rt_error)].sort_values(
                            by='intensity', ascending=False)
                        # append fragments
                        frag = str([i for i in df_DIA['mz'].values][:max_frag_num])
                        frag_all.append(frag)
                        # append ms2 spectra
                        
                        s = pd.Series(data=df_DIA['intensity'].values, index=df_DIA['mz'])
                        # Convert the series to a DataFrame
                        df = pd.DataFrame(s).reset_index()
                        df.columns = ['m/z', 'intensity']
                        
                        # Sort the dataframe by 'm/z'
                        df = df.sort_values(by='m/z')
                        
                        # Create a new column 'group' for data grouping
                        df.loc[:, 'group'] = (df['m/z'].diff() > 0.5).cumsum()
                        
                        # Keep the row with max 'intensity' from each group
                        df = df.loc[df.groupby('group')['intensity'].idxmax()]
                        
                        # Drop the 'group' column as it's no longer needed
                        df = df.drop(columns=['group'])
                        
                        # Convert the DataFrame back to a Series
                        result = pd.Series(df['intensity'].values, index=df['m/z']).astype(int)
                        
                        # Remove the name of the index
                        result.index.name = None
                        
                        result = result.sort_values(ascending=False).iloc[:max_frag_num].to_dict()
                        
                        spec_all.append(str(result))
                    
                    peak_all.loc[:, 'frag_DIA'] = frag_all
                    peak_all.loc[:, 'ms2_spec_DIA_dict'] = spec_all
            
            
            else:
                pass
        file_name = os.path.basename(file)
        peak_selected = identify_isotopes(peak_all)
        peak_selected = remove_unnamed_columns(peak_selected)
        peak_selected.to_excel(file.replace('.mzML', '.xlsx'))
    except Exception as e:
        # 捕获异常并将异常信息保存到error_info变量
        error_info = traceback.format_exc()
        print(error_info)


def multi_process(path, company, profile=True, control_group=['lab_blank', 'methanol'], processors=1, threshold=10,
                  i_threshold=200,
                  SN_threshold=3, peak_width=1, area_threshold=500, height_threshold=500, rt_error_alignment=0.05,
                  mz_error_alignment=0.015,
                  mz_overlap=1, ms2_analysis=True, frag_rt_error=0.02, split_n=20, rt_overlap=1, filter_type=1,
                  sat_intensity=False,
                  long_rt_split_n=1, step_size=0.02, orbi=False, max_frag_num=50):
    """
    Process mzML data and perform a comparison between the sample set and the control set. The resulting data will be used to generate an Excel file that summarizes the differences between the two sets.

    Args:
        path (str): The file path for the mzML files that will be processed. For example, '../Users/Desktop/my_HRMS_files'.
        company (str): The type of mass spectrometer used to acquire the data. Valid options are 'Waters', 'Thermo', 'Sciex', and 'Agilent'.
        profile (bool): Indicates whether the data is in profile or centroid mode. True for profile mode, False for centroid mode.
        processors (int): Determines the number of processors that will be used for data processing in parallel. If the memory usage exceeds 90%, some Excel files may not be generated.
        control_group (List[str]): A list of labels representing the control group. These labels are used in the search for relevant file names.
        filter_type (int): Determines the mode of operation.
            - 1: For data without triplicates; fold change is computed as the ratio of the sample area to the maximum control area.
            - 2: For data with triplicates; the function will calculate p-values, and fold change is computed as the ratio of the mean sample area to the mean control area.
        ms2_analysis (bool): Indicates whether to perform DIA fragment analysis. True to enable DIA fragment analysis, False to disable it.
        threshold (int): The threshold value for peak detection.
        i_threshold (int): The intensity threshold for peak detection.
        SN_threshold (int): The signal-to-noise threshold for peak detection.
        peak_width (float): The peak width for chromatographic peak detection.
        area_threshold (float): The minimum peak area threshold. Peaks with an area below this threshold will be excluded from analysis.
        height_threshold (float): The minimum peak height threshold. Peaks with a height below this threshold will be excluded from analysis.
        rt_error_alignment (float): The retention time error tolerance for alignment.
        mz_error_alignment (float): The m/z error tolerance for alignment.
        mz_overlap (float): The m/z overlap threshold.
        frag_rt_error (float): The retention time error tolerance for fragment MS2 analysis.
        split_n (int): The number of pieces to split the large dataframe.
        rt_overlap (float): The retention time overlap threshold.
        sat_intensity (bool): Indicates whether to consider saturation intensity. False to disable.
        long_rt_split_n (int): The number of pieces to split the MS1 data.
        step_size (float): Step size for data processing.
        orbi (bool): Indicates whether the data is in orbitrap data (True) or TOF-MS data (False).
        max_frag_num (int): Maximum number of fragments to consider in MS2 analysis.

    Returns:
        None. Generates Excel files that summarize the differences between the control sets and sample sets.
    """
    move_files(path)
    # Log function details
    func_name = inspect.currentframe().f_code.co_name
    func_params = inspect.getargvalues(inspect.currentframe()).locals
    log_function_details(path, func_name, func_params)
    
    files_mzml = glob(os.path.join(path, '*.mzML'))
    files_mzml_DDA = [file for file in files_mzml if 'DDA' in os.path.basename(file)]
    files_mzml = [file for file in files_mzml if 'DDA' not in os.path.basename(file)]
    # 第一个过程
    pool = Pool(processes=processors)
    for j, file in enumerate(files_mzml):
        print(file)
        message = f'No. {j + 1} : '
        pool.apply_async(first_process,
                         args=(file, company, profile, control_group, threshold, i_threshold, SN_threshold, peak_width,
                               area_threshold,
                               height_threshold, rt_error_alignment, mz_error_alignment, mz_overlap, ms2_analysis,
                               frag_rt_error, split_n,
                               sat_intensity, long_rt_split_n, rt_overlap, step_size, orbi, message, max_frag_num))
    
    print('                                                                            ')
    print('============================================================================')
    print('First process...')
    print('============================================================================')
    print('                                                                            ')
    pool.close()
    pool.join()
    
    # 检查是否有遗漏的
    files_excel_temp = glob(os.path.join(path, '*.xlsx'))
    files_excel_names = [os.path.basename(i)[:-5] for i in files_excel_temp]
    path_omitted = []
    if len(files_mzml) > len(files_excel_names):
        # 检查是哪个文件漏掉了
        for path1 in files_mzml:
            if os.path.basename(path1)[:-5] in files_excel_names:
                pass
            else:
                path_omitted.append(path1)
    if len(path_omitted) == 0:
        pass
    else:
        pool = Pool(processes=processors)
        for file in path_omitted:
            print('Omitted files')
            print(file)
            message = 'Omitted files'
            pool.apply_async(first_process,
                             args=(
                                 file, company, profile, control_group, threshold, i_threshold, SN_threshold,
                                 peak_width,
                                 area_threshold,
                                 height_threshold, rt_error_alignment, mz_error_alignment, mz_overlap, ms2_analysis,
                                 frag_rt_error, split_n,
                                 sat_intensity, long_rt_split_n, rt_overlap, step_size, orbi, message, max_frag_num))
        pool.close()
        pool.join()
    
    # 中间过程
    files_excel = glob(os.path.join(path, '*.xlsx'))
    peak_alignment(files_excel)
    ref_all = pd.read_excel(os.path.join(path, 'peak_ref.xlsx'), index_col='Unnamed: 0')
    
    # 第二个过程
    pool = Pool(processes=processors)
    for j, file in enumerate(files_mzml):
        message = f'No. {j + 1} : '
        pool.apply_async(second_process, args=(file, ref_all, company, profile, long_rt_split_n, orbi, message))
    print('                                                                            ')
    print('============================================================================')
    print('Second process...')
    print('============================================================================')
    print('                                                                            ')
    pool.close()
    pool.join()
    
    # 第三个过程, 做fold change filter
    print('                                                                            ')
    print('============================================================================')
    print('Third process...')
    print('============================================================================')
    print('                                                                            ')
    
    fold_change_filter(path, control_group=control_group, filter_type=filter_type)
    
    # 如果有DDA，将DDA数据加入到excel里
    DDA_to_DIA_result(path, company, profile)


def sep_scans(path, company, tool='pymzml', message=''):
    """
    Separates scans for MS1 and MS2 in mzML files using pymzml package.
    Args:
       path (str): The path of the mzML file.
       company (str): The instrument company name. Currently, supports 'Waters', 'Agilent', 'Thermo' or 'AB'.
       tool(str): pymzml or pyopenms
    Returns:
        Tuple: A tuple of two lists containing MS1 and MS2 scans respectively.
    """
    if tool == 'pymzml':
        if company.lower() == 'waters':
            # create a pymzml Reader object
            run = pymzml.run.Reader(path)
            ms1, ms2 = [], []
            # iterate over each scan in the mzML file
            for scan in tqdm(run, desc=f'{message}Separating MS1 and MS2', leave=False):
                # extract function value from the scan's id_dict attribute
                if scan.id_dict['function'] == 1:
                    ms1.append(scan)
                elif scan.ms_level == 2:
                    ms2.append(scan)
                else:
                    pass
            return ms1, ms2
        else:
            run = pymzml.run.Reader(path)
            ms1, ms2 = [], []
            for scan in tqdm(run, desc=f'{message}Separating MS1 and MS2', leave=False):
                if scan.ms_level == 1:
                    ms1.append(scan)
                elif scan.ms_level == 2:
                    ms2.append(scan)
                else:
                    pass
            return ms1, ms2
    
    else:
        ValueError("Invalid tool. Expected 'pymzml' or 'pyopenms'.")


def gen_df(ms1, ms_round=4, profile=True, raw_info=True):
    """
    Loads all raw data files and generates a big DataFrame. If the data is in profile mode,it will be transformed into centroid data.

    Args:
        ms1: A list of all MS1 scans generated from pymzml.
        ms_round: The number of decimal places to keep.
        profile: A boolean indicating whether the data is in profile mode (True) or centroid mode (False).
        raw_info: A boolean indicating whether to return raw data as a dictionary.

    Returns:
        A DataFrame of raw data and a dictionary of raw data (if raw_info=True).
    """
    
    # Convert centroid data to a DataFrame
    print('Loading data...', end="\r")
    if profile is False:
        data = [pd.Series(data=ms1[i].i, index=ms1[i].mz.round(ms_round),
                          name=round(ms1[i].scan_time[0], 3)) for i in range(len(ms1))]
        print('Generating DataFrame of data...', end="\r")
        df1 = pd.concat(data, axis=1)
        df2 = df1.fillna(0)
    # Convert profile data to a DataFrame
    else:
        peaks_index = [[i, scipy.signal.find_peaks(ms1[i].i.copy())[0]] for i in range(len(ms1))]
        data = [
            pd.Series(data=ms1[i].i[peaks], index=ms1[i].mz[peaks].round(ms_round), name=round(ms1[i].scan_time[0], 3))
            for i, peaks in peaks_index]
        print('Generating DataFrame of data...', end="\r")
        df1 = pd.concat(data, axis=1)
        df2 = df1.fillna(0)
    
    # Return raw data as a dictionary if raw_info=True
    if raw_info is True:
        raw_info = {round(ms1[i].scan_time[0], 3): pd.Series(data=ms1[i].i, index=ms1[i].mz.round(ms_round))
                    for i in range(len(ms1))}
        print('DataFrame of raw data already generated!')
        return df2, raw_info
    else:
        print('DataFrame of raw data already generated!')
        return df2


def find_locators(df_mass_list, target_mass_list):
    """
    Finds the locations in the `df_mass_list` where the `target_mass_list` cuts it.

    Args:
        df_mass_list: A sorted one-dimensional numpy array containing all mass values in the raw data.
        target_mass_list: A sorted one-dimensional numpy array of the mass values that cut `df_mass_list` into multiple sections.

    Returns:
        A one-dimensional numpy array containing the indices of the `df_mass_list` where the `target_mass_list` cuts it.
    """
    
    # Ensure target_mass_list is within the range of df_mass_list
    target_mass_list = np.clip(target_mass_list, df_mass_list[0], df_mass_list[-1])
    
    # Find the indices of the target masses in the df_mass_list
    locators = [bisect.bisect_left(df_mass_list, mass) for mass in target_mass_list]
    
    return np.array(locators)


def peak_finding(eic, threshold=10, width=1):
    """
    Finds peaks in a single extracted ion chromatogram (EIC) and returns the peak index, widths, and heights.

    Args:
        eic (ndarray): The extracted ion chromatogram data as a one-dimensional numpy array.
        threshold (float): The noise level threshold for a peak, as a scalar value. Default is 10.
        width (int): The minimum required width of a peak, as a scalar value. Default is 1.

    Returns:
        peak_index, widths, heights
        peak_index (ndarray): Indices of the detected peaks in the EIC.
        widths (ndarray): Widths of the detected peaks.
        heights (ndarray): Heights of the detected peaks.
    """
    
    # Ensure eic is a numpy array
    eic = np.asarray(eic)
    
    # Find the peaks in the EIC
    peaks, pro_dict = scipy.signal.find_peaks(eic, width=width)
    
    # Calculate the peak prominences, which represent the peak's height relative to its surroundings
    peak_prominence = pro_dict['prominences']
    widths = np.round(pro_dict['widths'], 2)
    
    # Apply peak-picking criteria to select only peaks with sufficient prominence
    if len(peaks) > 5:
        # Select only peaks whose prominence is greater than the median prominence times the threshold
        # 评估是否是离群点
        z_scores = zscore(peak_prominence)
        # 根据z_scores>1找到离群点
        index1 = np.where((z_scores > 0) & (widths > width))[0]
        
        if len(index1) > 0:
            # 找到离群点前后20个点，获得每个离群点的范围
            peak_prominence_median = np.array([
                np.median(peak_prominence[max(0, i - 20):min(len(peak_prominence), i + 20)])
                for i in index1
            ])
            # 获得每个点的s/n
            peak_sn = peak_prominence[index1] / peak_prominence_median
            target_index = np.where(peak_sn > threshold)
            peak_index = peaks[index1[target_index]]
            widths = widths[index1[target_index]]
        else:
            peak_index = np.array([])
            widths = np.array([])
    else:
        # If there are fewer than or equal to 5 peaks, keep all of them and apply width condition
        condition = widths > width
        peak_index = peaks[condition]
        widths = widths[condition]
    
    # Ensure that peak_index is not empty
    if len(peak_index) == 0:
        heights = np.array([], dtype=float)
    else:
        heights = eic[peak_index]
    return peak_index, widths, heights


def cal_bg(eic):
    """
    Calculate the background value in a chromatogram.

    Args:
        eic (numpy.ndarray): A one-dimensional numpy array containing extracted ion chromatogram data.

    Returns:
        float: The background value.
    """
    # Find peaks in the chromatogram
    peaks, _ = scipy.signal.find_peaks(eic, width=0)
    
    if len(peaks) == 0:
        # If there are no peaks, set the background to a value higher than the maximum intensity in the chromatogram.
        bg = max(eic) + 1
    else:
        # Get the heights of all the peaks found in the chromatogram
        peak_heights = eic[peaks]
        
        # Filter out peak heights that are too large and only keep peak heights smaller than 5 times the median peak height.
        peak_heights1 = peak_heights[peak_heights < np.median(peak_heights) * 5]
        
        # Set the background to the maximum intensity of the remaining peak heights plus one.
        bg = max(peak_heights1) + 1
    
    return bg


def peak_picking(df1, threshold=10, i_threshold=500, SN_threshold=3, peak_width=1, area_threshold=500,
                 height_threshold=500, profile_info=None, isotope_analysis=True, rt_error_alignment=0.05,
                 mz_error_alignment=0.015,
                 enable_progress_bar=True, alignment=True, step_size=0.02):
    """
    Find peaks in a large dataframe, analyze isotope and adduct information, and return a dataframe with
    information on the peaks including retention time, m/z value, intensity, and area.

    Args:
        df1 (pandas.DataFrame): Dataframe generated from the function gen_df().
        threshold (int): Threshold for finding peaks.
        i_threshold (int): Threshold for peak intensity.
        SN_threshold (float): Signal-to-noise threshold.
        peak_width (float): The minimum required width of a peak.
        area_threshold (float): The minimum peak area threshold. Peaks with an area below this threshold will be excluded from analysis.
        height_threshold (float): The minimum peak height threshold. Peaks with a height below this threshold will be excluded from analysis.
        profile_info (dict, optional): Profile information containing raw data.
        isotope_analysis (bool, optional): Whether to analyze isotope distribution.
        rt_error_alignment (float, optional): Retention time error alignment threshold.
        mz_error_alignment (float, optional): m/z error alignment threshold.
        enable_progress_bar (bool): Whether to enable the progress bar during processing. Default is True.
        alignment (bool): Whether to perform alignment of the retention time (RT) and mass-to-charge ratio (m/z) pairs. Default is True.
        step_size (float): Step size for data processing.

    Returns:
        pandas.DataFrame: A dataframe with information on the peaks including retention time, m/z value,
        intensity, peak width, peak height, area, and signal-to-noise ratio (S/N).
    """
    
    # Update the dataframe
    df1 = df1.sort_index(ascending=True)
    
    # Define target list for finding locators
    target_list = np.arange(min(df1.index.values), max(df1.index.values), step_size)
    
    # Find locators
    index = find_locators(df1.index.values, target_list)
    
    # Extract retention time values
    RT = np.array(df1.columns)
    
    # Create empty list to store peak information
    data = []
    
    # Loop over locators to find peaks
    num = len(index)
    
    # set a tqdm switch
    if enable_progress_bar:
        progress_bar = tqdm(total=num - 1, desc='Finding peaks')
    
    for i in range(num - 1):
        # Extract data from current locator to the next locator
        df2 = df1.iloc[index[i]:index[i + 1]]
        
        # Check if it is a empty dataframe
        if len(df2) != 0:
            # Extract the maximum intensity values from the array
            extract_c = df2.max(axis=0).values
            
            # Check if the maximum intensity is above the intensity threshold
            if max(extract_c) < i_threshold:
                pass
            else:
                # Find peaks in the intensity data
                peak_index, peak_widths, peak_heights = peak_finding(extract_c, threshold, width=peak_width)
                
                # Check if any peaks were found
                if len(peak_index) != 0:
                    # Extract peak height, background intensity, signal to noise ratio, and peak area
                    bg = cal_bg(extract_c)
                    SN = (peak_heights / bg).round(2)
                    df3 = df2[df2.columns[peak_index]]
                    intensity = np.round(np.array(df3.max().values), 0)
                    rt = np.round(RT[peak_index], 2)
                    mz = np.round(np.array(df3.idxmax().values), 4)
                    # calculate the peak area
                    left_indice = abs(np.array([argmin(abs(RT - (rt_ - 0.2))) for rt_ in rt]) - 1)
                    right_indice = np.array([argmin(abs(RT - (rt_ + 0.2))) for rt_ in rt])
                    left_right_indice = np.array([left_indice, right_indice]).T
                    rt_t = [RT[index[0]:index[1]] for index in left_right_indice]
                    eic_t = [extract_c[index[0]:index[1]] for index in left_right_indice]
                    area = [round(scipy.integrate.simpson(eic_t[i]), 0) for i in range(len(rt_t))]
                    df_array = np.array([rt, mz, intensity, peak_widths, peak_heights, area, SN]).T
                    df_array = df_array[(df_array[:, 2] > i_threshold) & (df_array[:, 4] > height_threshold) &
                                        (df_array[:, 5] > area_threshold) & (df_array[:, 6] > SN_threshold)]
                    data.append(df_array)
        if enable_progress_bar:
            progress_bar.update(1)
    if enable_progress_bar:
        progress_bar.close()
    # Check if no peaks were found.
    if len(data) == 0:
        return pd.DataFrame()
    else:
        peak_info = np.concatenate(data)
        peak_all = pd.DataFrame(data=peak_info,
                                columns=['rt', 'mz', 'intensity', 'peak_width', 'peak_height', 'area', 'S/N'])
        
        #  Perform alignment of the retention time (RT) and mass-to-charge ratio (m/z) pairs in the resulting dataframe.
        if alignment:
            # 组合 rt 和 mz 形成 KDTree 的数据点
            data = np.column_stack((peak_all['rt'], peak_all['mz']))
            if len(data) != 0:
                # Scale the tolerances relative to the range of each dimension
                rt_range = np.ptp(data[:, 0])
                mz_range = np.ptp(data[:, 1])
                if rt_range == 0:
                    rt_range = 0.01
                if mz_range == 0:
                    mz_range = 0.001
                
                scaled_rt_tol = rt_error_alignment / rt_range
                scaled_mz_tol = mz_error_alignment / mz_range
                
                # Create a KDTree with scaled data
                scaled_data = data / [rt_range, mz_range]
                tree = KDTree(scaled_data)
                
                reference_list = []
                visited = set()
                
                for idx, scaled_pair in enumerate(scaled_data):
                    if idx in visited:
                        continue
                    
                    # Find neighbors within a spherical range that's sure to encompass the rectangular range
                    neighbors = tree.query_ball_point(scaled_pair, r=max(scaled_rt_tol, scaled_mz_tol))
                    
                    # Filter these neighbors based on the actual tolerances
                    filtered_neighbors = [i for i in neighbors if abs(data[i, 0] - data[idx, 0]) <= rt_error_alignment
                                          and abs(data[i, 1] - data[idx, 1]) <= mz_error_alignment]
                    
                    # Mark these neighbors as visited and add the first one to the reference list
                    visited.update(filtered_neighbors)
                    reference_list.append(data[idx])
                
                # 转换为 NumPy 数组并创建 KDTree
                reference_array = np.array(reference_list)
                tree = KDTree(reference_array)
                
                # 查询每个数据点的最近邻
                _, indices = tree.query(data)
                
                # 获取最近邻的 reference_array 对应的索引
                aligned_indices = [f"{reference_array[idx][0]}_{reference_array[idx][1]}" for idx in indices]
                
                # 添加新列到 DataFrame
                peak_all['rt_mz'] = aligned_indices
                peak_all = peak_all.sort_values(by='area', ascending=False)
                peak_all = peak_all.drop_duplicates(subset='rt_mz', keep='first')
            # peak_all = peak_all.drop(labels='rt_mz', axis=1)
        
        # Record the isotope distribution
        if isotope_analysis is True:
            if enable_progress_bar:
                print('Recording isotope distribution...', end='')
            rts = peak_all.rt.values
            mzs = peak_all.mz.values
            iso_info = [str(isotope_distribution(spec_at_rt(df1, rts[i]), mzs[i])) for i in range(len(rts))]
            peak_all['iso_distribution'] = iso_info
            t2 = time.time()
        
        # Perform analysis of the profile raw data and transform profile masses into centroid masses by calculating the midpoint of the FWHM (full width at half maximum).
        if profile_info is None:
            return peak_all
        else:
            if enable_progress_bar:
                print('Optimizing ms1 based on profile data...', end='')
            rts = peak_all.rt.values
            mzs = peak_all.mz.values
            
            # loading data from raw_info
            indice1 = np.array([i for i in profile_info.keys()])
            rt_keys = [indice1[argmin(abs(indice1 - i))] for i in rts]  # 基于上述rt找到ms的时间索引
            spec1 = [profile_info[i] for i in rt_keys]  # 获得ms的spec
            # evaluate mass
            mz_result = np.array([list(evaluate_ms(target_spec(spec1[i], mzs[i], width=0.04).copy(), mzs[i]))
                                  for i in range(len(mzs))]).T
            mz_obs, mz_opt, resolution = mz_result[0], mz_result[2], mz_result[4]
            # mz_opt = [mz_opt[i] if abs(mzs[i] - mz_opt[i]) < 0.02 else mzs[i] for i in range(len(mzs))]  # 去掉偏差大的矫正结果
            peak_all['mz'] = mz_obs
            peak_all['mz_opt'] = mz_opt
            peak_all['resolution'] = resolution.astype(int)
            t4 = time.time()
            if enable_progress_bar:
                pass
        return peak_all


def isotope_distribution(spec1, mz, error=0.02):
    """
    Find the isotope distribution for a specific mass-to-charge ratio (m/z).

    Args:
    - spec1: A pandas DataFrame containing centroid data.
    - mz: A float representing the mass-to-charge ratio to find the isotope distribution for.
    - error: A float representing the mass error.

    Returns:
    - A dictionary containing the isotope distribution, where keys are floats representing the mass-to-charge
    ratios and values are floats representing the intensities of the corresponding peaks in the isotope distribution.
    """
    spec2 = spec1[spec1 > 0]
    spec3 = spec2[(spec2.index > mz - 5) & (spec2.index < mz + 5)]
    mz_s = spec3[(spec3.index > mz - error) * (spec3.index < mz + error)].sort_values().iloc[-1:]
    mz__1 = spec3[(spec3.index > mz - 1 - error) * (spec3.index < mz - 1 + error)].sort_values().iloc[-1:]
    mz__2 = spec3[(spec3.index > mz - 2 - error) * (spec3.index < mz - 2 + error)].sort_values().iloc[-1:]
    mz__3 = spec3[(spec3.index > mz - 3 - error) * (spec3.index < mz - 3 + error)].sort_values().iloc[-1:]
    mz__4 = spec3[(spec3.index > mz - 4 - error) * (spec3.index < mz - 4 + error)].sort_values().iloc[-1:]
    
    mz_1 = spec3[(spec3.index > mz + 1 - error) * (spec3.index < mz + 1 + error)].sort_values().iloc[-1:]
    mz_2 = spec3[(spec3.index > mz + 2 - error) * (spec3.index < mz + 2 + error)].sort_values().iloc[-1:]
    mz_3 = spec3[(spec3.index > mz + 3 - error) * (spec3.index < mz + 3 + error)].sort_values().iloc[-1:]
    mz_4 = spec3[(spec3.index > mz + 4 - error) * (spec3.index < mz + 4 + error)].sort_values().iloc[-1:]
    x = [mz_s, mz__1, mz__2, mz__3, mz__4, mz_1, mz_2, mz_3, mz_4]
    iso_info_s = pd.concat([i for i in x if len(x) != 0])
    if len(iso_info_s) == 0:
        return {}
    else:
        iso_info_s1 = (iso_info_s / iso_info_s.values.max()).sort_index().round(3)
        iso_info_s2 = iso_info_s1[iso_info_s1 > 0.015].to_dict()
        return iso_info_s2


# Reminder：I have change evaluate_ms3 to evaluate_ms3, so other place should be changed accordingly
def evaluate_ms(new_spec, mz_exp):
    """
    Evaluate the target mass spectrum and calculate its observed m/z, error, optimal m/z, error, and resolution.

    Args:
        new_spec (pd.Series): The target mass spectrum, must be a profile data.
        mz_exp (float): The expected m/z.

    Returns:
        Tuple[float, float, float, float, int]: A tuple of observed m/z, error, optimal m/z, error, and resolution.

    Note:
        - This function uses the interpolate_series method to generate more data points for the target spectrum.
        - It then finds peaks in the spectrum and determines the observed m/z as the closest peak to the expected m/z.
        - The optimal m/z is determined by finding the intersection points of the half-height line of the peak and
          calculating the average of the m/z values at those points.
        - The resolution is calculated as the observed m/z divided by the full width at half maximum (FWHM) of the peak.
    """
    
    # Find peaks in the target spectrum
    peaks, _ = scipy.signal.find_peaks(new_spec.values)
    
    # If there are no peaks or the maximum intensity is less than 100, return default values
    if (len(peaks) == 0) or (max(new_spec.values) < 100):
        mz_obs, error1, mz_opt, error2, resolution = mz_exp, 0, 0, 0, 0
    
    # Otherwise, calculate observed m/z, optimal m/z, and resolution
    else:
        try:
            # Calculate observed m/z as the closest peak to the expected m/z
            mz_obs = new_spec.index.values[peaks][argmin(abs(new_spec.index.values[peaks] - mz_exp))]
            
            # Generate more data points for the spectrum using interpolate_series
            x, y = interpolate_series(new_spec.index.values, new_spec.values)
            
            # Find peaks in the smoothed spectrum
            peaks1, left, right = peak_finding(y, threshold=0, width=1)
            
            # Calculate the index of the peak closest to the expected m/z
            max_index_index = argmin(abs(x[peaks1] - mz_exp))
            max_index = peaks1[max_index_index]
            
            # Calculate the half-height of the peak
            half_height = y[max_index] / 2
            
            # Find the intersection points of the half-height line with the peak
            intersect_index = [i for i in range(len(y) - 1) if ((y[i] < half_height) &
                                                                (y[i + 1] > half_height)) | (
                                       (y[i] > half_height) & (y[i + 1] < half_height))]
            
            target_list = x[intersect_index]
            
            half_mz_left = target_list[np.argwhere(target_list < mz_obs)[-1]][0]
            half_mz_right = target_list[np.argwhere(target_list > mz_obs)[0]][0]
            
            resolution = int(mz_obs / (half_mz_right - half_mz_left))
            mz_opt = round(half_mz_left + (half_mz_right - half_mz_left) / 2, 5)
            error1 = round((mz_obs - mz_exp) / mz_exp * 1000000, 1)
            error2 = round((mz_opt - mz_exp) / mz_exp * 1000000, 1)
        except:
            mz_obs, error1, mz_opt, error2, resolution = mz_exp, 0, 0, 0, 0
    return round(mz_obs, 5), error1, mz_opt, error2, resolution


def target_spec(spec, target_mz, width=0.04):
    """
    Narrow the spec to a certain mass range centered around a target mz.

    Args:
        spec (pd.Series): A pandas Series representing the raw spectrum at a certain retention time.
        target_mz (float): The target mz for inspection.
        width (float, optional): The width of the mass range to be extracted. Defaults to 0.04.

    Returns:
        pd.Series: A new pandas Series representing the narrow mass range around the target mz.

    """
    # Find the index of the left boundary of the target mass range
    index_left = argmin(abs(spec.index.values - (target_mz - width)))
    
    # Find the index of the right boundary of the target mass range
    index_right = argmin(abs(spec.index.values - (target_mz + width)))
    
    # Extract the mass range and create a copy of the resulting Series
    new_spec = spec.iloc[index_left:index_right].copy()
    
    # Set the intensity at the left boundary to 0
    new_spec[target_mz - width] = 0
    # Set the intensity at the right boundary to 0
    new_spec[target_mz + width] = 0
    # Sort the Series by index
    new_spec = new_spec.sort_index()
    return new_spec


def spec_at_rt(data, rt):
    """
    Obtain the raw mass spectrum at a specific retention time.

    Args:
        data: LC-MS data, either a pandas DataFrame generated by the `gen_df()` function or an ms1 list
        rt: Retention time for the desired mass spectrum

    Returns:
        A pandas Series representing the mass spectrum at the given retention time.
    """
    if isinstance(data, pd.DataFrame):
        index = np.argmin(np.abs(data.columns.values - rt))
        return data.iloc[:, index]
    elif isinstance(data, list):
        for scan in data:
            if scan.scan_time[0] >= rt:
                return pd.Series(data=scan.i, index=scan.mz)
    else:
        raise ValueError("Data type not supported. Supported types: pandas DataFrame, ms1 list")


def interpolate_series(x, y, num_points=1000):
    """
    Interpolates a series of x and y values.

    Args:
        x (array): An array of x values.
        y (array): An array of y values.
        num_points (int): The number of points to interpolate.

    Returns:
        tuple: A tuple containing the interpolated x and y values.
    """
    f = interp1d(x, y)
    x_new = np.linspace(x.min(), x.max(), num=num_points, endpoint=True)
    y_new = f(x_new)
    return x_new, y_new


def split_peak_picking(ms1, profile=True, split_n=20, threshold=10, i_threshold=500, SN_threshold=3, peak_width=1,
                       area_threshold=500, height_threshold=500, noise_threshold=0, rt_error_alignment=0.05,
                       mz_error_alignment=0.015, mz_overlap=1, sat_intensity=False, orbi=True, step_size=0.02,
                       message='', isotope_analysis=True):
    if orbi is True:
        pass
    
    def target_spec1(spec, target_mz, width=0.04):
        """
        :param spec: spec generated from function spec_at_rt()
        :param target_mz: target mz for inspection
        :param width: width for data points
        :return: new spec and observed mz
        """
        index_left = argmin(abs(spec.index.values - (target_mz - width)))
        index_right = argmin(abs(spec.index.values - (target_mz + width)))
        new_spec = spec.iloc[index_left:index_right].copy()
        new_spec[target_mz - width] = 0
        new_spec[target_mz + width] = 0
        new_spec = new_spec.sort_index()
        return new_spec
    
    # 第一步： loading data
    if profile is True:
        raw_info_profile = {}
        raw_info_centroid = {}
        
        for i in tqdm(range(len(ms1)), desc=f'{message} Loading Data', leave=False, colour='Green'):
            # 1. 记录profile原始数据
            key1 = round(ms1[i].scan_time[0], 3)
            mz_info = ms1[i].mz.round(5)
            intensity_info = ms1[i].i.round(0).astype(np.float32)
            # array1 = np.array([mz_info,intensity_info])
            # 更新成新的array
            i_median = np.median(intensity_info)
            index1 = np.where(intensity_info > i_median)[0]
            array1 = np.array([mz_info[index1], intensity_info[index1]])
            
            raw_info_profile[key1] = array1
            
            # 2. 找spec的index，记录centroid原始数据
            peak_idx = scipy.signal.find_peaks(intensity_info)[0]
            mz_info1 = mz_info[peak_idx]
            intensity_info1 = intensity_info[peak_idx]
            array2 = np.array([mz_info1, intensity_info1])
            raw_info_centroid[key1] = array2
    
    
    else:
        raw_info_centroid = {}
        for i in tqdm(range(len(ms1)), desc=f'{message} Loading Data', leave=False, colour='Green'):
            key1 = round(ms1[i].scan_time[0], 3)
            mz_info = ms1[i].mz.round(5)
            intensity_info = ms1[i].i.round(0).astype(np.float32)
            array1 = np.array([mz_info, intensity_info])
            raw_info_centroid[key1] = array1
    
    # 第二步 将样品按照质量分割
    # 清理变量
    ms1.clear()
    ms1 = None  # 这样不会影响外部
    gc.collect()
    # 2. 开始分割
    
    all_data = [[] for _ in range(split_n)]
    ms_increase = int(1700 / split_n)
    
    for i, (k, v) in tqdm(enumerate(raw_info_centroid.items()), desc=f'{message} Split series', leave=False,
                          colour='Green'):
        s1 = pd.Series(data=v[1], index=v[0], name=k)
        s1.index = np.round(s1.index.values, 3).astype(np.float32) # 之前的s1.index.round(3).astype(np.float32)
        s1 = s1.groupby(s1.index).max()
        low, high = 50, 50 + ms_increase
        for j in range(split_n):
            # 直接用 list 存储，避免 locals()
            filtered_s1 = s1[
                (s1.index < high + mz_overlap) & (s1.index >= low - mz_overlap) & (s1.index > noise_threshold)]
            all_data[j].append(filtered_s1)
            
            low += ms_increase
            high += ms_increase
    
    # 第三步. 开始分段提取
    all_peak_all = []
    for i in tqdm(range(len(all_data)), desc=f'{message}Split peak picking process', leave=False, colour='Green'):
        data = all_data[i]
        df1 = pd.concat(data, axis=1)
        df1 = df1.fillna(0)
        if len(df1) == 0:
            pass
        else:
            peak_all = peak_picking(df1, isotope_analysis=False, threshold=threshold, peak_width=peak_width,
                                    area_threshold=area_threshold,
                                    height_threshold=height_threshold, i_threshold=i_threshold,
                                    SN_threshold=SN_threshold,
                                    rt_error_alignment=rt_error_alignment, mz_error_alignment=mz_error_alignment,
                                    enable_progress_bar=False,
                                    alignment=False, step_size=step_size)
            all_peak_all.append(peak_all)
        # 逐步清理 all_data
        all_data[i] = None
    
    peak_all = pd.concat(all_peak_all).sort_values(by='intensity', ascending=False).reset_index(drop=True)
    
    # 第四步，做self-alignment,  Perform alignment of the retention time (RT) and mass-to-charge ratio (m/z) pairs in the resulting dataframe.
    
    # 组合 rt 和 mz 形成 KDTree 的数据点
    data = np.column_stack((peak_all['rt'], peak_all['mz']))
    
    # Scale the tolerances relative to the range of each dimension
    rt_range = np.ptp(data[:, 0])
    mz_range = np.ptp(data[:, 1])
    if rt_range == 0:
        rt_range = 0.01
    if mz_range == 0:
        mz_range = 0.001
    
    scaled_rt_tol = rt_error_alignment / rt_range
    scaled_mz_tol = mz_error_alignment / mz_range
    
    # Create a KDTree with scaled data
    scaled_data = data / [rt_range, mz_range]
    tree = KDTree(scaled_data)
    
    reference_list = []
    visited = set()
    
    for idx, scaled_pair in tqdm(enumerate(scaled_data), desc='Aligning all rt_mz pairs(split)', leave=False,
                                 colour='Green'):
        if idx in visited:
            continue
        
        # Find neighbors within a spherical range that's sure to encompass the rectangular range
        neighbors = tree.query_ball_point(scaled_pair, r=max(scaled_rt_tol, scaled_mz_tol))
        
        # Filter these neighbors based on the actual tolerances
        filtered_neighbors = [i for i in neighbors if abs(data[i, 0] - data[idx, 0]) <= rt_error_alignment
                              and abs(data[i, 1] - data[idx, 1]) <= mz_error_alignment]
        
        # Mark these neighbors as visited and add the first one to the reference list
        visited.update(filtered_neighbors)
        reference_list.append(data[idx])
    
    # 转换为 NumPy 数组并创建 KDTree
    reference_array = np.array(reference_list)
    tree = KDTree(reference_array)
    
    # 查询每个数据点的最近邻
    _, indices = tree.query(data)
    
    # 获取最近邻的 reference_array 对应的索引
    aligned_indices = [f"{reference_array[idx][0]}_{reference_array[idx][1]}" for idx in indices]
    
    # 添加新列到 DataFrame
    peak_all['rt_mz'] = aligned_indices
    peak_all = peak_all.sort_values(by='area', ascending=False)
    peak_all = peak_all.drop_duplicates(subset='rt_mz', keep='first')
    peak_all = peak_all.drop(labels='rt_mz', axis=1)
    peak_all = peak_all.reset_index(drop=True)  # 先更新一下index,因为前面alignment后删除了很多
    
    # 后面的isotope analysis和mz opt都需要用,不管是不是centroid
    raw_info_rts = np.array([k for k, v in raw_info_centroid.items()])
    # Convert rts and mzs to NumPy arrays if they aren't already
    rts = np.array(peak_all.rt.values)
    mzs = np.array(peak_all.mz.values)
    # Vectorized calculation to find the closest rt_key for each rt value
    rt_diffs = np.abs(raw_info_rts[:, np.newaxis] - rts)
    closest_indices = np.argmin(rt_diffs, axis=0)
    rt_keys = raw_info_rts[closest_indices]
    
    # 第五步. 对同位素丰度进行记录
    if isotope_analysis:
        iso_info = []
        for i in tqdm(range(len(mzs)), desc=f'{message}Recording iso_info', leave=False, colour='Green'):
            target_mz, target_intensity = raw_info_centroid[rt_keys[i]]
            s1 = pd.Series(target_intensity, index=target_mz)
            iso_info.append(str(isotope_distribution(s1, mzs[i])))
        peak_all['iso_distribution'] = iso_info
    
    # 第六步. 更新质量数据
    if profile is True:
        spec1 = [pd.Series(data=raw_info_profile[i][1], index=raw_info_profile[i][0]) for i in rt_keys]  # 获得ms的spec,*
        mz_result = np.array(
            [list(evaluate_ms(target_spec1(spec1[i], mzs[i], width=0.04), mzs[i])) for i
             in tqdm(range(len(mzs)), desc=f'{message} Correcting m/z', leave=False)]).T
        mz_obs, mz_opt, resolution = mz_result[0], mz_result[2], mz_result[4]
        mz_opt = [mz_opt[i] if abs(mzs[i] - mz_opt[i]) < 0.02 else
                  mzs[i] for i in tqdm(range(len(mzs)), desc=f'{message}Checking the corrected m/z', leave=False,
                                       colour='Green')]  # 去掉偏差大的矫正结果
        peak_all.loc[:, ['mz', 'mz_opt', 'resolution']] = np.array([mz_obs, mz_opt, resolution.astype(int)]).T
    else:
        spec1 = [pd.Series(data=raw_info_centroid[i][1], index=raw_info_centroid[i][0]) for i in rt_keys]  # 获得ms的spec,*
        target_spec = [spec1[i][(spec1[i].index > mzs[i] - 0.015) & (spec1[i].index < mzs[i] + 0.015)] for i in
                       tqdm(range(len(spec1)), desc=f'{message}Correcting m/z', leave=False, colour='Green')]
        mzs_obs = [
            target_spec[i].index.values[[np.argmax(target_spec[i].values)]][0] if len(target_spec[i]) != 0 else mzs[i]
            for i in tqdm(range(len(target_spec)), desc=f'{message}Checking obs m/z', leave=False, colour='Green')]
        peak_all['mz'] = mzs_obs
    
    # 如果担心饱和质量不准，使用sat_intensity 更新质量
    if (sat_intensity is False) | (sat_intensity is None) | (sat_intensity < 100000) | (sat_intensity == ''):
        pass
    else:
        if profile is True:
            for j in tqdm(range(len(peak_all)), desc=f'{message}Optimize m/z based on sat_intensity', leave=False,
                          colour='Green'):
                mz = peak_all.loc[j, 'mz']
                rt = peak_all.loc[j, 'rt']
                intensity = peak_all.loc[j, 'intensity']
                if intensity > sat_intensity:
                    for k, v in raw_info_profile.items():
                        if k > rt:  # find the time
                            s1 = pd.Series(data=raw_info_profile[k][1], index=raw_info_profile[k][0])
                            new_spec1 = target_spec1(s1, mz,
                                                     0.2)  # cut the spectrum in a certain range. 1 m/z in this case.
                            peak_index, *_ = scipy.signal.find_peaks(new_spec1.values)
                            if max(new_spec1.values[peak_index]) < sat_intensity:
                                insat_mz_obs, error1, insat_mz_opt, error2, resolution = evaluate_ms(new_spec1, mz)
                                peak_all.loc[j, 'mz'] = insat_mz_obs
                                peak_all.loc[j, 'mz_opt'] = insat_mz_opt
                                peak_all.loc[j, 'resolution'] = resolution
                                break
        else:
            for j in tqdm(range(len(peak_all)), desc=f'{message}Optimize m/z based on sat_intensity', leave=False,
                          colour='Green'):
                mz = peak_all.loc[j, 'mz']
                rt = peak_all.loc[j, 'rt']
                intensity = peak_all.loc[j, 'intensity']
                if intensity > sat_intensity:
                    for k, v in raw_info_centroid.items():
                        if k > rt:  # find the time
                            s1 = pd.Series(data=raw_info_centroid[k][1], index=raw_info_centroid[k][0])
                            new_spec1 = target_spec1(s1, mz,
                                                     0.2)  # cut the spectrum in a certain range. 1 m/z in this case.
                            max_intensity = max(new_spec1)
                            update_mz = new_spec1.idxmax()
                            if max_intensity < sat_intensity:
                                peak_all.loc[j, 'mz'] = update_mz
                                break
    
    return peak_all.reset_index(drop=True)


# def split_peak_picking(ms1, profile=True, split_n=20, threshold=10, i_threshold=500, SN_threshold=3, peak_width=1,
#                        area_threshold=500, height_threshold=500, noise_threshold=0, rt_error_alignment=0.05,
#                        mz_error_alignment=0.015, mz_overlap=1, sat_intensity=False, orbi=True, step_size=0.02,
#                        message='', isotope_analysis=True):
#   """
#     Find peaks in the original ms1 list, analyze isotope and adduct information, and return a dataframe with
#     information on the peaks including retention time, m/z value, intensity, and area.
#
#     Args:
#         ms1 (scan list): List of MS1 scans generated from sep_scans(file.mzML).
#         profile (bool): Indicates whether the data is in profile mode (True) or centroid mode (False).
#         split_n (int): The number of pieces to split the large dataframe.
#         threshold (int): Threshold for finding peaks.
#         i_threshold (int): Threshold for peak intensity.
#         SN_threshold (float): Signal-to-noise threshold.
#         peak_width (float): The peak width for chromatographic peak detection.
#         area_threshold (float): The minimum peak area threshold. Peaks with an area below this threshold will be excluded from analysis.
#         height_threshold (float): The minimum peak height threshold. Peaks with a height below this threshold will be excluded from analysis.
#         noise_threshold (float): The noise threshold for peak detection.
#         rt_error_alignment (float): Retention time error alignment threshold.
#         mz_error_alignment (float): m/z error alignment threshold.
#         mz_overlap (float): The overlap between adjacent sections of data when splitting it.
#         sat_intensity (bool): Indicates whether to consider saturation intensity. False to disable.
#         orbi (bool): Indicates whether the data is in orbitrap data (True) or TOF-MS data (False).
#         step_size (float): Step size for data processing.
#         message (str): A message to display during processing.
#
#     Returns:
#         pandas.DataFrame: A dataframe with information on the peaks including retention time, m/z value,
#         intensity, and area.
#     """
#
#   def target_spec1(spec, target_mz, width=0.04):
#       """
#         :param spec: spec generated from function spec_at_rt()
#         :param target_mz: target mz for inspection
#         :param width: width for data points
#         :return: new spec and observed mz
#         """
#       index_left = argmin(abs(spec.index.values - (target_mz - width)))
#       index_right = argmin(abs(spec.index.values - (target_mz + width)))
#       new_spec = spec.iloc[index_left:index_right].copy()
#       new_spec[target_mz - width] = 0
#       new_spec[target_mz + width] = 0
#       new_spec = new_spec.sort_index()
#       return new_spec
#
#   # 1. Loading data...
#
#   if profile is True:
#       peaks_index = [[i, scipy.signal.find_peaks(ms1[i].i.copy())[0]]
#                      for i in tqdm(range(len(ms1)), desc=f'{message}Loading Data', leave=False, colour='Green')]
#       raw_info_centroid = {
#           round(ms1[i].scan_time[0], 3): pd.Series(
#               data=ms1[i].i[peaks],
#               index=ms1[i].mz[peaks].round(5),
#               name=round(ms1[i].scan_time[0], 3)) for i, peaks in
#           tqdm(peaks_index, desc=f'{message}Convert to Centroid', leave=False, colour='Green')}
#       raw_info_profile = {round(ms1[i].scan_time[0], 3):
#                               pd.Series(data=ms1[i].i, index=ms1[i].mz.round(5), name=round(ms1[i].scan_time[0], 3))
#                           for i in tqdm(range(len(ms1)), desc=f'{message}Recording raw profile info', leave=False,
#                                         colour='Green')}
#       if orbi is True:
#           data = []
#           for k, v in tqdm(raw_info_centroid.items(), desc=f'{message}Checking orbitrap data', leave=False,
#                            colour='Green'):
#               df = v.to_frame().reset_index()
#               df = df.sort_values(['index', k])
#               df.loc[:, 'index'] = np.round(df['index'].values, 3)
#               df = df.drop_duplicates('index', keep='last')
#               s = pd.Series(df[k].values, index=df['index'], name=k)
#               data.append(s)
#       else:
#           data = [pd.Series(data=v.values, index=v.index.values.round(3), name=v.name) for k, v in
#                   tqdm(raw_info_centroid.items(), leave=False, desc=f'{message}Appending centroid data',
#                        colour='Green')]
#   else:
#       raw_info_centroid = {round(ms1[i].scan_time[0], 3): pd.Series(
#           data=ms1[i].i, index=ms1[i].mz.round(5), name=round(ms1[i].scan_time[0], 3)) for i in
#           tqdm(range(len(ms1)), desc=f'{message}Loading Data', leave=False, colour='Green')}
#       if orbi is True:
#           data = []
#           for k, v in tqdm(raw_info_centroid.items(), desc=f'{message}Checking orbitrap data', leave=False,
#                            colour='Green'):
#               df = v.to_frame().reset_index()
#               df = df.sort_values(['index', k])
#               df.loc[:, 'index'] = np.round(df['index'].values, 3)
#               df = df.drop_duplicates('index', keep='last')
#               s = pd.Series(df[k].values, index=df['index'], name=k)
#               data.append(s)
#       else:
#           data = [pd.Series(data=v.values, index=v.index.values.round(3), name=v.name) for k, v in
#                   tqdm(raw_info_centroid.items(), desc=f'{message}Appending centroid data', leave=False,
#                        colour='Green')]
#
#   # 2. 开始分割
#   # 定义变量名称
#   all_data = []
#   for j in range(split_n):
#       name = 'a' + str(j + 1)
#       locals()[name] = []
#   # 对series进行切割
#   ms_increase = int(1700 / split_n)
#   for i in tqdm(range(len(data)), desc=f'{message}Split series', leave=False, colour='Green'):
#       s1 = data[i]
#       low, high = 50, 50 + ms_increase
#       for j in range(split_n):
#           name = 'a' + str(j + 1)
#           locals()[name].append(
#               s1[(s1.index < high + mz_overlap) & (s1.index >= low - mz_overlap) & (s1.index > noise_threshold)])
#           low += ms_increase
#           high += ms_increase
#   for j in range(split_n):
#       name = 'a' + str(j + 1)
#       all_data.append(locals()[name])
#
#   # 3. 开始分段提取
#   all_peak_all = []
#   for data in tqdm(all_data, desc=f'{message}Split peak picking process', leave=False, colour='Green'):
#       df1 = pd.concat(data, axis=1)
#       df1 = df1.fillna(0)
#       if len(df1) == 0:
#           pass
#       else:
#           peak_all = peak_picking(df1, isotope_analysis=False, threshold=threshold, peak_width=peak_width,
#                                   area_threshold=area_threshold,
#                                   height_threshold=height_threshold, i_threshold=i_threshold,
#                                   SN_threshold=SN_threshold,
#                                   rt_error_alignment=rt_error_alignment, mz_error_alignment=mz_error_alignment,
#                                   enable_progress_bar=False,
#                                   alignment=False, step_size=step_size)
#           all_peak_all.append(peak_all)
#
#   peak_all = pd.concat(all_peak_all).sort_values(by='intensity', ascending=False).reset_index(drop=True)
#
#   # 4. 做alignment
#   #  Perform alignment of the retention time (RT) and mass-to-charge ratio (m/z) pairs in the resulting dataframe.
#
#   # 组合 rt 和 mz 形成 KDTree 的数据点
#   data = np.column_stack((peak_all['rt'], peak_all['mz']))
#
#   # Scale the tolerances relative to the range of each dimension
#   rt_range = np.ptp(data[:, 0])
#   mz_range = np.ptp(data[:, 1])
#   if rt_range == 0:
#       rt_range = 0.01
#   if mz_range == 0:
#       mz_range = 0.001
#
#   scaled_rt_tol = rt_error_alignment / rt_range
#   scaled_mz_tol = mz_error_alignment / mz_range
#
#   # Create a KDTree with scaled data
#   scaled_data = data / [rt_range, mz_range]
#   tree = KDTree(scaled_data)
#
#   reference_list = []
#   visited = set()
#
#   for idx, scaled_pair in tqdm(enumerate(scaled_data), desc='Aligning all rt_mz pairs(split)', leave=False,
#                                colour='Green'):
#       if idx in visited:
#           continue
#
#       # Find neighbors within a spherical range that's sure to encompass the rectangular range
#       neighbors = tree.query_ball_point(scaled_pair, r=max(scaled_rt_tol, scaled_mz_tol))
#
#       # Filter these neighbors based on the actual tolerances
#       filtered_neighbors = [i for i in neighbors if abs(data[i, 0] - data[idx, 0]) <= rt_error_alignment
#                             and abs(data[i, 1] - data[idx, 1]) <= mz_error_alignment]
#
#       # Mark these neighbors as visited and add the first one to the reference list
#       visited.update(filtered_neighbors)
#       reference_list.append(data[idx])
#
#   # 转换为 NumPy 数组并创建 KDTree
#   reference_array = np.array(reference_list)
#   tree = KDTree(reference_array)
#
#   # 查询每个数据点的最近邻
#   _, indices = tree.query(data)
#
#   # 获取最近邻的 reference_array 对应的索引
#   aligned_indices = [f"{reference_array[idx][0]}_{reference_array[idx][1]}" for idx in indices]
#
#   # 添加新列到 DataFrame
#   peak_all['rt_mz'] = aligned_indices
#   peak_all = peak_all.sort_values(by='area', ascending=False)
#   peak_all = peak_all.drop_duplicates(subset='rt_mz', keep='first')
#   peak_all = peak_all.drop(labels='rt_mz', axis=1)
#
#   # 后面的isotope analysis和mz opt都需要用,不管是不是centroid
#   raw_info_rts = np.array([v.name for k, v in raw_info_centroid.items()])
#   # Convert rts and mzs to NumPy arrays if they aren't already
#   rts = np.array(peak_all.rt.values)
#   mzs = np.array(peak_all.mz.values)
#   # Vectorized calculation to find the closest rt_key for each rt value
#   rt_diffs = np.abs(raw_info_rts[:, np.newaxis] - rts)
#   closest_indices = np.argmin(rt_diffs, axis=0)
#   rt_keys = raw_info_rts[closest_indices]
#
#   # 5. 对同位素丰度进行记录
#   if isotope_analysis:
#       iso_info = [str(isotope_distribution(raw_info_centroid[rt_keys[i]], mzs[i]))
#                   for i in tqdm(range(len(mzs)), desc=f'{message}Recording iso_info', leave=False, colour='Green')]
#       peak_all['iso_distribution'] = iso_info
#
#   # 6. 更新质量数据
#   if profile is True:
#       spec1 = [raw_info_profile[i] for i in rt_keys]  # 获得ms的spec,*
#       mz_result = np.array(
#           [list(evaluate_ms(target_spec1(spec1[i], mzs[i], width=0.04).copy(), mzs[i])) for i
#            in tqdm(range(len(mzs)), desc=f'{message} Correcting m/z', leave=False)]).T
#       mz_obs, mz_opt, resolution = mz_result[0], mz_result[2], mz_result[4]
#       mz_opt = [mz_opt[i] if abs(mzs[i] - mz_opt[i]) < 0.02 else
#                 mzs[i] for i in tqdm(range(len(mzs)), desc=f'{message}Checking the corrected m/z', leave=False,
#                                      colour='Green')]  # 去掉偏差大的矫正结果
#
#       peak_all.loc[:, ['mz', 'mz_opt', 'resolution']] = np.array([mz_obs, mz_opt, resolution.astype(int)]).T
#   else:
#       spec1 = [raw_info_centroid[i] for i in rt_keys]  # 获得ms的spec,*
#       target_spec = [spec1[i][(spec1[i].index > mzs[i] - 0.015) & (spec1[i].index < mzs[i] + 0.015)] for i in
#                      tqdm(range(len(spec1)), desc=f'{message}Correcting m/z', leave=False, colour='Green')]
#       mzs_obs = [
#           target_spec[i].index.values[[np.argmax(target_spec[i].values)]][0] if len(target_spec[i]) != 0 else mzs[i]
#           for i in tqdm(range(len(target_spec)), desc=f'{message}Checking obs m/z', leave=False, colour='Green')]
#       peak_all['mz'] = mzs_obs
#
#   peak_all = peak_all.reset_index(drop=True)  # 先更新一下index
#   # 如果担心饱和质量不准，使用sat_intensity 更新质量
#   if (sat_intensity is False) | (sat_intensity is None) | (sat_intensity < 100000) | (sat_intensity == ''):
#       pass
#   else:
#       if profile is True:
#           for j in tqdm(range(len(peak_all)), desc=f'{message}Optimize m/z based on sat_intensity', leave=False,
#                         colour='Green'):
#               mz = peak_all.loc[j, 'mz']
#               rt = peak_all.loc[j, 'rt']
#               intensity = peak_all.loc[j, 'intensity']
#               if intensity > sat_intensity:
#                   for k, v in raw_info_profile.items():
#                       if k > rt:  # find the time
#                           s1 = raw_info_profile[k]
#                           new_spec1 = target_spec1(s1, mz,
#                                                    0.2)  # cut the spectrum in a certain range. 1 m/z in this case.
#                           peak_index, *_ = scipy.signal.find_peaks(new_spec1.values)
#                           if max(new_spec1.values[peak_index]) < sat_intensity:
#                               insat_mz_obs, error1, insat_mz_opt, error2, resolution = evaluate_ms(new_spec1, mz)
#                               peak_all.loc[j, 'mz'] = insat_mz_obs
#                               peak_all.loc[j, 'mz_opt'] = insat_mz_opt
#                               peak_all.loc[j, 'resolution'] = resolution
#                               break
#       else:
#           for j in tqdm(range(len(peak_all)), desc=f'{message}Optimize m/z based on sat_intensity', leave=False,
#                         colour='Green'):
#               mz = peak_all.loc[j, 'mz']
#               rt = peak_all.loc[j, 'rt']
#               intensity = peak_all.loc[j, 'intensity']
#               if intensity > sat_intensity:
#                   for k, v in raw_info_centroid.items():
#                       if k > rt:  # find the time
#                           s1 = raw_info_centroid[k]
#                           new_spec1 = target_spec1(s1, mz,
#                                                    0.2)  # cut the spectrum in a certain range. 1 m/z in this case.
#                           max_intensity = max(new_spec1)
#                           update_mz = new_spec1.idxmax()
#                           if max_intensity < sat_intensity:
#                               peak_all.loc[j, 'mz'] = update_mz
#                               break
#   return peak_all.reset_index(drop=True)


def remove_unnamed_columns(df):
    """
    Remove any columns in the input DataFrame that are named 'Unnamed:*'.

    Args:
        df (pandas.DataFrame): The input DataFrame to process.

    Returns:
        pandas.DataFrame: A new DataFrame with the 'Unnamed:*' columns removed.
    """
    unnamed_columns = [col for col in df.columns if col.startswith('Unnamed:')]
    return df.drop(columns=unnamed_columns).reset_index(drop=True)


def identify_isotopes(cmp, iso_error=0.005, rt_error=0.015):
    """
    Identify isotopes and adducts in the unique compounds dataframe based on their mass-to-charge ratio (m/z) and retention time (rt).

    Args:
        cmp: pandas DataFrame of unique compounds
        iso_error: maximum allowable mass error for identifying isotopes and adducts

    Returns:
        A pandas DataFrame with the identified isotopes and adducts labeled.

    """
    # 元素周期表
    atom_mass_table1 = pd.Series(
        data={'C': 12.000000, 'Ciso': 13.003355, 'N': 14.003074, 'Niso': 15.000109, 'O': 15.994915, 'H': 1.007825,
              'Oiso': 17.999159, 'F': 18.998403, 'K': 38.963708, 'P': 30.973763, 'Cl': 34.968853, 'Cliso': 36.965903,
              'S': 31.972072, 'Siso': 33.967868, 'Br': 78.918336, 'Briso': 80.916290, 'Na': 22.989770, 'Si': 27.976928,
              'Fe': 55.934939, 'Se': 79.916521, 'As': 74.921596, 'I': 126.904477, 'D': 2.014102,
              'Co': 58.933198, 'Au': 196.966560, 'B': 11.009305, 'e': 0.0005486
              })
    
    # 计算不同同位素和adducts之间的差值
    Ciso = atom_mass_table1['Ciso'] - atom_mass_table1['C']
    Cliso = atom_mass_table1['Cliso'] - atom_mass_table1['Cl']
    Na = atom_mass_table1['Na'] - atom_mass_table1['H']
    K = atom_mass_table1['K'] - atom_mass_table1['H']
    NH3 = 3 * atom_mass_table1['H'] + atom_mass_table1['N']
    
    all_rts = list(set(cmp['rt'].values))
    for i in tqdm(range(len(all_rts)), desc='Finding Isotopes and adducts', leave=False):
        cmp_rt = cmp[(cmp['rt'] >= all_rts[i] - rt_error) & (cmp['rt'] <= all_rts[i] + rt_error)].sort_values(by='mz')
        mzs = cmp_rt['mz'].values
        for mz in mzs:
            C_fold = 1
            differ = mzs - mz
            # 拿到此mz的intensity
            mz_i = cmp_rt[cmp_rt['mz'] == mz]['intensity'].values[0]  # 数值
            
            # 搜索C13同位素
            i_C13_1 = np.where((differ < Ciso + iso_error) & (differ > Ciso - iso_error))[0]
            if len(i_C13_1) == 0:
                pass
            elif len(i_C13_1) == 1:
                index_ = cmp_rt.index[i_C13_1]
                compare_i = cmp_rt.loc[index_, 'intensity'].values[0]
                if mz_i * C_fold > compare_i:
                    cmp.loc[index_, 'Ciso'] = f'C13:{all_rts[i]} _{mz}'
            else:
                index_ = cmp_rt.index[i_C13_1]
                for index in index_:
                    compare_i = cmp_rt.loc[index, 'intensity']
                    if mz_i * C_fold > compare_i:
                        cmp.loc[index, 'Ciso'] = f'C13: {all_rts[i]} _{mz}'
            
            # 搜索Cl同位素
            i_Cl = np.where((differ < Cliso + iso_error) & (differ > Cliso - iso_error))[0]
            if len(i_Cl) == 0:
                pass
            elif len(i_Cl) == 1:
                index_ = cmp_rt.index[i_Cl]
                compare_i = cmp_rt.loc[index_, 'intensity'].values[0]
                if (mz_i * 0.45 > compare_i) & (mz_i * 0.2 < compare_i):
                    cmp.loc[index_, 'Cliso'] = f'1Cl:{all_rts[i]}_{mz}'
                elif (mz_i * 0.5 < compare_i) & (mz_i * 0.8 > compare_i):
                    cmp.loc[index_, 'Cliso'] = f'2Cl:{all_rts[i]}_{mz}'
                elif (mz_i * 0.8 < compare_i) & (mz_i * 1.2 > compare_i):
                    cmp.loc[index_, 'Briso'] = f'1Br:{all_rts[i]}_{mz}'
                elif (mz_i * 1.5 < compare_i) & (mz_i * 2.5 > compare_i):
                    cmp.loc[index_, 'Briso'] = f'2Br:{all_rts[i]}_{mz}'
            
            else:
                index_ = cmp_rt.index[i_Cl]
                for index in index_:
                    compare_i = cmp_rt.loc[index, 'intensity']
                    if (mz_i * 0.45 > compare_i) & (mz_i * 0.2 < compare_i):
                        cmp.loc[index, 'Cliso'] = f'1Cl:{all_rts[i]}_{mz}'
                    elif (mz_i * 0.5 < compare_i) & (mz_i * 0.8 < compare_i):
                        cmp.loc[index_, 'Cliso'] = f'2Cl:{all_rts[i]}_{mz}'
                    elif (mz_i * 0.8 < compare_i) & (mz_i * 1.2 > compare_i):
                        cmp.loc[index_, 'Briso'] = f'1Br:{all_rts[i]}_{mz}'
                    elif (mz_i * 1.5 < compare_i) & (mz_i * 2.5 > compare_i):
                        cmp.loc[index_, 'Briso'] = f'2Br:{all_rts[i]}_{mz}'
            
            # 搜索+Na+峰
            i_Na = np.where((differ < Na + iso_error) & (differ > Na - iso_error))[0]  # Na+:22.9892, Na+-H: 21.9814
            if len(i_Na) == 0:
                pass
            elif len(i_Na) == 1:
                index_ = cmp_rt.index[i_Na]
                cmp.loc[index_, 'Na adducts'] = f'Na adducts: {all_rts[i]} _{mz}'
            
            else:
                index_ = cmp_rt.index[i_Na]
                for index in index_:
                    cmp.loc[index, 'Na adducts'] = f'Na adducts: {all_rts[i]} _{mz}'
            
            # 搜索+K+峰
            i_Na = np.where((differ < K + iso_error) & (differ > K - iso_error))[0]
            if len(i_Na) == 0:
                pass
            elif len(i_Na) == 1:
                index_ = cmp_rt.index[i_Na]
                cmp.loc[index_, 'K adducts'] = f'K adducts: {all_rts[i]} _{mz}'
            
            else:
                index_ = cmp_rt.index[i_Na]
                for index in index_:
                    cmp.loc[index, 'K adducts'] = f'K adducts: {all_rts[i]} _{mz}'
            
            # 搜索+NH4+峰
            i_NH4 = np.where((differ < NH3 + iso_error) & (differ > NH3 - iso_error))[0]  # NH3:17.0266
            if len(i_NH4) == 0:
                pass
            elif len(i_NH4) == 1:
                index_ = cmp_rt.index[i_NH4]
                cmp.loc[index_, 'NH4 adducts'] = f'NH4 adducts:  {all_rts[i]} _{mz}'
            else:
                index_ = cmp_rt.index[i_NH4]
                for index in index_:
                    cmp.loc[index, 'NH4 adducts'] = f'NH4 adducts: {all_rts[i]} _{mz}'
    
    iso_adducts_df = cmp[
        [i for i in cmp.columns if i in ['Ciso', 'Cliso', 'Na adducts', 'NH4 adducts', 'Briso', 'K adducts']]]
    cmp.loc[:, 'isotope/adducts label'] = iso_adducts_df.apply(
        lambda row: {item.split(':', 1)[0].strip(): item.split(':', 1)[1].strip()
                     for item in row.dropna() if ':' in item}, axis=1).astype(str)
    cmp.drop(columns=['Ciso', 'Cliso', 'Na adducts', 'NH4 adducts', 'Briso', 'K adducts'], errors='ignore',
             inplace=True)
    sorted_columns = sort_columns_name(cmp.columns)
    cmp = cmp.loc[:, sorted_columns]
    return cmp


def sort_columns_name(columns):
    """
    :param columns: columns need to sort
    :return: new_columns
    """
    final_columns = []
    locators = ['new_index', 'rt', 'mz', 'intensity', 'S/N', 'area', 'area_mean', 'area_std', 'mz_opt',
                'frag_DIA', 'frag_DDA', 'iso_distribution', 'resolution', 'isotope/adducts label', 'fold_change',
                'p_values']
    for name in locators:
        if name in columns:
            final_columns.append(name)
    for name in columns:
        if name not in final_columns:
            final_columns.append(name)
    return final_columns


def peak_alignment(files_excel, rt_error=0.1, mz_error=0.015):
    """
    Alignment all the mz&rt pair, combining the rt&mz pairs with specific rt_error and mz_erros, and generating reference mz&rt pair.Then go to each result excel file, and based on each rt&mz pair, assign a reference mz&rt pair
    Args:
        files_excel: files path list for excels of peak picking and peak checking;
        rt_error: rt error for combining
        mz_error: mz error for combining
    returns:
        Export to excel files
    """
    
    peak_ref = gen_ref(files_excel, rt_error=rt_error, mz_error=mz_error)
    pd.DataFrame(peak_ref, columns=['rt', 'mz']).to_excel(
        os.path.join(os.path.split(files_excel[0])[0], 'peak_ref.xlsx'))
    for file in tqdm(files_excel, desc='Alignment', leave=False, colour='Green'):
        peak_p = pd.read_excel(file, index_col='Unnamed: 0').loc[:, ['rt', 'mz']].values
        peak_df = pd.read_excel(file, index_col='Unnamed: 0')
        new_all_index = []
        for i in range(len(peak_p)):
            rt1, mz1 = peak_p[i]
            index = np.where((peak_ref[:, 0] <= rt1 + rt_error) & (peak_ref[:, 0] >= rt1 - rt_error)
                             & (peak_ref[:, 1] <= mz1 + mz_error) & (peak_ref[:, 1] >= mz1 - mz_error))
            new_index = str(peak_ref[index][0][0]) + '_' + str(peak_ref[index][0][1])
            new_all_index.append(new_index)
        peak_df.loc[:, 'new_index'] = new_all_index
        peak_df = peak_df.set_index('new_index')
        peak_df = peak_df[~peak_df.index.duplicated(keep='first')]
        peak_df.to_excel(file.replace('.xlsx', '_alignment.xlsx'))


def gen_ref(files_excel, rt_error=0.1, mz_error=0.015):
    data1 = [pd.read_excel(file).loc[:, ['rt', 'mz']].values
             for file in tqdm(files_excel, desc='Reading each excel file',
                              leave=False, colour='Green', ncols=100)]
    
    # Concatenate all peaks
    data = np.vstack(data1)
    
    # Scale the tolerances relative to the range of each dimension
    rt_range = np.ptp(data[:, 0])
    mz_range = np.ptp(data[:, 1])
    scaled_rt_tol = rt_error / rt_range
    scaled_mz_tol = mz_error / mz_range
    
    # Create a KDTree with scaled data
    scaled_data = np.copy(data)
    scaled_data[:, 0] /= rt_range
    scaled_data[:, 1] /= mz_range
    tree = KDTree(scaled_data)
    
    reference_list = []
    visited = set()
    
    for idx, scaled_pair in tqdm(enumerate(scaled_data), desc='Aligning all rt_mz pairs(gen_df)', leave=False,
                                 colour='Green'):
        if idx in visited:
            continue
        
        # Find neighbors within a spherical range that's sure to encompass the rectangular range
        neighbors = tree.query_ball_point(scaled_pair, r=max(scaled_rt_tol, scaled_mz_tol))
        
        # Filter these neighbors based on the actual tolerances
        filtered_neighbors = [i for i in neighbors if abs(data[i, 0] - data[idx, 0]) <= rt_error
                              and abs(data[i, 1] - data[idx, 1]) <= mz_error]
        
        # Mark these neighbors as visited and add the first one to the reference list
        visited.update(filtered_neighbors)
        reference_list.append(data[idx])
    
    return np.array(reference_list)


def second_process(file, ref_all, company, profile=True, long_rt_split_n=1, orbi=False, message=''):
    """
    This function will use the reference rt&mz pair, and obtain the peak area at specific rt & mz
    Args:
        profile: True or False
        file: single file to process
        ref_all: all reference peaks
        company: e.g., 'Waters', 'Agilent',etc,
        orbi: A boolean indicating whether the data is in orbitrap data (True) or TOF-MS data (False)
    returns:
        export to files

    """
    try:
        ms_round = 4
        ms1, ms2 = sep_scans(file, company, message=message)
        
        name1 = os.path.basename(file).split('.mzML')[0]
        final_result = ultimate_checking_area(ref_all, ms1, name1, profile=profile,
                                              rt_overlap=1, long_rt_split_n=long_rt_split_n, orbi=orbi, message=message)
        final_result.to_excel(file.replace('.mzML', '_final_area.xlsx'))
    
    except Exception as e:
        # 捕获异常并将异常信息保存到error_info变量
        error_info = traceback.format_exc()
        print(error_info)


def ultimate_checking_area(ref_all, ms1, name1, profile=True,
                           split_n=20, rt_overlap=1, long_rt_split_n=4, orbi=False, message=''):
    """
    Based on peak reference, intergrate peak are for each reference m/z and retention time pair.

    Args:
        ref_all: reference m/z and retention time pair
        ms1: generated from sep_scans(file.mzML).
        name1: file name.
        profile: A boolean indicating whether the data is in profile mode (True) or centroid mode (False)
        split_n: The number of pieces to split the large dataframe.
        long_rt_split_n: The number of pieces to split the ms1.
        rt_overlap: The rt overlap (min) between adjacent sections of data when splitting it.
        orbi: A boolean indicating whether the data is in orbitrap data (True) or TOF-MS data (False)
    return:
        The final areas for reference m/z and retention time pair.
    """
    
    if long_rt_split_n == 1:
        final_area = peak_checking_area_split(ref_all, ms1, name1, profile=profile, split_n=split_n, noise_threshold=0,
                                              orbi=orbi, message=message)
    
    else:
        # Calculate the length of each part
        total_spectra = len(ms1)
        part_length = total_spectra // long_rt_split_n
        overlap_spectra = int(rt_overlap / (ms1[1].scan_time[0] - ms1[0].scan_time[
            0]))  # calculate the number of spectra in 1 minute of retention time
        
        # Split the list into parts
        parts = []
        for i in range(long_rt_split_n):
            start_index = i * part_length - overlap_spectra
            start_index = max(start_index, 0)  # set start index to 0 if it is less than 0
            end_index = (i + 1) * part_length + overlap_spectra
            part = ms1[start_index:end_index]
            parts.append(part)
        
        # Add any remaining spectra to the last part
        if end_index < total_spectra:
            last_part = ms1[end_index:]
            parts[-1] += last_part
        
        parts1 = [ms1[i * part_length:(i + 1) * part_length] for i in range(long_rt_split_n)]
        mz_list = [round(part[0].scan_time[0], 3) for part in parts1]
        mz_list.append(parts1[-1][-1].scan_time[0])
        ranges = [[mz_list[i], mz_list[i + 1]] for i in range(len(mz_list) - 1)]
        # start to split ref_all
        ref_all = remove_unnamed_columns(ref_all)
        ref_all_parts = [ref_all[(ref_all['rt'] >= ranges1[0]) & (ref_all['rt'] < ranges1[1])] for ranges1 in ranges]
        
        # start to collect each peak_all
        peak_area_all = []
        for i in range(len(parts)):
            each_peak_area = peak_checking_area_split(ref_all_parts[i], parts[i], '', profile=profile, split_n=split_n,
                                                      orbi=orbi)
            peak_area_all.append(each_peak_area)
        final_area = pd.concat(peak_area_all)
        final_area.columns = [name1]
    return final_area


def peak_checking_area(ref_all, df1, name, sn_info=False):
    """
    Obtain the area for each rt&mz pair in df1
    :param ref_all:  peak_reference
    :param df1: dataframe df1
    :param name: name
    :return: new_dataframe
    """
    df1.sort_index(inplace=True)
    # 1. sort ref_all, obtain the rts and mzs
    ref_all1 = ref_all.sort_values(by='mz')
    rts, mzs = ref_all1.rt.values, ref_all1.mz.values
    peak_index = np.array([str(rts[i]) + '_' + str(mzs[i]) for i in range(len(rts))])
    # 2. find locators of mz
    df_mz_list = sorted(df1.index.values)
    left_locator = find_locators(df_mz_list, mzs - 0.015)
    right_locator = find_locators(df_mz_list, mzs + 0.015)
    mz_locators = np.array([left_locator, right_locator]).T
    
    # 3. find the locators of rt
    df_rt = df1.columns.values
    rt_locators = [[argmin(abs(df_rt - (rt - 0.2))), argmin(abs(df_rt - (rt + 0.2)))] for rt in rts]
    rt_locators = [[x[0], x[1] if x[0] != x[1] else x[1] + 1] for x in rt_locators]  # 有时候locators是一样的[616:616] 加个保护机制
    # 4. obtain the peak areas
    area_all = []
    #     rt_target_all = []
    #     eic_target_all = []
    for i in range(len(mz_locators)):
        # 截取数据
        df2 = df1.iloc[mz_locators[i][0]:mz_locators[i][1],
              rt_locators[i][0]:rt_locators[i][1]]
        sub_array = df2.values
        # 按列求和
        column_sums = sub_array.sum(axis=0)
        # 计算Simpson积分
        integral = scipy.integrate.simpson(column_sums - min(column_sums))
        # 对积分结果四舍五入，并加1
        rounded_integral = round(integral, 0) + 1
        # 将结果添加到列表中
        area_all.append(rounded_integral)
    # 获得原始数据
    #         rt_target_all.append(str(df2.columns.values))
    #         eic_target_all.append(str(df2.sum(axis=0).values))
    # Uses the locators found in stepas 2 and 3 to calculate the peak areas for each rt&mz pair in `df1`, using the `scipy.integrate.simps` function.
    
    if sn_info == False:
        sample_area = pd.DataFrame(area_all, index=peak_index, columns=[name])
        return sample_area  # Adds 1 to each value in the resulting data frame and returns it to avoid zero value in result.
    else:
        rt_locators_point = [argmin(abs(df_rt - rt)) for rt in rts]
        sn_all = []
        for i in range(len(mz_locators)):
            df2 = df1.iloc[mz_locators[i][0]:mz_locators[i][1], :]
            eic = df2.values.sum(axis=0)
            try:
                bg = int(cal_bg(eic))
            except:
                bg = np.inf
            peak_height = eic[rt_locators_point[i]]
            sn = round(peak_height / bg, 1)
            sn_all.append(sn)
        sample_area = pd.DataFrame({f'{name}': area_all, f'{name}_S/N': sn_all}, index=peak_index)
        return sample_area


def peak_checking_area_split(ref_all, ms1, name1, profile=True, split_n=20, noise_threshold=0, orbi=False, message='',
                             sn_info=False):
    # 需要给ref_all排序
    
    ref_all1 = ref_all.sort_values(by='mz')
    
    if profile is True:
        raw_info_centroid = {}
        
        for i in tqdm(range(len(ms1)), desc=f'{message} Loading Data', leave=False, colour='Green'):
            # 1. 记录profile原始数据
            key1 = round(ms1[i].scan_time[0], 3)
            mz_info = ms1[i].mz.round(5).astype(np.float32)
            intensity_info = ms1[i].i.round(0).astype(np.float32)
            
            # 2. 找spec的index，记录centroid原始数据
            peak_idx = scipy.signal.find_peaks(intensity_info)[0]
            mz_info1 = mz_info[peak_idx]
            intensity_info1 = intensity_info[peak_idx]
            array2 = np.array([mz_info1, intensity_info1])
            raw_info_centroid[key1] = array2
    
    else:
        raw_info_centroid = {}
        for i in tqdm(range(len(ms1)), desc=f'{message} Loading Data', leave=False, colour='Green'):
            key1 = round(ms1[i].scan_time[0], 3)
            mz_info = ms1[i].mz.round(5).astype(np.float32)
            intensity_info = ms1[i].i.round(0).astype(np.float32)
            array1 = np.array([mz_info, intensity_info])
            raw_info_centroid[key1] = array1
    
    # 第二步 将样品按照质量分割
    # 清理变量
    ms1.clear()
    ms1 = None  # 这样不会影响外部
    gc.collect()
    # 2. 开始分割
    
    all_data = [[] for _ in range(split_n)]
    ms_increase = int(1700 / split_n)
    
    for i, (k, v) in tqdm(enumerate(raw_info_centroid.items()), desc=f'{message} Split series', leave=False,
                          colour='Green'):
        s1 = pd.Series(data=v[1], index=v[0], name=k)
        s1.index = np.round(s1.index.values, 3).astype(np.float32) # s1.index.round(3).astype(np.float32)
        s1 = s1.groupby(s1.index).max()
        low, high = 50, 50 + ms_increase
        for j in range(split_n):
            # 直接用 list 存储，避免 locals()
            filtered_s1 = s1[
                (s1.index < high + 0.1) & (s1.index >= low - 0.1) & (s1.index > noise_threshold)]
            all_data[j].append(filtered_s1)
            
            low += ms_increase
            high += ms_increase
    
    # 开始分割peak_ref
    all_peak_ref = []
    # 对peak_ref进行切割
    ms_increase = int(1700 / split_n)
    low, high = 50, 50 + ms_increase
    for j in range(split_n):
        name = 'b' + str(j + 1)
        locals()[name] = ref_all1[(ref_all1.mz < high) & (ref_all1.mz >= low)]
        low += ms_increase
        high += ms_increase
        all_peak_ref.append(locals()[name])
    
    # 获取所有area
    area_all = []
    for i in tqdm(range(split_n), desc=f'{message}Collecting area info', leave=False, colour='Green'):
        peak_ref1 = all_peak_ref[i]
        df1 = pd.concat(all_data[i], axis=1)
        if len(df1) == 0:
            pass
        else:
            df1 = df1.fillna(0).sort_index()
            df_area = peak_checking_area(peak_ref1, df1, 'split', sn_info=sn_info)
            area_all.append(df_area)
        all_data[i] = None
    
    # 合成所有的area
    
    filtered_area_all = [df for df in area_all if not df.empty and not df.isna().all().all()]
    final_df = pd.concat(filtered_area_all)
    final_df.columns = [name1] if len(final_df.columns) == 1 else [name1, f'{name1}_S/N']
    return final_df


#
# def peak_checking_area_split(ref_all, ms1, name1, profile=True, split_n=20, noise_threshold=0, orbi=False, message='',
#                              sn_info=False):
#   # 需要给ref_all排序
#
#   ref_all1 = ref_all.sort_values(by='mz')
#
#   if profile is True:
#       peaks_index = [[i, scipy.signal.find_peaks(ms1[i].i.copy())[0]]
#                      for i in tqdm(range(len(ms1)), desc=f'{message}Loading Data', leave=False, colour='Green')]
#       raw_info_centroid = {
#           round(ms1[i].scan_time[0], 3): pd.Series(
#               data=ms1[i].i[peaks], index=ms1[i].mz[peaks].round(4),
#               name=round(ms1[i].scan_time[0], 3)) for i, peaks in tqdm(
#               peaks_index, desc=f'{message}Loading Data', leave=False, colour='Green')}
#       if orbi is True:
#           data = []
#           for k, v in tqdm(raw_info_centroid.items(), desc=f'{message}Checking orbitrap data', leave=False,
#                            colour='Green'):
#               df = v.to_frame().reset_index()
#               df = df.sort_values(['index', k])
#               df.loc[:, 'index'] = np.round(df['index'].values, 3)
#               df = df.drop_duplicates('index', keep='last')
#               s = pd.Series(df[k].values, index=df['index'], name=k)
#               data.append(s)
#       else:
#           data = [pd.Series(data=v.values, index=v.index.values.round(3), name=v.name) for k, v in
#                   tqdm(raw_info_centroid.items(), desc=f'{message}Appending centroid data', leave=False,
#                        colour='Green')]
#   else:
#       raw_info_centroid = {round(ms1[i].scan_time[0], 3): pd.Series(
#           data=ms1[i].i, index=ms1[i].mz.round(4), name=round(ms1[i].scan_time[0], 3)) for i in
#           tqdm(range(len(ms1)), desc=f'{message}Loading Data', leave=False, colour='Green')}
#
#       if orbi is True:
#           data = []
#           for k, v in tqdm(raw_info_centroid.items(), desc=f'{message}Checking orbitrap data', leave=False,
#                            colour='Green'):
#               df = v.to_frame().reset_index()
#               df = df.sort_values(['index', k])
#               df.loc[:, 'index'] = np.round(df['index'].values, 3)
#               df = df.drop_duplicates('index', keep='last')
#               s = pd.Series(df[k].values, index=df['index'], name=k)
#               data.append(s)
#       else:
#           data = [pd.Series(data=v.values, index=v.index.values.round(3), name=v.name) for k, v in
#                   tqdm(raw_info_centroid.items(), desc=f'{message}Appending centroid data', leave=False,
#                        colour='Green')]
#
#   # 开始分割 series数据
#   # 定义变量名称
#   all_data = []
#   for j in range(split_n):
#       name = 'a' + str(j + 1)
#       locals()[name] = []
#   # 对series进行切割
#   ms_increase = int(1700 / split_n)
#   for i in tqdm(range(len(data)), desc=f'{message}Split series', leave=False, colour='Green'):
#       s1 = data[i]
#       low, high = 50, 50 + ms_increase
#       for j in range(split_n):
#           name = 'a' + str(j + 1)
#           locals()[name].append(s1[(s1.index < high + 0.1) & (s1.index >= low - 0.1) & (s1.index > noise_threshold)])
#           low += ms_increase
#           high += ms_increase
#   for j in range(split_n):
#       name = 'a' + str(j + 1)
#       all_data.append(locals()[name])
#
#   # 开始分割peak_ref
#   all_peak_ref = []
#   # 对peak_ref进行切割
#   ms_increase = int(1700 / split_n)
#   low, high = 50, 50 + ms_increase
#   for j in range(split_n):
#       name = 'b' + str(j + 1)
#       locals()[name] = ref_all1[(ref_all1.mz < high) & (ref_all1.mz >= low)]
#       low += ms_increase
#       high += ms_increase
#       all_peak_ref.append(locals()[name])
#
#   # 获取所有area
#   area_all = []
#   for i in tqdm(range(split_n), desc=f'{message}Collecting area info', leave=False, colour='Green'):
#       peak_ref1 = all_peak_ref[i]
#       df1 = pd.concat(all_data[i], axis=1)
#       if len(df1) == 0:
#           pass
#       else:
#           df1 = df1.fillna(0).sort_index()
#           df_area = peak_checking_area(peak_ref1, df1, 'split', sn_info=sn_info)
#           area_all.append(df_area)
#
#   # 合成所有的area
#
#   filtered_area_all = [df for df in area_all if not df.empty and not df.isna().all().all()]
#   final_df = pd.concat(filtered_area_all)
#   final_df.columns = [name1] if len(final_df.columns) == 1 else [name1, f'{name1}_S/N']
#   return final_df


def concat_alignment(files_excel):
    """
    Concatenate all dataframes containing 'area' in their name
    and return the final dataframe.

    Args:
        files_excel: list of excel file paths.

    Returns:
        pandas.DataFrame: concatenated dataframe.
    """
    align = [file for file in files_excel if 'area' in file]
    data = {}
    data_to_concat = []
    for i in tqdm(range(len(align)), desc='Concatenating all areas', leave=False, colour='Green'):
        name = 'data' + str(i)
        data[name] = pd.read_excel(align[i], index_col='Unnamed: 0')
        data_to_concat.append(data[name])
    final_data = pd.concat(data_to_concat, axis=1)
    return final_data


def fold_change_filter(path, control_group=['lab_blank'], filter_type=1):
    """
    This function calculates the fold change and optionally p-values
    by comparing a set of samples to a control group.

    The computation of fold change differs based on whether the data
    consists of triplicates or not, which is determined by the 'filter_type' parameter.

    Args:
        path (str): The file path for the mzML files to be processed.
        control_group (List[str]): A list of labels representing the control group.
                                   These labels are used in the search for relevant file names.
        filter_type (int): Determines the mode of operation.
                           Set to 1 for data without triplicates; fold change is computed
                           as the ratio of the sample area to the maximum control area.
                           Set to 2 for data with triplicates; the function will calculate p-values,
                           and fold change is computed as the ratio of the mean sample area
                           to the mean control area.

    Returns:
        None. The output, saved as an Excel file with the suffix '_unique_cmps.xlsx',
        contains the computed fold change (and p-values if 'filter_type' is set to 2).
    """
    
    # Assume df1 and df2 are your dataframes
    
    def calculate_p_value(row1, row2):
        t_stat, p_value = ttest_ind(row1, row2)
        return p_value
    
    # locate files data with alignment and final_area.
    excel_path = os.path.join(path, '*.xlsx')
    files_excel = glob(excel_path)
    alignment = [file for file in files_excel if 'alignment' in file]
    area_files = [file for file in files_excel if 'final_area' in file]
    
    # Use control_group variable in file checks
    blk_files = [file for file in area_files if
                 any(group.lower() in os.path.basename(file).lower() for group in control_group)]
    
    blk_df = concat_alignment(blk_files)  # 生成所有blank的dataframe表
    
    # 整合每个area_file与blank的对比结果，输出fold change 大于fold_change倍的值
    area_files_sample = [file for file in area_files if
                         not any(group.lower() in os.path.basename(file).lower() for group in control_group)]
    
    if filter_type == 1:
        all_names = list(
            set([os.path.basename(x).replace('_final_area.xlsx', '') for x in area_files_sample]))  # 拿到所有样品名称
        for i in tqdm(range(len(area_files_sample)), desc='Fold change processing', leave=False, colour='Green'):
            # 基于峰面积的对比拿到比较数据
            sample = pd.read_excel(area_files_sample[i], index_col='Unnamed: 0')
            # 开始处理alignment文件，不能有重复的index
            name = os.path.basename(area_files_sample[i]).replace('_final_area.xlsx', '') + '_alignment'  # 拿到名字
            alignment_path = [file for file in alignment if name  + '.xlsx'  == os.path.basename(file)][0]
            alignment_df = pd.read_excel(alignment_path, index_col='new_index').sort_values(by='intensity')
            alignment_df1 = alignment_df[~alignment_df.index.duplicated(keep='last')]  # 去掉重复索引
            # 找到共有的new_index
            final_index = np.intersect1d(alignment_df1.index.values, sample.index.values)
            
            for control in control_group:
                final_blk = blk_df.loc[:, [i for i in blk_df.columns if control in i]]
                if len(final_blk.columns) > 1:
                    final_blk = final_blk.max(axis=1)
                elif len(final_blk.columns) < 1:
                    print(f'"{control}" is not in the files!')
                compare = pd.concat((sample, final_blk), axis=1)
                compare[f'{control}_fold_change'] = (compare.iloc[:, 0] / compare.iloc[:, 1]).round(2)
                compare1 = compare.loc[final_index]
                compare2 = compare1.iloc[:, -1:]
                alignment_df1 = pd.concat([alignment_df1, compare2], axis=1)
            alignment_df1 = alignment_df1.sort_values(by='intensity', ascending=False)
            alignment_df1.index.name = 'new_index'
            alignment_df1.to_excel(alignment_path.replace('_alignment', '_unique_cmps'))
    elif filter_type == 2:
        all_names = list(
            set([os.path.basename(x).replace('_final_area.xlsx', '')[:-1] for x in area_files_sample]))  # 拿到所有样品名称
        # 根据样品名称一个个处理
        for name in tqdm(all_names, desc='Processing triplicate samples', leave=False, colour='Green'):
            # 获得该名称下的文件
            sample_files = [file for file in area_files_sample if name in os.path.basename(file)]
            # 获得所有final_area
            sample_df_all = []
            for sample_file in sample_files:
                df = pd.read_excel(sample_file, index_col='Unnamed: 0')
                sample_df_all.append(df)
            sample_final_area = pd.concat(sample_df_all, axis=1)
            # 计算样品平均值和方差
            sample_mean = round(sample_final_area.mean(axis=1), 0)
            sample_std = round(sample_final_area.std(axis=1) / sample_final_area.mean(axis=1), 2)
            sample_area_info = pd.concat([sample_mean, sample_std], axis=1)
            sample_area_info.columns = ['Sample_area_mean', 'Sample_area_std']
            # 获得所有control的结果
            all_result = []
            for control in control_group:
                control_column = [column for column in blk_df.columns if control in column]
                if len(control_column) == 0:
                    pass
                else:
                    control_df = blk_df.loc[:, control_column]
                    p_values = sample_final_area.apply(lambda row: calculate_p_value(row, control_df.loc[row.name]),
                                                       axis=1)
                    p_values.name = f'{control}_p_values'
                    all_result.append(p_values)
                    fold_change = round(sample_final_area.mean(axis=1) / control_df.mean(axis=1), 2)
                    fold_change.name = f'{control}_fold_change'
                    all_result.append(fold_change)
            all_result_df = pd.concat(all_result, axis=1)
            # 开始写入每一个alignment文件
            alignment_path = [file for file in alignment if name in file]
            for alignment_file in alignment_path:
                alignment_df = pd.read_excel(alignment_file, index_col='new_index').sort_values(by='intensity')
                alignment_df1 = alignment_df[~alignment_df.index.duplicated(keep='last')]  # 去掉重复索引
                # 找到共有的new_index
                final_index = np.intersect1d(alignment_df1.index.values, sample_final_area.index.values)
                # 根据索引填充数据
                alignment_df1 = pd.concat([alignment_df1, sample_area_info.loc[final_index, :]], axis=1)
                alignment_df2 = pd.concat([alignment_df1, all_result_df.loc[final_index, :]], axis=1)
                alignment_df2 = alignment_df2.sort_values(by='intensity', ascending=False)
                alignment_df2.index.name = 'new_index'
                alignment_df2.to_excel(alignment_file.replace('_alignment', '_unique_cmps'))
    else:
        print(f'filter_type = {filter_type} is not Supported, please use 1 or 2.')


def ms_to_centroid(profile_data):
    """
    Transform profile data to centroid data.

    Args:
        profile_data: pandas Series containing profile data.

    Returns:
        pandas Series containing centroid data
    """
    # Find peaks in profile data
    peaks, _ = scipy.signal.find_peaks(profile_data.values.copy())
    
    # Extract peak index and value data
    peak_index = profile_data.index.values[peaks]
    peak_values = profile_data.values[peaks]
    
    # Create new Series with peak data as centroid data
    if len(peak_index) > 0:
        centroid_data = pd.Series(peak_values, peak_index, name=profile_data.name, dtype='float64')
    else:
        centroid_data = pd.Series(name=profile_data.name, dtype='float64')
    
    return centroid_data


def gen_DDA_ms2_df(ms1, ms2, i_threshold=0, profile=True, opt=False, more_info=False, message=''):
    """
    Generates a DataFrame from DDA MS2 data with detailed information on retention times,
    precursors, fragments, and additional metrics depending on specified options.

    Args:
        ms1 (list): List of MS1 scans.
        ms2 (list): List of MS2 scans.
        i_threshold (float): Minimum intensity threshold for peak consideration. Defaults to 0.
        profile (bool): Indicates if data is in profile mode (True) or centroid mode (False). Defaults to True.
        opt (bool): If True, performs optimization on mass data. Defaults to False.
        more_info (bool): If True, additional information from MS1 is appended to the DataFrame. Defaults to False.
        message (str): Message to display during extended information gathering. Defaults to an empty string.

    Returns:
        pandas.DataFrame: Contains columns for retention time (rt), precursor m/z, fragments (frag),
                          intensity, collision energy, mode of ionization, scan index, MS2 spectra,
                          isotope distribution, and optionally optimized fragment m/z and MS1 data.

    Note:
        The function supports dynamic generation of data based on the `profile`, `opt`, and `more_info` flags,
        adapting the output DataFrame accordingly. The function requires tqdm and pandas libraries for execution.
    """
    
    # Initialize empty lists to hold precursor, rt, fragment, intensity, collision energy, and mode data
    precursors, rts, frags, intensities, collision_energies, modes, scan_indices, s_all, iso_info = [], [], [], [], [], [], [], [], []
    
    # Loop through each MS2 scan
    for i, scan in tqdm(enumerate(ms2), desc='Collecting MS2 info', colour='Green', leave=False):
        # Get the precursor m/z value
        precursor = round(scan.selected_precursors[0]['mz'], 5)
        precursors.append(precursor)
        
        # Get the RT of the scan
        rt = round(scan.scan_time[0], 3)
        rts.append(rt)
        
        # Get the collision energy of the scan
        collision_energy = int(scan['collision energy']) if isinstance(scan['collision energy'], float) else None
        collision_energies.append(collision_energy)
        
        # Get the scan index
        scan_indices.append(i)
        
        # Get the polarity mode of the scan
        if scan['negative scan'] is True:
            modes.append('neg')
        elif scan['positive scan'] is True:
            modes.append('pos')
        else:
            modes.append('Unknown')
        
        # Get the m/z and intensity values from the scan
        mz = scan.mz
        intensity = scan.i
        
        # Get the isotope information
        spec = pd.Series(index=np.round(mz, 4), data=intensity, name=rt)
        iso_result = isotope_distribution(spec, precursor, error=0.02)
        iso_info.append(iso_result)
        
        # If data is in profile mode, convert it to centroid mode
        if profile is True:
            spec = pd.Series(data=intensity, index=mz, dtype='float64')  # Explicit dtype
            new_spec = ms_to_centroid(spec)
            mz = new_spec.index.values
            intensity = new_spec.values
        
        # Filter out low intensity peaks and get the top 100 peaks
        s = pd.Series(data=intensity, index=np.round(mz, 4), dtype='float64').sort_values(ascending=False).iloc[
            :100]  # Explicit dtype
        s = s[s > i_threshold]
        
        # Get the fragment m/z values and their intensities
        s_all.append(str(s.to_dict()))
        frag = [round(i,4) for i in s.index.values]      # list(map(float, s.index.round(4)))  # list(s.index.values.round(4))
        frags.append(frag)
        intensities.append(list(s.values))
    
    # Create a DataFrame with precursor, rt, fragment, intensity, collision energy, mode, and scan index data
    DDA_df = pd.DataFrame(
        [precursors, rts, collision_energies, frags, intensities, modes, scan_indices, s_all, iso_info],
        index=['precursor', 'rt', 'collision energy', 'frag',
               'ms2_intensities', 'mode', 'scan_index', 'MS2_spec_DDA_dict', 'iso_distribution']).T
    
    # Optimize mass if required
    if profile and opt:
        mz_opt_all = []
        for i in tqdm(range(len(DDA_df)), desc='Optimizing mass'):
            frag = DDA_df.loc[i].frag
            x = DDA_df.loc[i].scan_index
            s1 = pd.Series(ms2[x].i, ms2[x].mz.round(4), dtype='float64')  # Explicit dtype
            mz_opt = [evaluate_ms(target_spec(s1, mz), mz)[2] for mz in frag]
            mz_opt_all.append(mz_opt)
        
        DDA_df.loc[:, 'frag_opt'] = mz_opt_all
    
    # find the intensity
    if more_info is True:
        for i in tqdm(range(len(DDA_df)), desc=f'{message}Obtain more information', colour='Green', leave=False):
            rt = DDA_df.loc[i, 'rt']
            precursor = DDA_df.loc[i, 'precursor']
            for j in range(len(ms1)):
                if (ms1[j].scan_time[0] >= rt) & (j > 1):
                    spec = pd.Series(data=ms1[j - 1].i, index=ms1[j - 1].mz)
                    # 检查 spec 是否为空，或不包含 precursor 附近的范围
                    if spec.empty or not ((spec.index >= precursor - 0.2) & (spec.index <= precursor + 0.2)).any():
                        DDA_df.loc[i, 'intensity'] = 0  # 标记为无数据
                        DDA_df.loc[i, 'ms1_obs'] = round(precursor, 5)
                        break
                        
                    if profile is True:
                        spec1 = target_spec(spec, precursor, width=0.2)
                        
                        intensity = spec1.max()
                        mz_obs, error1, mz_opt, error2, resolution = evaluate_ms(spec1, precursor)
                        try:
                            DDA_df.loc[i, 'intensity'] = round(intensity, 5)
                        except:
                            DDA_df.loc[i, 'intensity'] = 1.1  # 做个标记，看哪里出问题
                        try:
                            DDA_df.loc[i, 'ms1_obs'] = round(mz_obs, 5)
                        except:
                            DDA_df.loc[i, 'ms1_obs'] = round(precursor, 5)
                    
                    else:
                        spec1 = target_spec(spec, precursor, width=0.2)
                        intensity = spec1.max()
                        ms1_obs = spec1.index[np.argmin(abs(spec1.index - precursor))]
                        
                        try:
                            DDA_df.loc[i, 'intensity'] = round(intensity, 0)
                        except:
                            DDA_df.loc[i, 'intensity'] = 1.2  # 做个标记，看哪里出问题
                        try:
                            DDA_df.loc[i, 'ms1_obs'] = round(ms1_obs, 5)
                        except:
                            DDA_df.loc[i, 'ms1_obs'] = round(precursor, 5)
                    
                    break
        bad_idx = DDA_df[DDA_df['ms1_obs'].isna()].index
        DDA_df.loc[bad_idx, 'ms1_obs'] = DDA_df.loc[bad_idx, 'precursor']
    return DDA_df


def gen_DDA_ms2_df_from_mzml(DDA_file, i_threshold=0, profile=True):
    """
    Generates a DataFrame from DDA MS2 data with detailed information on retention times,
    precursors, fragments, and additional metrics depending on specified options.

    Args:
        ms1 (list): List of MS1 scans.
        ms2 (list): List of MS2 scans.
        i_threshold (float): Minimum intensity threshold for peak consideration. Defaults to 0.
        profile (bool): Indicates if data is in profile mode (True) or centroid mode (False). Defaults to True.
        opt (bool): If True, performs optimization on mass data. Defaults to False.
        more_info (bool): If True, additional information from MS1 is appended to the DataFrame. Defaults to False.
        message (str): Message to display during extended information gathering. Defaults to an empty string.

    Returns:
        pandas.DataFrame: Contains columns for retention time (rt), precursor m/z, fragments (frag),
                          intensity, collision energy, mode of ionization, scan index, MS2 spectra,
                          isotope distribution, and optionally optimized fragment m/z and MS1 data.

    Note:
        The function supports dynamic generation of data based on the `profile`, `opt`, and `more_info` flags,
        adapting the output DataFrame accordingly. The function requires tqdm and pandas libraries for execution.
    """
    run = pymzml.run.Reader(DDA_file)
    # Initialize empty lists to hold precursor, rt, fragment, intensity, collision energy, and mode data
    precursors, rts, frags, intensities, collision_energies, modes, scan_indices, s_all, iso_info = [], [], [], [], [], [], [], [], []
    
    # Loop through each MS2 scan
    latest_ms1_scan = None
    for i, scan in tqdm(enumerate(run), desc='Collecting MS2 info', colour='Green', leave=False):
        if scan.ms_level == 1:
            latest_ms1_scan = scan
        if scan.ms_level == 2:
            # Get the precursor m/z value
            precursor = round(scan.selected_precursors[0]['mz'], 5)
            precursors.append(precursor)
            
            # Get the RT of the scan
            rt = round(scan.scan_time[0], 3)
            rts.append(rt)
            
            # Get the collision energy of the scan
            collision_energy = int(scan['collision energy']) if isinstance(scan['collision energy'], float) else None
            collision_energies.append(collision_energy)
            
            # Get the scan index
            scan_indices.append(i)
            
            # Get the polarity mode of the scan
            if scan['negative scan'] is True:
                modes.append('neg')
            elif scan['positive scan'] is True:
                modes.append('pos')
            else:
                modes.append('Unknown')
            
            # Get the m/z and intensity values from the scan
            mz = scan.mz
            intensity = scan.i
            
            # Get the isotope information
            spec = pd.Series(index=np.round(latest_ms1_scan.mz, 4), data=latest_ms1_scan.i)
            iso_result = isotope_distribution(spec, precursor, error=0.02)
            iso_info.append(iso_result)
            
            # If data is in profile mode, convert it to centroid mode
            if profile is True:
                spec = pd.Series(data=intensity, index=mz, dtype='float64')  # Explicit dtype
                new_spec = ms_to_centroid(spec)
                mz = new_spec.index.values
                intensity = new_spec.values
            
            # Filter out low intensity peaks and get the top 20 peaks
            s = pd.Series(data=intensity, index=np.round(mz, 4), dtype='float64').sort_values(ascending=False).iloc[
                :20]  # Explicit dtype
            s = s[s > i_threshold]
            
            # Get the fragment m/z values and their intensities
            s_all.append(str(s.to_dict()))
            frag = list(map(float, s.index.round(4)))  # list(s.index.values.round(4))
            frags.append(frag)
            intensities.append(list(s.values))
    
    # Create a DataFrame with precursor, rt, fragment, intensity, collision energy, mode, and scan index data
    DDA_df = pd.DataFrame(
        [precursors, rts, collision_energies, frags, intensities, modes, scan_indices, s_all, iso_info],
        index=['precursor', 'rt', 'collision energy', 'frag',
               'ms2_intensities', 'mode', 'scan_index', 'MS2_spec_DDA_dict', 'iso_distribution']).T
    # bad_idx = DDA_df[DDA_df['ms1_obs'].isna()].index
    # DDA_df.loc[bad_idx, 'ms1_obs'] = DDA_df.loc[bad_idx, 'precursor']
    return DDA_df


def ms2_matching(unique, database, ms1_error=50, ms2_error=0.015, mode='pos', frag_DIA='frag_DIA', frag_DDA='frag_DDA'):
    """
    Match masses and fragments by comparing these values with those in the database.Warning: The precursor is the observed m/z in instrument.

    Args:
        unique (pandas.DataFrame): DataFrame containing unique compounds to be matched.
        database (pandas.DataFrame): DataFrame containing the database to match against.
        ms1_error (float): Precursor mass error in ppm.
        ms2_error (float): Fragment mass error in Da.
        mode (str): Mode of the mass spectrometer. Either 'pos' or 'neg'.
        frag_DIA(str): Column name for DIA fragment list.
        frag_DDA(str): Column name for DDA fragment list.
    Returns:
        pandas.DataFrame: DataFrame with the matching results.
    """
    # 先检查数据库
    if 'Source' not in database.columns.values:
        database['Source'] = 'None'
    if 'Source info' not in database.columns.values:
        database['Source info'] = 'None'
    
    database['Source'] = database['Source'].fillna('None')
    database['Source info'] = database['Source info'].fillna('None')
    
    columns = list(unique.columns.values)
    DIA = [column for column in columns if frag_DIA in column]
    DDA = [column for column in columns if frag_DDA in column]
    print(' ')
    print('DIA columns:', DIA)
    print('DDA columns:', DDA)
    database1 = database[database['mode'] == mode]  # 匹配mode模式
    if len(DIA) != 0:
        for i in tqdm(range(len(unique)), desc='Starting DIA ms2 matching:', leave=False):
            mz = unique.loc[i]['mz']
            mz_opt = unique.loc[i]['mz_opt'] if 'mz_opt' in unique.columns.values else None  # 如果有mz_opt则读入
            iso_info = eval(
                unique.loc[i, 'iso_distribution']) if 'iso_distribution' in unique.columns else None  # 增加iso_info
            
            # 和原来不一样了，不是中性质量了
            precursor = mz
            precursor_opt = mz_opt if mz_opt is not None else None
            
            frag_obs = np.array(eval(unique.loc[i][DIA[0]]))
            # 根据 precursor在数据库database里做ms1匹配
            if precursor_opt is None:
                match_result = database1[(database1['Precursor'] < precursor * (1 + ms1_error * 1e-6)) & (
                        database1['Precursor'] > precursor * (1 - ms1_error * 1e-6))]
            else:
                match_result = database1[((database1['Precursor'] < precursor * (1 + ms1_error * 1e-6)) & (
                        database1['Precursor'] > precursor * (1 - ms1_error * 1e-6))) |
                                         ((database1['Precursor'] < precursor_opt * (1 + ms1_error * 1e-6)) & (
                                                 database1['Precursor'] > precursor_opt * (1 - ms1_error * 1e-6)))]
            
            match_result_dict = []  # 定义一个列表接收数据
            
            # 对匹配结果依次分析
            if len(match_result) == 0:  # 匹配失败
                pass
            else:
                for j in range(len(match_result)):
                    ik_match = match_result['Inchikey'].iloc[j]  # 匹配的ik
                    source = match_result.iloc[j]['Source']
                    source_info = match_result.iloc[j]['Source info']
                    
                    formula = match_result.iloc[j]['Formula']
                    adduct_type = match_result.iloc[j]['adduct_type']
                    
                    try:
                        iso_score = isotope_score(iso_info, formula, mode=mode,
                                                  adducts_type=adduct_type)  # 这里会自动转换，所以不需要提前转换
                    except:
                        iso_score = 0
                    precursor_match = match_result['Precursor'].iloc[j]
                    ms1_error_obs = round((precursor_match - precursor) / precursor_match * 1e6, 1)  # 计算ms1 error
                    ms1_error_opt = round((precursor_match - precursor_opt) / precursor_match * 1e6,
                                          1) if precursor_opt is not None else None  # 计算ms1_opt error
                    try:
                        frag_exp = np.array(eval(match_result['Frag'].iloc[j]))
                        frag_exp = frag_exp[frag_exp < precursor-5]
                        
                    except:
                        frag_exp = []
                    try:
                        compare_result = compare_frag(frag_obs, frag_exp, error=ms2_error)
                    except:
                        # print(frag_exp)
                        compare_result = []
                    
                    if len(compare_result) == 0:
                        pass
                    else:
                        single_result_dict = {}  # 建立一个字典
                        compare_frag_dict = compare_result.round(4).to_dict()  # 匹配的具体数据

                        match_num = len(compare_frag_dict)  # 匹配的个数
                        
                        match_percent = round(len(compare_frag_dict) / len(set(frag_exp.round())), 2)  # 匹配的百分比
                        
                        single_result_dict['ik'] = ik_match
                        single_result_dict['ms1_error'] = ms1_error_obs
                        single_result_dict['ms1_opt_error'] = ms1_error_opt
                        single_result_dict['iso_score'] = iso_score
                        single_result_dict['match_num'] = match_num
                        single_result_dict['match_percent'] = match_percent
                        single_result_dict['match_info'] = compare_frag_dict
                        single_result_dict['adduct_type'] = adduct_type
                        single_result_dict['Source'] = source
                        single_result_dict['Source info'] = source_info
                        
                        match_result_dict.append(single_result_dict)
            # 输出结果
            unique.loc[i, 'match_result_DIA'] = str(match_result_dict)
            if len(match_result_dict) == 0:
                unique.loc[i, 'best_results_DIA'] = str([])
            else:
                
                optimized_result = pd.concat([pd.Series(a) for a in match_result_dict], axis=1).T
                optimized_result['ms1_error_obs'] = optimized_result['ms1_error'].abs()
                optimized_result = optimized_result.sort_values(
                    by=['match_num', 'ms1_error_obs', 'iso_score', 'match_percent'],
                    ascending=[False, True, False, False])
                optimized_result.drop('ms1_error_obs', axis=1, inplace=True)
                unique.loc[i, 'best_results_DIA'] = str(optimized_result.iloc[0].to_dict())
    
    if len(DDA) != 0:
        for i in tqdm(range(len(unique)), desc='Starting DDA ms2 matching:', leave=False):
            mz = unique.loc[i]['mz']
            mz_opt = unique.loc[i]['mz_opt'] if 'mz_opt' in unique.columns.values else None  # 如果有mz_opt则读入
            iso_info = eval(
                unique.loc[i, 'iso_distribution']) if 'iso_distribution' in unique.columns else None  # 增加iso_info
            # 和原来不一样了，不是中性质量了
            precursor = mz
            precursor_opt = mz_opt if mz_opt is not None else None
            
            frag_obs = np.array(eval(unique.loc[i][DDA[0]]))
            # 根据 precursor在数据库database里做ms1匹配
            if precursor_opt is None:
                match_result = database1[(database1['Precursor'] < precursor * (1 + ms1_error * 1e-6)) & (
                        database1['Precursor'] > precursor * (1 - ms1_error * 1e-6))]
            else:
                match_result = database1[((database1['Precursor'] < precursor * (1 + ms1_error * 1e-6)) & (
                        database1['Precursor'] > precursor * (1 - ms1_error * 1e-6))) |
                                         ((database1['Precursor'] < precursor_opt * (1 + ms1_error * 1e-6)) & (
                                                 database1['Precursor'] > precursor_opt * (1 - ms1_error * 1e-6)))]
            
            match_result_dict = []  # 定义一个列表接收数据
            # 对匹配结果依次分析
            if len(match_result) == 0:  # 匹配失败
                pass
            else:
                for j in range(len(match_result)):
                    ik_match = match_result['Inchikey'].iloc[j]  # 匹配的ik
                    source_info = match_result.iloc[j]['Source info']
                    source = match_result.iloc[j]['Source']
                    formula = match_result.iloc[j]['Formula']
                    adduct_type = match_result.iloc[j]['adduct_type']
                    try:
                        iso_score = isotope_score(iso_info, formula, mode=mode,
                                                  adducts_type=adduct_type)  # 这里会自动转换，所以不需要提前转换
                    except:
                        iso_score = 0
                    
                    precursor_match = match_result['Precursor'].iloc[j]
                    ms1_error_obs = round((precursor_match - precursor) / precursor * 1e6, 1)  # 计算ms1 error
                    ms1_error_opt = round((precursor_match - precursor_opt) / precursor_opt * 1e6,
                                          1) if precursor_opt is not None else None  # 计算ms1_opt error
                    try:
                        frag_exp = np.array(eval(match_result['Frag'].iloc[j]))
                        frag_exp = frag_exp[frag_exp < precursor-5]
                    except:
                        frag_exp = []
                    compare_result = compare_frag(frag_obs, frag_exp, error=ms2_error)
                    if len(compare_result) == 0:
                        pass
                    else:
                        single_result_dict = {}  # 建立一个字典
                        compare_frag_dict = compare_result.round(4).to_dict()  # 匹配的具体数据
                        match_num = len(compare_frag_dict)  # 匹配的个数
                        
                        match_percent = round(len(compare_frag_dict) / len(set(frag_exp.round())), 2)  # 匹配的百分比
                        
                        single_result_dict['ik'] = ik_match
                        single_result_dict['ms1_error'] = ms1_error_obs
                        single_result_dict['ms1_opt_error'] = ms1_error_opt
                        single_result_dict['match_num'] = match_num
                        single_result_dict['match_percent'] = match_percent
                        single_result_dict['match_info'] = compare_frag_dict
                        single_result_dict['iso_score'] = iso_score
                        single_result_dict['adduct_type'] = adduct_type
                        single_result_dict['Source'] = source
                        single_result_dict['Source info'] = source_info
                        match_result_dict.append(single_result_dict)
            # 输出结果
            unique.loc[i, 'match_result_DDA'] = str(match_result_dict)
            
            if len(match_result_dict) == 0:
                unique.loc[i, 'best_results_DDA'] = '[]'
            else:
                
                optimized_result = pd.concat([pd.Series(a) for a in match_result_dict], axis=1).T
                optimized_result['ms1_error_obs'] = optimized_result['ms1_error'].abs()
                
                optimized_result = optimized_result.sort_values(
                    by=['match_num', 'ms1_error_obs', 'iso_score', 'match_percent'],
                    ascending=[False, True, False, False])
                
                optimized_result.drop('ms1_error_obs', axis=1, inplace=True)
                unique.loc[i, 'best_results_DDA'] = str(optimized_result.iloc[0].to_dict())
    return unique


def compare_frag(frag_obs, frag_exp, error=0.015):
    """
    Compare the similarity of observed and expected fragments.

    Args:
        frag_obs: observed fragments, as a numpy array
        frag_exp: expected fragments from the database, as a numpy array
        error: maximum allowed mass difference for two fragments to be considered a match, in Da

    Returns:
        A pandas series with matching results, showing the matched mass and the mass difference.
        If no matches are found, an empty series is returned.
    """
    
    # Sort the observed and expected fragments in ascending order
    frag_obs = np.sort(frag_obs)
    frag_exp = np.sort(frag_exp)
    compare_result = {}
    
    # Compare observed and expected fragments
    if len(frag_obs) < len(frag_exp):
        for mz in frag_obs:
            # Find the closest fragment in the expected fragments
            index = np.argmin(abs(frag_exp - mz))
            matched_mz = frag_exp[index]
            compare_result[mz] = matched_mz - mz
    else:
        for mz in frag_exp:
            # Find the closest fragment in the observed fragments
            index = np.argmin(abs(frag_obs - mz))
            matched_mz = frag_obs[index]
            compare_result[matched_mz] = mz - matched_mz
    
    # Filter the matched fragments by the error threshold and sort them in ascending order
    if len(compare_result) == 0:
        s2 = pd.Series(dtype=object)
    else:
        s1 = pd.Series(compare_result)
        s2 = s1[abs(s1) < error].sort_values()
        s3 = s2.copy()
        s3.index = s3.index.values.round(1)  # Round the index values to one decimal place to remove duplicates
        s2 = s2[~s3.index.duplicated()].sort_index()
    
    return s2


def multi_process_database_matching_old(path, database, processors=1, ms1_error=50, ms2_error=0.015, rt_error=0.1,
                                        mode='pos'):
    """
    Matches compounds in the database using multiprocessing method. Warning: The precursor is the observed m/z in instrument.

    Args:
        path (str): The path to the folder containing the excel files with suffix "unique_cmp".
        database (pd.DataFrame): A database dataframe. See https://pypi.org/project/pyhrms/ for more information on how to build a database.
        processors (int): The number of processors to use for parallel running.
        ms1_error (float): The allowable mass error for MS1 in parts per million (ppm).
        ms2_error (float): The allowable mass error for MS2 in Daltons (Da).
        rt_error (float): The allowable retention time (RT) error in minutes (min).
        mode (str): The ionization mode used for mass spectrometry, either 'pos' for positive mode or 'neg' for negative mode.

    Returns:
        None. The function generates database matched result files with the suffix "_rt_ms2_match.xlsx".
    """
    
    unique_files = [file for file in glob(os.path.join(path, '*.xlsx')) if 'unique_cmp' in file]
    
    print('                          ')
    print('==========================')
    print('Matching started...')
    print('==========================')
    print('                          ')
    
    pool = Pool(processes=processors)
    for file in unique_files:
        print(file)
        pool.apply_async(database_match, args=(file, database, ms1_error, ms2_error, rt_error, mode,))
    pool.close()
    pool.join()


def multi_process_database_matching(path, database, processors=None, ms1_error=50, ms2_error=0.015, rt_error=0.1,
                                    mode='pos', frag_DIA='frag_DIA', frag_DDA='frag_DDA'):
    """
    Matches compounds in the database using multiprocessing method.

    Args:
        path (str): The path to the folder containing the excel files with suffix "unique_cmp".
        database (pd.DataFrame): A database dataframe. See https://pypi.org/project/pyhrms/ for more information on how to build a database.
        processors (int): The number of processors to use for parallel running. If None, will use all available processors.
        ms1_error (float): The allowable mass error for MS1 in parts per million (ppm).
        ms2_error (float): The allowable mass error for MS2 in Daltons (Da).
        rt_error (float): The allowable retention time (RT) error in minutes (min).
        mode (str): The ionization mode used for mass spectrometry, either 'pos' for positive mode or 'neg' for negative mode.
        frag_DIA(str): Column name for DIA fragment list.
        frag_DDA(str): Column name for DDA fragment list.

    Returns:
        None. The function generates database matched result files with the suffix "_rt_ms2_match.xlsx".
    """
    
    unique_files = [file for file in glob(os.path.join(path, '*.xlsx')) if 'unique_cmp' in file]
    
    print('==========================')
    print('Matching started...')
    print('==========================')
    
    if processors is None:
        processors = int(round(cpu_count() / 2, 0))
    
    if processors > 1:
        with Pool(processes=processors) as pool:
            results = []
            for file in unique_files:
                result = pool.apply_async(database_match,
                                          args=(
                                          file, database, ms1_error, ms2_error, rt_error, mode, frag_DIA, frag_DDA))
                results.append(result)
            for result in results:
                result.wait()
    elif processors == 1:
        for file in unique_files:
            database_match(file, database, ms1_error, ms2_error, rt_error, mode, frag_DIA, frag_DDA)
    print('==========================')
    print('Matching complete!')
    print('==========================')


def database_match(file, database, ms1_error=50, ms2_error=0.015, rt_error=0.1, mode='pos', frag_DIA='frag_DIA',
                   frag_DDA='frag_DDA'):
    """
    Matches retention time, mass, and fragments by comparing them with values in the database.

    Args:
        file (str): Path to the input file.
        database (pandas.DataFrame): A database containing the compounds to match.
            See https://pypi.org/project/pyhrms/ for more information on how to build a database.
        ms1_error (float): Maximum allowed mass error in parts per million (ppm) for the precursor ion.
        ms2_error (float): Maximum allowed mass error in Daltons (Da) for the product ions.
        rt_error (float): Maximum allowed retention time error in minutes.
        mode (str): Ionization mode. Valid values are 'pos' (positive) or 'neg' (negative).
        frag_DIA(str): Column name for DIA fragment list.
        frag_DDA(str): Column name for DDA fragment list.
    Returns:
        None. Exports the matched results to a file with the same name as the input file,
        but with the suffix "_matched.xlsx".
    """
    try:
        unique = pd.read_excel(file)
        unique_ms2_match = ms2_matching(unique, database, ms1_error=ms1_error, ms2_error=ms2_error, mode=mode,
                                        frag_DIA=frag_DIA, frag_DDA=frag_DDA)
        unique_rt_ms2_match = rt_matching(unique_ms2_match, database, ms1_error=ms1_error, rt_error=rt_error,
                                          mode=mode)
        
        unique_rt_ms2_match.to_excel(file.replace('.xlsx', '_rt_ms2_match.xlsx'))
    
    except Exception as e:
        # 捕获异常并将异常信息保存到error_info变量
        error_info = traceback.format_exc()
        print(error_info)


def rt_matching(unique, database, ms1_error=50, rt_error=0.1, mode='pos'):
    """
    Match retention time and mass by comparing these values to the database.Warning: The precursor is the observed m/z in instrument.

    Args:
        unique (pandas.DataFrame): The target unique compounds dataframe.
        database (pandas.DataFrame): The reference database.
        ms1_error (float): The allowed error in mass-to-charge ratio (ppm).
        rt_error (float): The allowed error in retention time (minutes).
        mode (str): The ionization mode ('pos' for positive or 'neg' for negative).

    Returns:
        pandas.DataFrame: A result dataframe with the matching results.
    """
    
    db = database[(database['mode'] == mode) & (~database['rt'].isna())]
    for i in tqdm(range(len(unique)), desc='Starting rt & m/z matching:', leave=False):
        iso_info = eval(unique.loc[i, 'iso_distribution']) if 'iso_distribution' in unique.columns else None
        if 'mz_opt' in unique.columns.values:
            rt, mz, mz_opt = unique.loc[i, ['rt', 'mz', 'mz_opt']]
        else:
            rt, mz = unique.loc[i, ['rt', 'mz']]
            mz_opt = None
        
        # 和原来不一样了，不是中性质量了
        precursor = mz
        mz_opt1 = mz_opt if mz_opt is not None else None
        
        if mz_opt1 is None:
            result = db[(db['rt'] > rt - rt_error) & (db['rt'] < rt + rt_error) &
                        (db['Precursor'] > precursor * (1 - ms1_error * 1e-6)) & (
                                db['Precursor'] < precursor * (1 + ms1_error * 1e-6))]
        else:
            result = db[(db['rt'] > rt - rt_error) & (db['rt'] < rt + rt_error) &
                        ((db['Precursor'] > precursor * (1 - ms1_error * 1e-6)) &
                         (db['Precursor'] < precursor * (1 + ms1_error * 1e-6)) |
                         (db['Precursor'] > mz_opt1 * (1 - ms1_error * 1e-6))
                         & (db['Precursor'] < mz_opt1 * (1 + ms1_error * 1e-6))
                         )]
        
        if len(result) != 0:
            result1 = result.copy()
            adduct_type = result.iloc[0]['adduct_type']
            formula = result.iloc[0]['Formula']
            result1['rt_error'] = (result1['rt'] - rt).round(3)
            result1['mz_error'] = ((result1['Precursor'] - precursor) / result1['Precursor'] * 1e6).round(1)
            result1['mz_opt_error'] = ((result1['Precursor'] - mz_opt1) / result1['Precursor'] * 1e6).round(
                1) if mz_opt1 is not None else None
            result1['ik'] = result1['Inchikey']
            
            try:
                iso_score = isotope_score(iso_info, formula, mode=mode, adducts_type=adduct_type)
            except:
                iso_score = 0
            result1['iso_score'] = iso_score
            result1['mz_error_abs'] = result1['mz_error'].abs()
            result2 = result1.loc[:, ['ik', 'rt_error', 'mz_error',
                                      'mz_opt_error', 'iso_score', 'mz_error_abs']]
            result2 = result2.sort_values(by=['mz_error_abs', 'iso_score'], ascending=[True, False])
            result2 = result2.drop('mz_error_abs', axis=1)
            result_str = str(result2.iloc[0, :].T.to_dict())
            unique.loc[i, 'rt_match_result'] = result_str
        
        else:
            unique.loc[i, 'rt_match_result'] = str([])
    return unique


def post_filter(path, fold_change=5, p_value=0.05, i_threshold=500, area_threshold=500, drop=None):
    '''
    This function lets users filter results based on criteria such as p-value, fold change, intensity, and area. Any feature with a p-value greater than the user-defined threshold (e.g., 0.05) will be removed from the result dataframe. The filtered result will be automatically exported with a filename suffix "_filter.xlsx".

    Args:
        path: The folder path of the input excel files to be processed, for example, '../Users/Desktop/my_result_excel_files'.
        fold_change: The threshold for fold change. Any features with a fold change below this threshold will be removed from the result dataframe.
        p_value: The maximum threshold for p-value. Any features with a p-value above this threshold will be removed from the result dataframe.
        i_threshold: The minimum threshold for feature intensity. Any features with an intensity below this threshold will be removed from the result dataframe.
        area_threshold: The minimum threshold for peak area. Any features with an area below this threshold will be removed from the result dataframe.
        drop: the columns need to drop
    returns:
        None. Export files with suffix "_filter.xlsx".
    '''
    
    files = glob(os.path.join(path, '*.xlsx'))
    for i in tqdm(range(len(files))):
        try:
            df = pd.read_excel(files[i], index_col='Unnamed: 0')
        except:
            df = pd.read_excel(files[i])
        if drop == None:
            pass
        else:
            for name1 in drop:
                if name1 in df.columns.values:
                    df = df.drop(name1, axis=1)
                else:
                    pass
        
        fold_change_columns = [i for i in df.columns if 'fold_change' in i]
        p_values_columns = [i for i in df.columns if 'p_value' in i]
        
        for fold_change1 in fold_change_columns:
            df = df[df[fold_change1] > fold_change]
        for p_value1 in p_values_columns:
            df = df[df[p_value1] < p_value].reset_index(drop=True)
        # other parameters
        if 'intensity' in df.columns:
            df = df[(df.intensity > i_threshold)].reset_index(drop=True)
        if 'area' in df.columns:
            df = df[(df.area > area_threshold)].reset_index(drop=True)
        
        df.to_excel(files[i].replace('.xlsx', '_filter.xlsx'))


def summarize_results(df, suspect_list=None, db_toxicity=None,
                      rt_matched_column='rt_match_result', matched_DDA_column='match_result_DDA',
                      matched_DIA_column='match_result_DIA', best_matched_DDA_column='best_results_DDA',
                      best_matched_DIA_column='best_results_DIA', MS2_spec_column='MS2_spectra'):
    '''
    The function is designed to collect identified features and ignore unidentified ones, resulting in a dataframe with the relevant information. In order to achieve this, the function requires three input dataframes: a suspect list from the Norman network, an ecotoxicity database from the Norman network, and a compound's category excel.When the function is used, it will extract the name, smile, CAS number, categories, and toxicity data for each identified feature. This information is then compiled into a new dataframe, which includes only the identified features and their associated data. By using this function, users can easily extract and organize the relevant information for identified features, without having to manually sift through large amounts of data.
    Args:
        df: result dataframe

        suspect_list: suspect_list can be downloaded from <http://www.norman-network.com/?q=node/236>.
        db_toxicity: toxicity database can be downloaded from  <https://www.norman-network.com/nds/ecotox/>
    returns:
        summarized dataframe.
    '''
    # 检查这些元素在不在列表名里
    if rt_matched_column not in df.columns.values:
        df[rt_matched_column] = '[]'
    if best_matched_DDA_column not in df.columns.values:
        df[best_matched_DDA_column] = '[]'
    if best_matched_DIA_column not in df.columns.values:
        df[best_matched_DIA_column] = '[]'
    if matched_DDA_column not in df.columns.values:
        df[matched_DDA_column] = '[]'
    if matched_DIA_column not in df.columns.values:
        df[matched_DIA_column] = '[]'
    
    exp_columns = ['new_index', 'rt', 'mz', 'intensity', 'S/N', 'area', 'mz_opt', 'frag_DIA', 'iso_distribution',
                   'resolution', MS2_spec_column]
    assured_columns = [i for i in exp_columns if i in df.columns]
    
    sorted_columns = ['new_index', 'name', 'formula', 'CAS', 'ik', 'Smile', 'rt', 'mz', 'intensity', 'iso_distribution',
                      'S/N', 'area', 'frag_DIA', 'mz_opt', 'resolution', 'MS2_spectra', 'rt_error', 'ms1_error',
                      'ms1_opt_error', 'match_num', 'iso_score',
                      'match_percent', 'match_info', 'MS2 mode', 'Source', 'Source info', 'Norman_SusDat_ID',
                      'Lowest PNEC Freshwater [µg//l]', 'Lowest PNEC Marine water [µg//l]',
                      'Lowest PNEC Sediments [µg//kg dw]', 'Lowest PNEC Biota (fish) [µg//kg ww]']
    final_result_all = []
    for i in tqdm(range(len(df)), desc='Summarizing matched result'):
        
        cmp = df.loc[i, assured_columns]
        # 1. 把所有信息合并一起
        result_all = []
        rt_result = pd.DataFrame([eval(df.loc[i, rt_matched_column])]) if len(
            eval(df.loc[i, rt_matched_column])) != 0 else []
        if len(rt_result) != 0:
            rt_result.columns = [i.replace('mz_error', 'ms1_error').replace('mz_opt_error', 'ms1_opt_error')
                                 for i in rt_result.columns]  # 确保名字统一
            result_all.append(rt_result)
        DIA_result = pd.DataFrame(eval(df.loc[i, matched_DIA_column]))
        
        if len(DIA_result) != 0:
            DIA_result['MS2 mode'] = 'DIA'
            result_all.append(DIA_result)
        DDA_result = pd.DataFrame(eval(df.loc[i, matched_DDA_column]))
        if len(DDA_result) != 0:
            DDA_result['MS2 mode'] = 'DDA'
            result_all.append(DDA_result)
        
        # 2. 开始具体分析
        if len(result_all) == 0:  # 如果没有数据，pass
            pass
        else:
            result_all_df = pd.concat(result_all, axis=0)  # 合并所有数据
            result_all_df.loc[:, 'ms1_error_abs'] = result_all_df['ms1_error'].abs()
            if 'rt_error' in result_all_df.columns:
                rt_ik_df = result_all_df[~result_all_df['rt_error'].isna()]
                target_ik = rt_ik_df.ik.values[0] if rt_ik_df is not None else None
                rt_error = rt_ik_df.rt_error.values[0] if rt_ik_df is not None else None
                ik_all = result_all_df[(result_all_df['ik'] ==
                                        target_ik) & (result_all_df['rt_error'].isna())]  # 获得该ik所有二级匹配
                if len(ik_all) == 0:  # 说明只匹配到ms1和rt
                    good_match = rt_ik_df.iloc[0].copy()
                else:
                    good_match = ik_all.sort_values(by=['match_num', 'ms1_error_abs'], ascending=[False, True]).iloc[
                        0].copy()  # 获得该ik最多的匹配
                    good_match['rt_error'] = rt_error
                    a_mode = list(set(ik_all['MS2 mode'].values))
                    if ('DDA' in a_mode) & ('DIA' in a_mode):
                        good_match['MS2 mode'] = 'DDA&DIA'
            else:
                ik_all1 = result_all_df.sort_values(by=['match_num', 'ms1_error_abs'],
                                                    ascending=[False, True]).reset_index(drop=True)
                good_match = ik_all1.loc[0].copy()
                target_ik = ik_all1.loc[0, 'ik']
                ik_all2 = ik_all1[ik_all1['ik'] == target_ik]
                a_mode = list(set(ik_all2['MS2 mode'].values))
                if ('DDA' in a_mode) & ('DIA' in a_mode):
                    good_match['MS2 mode'] = 'DDA&DIA'
            
            final_result = pd.concat([cmp, good_match], axis=0)
            # 3. 如果suspect list有的话，就导入数据
            if suspect_list is None:
                final_result2 = final_result
            else:
                x = suspect_list[suspect_list['StdInChIKey'] == target_ik]
                if len(x) != 0:
                    x1 = x.loc[:, ['SMILES', 'Name', 'CAS_RN', 'Molecular_Formula', 'Norman_SusDat_ID']].iloc[0]
                    x1.index = ['Smile', 'name', 'CAS', 'formula', 'Norman_SusDat_ID']
                    final_result1 = pd.concat([final_result, x1])
                    Norman_SusDat_ID = x1.loc['Norman_SusDat_ID']
                    # 4. 如果有 toxicity data加入
                    if db_toxicity is None:
                        final_result2 = final_result1
                    else:
                        y = db_toxicity[db_toxicity['Norman SusDat ID'] == Norman_SusDat_ID]
                        if len(y) != 0:
                            y1 = y.iloc[0]
                            y2 = y1.loc[['Lowest PNEC Freshwater [µg//l]', 'Lowest PNEC Marine water [µg//l]',
                                         'Lowest PNEC Sediments [µg//kg dw]', 'Lowest PNEC Biota (fish) [µg//kg ww]']]
                            final_result2 = pd.concat([final_result1, y2])
                        else:
                            final_result2 = final_result1
                else:
                    final_result2 = final_result
            final_result_all.append(final_result2)
    final_result_all_df = pd.concat(final_result_all, axis=1).T
    sorted_columns1 = [i for i in sorted_columns if i in final_result_all_df.columns]
    
    final_result_all_df1 = final_result_all_df.loc[:, sorted_columns1]
    return final_result_all_df1


def summarize_results_export(path, suspect_list=None, db_toxicity=None,
                             rt_matched_column='rt_match_result', matched_DDA_column='match_result_DDA',
                             matched_DIA_column='match_result_DIA', best_matched_DDA_column='best_results_DDA',
                             best_matched_DIA_column='best_results_DIA', MS2_spec_column='MS2_spectra'):
    """
    Finds all .xlsx files in the specified path, applies summarize_results function,
    and saves the results as new files with '_summarized_result.xlsx' suffix.

    :param path: Directory containing Excel files
    :param suspect_list: Optional, list of suspect compounds
    :param db_toxicity: Optional, toxicity database
    :param rt_matched_column: RT match result column name
    :param matched_DDA_column: DDA match result column name
    :param matched_DIA_column: DIA match result column name
    :param best_matched_DDA_column: Best DDA results column name
    :param best_matched_DIA_column: Best DIA results column name
    :param MS2_spec_column: MS2 spectra column name
    """
    # Ensure the directory exists
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist!")
        return
    
    # Find all .xlsx files in the directory
    files = glob(os.path.join(path, "*.xlsx"))
    
    for file in files:
        try:
            # Read the Excel file
            df = pd.read_excel(file)
            
            # Process the data using summarize_results function
            summarized_df = summarize_results(df, suspect_list, db_toxicity,
                                              rt_matched_column, matched_DDA_column, matched_DIA_column,
                                              best_matched_DDA_column, best_matched_DIA_column, MS2_spec_column)
            
            # Generate the output filename
            output_file = file.replace(".xlsx", "_summarized_result.xlsx")
            
            # Save the processed data
            summarized_df.to_excel(output_file, index=False)
            print(f"Processed: {os.path.basename(file)} → {os.path.basename(output_file)}")
        
        except Exception as e:
            print(f" Error processing {os.path.basename(file)}: {e}")
    
    print("All files processed!")


def summarized_results_concat(path, all_name_index, mode):
    """
    Summarizes the results from multiple sample sets with specific ESI polarities, and returns a consolidated
    dataframe with unique values (based on site and compound).

    Args:
        path (str): The file path for the summarized result files.
        all_name_index (list[str]): A list of unique identifiers that represent each sample set.
        mode (str): The ESI polarity of the samples. Either 'pos' for positive or 'neg' for negative.

    Returns:
        A consolidated dataframe with unique values (based on site and compound).
    """
    files = glob(os.path.join(path, '*.xlsx'))
    df_all = []
    for file in tqdm(files):
        df = pd.read_excel(file)
        if len(df) == 0:
            pass
        else:
            name_index = [i for i in all_name_index if i in os.path.basename(file)][0]
            df.loc[:, 'site'] = name_index
            # 确保索引的column都在里面
            if 'rt_error' not in df.columns.values:
                df.loc[:, 'rt_error'] = np.nan
            if 'MS2 mode' not in df.columns.values:
                df.loc[:, 'MS2 mode'] = np.nan
            # 每个数据进行分级
            # level1
            need_change_index1 = df[((df['MS2 mode'] == 'DDA')
                                     | (df['MS2 mode'] == 'DIA')
                                     | (df['MS2 mode'] == 'DDA&DIA')) & ~df['rt_error'].isna()].index
            df.loc[need_change_index1, 'Confidence level'] = 1
            # level2
            need_change_index2 = df[((df['MS2 mode'] == 'DDA')
                                     | (df['MS2 mode'] == 'DIA')
                                     | (df['MS2 mode'] == 'DDA&DIA')) & df['rt_error'].isna()].index
            df.loc[need_change_index2, 'Confidence level'] = 2
            # level3
            need_change_index3 = df[~((df['MS2 mode'] == 'DDA')
                                      | (df['MS2 mode'] == 'DIA')
                                      | (df['MS2 mode'] == 'DDA&DIA')) & ~df['rt_error'].isna()].index
            df.loc[need_change_index3, 'Confidence level'] = 3
            df_all.append(df)
    df_all_df = pd.concat(df_all).sort_values(by='intensity', ascending=False).reset_index(drop=True)
    drop_duplicate_index = df_all_df.loc[:, ['ik', 'site', 'Confidence level']].drop_duplicates().index
    df_all_df_no_duplicate = df_all_df.loc[drop_duplicate_index].reset_index(drop=True)
    df_all_df_no_duplicate['mode'] = mode
    # 第二步，整理结果：
    all_df = df_all_df_no_duplicate  # 先赋值，免得下面改了
    iks = all_df['ik'].value_counts().index
    data_all = []
    for i in range(len(iks)):
        df1 = all_df[all_df['ik'] == iks[i]]  # 所有有此ik的物质
        
        # 确定一下不同样品中的质量最准的
        df_temp = df1.copy()
        df_temp['error_obs_abs'] = df_temp['ms1_error'].abs()
        df_temp1 = df_temp.sort_values(by='error_obs_abs').iloc[0]
        best_mz_obs = df_temp1['mz']
        best_mz_error = df_temp1['ms1_error']
        best_ms1_opt_error = df_temp1['ms1_opt_error']
        # 记录一下详细的质量信息
        df_temp = df1.copy()
        df2_ = df_temp.loc[:, ['ms1_error', 'ms1_opt_error', 'site']].sort_values(by='site')
        df2__ = df2_.set_index('site')
        ms_error_detail = df2__.to_dict()
        
        # 要先看是否有保留时间
        rt_check = df1[~df1['rt_error'].isna()]
        if len(rt_check) != 0:
            right_rt_list = df1[df1['Confidence level'] == 1].rt.values  # 选取一个锚定保留时间
            if len(right_rt_list) == 0:
                df1 = df1.sort_values(by=['Confidence level', 'intensity'], ascending=[True, False])
                df2 = df1.iloc[0]
                df3 = df2.to_dict()
                df3['site'] = str(list(set(df1['site'].values)))
                df3['sites_num'] = len(list(set(df1['site'].values)))
                df3['ms_error_detail'] = ms_error_detail
                df4 = pd.Series(df3)
            else:
                right_rt = right_rt_list[0]
                df2 = df1[(df1['rt'] > right_rt - 0.1) & (df1['rt'] < right_rt + 0.1)]  # 这些都定义为level1
                df3 = df2.iloc[0].to_dict()
                mode_index = df2['MS2 mode'].value_counts().index.values
                if 'DDA&DIA' in mode_index:
                    df3['MS2 mode'] = 'DDA&DIA'
                elif 'DDA' in mode_index:
                    df3['MS2 mode'] = 'DDA'
                elif 'DIA' in mode_index:
                    df3['MS2 mode'] = 'DIA'
                # 更新最好的信息
                df3['site'] = str(list(set(df2['site'].values)))
                
                df3['rt_error'] = df2['rt_error'].value_counts().index[0]
                df_ = df2.sort_values(by='match_num', ascending=False).iloc[0]
                df3['match_num'] = df_.loc['match_num']
                df3['match_percent'] = df_.loc['match_percent']
                df3['match_info'] = df_.loc['match_info']
                df3['sites_num'] = len(list(set(df2['site'].values)))
                df3['ms_error_detail'] = ms_error_detail
                df3['Confidence level'] = 1
                df4 = pd.Series(df3)
        else:
            df1 = df1.sort_values(by=['match_num', 'intensity'], ascending=[False, False])
            right_rt = df1.rt.iloc[0]
            df2 = df1[(df1['rt'] > right_rt - 0.1) & (df1['rt'] < right_rt + 0.1)]  # 如果保留时间偏差太大就不是一个物质
            df3 = df2.iloc[0].to_dict()
            mode_index = df2['MS2 mode'].value_counts().index.values
            if 'DDA&DIA' in mode_index:
                df3['MS2 mode'] = 'DDA&DIA'
            elif 'DDA' in mode_index:
                df3['MS2 mode'] = 'DDA'
            elif 'DIA' in mode_index:
                df3['MS2 mode'] = 'DIA'
            df3['site'] = str(list(set(df2['site'].values)))
            df3['sites_num'] = len(list(set(df2['site'].values)))
            df3['ms_error_detail'] = ms_error_detail
            df4 = pd.Series(df3)
        df4['best_mz_obs'] = best_mz_obs
        df4['best_mz_error'] = best_mz_error
        df4['best_ms1_opt_error'] = best_ms1_opt_error
        data_all.append(df4)
    dfx = pd.concat(data_all, axis=1).T
    
    return dfx


def summarize_pos_neg_result(all_df_pos, all_df_neg):
    """
    This function can concat the df in pos and neg mode.

    Args:
        all_df_pos: all_df_pos
        all_df_neg: all_df_neg
    return: final result
    """
    df_pos_neg = pd.concat([all_df_pos, all_df_neg], axis=0)
    iks = df_pos_neg['ik'].value_counts().index
    df_all = []
    for ik in tqdm(iks, desc='Collecting Info'):
        df1 = df_pos_neg[df_pos_neg['ik'] == ik].copy()
        
        index_info = df1.loc[:, ['new_index', 'mode']]
        index_pos = index_info[index_info['mode'].str.contains('pos')]['new_index']
        index_neg = index_info[index_info['mode'].str.contains('neg')]['new_index']
        index_pos1 = index_pos.values[0] if len(index_pos) != 0 else np.nan
        index_neg1 = index_neg.values[0] if len(index_neg) != 0 else np.nan
        df1['new_index_pos'] = index_pos1
        df1['new_index_neg'] = index_neg1
        
        df1 = df1.sort_values(by='Confidence level')
        df2 = df1.iloc[0]
        df3 = df2.to_dict()
        # 更新点位的名称，和点位的个数
        site = list(set([j for i in df1['site'].values for j in eval(i)]))
        df3['site'] = str(site)
        df3['sites_num'] = len(site)
        # 更新mode，如果pos和neg都有，要说明各有几个
        site_info = df1.loc[:, ['mode', 'sites_num']]
        site_info1 = site_info.set_index('mode').to_dict()['sites_num']
        df3['mode'] = str(site_info1)
        # 更新MS2 mode
        mode_index = df1['MS2 mode'].values
        if 'DDA&DIA' in mode_index:
            df3['MS2 mode'] = 'DDA&DIA'
        elif 'DDA' in mode_index:
            df3['MS2 mode'] = 'DDA'
        elif 'DIA' in mode_index:
            df3['MS2 mode'] = 'DIA'
        df4 = pd.Series(df3)
        df_all.append(df4)
    return pd.concat(df_all, axis=1).T.reset_index(drop=True)


def parent_tp_analysis(result_excel_file, identified_cmp_only=True, frag_num_threshold=2):
    """
    Identifies potential parent-transformation product relationships from DDA raw data
    using shared fragments.

    Args:
        result_excel_file (str): The path to the result file after database matching.
        identified_cmp_only (bool, optional): If True, focus on only the identified compounds.
                                              Default is True.
        frag_num_threshold (int, optional): Minimum number of common fragments required to
                                            establish a relationship. Default is 2.

    Returns:
        None: This function modifies the input file directly without returning a value.
    """
    # Read the excel file containing the results
    cmp_result = pd.read_excel(result_excel_file)
    # avoid duplicated new_index
    # Convert the 'frag_DDA' column to a list
    cmp_result['frag_DDA'] = cmp_result['frag_DDA'].apply(eval)
    # Create a new column to store the length of each list in 'frag_DDA'
    cmp_result['frag_DDA_count'] = cmp_result['frag_DDA'].apply(len)
    # Sort the dataframe based on 'new_index' and 'frag_DDA_count' in descending order
    cmp_result_sorted = cmp_result.sort_values(by=['new_index', 'frag_DDA_count'], ascending=[True, False])
    # Drop duplicates based on 'new_index' and retain the first entry
    cmp_result_deduplicated = cmp_result_sorted.drop_duplicates(subset='new_index', keep='first')
    # Drop the 'frag_DDA_count' column
    cmp_result = cmp_result_deduplicated.drop(columns=['frag_DDA_count']).reset_index(drop=True)
    # convert back
    cmp_result['frag_DDA'] = cmp_result['frag_DDA'].apply(str)
    
    # must have column with frag_DDA
    if 'frag_DDA' in cmp_result.columns.values:
        # Extract DDA results and their respective indices
        DDA_result = [np.array(eval(i)) for i in cmp_result.frag_DDA]
        DDA_index = [n for n, i in enumerate(cmp_result.frag_DDA) if len(eval(i)) > 0]
        
        # Check if there are any DDA results available
        if len(DDA_index) == 0:
            pass
        else:
            # Generate all possible combinations of DDA results
            combinations = itertools.combinations(DDA_index, 2)
            t = [list(i) for i in combinations]
            
            # whether consider identification?
            if identified_cmp_only is True:
                # Filter out the combinations that do not have level 1 or 2 results
                level1_2_index = cmp_result[(~(cmp_result['best_results_DDA']  # 只考虑有定性结果的，level1，level2，level3
                                               == '[]')) | (~(cmp_result['rt_match_result'] == '[]'))].index
                t = [i for i in t if (i[0] in level1_2_index) | (i[1] in level1_2_index)]
                
                # Compare all possible DDA combinations
                compare_result = [compare_frag(DDA_result[t[i][0]], DDA_result[t[i][1]]) for i in
                                  range(len(t))]  # 比较所有可能DDA
                
                # Count the number of common fragments in each comparison
                nums = [len(s) for s in compare_result]  # 比较每种可能性
                
                # Create a dataframe to store the results
                result_df = pd.DataFrame(data=t)
                result_df.columns = ['cmp1', 'cmp2']
                result_df.cmp1 = cmp_result.new_index.loc[result_df.cmp1.values].values
                result_df.cmp2 = cmp_result.new_index.loc[result_df.cmp2.values].values
                result_df.loc[:, 'same_frag_num'] = nums
                result_df.loc[:, 'frag_info'] = [str(a.round(4).to_dict()) for a in compare_result]
                
                # Filter out comparisons with no common fragments
                result_df = result_df[result_df.same_frag_num > frag_num_threshold]
                result_df = result_df.sort_values(by='same_frag_num', ascending=False).reset_index(drop=True)
                
                # Assign a level to each compound based on the available results
                index1 = list(set(np.hstack([result_df['cmp1'].values, result_df['cmp2'].values])))  # 将所有index合并
                level = []
                # 对index进行分级
                for index in index1:
                    df_index = cmp_result[cmp_result['new_index'] == index]
                    if (df_index['rt_match_result'].values != '[]') & (df_index['best_results_DDA'].values != '[]'):
                        level.append(1)
                    elif (df_index['rt_match_result'].values != '[]') & (df_index['best_results_DDA'].values == '[]'):
                        level.append(3)
                    elif (df_index['rt_match_result'].values == '[]') & (df_index['best_results_DDA'].values != '[]'):
                        level.append(2)
                    else:
                        level.append(None)
                s2 = pd.Series(level, index1)
                for i in range(len(result_df)):
                    cmp1_index, cmp2_index = result_df.loc[i, 'cmp1'], result_df.loc[i, 'cmp2']
                    result_df.loc[i, 'cmp1_level'] = s2.loc[cmp1_index]
                    result_df.loc[i, 'cmp2_level'] = s2.loc[cmp2_index]
                result_df = result_df.loc[:, ['cmp1', 'cmp1_level', 'cmp2', 'cmp2_level', 'same_frag_num', 'frag_info']]
            else:
                # Compare all possible DDA combinations
                compare_result = [compare_frag(DDA_result[t[i][0]], DDA_result[t[i][1]]) for i in
                                  range(len(t))]  # 比较所有可能DDA
                
                # Count the number of common fragments in each comparison
                nums = [len(s) for s in compare_result]  # 比较每种可能性
                
                # Create a dataframe to store the results
                result_df = pd.DataFrame(data=t)
                result_df.columns = ['cmp1', 'cmp2']
                result_df.cmp1 = cmp_result.new_index.loc[result_df.cmp1.values].values
                result_df.cmp2 = cmp_result.new_index.loc[result_df.cmp2.values].values
                result_df.loc[:, 'same_frag_num'] = nums
                result_df.loc[:, 'frag_info'] = [str(a.round(4).to_dict()) for a in compare_result]
                # Filter out comparisons with no common fragments
                result_df = result_df[result_df.same_frag_num > frag_num_threshold]
                result_df = result_df.sort_values(by='same_frag_num', ascending=False).reset_index(drop=True)
            
            with ExcelWriter(result_excel_file) as writer:
                cmp_result.to_excel(writer, sheet_name='Original Data')
                result_df.to_excel(writer, sheet_name='DDA_parent_products_analysis')


def isotope_matching(iso_info, formula, adduct='+H'):
    """
    Compare the real isotope distribution with the theoretical isotope distribution of a given formula.

    Args:
        iso_info (dict): A dictionary with the isotope distribution information.
        formula (str): The chemical formula for comparison.
        adduct (str): The ion adduct, '+H' or '-H','+','-'.

    Returns:
        A pandas DataFrame containing the comparison results with columns for the expected and observed
        mass-to-charge ratio (mz), their respective distributions, the absolute difference between the
        distributions (dis_diff), and the absolute difference between the mz values (mz_diff).
    """
    
    isotopes, distribution = formula_to_distribution(formula, num=5, adducts=adduct)
    s_obs = pd.Series(iso_info)
    
    # Align mz values to a tolerance of 0.015
    a = sorted(np.hstack([isotopes, s_obs.index]))  # 所有的质量放一起
    if len(a) > 1:
        b = [a[0] if abs(a[1] - a[0]) > 0.015 else a[0]] + [a[i + 1] for i in range(len(a) - 1) if
                                                            abs(a[i] - a[i + 1]) > 0.015]
    else:
        b = a  # b为alignment之后的质量
    
    # Create dataframes for expected and observed isotope information
    df_exp = pd.DataFrame(index=[b[argmin(abs(b - x))] for x in isotopes],
                          data=np.vstack([isotopes, distribution / 100]).T,
                          columns=['mz_exp', 'exp_distribution'])
    
    df_obs = pd.DataFrame(index=[b[argmin(abs(b - x))] for x in s_obs.index.values],
                          data=np.vstack([s_obs.index.values, s_obs.values]).T,
                          columns=['mz_obs', 'obs_distribution'])
    
    # Join dataframes and compute differences
    compare_result = pd.concat([df_exp, df_obs], axis=1)
    compare_result = compare_result[~compare_result.mz_exp.isna()].fillna(0)
    compare_result['dis_diff'] = abs(compare_result.exp_distribution - compare_result.obs_distribution)
    compare_result['mz_diff'] = abs(compare_result.mz_exp - compare_result.mz_obs)
    return compare_result


def remove_adducts(df, mode='pos'):
    """
    Remove adducts and isotopes from a dataframe, while preserving matching results.

    Args:
        df: A pandas dataframe with columns 'match_result_DIA', 'best_results_DIA',
            'match_result_DDA', 'best_results_DDA', and 'rt_match_result'.
        mode: A string indicating whether to remove positive ('pos') or negative ('neg') adducts.

    Returns:
        A new pandas dataframe with adducts and isotopes removed.
    """
    
    # If any required columns are missing, create them with empty lists as values.
    columns_names = ['match_result_DIA', 'best_results_DIA',
                     'match_result_DDA', 'best_results_DDA', 'rt_match_result']
    for columns_name in columns_names:
        if columns_name not in df.columns.values:
            df[columns_name] = str([])
    
    # Filter for rows with matching results.
    df_info1 = df[(df['match_result_DIA'] != '[]') | (df['match_result_DDA'] != '[]') | (df['rt_match_result'] != '[]')]
    
    # Remove specified adducts and isotopes.
    if mode == 'pos':
        names = ['Ciso', 'Cliso', 'Na adducts', 'NH4 adducts', 'Briso', 'K adducts']
    else:
        names = ['Ciso', 'Cliso', 'Briso']
    for name in names:
        if name in df.columns.values:
            df = df[(df[name].isna())]
    
    # Combine all information and sort by intensity.
    final_info = pd.concat([df, df_info1]).sort_values(by='intensity')
    
    # Drop duplicates based on 'new_index' column.
    final_info = final_info.drop_duplicates(subset=['new_index'], keep='first')
    
    # Drop any columns with 'Unnamed:' in the name.
    names2 = [name for name in final_info.columns.values if 'Unnamed:' in name]
    final_info = final_info.drop(columns=names2)
    
    # Reset the index and return the final dataframe.
    return final_info.reset_index(drop=True)


def remove_adducts_all(path, mode):
    """
    Remove adducts from all Excel files in a specified directory using remove_adducts function.

    Args:
        path: A string indicating the directory path containing Excel files to process.
        mode: A string indicating whether to remove positive ('pos') or negative ('neg') adducts.

    Returns:
        None. Generates new Excel files with adducts removed.
    """
    
    # Find all Excel files in specified directory.
    files = glob(os.path.join(path, '*.xlsx'))
    
    # Process each file and save output as a new Excel file.
    for file in tqdm(files):
        df = pd.read_excel(file)
        df1 = remove_adducts(df, mode=mode)
        df1.to_excel(file.replace('.xlsx', '_removing_adducts.xlsx'))


def DDA_to_DIA_result(path, company, profile, intensity_threshold=200):
    """
      This function processes DDA (Data-Dependent Acquisition) data in mzML format
      and integrates the results into existing Excel files containing unique company information.

      Args:
          path (str): Path to the directory containing mzML files and Excel files.
          company (str): Name of the company associated with the data.
          profile (str): Profile to be used for DDA data processing.
          intensity_threshold(int): intensity threshold.
      Returns:
          None. The function modifies the existing Excel files in-place.

      **Notes:**
          - This function assumes the Excel files have columns named 'rt' and 'mz'.
          - The function relies on the `sep_scans`, `gen_DDA_ms2_df`, and Pandas library functions.
   """
    # 如果有DDA，将DDA数据加入到excel里
    files_excel = glob(os.path.join(path, '*.xlsx'))
    unique_cmps = [file for file in files_excel if 'unique_cmps' in os.path.basename(file)]
    files_mzml_DDA = [file for file in glob(os.path.join(path, '*.mzML')) if 'DDA' in file]
    num = 0
    for file in files_mzml_DDA:
        num += 1
        ms1, ms2 = sep_scans(file, company)
        df2 = gen_DDA_ms2_df(ms1, ms2, i_threshold=0, profile=profile, opt=False, more_info=False, message=f'No.{num} ')
        ce_num = df2['collision energy'].value_counts().index.values
        name = os.path.basename(file).replace('-DDA', '').replace('_DDA', '').replace('.mzML', '')  # 获得DDA文件的特征名称
        for file_excel in unique_cmps:
            if name in os.path.basename(file_excel):
                df1 = pd.read_excel(file_excel)
                for i in range(len(df1)):
                    rt, mz = df1.loc[i, ['rt', 'mz']]
                    df_frag_ = df2[(df2['precursor'] >= mz - 0.015) & (df2['precursor'] <= mz + 0.015)
                                   & (df2['rt'] >= rt - 0.1) & (df2['rt'] <= rt + 0.1)]
                    frag_DDA_all = []  # 创建一个列表来接收
                    
                    if len(ce_num) == 0:
                        df_frag = df_frag_
                        if len(df_frag) == 0:
                            df1.loc[i, f'MS2_spec_DDA_-1V'] = str({})
                            df1.loc[i, f'frag_DDA'] = str([])
                        else:
                            s_ms2_info = df_frag.iloc[np.argmin(abs(df_frag['rt'].values - rt))]
                            ms2_rt = df_frag['rt'].values[np.argmin(abs(df_frag['rt'].values - rt))]
                            s_ms2 = pd.Series(data=s_ms2_info['ms2_intensities'], index=s_ms2_info['frag'], name=ms2_rt)
                            s_ms2 = s_ms2[s_ms2 > 200]
                            frag_DDA_all.extend(list(s_ms2.index))
                            df1.loc[i, f'MS2_spec_DDA_-1V'] = str(s_ms2.astype(int).to_dict())
                            df1.loc[i, f'frag_DDA'] = str(frag_DDA_all)
                    else:
                        for ce in ce_num:
                            df_frag = df_frag_[df_frag_['collision energy'] == ce]
                            if len(df_frag) == 0:
                                df1.loc[i, f'MS2_spec_DDA_{ce}V'] = str({})
                                df1.loc[i, f'frag_DDA'] = str([])
                            # df1.loc[i, f'frag_DDA'] = str([])
                            else:
                                s_ms2_info = df_frag.iloc[np.argmin(abs(df_frag['rt'].values - rt))]
                                ms2_rt = df_frag['rt'].values[np.argmin(abs(df_frag['rt'].values - rt))]
                                s_ms2 = pd.Series(data=s_ms2_info['ms2_intensities'], index=s_ms2_info['frag'],
                                                  name=ms2_rt,
                                                  dtype='float64')
                                s_ms2 = s_ms2[s_ms2 > intensity_threshold]
                                frag_DDA_all.extend(list(s_ms2.index))
                                # df1.loc[i, 'frag_DDA'] = str(list(s_ms2.index))
                                df1.loc[i, f'MS2_spec_DDA_{ce}V'] = str(s_ms2.astype(int).to_dict())
                        df1.loc[i, f'frag_DDA'] = str(frag_DDA_all)
                df1.to_excel(file_excel)


"""
========================================================================================================
2. Swath data process
========================================================================================================
"""


def swath_window_checking(file, precursor_ion_start_mass=99.5, mz_overlap=1):
    """
    Analyzes the precursor ion windows in a given mzML file. This function separates MS1 and MS2 scans,
    determines unique precursor ions, and calculates the mass spectrum range for each precursor ion window
    based on the starting mass and overlap values.

    Parameters:
    - file (str): Path to the mzML file containing mass spectrometry data.
    - precursor_ion_start_mass (float, optional): Specifies the initial mass value for the sequential mass window in ion analysis.
      Defaults to 99.5.
    - mz_overlap (float, optional): Defines the amount of overlap between consecutive MS2 windows in mass units. Defaults to 1.

    Returns:
    - dict: A dictionary mapping each precursor ion to its corresponding mass spectrum range [start, end].

    Note:
    The function first calculates the window size for the initial precursor ion manually and then iteratively for the remaining ions,
    considering the specified overlap.
    """
    
    ms1, ms2 = sep_scans(file, 'AB')  # 分离ms1和ms2
    # 1. 获得所有selected precursors
    all_precursors = []
    for scan in ms2:
        all_precursors.append(round(scan.selected_precursors[0]['mz'], 1))
    precursors = list(set(all_precursors))
    precursors = sorted(precursors)
    
    # ======计算窗口大小=============
    
    precursor = precursors[0]
    # 第一个要手动
    ms_range = {}
    next_gap = precursors[0] - precursor_ion_start_mass
    ms_range[precursor] = [precursor - next_gap, precursor + next_gap]
    end_mz = round(precursor + next_gap, 1)
    for precursor in precursors[1:]:
        next_start_mz = round(end_mz - mz_overlap, 1)
        next_gap = precursor - next_start_mz
        end_mz = round(precursor + next_gap, 1)
        ms_range[precursor] = [next_start_mz, end_mz]
    return ms_range


def one_step_process_swath(path, company, profile=True,
                           control_group=['lab_blank', 'methanol'],
                           precursor_ion_start_mass=99.5,
                           filter_type=1,
                           peak_width=1,
                           threshold=15,
                           i_threshold=500,
                           SN_threshold=3,
                           mz_overlap=1,
                           rt_error=0.05, sat_intensity=False):
    """
    This function using one processor to process mzML data and perform a comparison between the sample set and the control set. The resulting data will be used to generate an Excel file that summarizes the differences between the two sets.
    Args:
       - path: The file path for the mzML files that will be processed. For example, '../Users/Desktop/my_HRMS_files'.
       - profile: A Boolean value that indicates whether the data is in profile or centroid mode. True for profile mode, False for centroid mode.
       - control_group (List[str]): A list of labels representing the control group.These labels are used in the search for relevant file names.

       - precursor_ion_start_mass: The starting point of the mass spectrum range for the sequential analysis of mass windows.

       - filter_type (int): Determines the mode of operation.
                           Set to 1 for data without triplicates; fold change is computed
                           as the ratio of the sample area to the maximum control area.
                           Set to 2 for data with triplicates; the function will calculate p-values,
                           and fold change is computed as the ratio of the mean sample area
                           to the mean control area.
        - mz_overlap: MS2 window overlap

    returns:
        None.Generate Excel files that summarizes the differences between the control sets and sample sets.

    """
    print('                                                                            ')
    print('============================================================================')
    print('First process...')
    print('============================================================================')
    print('                                                                            ')
    move_files(path)
    # Log function details
    func_name = inspect.currentframe().f_code.co_name
    func_params = inspect.getargvalues(inspect.currentframe()).locals
    log_function_details(path, func_name, func_params)
    
    files_mzml = glob(os.path.join(path, '*.mzML'))
    
    for j, file in enumerate(files_mzml):
        swath_result = swath_process(file, precursor_ion_start_mass=precursor_ion_start_mass,
                                     profile=profile,
                                     peak_width=peak_width,
                                     threshold=threshold,
                                     i_threshold=i_threshold,
                                     SN_threshold=SN_threshold,
                                     mz_overlap=mz_overlap,
                                     rt_error=rt_error, sat_intensity=sat_intensity, message=f'No. {j + 1} : ')
        
        swath_result.to_excel(file.replace('.mzML', '.xlsx'))
    
    # 中间过程
    files_excel = glob(os.path.join(path, '*.xlsx'))
    peak_alignment(files_excel)
    ref_all = pd.read_excel(os.path.join(path, 'peak_ref.xlsx'), index_col='Unnamed: 0')
    
    # 第二个过程
    print('                                                                            ')
    print('============================================================================')
    print('Second process...')
    print('============================================================================')
    print('                                                                            ')
    for j, file in enumerate(files_mzml):
        second_process(file, ref_all, company, profile=profile, message=f'No. {j + 1} ')
    
    # 第三个过程, 做fold change filter
    print('                                                                            ')
    print('============================================================================')
    print('Third process...')
    print('============================================================================')
    print('                                                                            ')
    
    fold_change_filter(path, control_group=control_group, filter_type=filter_type)


def swath_process(file, precursor_ion_start_mass=99.5, profile=True, peak_width=1,
                  threshold=15, i_threshold=500, SN_threshold=3, mz_overlap=1, rt_error=0.05, sat_intensity=False,
                  message=''):
    """
    Processing swath-ms data and return a dataframe with all informations
    :param file: file in mzml format
    :param precursor_ion_start_mass: The starting point of the mass spectrum range for the sequential analysis of mass windows.
    :param profile: if profile: True, Centroid: False
    :param threshold: peak picking threshold
    :param i_threshold: intensity threshold
    :param SN_threshold: singal to noise threshold
    :param mz_overlap: MS2 window overlap
    :param rt_error: rt_error
    :return: A dataframe with peak informations
    """
    ms1, ms2 = sep_scans(file, 'AB', message=message)  # 分离ms1和ms2
    
    peak_all_ms1 = split_peak_picking(ms1, profile=profile, threshold=threshold, peak_width=peak_width,
                                      i_threshold=i_threshold, SN_threshold=SN_threshold, message=message,
                                      sat_intensity=sat_intensity, orbi=True)
    
    # 1. 获得所有selected precursors
    all_precursors = []
    for scan in ms2:
        all_precursors.append(round(scan.selected_precursors[0]['mz'], 1))
    precursors = list(set(all_precursors))
    precursors = sorted(precursors)
    # precursor_diff = round((precursors[1]-precursors[0])/2,0)
    
    # 2. 创建好接收scans的变量
    all_data = {}
    for precursor in precursors:
        name = 'ms' + str(precursor)
        locals()[name] = []
        all_data[precursor] = name
    # 3. 接收变量
    for scan in ms2:
        name = 'ms' + str(round(scan.selected_precursors[0]['mz'], 1))
        locals()[name].append(scan)
    
    # 4. 开始分批提取峰
    all_peak_all = {}
    for k, v in all_data.items():
        message1 = f'Processing m/z: {k}:'
        message2 = message + message1
        x = locals()[v]
        peak_all = split_peak_picking_swath(x, k, profile=profile,
                                            i_threshold=i_threshold, peak_width=peak_width, message=message2)
        all_peak_all[k] = peak_all
    
    # ======计算窗口大小=============
    
    precursor = precursors[0]
    # 第一个要手动
    ms_range = {}
    next_gap = precursors[0] - precursor_ion_start_mass
    ms_range[precursor] = [precursor - next_gap, precursor + next_gap]
    end_mz = round(precursor + next_gap, 1)
    for precursor in precursors[1:]:
        next_start_mz = round(end_mz - mz_overlap, 1)
        next_gap = precursor - next_start_mz
        end_mz = round(precursor + next_gap, 1)
        ms_range[precursor] = [next_start_mz, end_mz]
    
    # ======将提取的峰赋值=============
    for i in tqdm(range(len(peak_all_ms1)), desc='Assign the extracted peaks', leave=False):
        rt, mz = peak_all_ms1.loc[i, ['rt', 'mz']]
        for k, v in ms_range.items():
            if (mz <= v[1] - 0.5) & (mz > v[0] + 0.5):
                scan_index = k
                break
        target_s = all_peak_all[scan_index]
        if len(target_s) == 0:
            peak_all_ms1.loc[i, 'frag_swath'] = str([])
            # peak_all_ms1.loc[i, 'MS2_spectra_swath'] = str([]) # 以后不要这个了
            peak_all_ms1.loc[i, 'MS2_spectra_swath_dict'] = str([])
        else:
            target_s_df = target_s[(target_s['rt'] > rt - rt_error) & (target_s['rt'] < rt + rt_error)]
            mz2, intensity2 = target_s_df['mz'].values, target_s_df['intensity'].values
            frag_s = pd.Series(data=intensity2, index=mz2)
            peak_all_ms1.loc[i, 'frag_swath'] = str(list(mz2))
            # peak_all_ms1.loc[i, 'MS2_spectra_swath'] = str(frag_s) # 以后不要这个了
            peak_all_ms1.loc[i, 'MS2_spectra_swath_dict'] = str(frag_s.to_dict())
    peak_all_ms1 = identify_isotopes(peak_all_ms1)
    return peak_all_ms1


def split_peak_picking_swath(ms1, highest_mz, profile=True, split_n=20, threshold=15, peak_width=1, i_threshold=1000,
                             SN_threshold=5, noise_threshold=0, rt_error_alignment=0.05, mz_error_alignment=0.015,
                             message=''):
    def target_spec1(spec, target_mz, width=0.04):
        """
        :param spec: spec generated from function spec_at_rt()
        :param target_mz: target mz for inspection
        :param width: width for data points
        :return: new spec and observed mz
        """
        index_left = argmin(abs(spec.index.values - (target_mz - width)))
        index_right = argmin(abs(spec.index.values - (target_mz + width)))
        new_spec = spec.iloc[index_left:index_right].copy()
        new_spec[target_mz - width] = 0
        new_spec[target_mz + width] = 0
        new_spec = new_spec.sort_index()
        return new_spec
    
    if profile is True:
        peaks_index = [[i, scipy.signal.find_peaks(ms1[i].i.copy())[0]]
                       for i in tqdm(range(len(ms1)), desc=f'{message}Loading Data', leave=False)]
        raw_info_centroid = {
            round(ms1[i].scan_time[0], 3): pd.Series(data=ms1[i].i[peaks], index=ms1[i].mz[peaks].round(4),
                                                     name=round(ms1[i].scan_time[0], 3)) for i, peaks in
            tqdm(peaks_index, desc=f'{message}Convert to Centroid', leave=False, colour='Green')}
        raw_info_profile = {round(ms1[i].scan_time[0], 3):
                                pd.Series(data=ms1[i].i, index=ms1[i].mz.round(4), name=round(ms1[i].scan_time[0], 3))
                            for i in tqdm(range(len(ms1)), desc=f'{message}Recording raw profile info', leave=False,
                                          colour='Green')}
        data = []
        for k, v in tqdm(raw_info_centroid.items(), desc=f'{message}Checking re-index data', leave=False,
                         colour='Green'):
            df = v.to_frame().reset_index()
            df = df.sort_values(['index', k])
            df.loc[:, 'index'] = np.round(df['index'].values, 3)
            df = df.drop_duplicates('index', keep='last')
            s = pd.Series(df[k].values, index=df['index'], name=k)
            data.append(s)
    else:
        raw_info_centroid = {round(ms1[i].scan_time[0], 3): pd.Series(
            data=ms1[i].i, index=ms1[i].mz.round(4), name=round(ms1[i].scan_time[0], 3)) for i in
            tqdm(range(len(ms1)), desc=f'{message}Loading data', leave=False,
                 colour='Green')}
        data = []
        for k, v in tqdm(raw_info_centroid.items(), desc=f'{message}Checking re-index data', leave=False,
                         colour='Green'):
            df = v.to_frame().reset_index()
            df = df.sort_values(['index', k])
            df.loc[:, 'index'] = np.round(df['index'].values, 3)
            df = df.drop_duplicates('index', keep='last')
            s = pd.Series(df[k].values, index=df['index'], name=k)
            data.append(s)
    
    # 开始分割
    # 定义变量名称
    all_data = []
    for j in range(split_n):
        name = 'a' + str(j + 1)
        locals()[name] = []
    # 对series进行切割
    ms_increase = int(1700 / split_n)
    for i in tqdm(range(len(data)), desc=f'{message}Split series', leave=False, colour='Green'):
        s1 = data[i]
        low, high = 50, 50 + ms_increase
        for j in range(split_n):
            name = 'a' + str(j + 1)
            if low > highest_mz:
                break
            locals()[name].append(s1[(s1.index < high) & (s1.index >= low) & (s1.index > noise_threshold)])
            low += ms_increase
            high += ms_increase
    
    # 将所有数据合并到all_data里
    for j in range(split_n):
        name = 'a' + str(j + 1)
        all_data.append(locals()[name])
    
    # 开始分段提取
    all_peak_all = []
    for i in tqdm(range(len(all_data)), desc=f'{message}Peak_picking', leave=False, colour='Green'):
        data1 = all_data[i]
        if len(data1) == 0:
            pass
        else:
            df1 = pd.concat(data1, axis=1)
            
            df1 = df1.fillna(0)
            if len(df1) == 0:
                pass
            else:
                highest_mz = df1.index.values.max()
                peak_all = peak_picking(df1, isotope_analysis=False, threshold=threshold, peak_width=peak_width,
                                        i_threshold=i_threshold, SN_threshold=SN_threshold,
                                        rt_error_alignment=rt_error_alignment,
                                        mz_error_alignment=mz_error_alignment, enable_progress_bar=False)
                all_peak_all.append(peak_all)
    
    # 避免concat空列表
    if len(all_peak_all) == 0:
        peak_all = pd.DataFrame()
    else:
        peak_all = pd.concat(all_peak_all)
    
    if len(peak_all) == 0:
        pass
    else:
        peak_all = peak_all.sort_values(by='intensity', ascending=False).reset_index(drop=True)
        raw_info_rts = [v.name for k, v in raw_info_centroid.items()]
        rts = peak_all.rt.values
        mzs = peak_all.mz.values
        rt_keys = [raw_info_rts[argmin(abs(np.array(raw_info_rts) - i))] for i in rts]  # 基于上述rt找到ms的时间索引
        
        # 更新质量数据
        if profile is True:
            spec1 = [raw_info_profile[i] for i in rt_keys]  # 获得ms的spec
            mz_result = np.array(
                [list(evaluate_ms(target_spec1(spec1[i], mzs[i], width=0.04).copy(), mzs[i])) for i in
                 tqdm(range(len(mzs)), desc=f'{message} Correcting m/z', leave=False)]).T
            mz_obs, mz_opt, resolution = mz_result[0], mz_result[2], mz_result[4]
            mz_opt = [mz_opt[i] if abs(mzs[i] - mz_opt[i]) < 0.02 else mzs[i] for i in range(len(mzs))]  # 去掉偏差大的矫正结果
            
            peak_all.loc[:, ['mz', 'mz_opt', 'resolution']] = np.array([mz_obs, mz_opt, resolution.astype(int)]).T
        
        else:
            spec1 = [raw_info_centroid[i] for i in rt_keys]  # 获得ms的spec
            target_spec = [spec1[i][(spec1[i].index > mzs[i] - 0.015) & (spec1[i].index < mzs[i] + 0.015)] for i in
                           range(len(spec1))]
            mzs_obs = [target_spec[i].index.values[[np.argmax(target_spec[i].values)]][0] for i in
                       range(len(target_spec))]
            peak_all['mz'] = mzs_obs
    return peak_all


def swath_frag_extract(ms2, mz, frag, error=50, precursor_ion_start_mass=99.5):
    '''
    Chromatogram extract based on precusor and fragment.
    :param ms2: ms2 from sep_scans
    :param mz: precursor
    :param frag: fragment to extract
    :param error: mass error window
    :param precursor_ion_start_mass: precursor_ion_start_mass
    :return: rts, eic
    '''
    
    def swath_window(ms2, precursors=[], precursor_ion_start_mass=precursor_ion_start_mass):
        precursor_ion_start_mass = 99.5
        mz_overlap = 1
        ms_range = {}
        precursor = precursors[0]
        # 第一个要手动
        ms_range = {}
        next_gap = precursors[0] - precursor_ion_start_mass
        ms_range[precursor] = [precursor - next_gap, precursor + next_gap]
        end_mz = round(precursor + next_gap, 1)
        for precursor in precursors[1:]:
            next_start_mz = round(end_mz - mz_overlap, 1)
            next_gap = precursor - next_start_mz
            end_mz = round(precursor + next_gap, 1)
            ms_range[precursor] = [next_start_mz, end_mz]
        return ms_range
    
    # 1. 获得所有selected precursors
    all_precursors = []
    for scan in ms2:
        all_precursors.append(round(scan.selected_precursors[0]['mz'], 1))
    precursors = list(set(all_precursors))
    precursors = sorted(precursors)
    # precursor_diff = round((precursors[1]-precursors[0])/2,0)
    
    # 2. 创建好接收scans的变量
    all_data = {}
    for precursor in precursors:
        name = 'ms' + str(precursor)
        locals()[name] = []
        all_data[precursor] = name
    # 3. 接收变量
    for scan in ms2:
        name = 'ms' + str(round(scan.selected_precursors[0]['mz'], 1))
        locals()[name].append(scan)
    
    # 4. 存储变量
    all_data1 = {}
    for precursor in precursors:
        name = 'ms' + str(precursor)
        all_data1[precursor] = locals()[name]
    
    ms_range = swath_window(ms2, precursors=precursors, precursor_ion_start_mass=precursor_ion_start_mass)
    for k, v in ms_range.items():
        if (mz <= v[1] - 0.5) & (mz > v[0] + 0.5):
            scan_index = k
            break
    new_ms2 = all_data1[scan_index]
    rts, eic = extract(new_ms2, frag, error=error)
    return rts, eic


def swath_frag_raw(ms2, mz, rt, precursor_ion_start_mass=99.5):
    '''
    Chromatogram extract based on precusor and fragment.
    :param ms2: ms2 from sep_scans
    :param mz: precursor
    :param rt: retention time
    :param precursor_ion_start_mass: precursor_ion_start_mass
    :return: mzs,intensities
    '''
    
    def swath_window(ms2, precursors=[], precursor_ion_start_mass=precursor_ion_start_mass):
        precursor_ion_start_mass = 99.5
        mz_overlap = 1
        ms_range = {}
        precursor = precursors[0]
        # 第一个要手动
        ms_range = {}
        next_gap = precursors[0] - precursor_ion_start_mass
        ms_range[precursor] = [precursor - next_gap, precursor + next_gap]
        end_mz = round(precursor + next_gap, 1)
        for precursor in precursors[1:]:
            next_start_mz = round(end_mz - mz_overlap, 1)
            next_gap = precursor - next_start_mz
            end_mz = round(precursor + next_gap, 1)
            ms_range[precursor] = [next_start_mz, end_mz]
        return ms_range
    
    # 1. 获得所有selected precursors
    all_precursors = []
    for scan in ms2:
        all_precursors.append(round(scan.selected_precursors[0]['mz'], 1))
    precursors = list(set(all_precursors))
    precursors = sorted(precursors)
    # precursor_diff = round((precursors[1]-precursors[0])/2,0)
    
    # 2. 创建好接收scans的变量
    all_data = {}
    for precursor in precursors:
        name = 'ms' + str(precursor)
        locals()[name] = []
        all_data[precursor] = name
    # 3. 接收变量
    for scan in ms2:
        name = 'ms' + str(round(scan.selected_precursors[0]['mz'], 1))
        locals()[name].append(scan)
    
    # 4. 存储变量
    all_data1 = {}
    for precursor in precursors:
        name = 'ms' + str(precursor)
        all_data1[precursor] = locals()[name]
    
    ms_range = swath_window(ms2, precursors=precursors, precursor_ion_start_mass=precursor_ion_start_mass)
    for k, v in ms_range.items():
        if (mz <= v[1] - 0.5) & (mz > v[0] + 0.5):
            scan_index = k
            break
    new_ms2 = all_data1[scan_index]
    for scan in new_ms2:
        if scan.scan_time[0] > rt:
            break
    mzs = scan.mz
    intensities = scan.i
    return mzs, intensities


def extract(df, mz, error=50):
    """
    Extract chromatogram from a LC-MS DataFrame or a list of MS scans.

    Parameters:
        df (pd.DataFrame or list): LC-MS DataFrame generated by gen_df() or a list of MS scans.
        mz (float): Target mass for extraction.
        error (float, optional): Mass error for extraction. Default is 50.

    Returns:
        tuple: Tuple containing RT and EIC arrays.
    """
    if isinstance(df, pd.DataFrame):
        low_mz = mz * (1 - error * 1e-6)
        high_mz = mz * (1 + error * 1e-6)
        df2 = df.loc[df.index[(df.index > low_mz) & (df.index < high_mz)]]
        rt = df.columns.values
        intensity = np.zeros(len(df.columns))
        if len(df2) != 0:
            intensity = df2.max(axis=0).values
    elif isinstance(df, list):
        rt = []
        intensity = []
        low_mz = mz * (1 - error * 1e-6)
        high_mz = mz * (1 + error * 1e-6)
        for scan in df:
            mz_all = scan.mz
            i_all = scan.i
            rt1 = scan.scan_time[0]
            rt.append(rt1)
            index_e = np.where((mz_all <= high_mz) & (mz_all >= low_mz))
            eic1 = 0 if len(index_e[0]) == 0 else i_all[index_e[0]].max()
            intensity.append(eic1)
    else:
        rt, intensity = None, None
    return rt, intensity


def precursor_frag_peak_area(files_unique, path_to_mzml, company, rt_error=0.1,
                             ms1_error=0.01, ms2_error=0.015,
                             precursor_ion_start_mass=99.5, profile=True, mz_overlap=1, sn_info=False):
    """
    Analyzes swath mass spectrometry data to collect peak areas for fragment ions within specified retention time (RT) and precursor ranges. This function integrates multiple processing steps, including generating reference peaks, separating scans from mzML files, and calculating peak areas.

    Parameters:
    files_excel (list of str): Paths to Excel files containing swath result data.
    path_to_mzml (str): Directory path where mzML files are stored.
    company (str): The name of the company that manufactured the mass spectrometry instrument (e.g., "Agilent", "Waters", "AB", "Thermo").
    rt_error (float): The error tolerance for retention time. Default is 0.1.
    ms1_error (float): The error tolerance for the mass-to-charge ratio (m/z) in MS1. Default is 0.01.
    ms2_error (float): The error tolerance for the mass-to-charge ratio (m/z) in MS2. Default is 0.015.
    precursor_ion_start_mass (float): The starting mass of the scan range for precursor ions. Default is 99.5.
    mz_overlap (float): The overlap between the fragment windows in m/z units. Default is 1.

    Returns:
    None: This function does not return a value. Instead, it generates Excel files directly, containing the calculated peak areas for each fragment. Each Excel file corresponds to a processed mzML file and is saved in the same directory as the input mzML file.
    """
    
    # 1. 处理获得peak_ref
    peak_ref = gen_ref_swath(files_unique, rt_error=rt_error, ms1_error=ms1_error, ms2_error=ms2_error)
    peak_ref = [i for i in peak_ref if i[1] > i[2]]
    peak_ref = np.array(peak_ref)
    
    # 2. 获得每个final_area并导出
    files_mzml = glob(os.path.join(path_to_mzml, '*.mzML'))
    for i, file in enumerate(files_mzml):
        ms1, ms2 = sep_scans(file, company)
        final_area = peak_checking_area_precursor_frag_swath(peak_ref, ms2,
                                                             precursor_ion_start_mass=precursor_ion_start_mass,
                                                             profile=profile,
                                                             mz_overlap=mz_overlap, message=f'No. {i + 1} :',
                                                             sn_info=sn_info)
        final_area.to_excel(file.replace('.mzML', '_precursor_frag_final_area.xlsx'))


def peak_checking_area_precursor_frag_swath(peak_ref, ms2, precursor_ion_start_mass=99.5, profile=True, mz_overlap=1,
                                            name='area', message='', sn_info=False):
    """
    Collects the peak areas for fragments within specified retention time (RT) and precursor ranges from MS2 scans.

    This function processes MS2 scans to extract peak areas of fragments that fall within the RT and precursor mass range defined by the peak reference data. It considers the precursor ion start mass and the overlap between fragment windows to segment the data accurately.

    Parameters:
    peak_ref (numpy.ndarray): A numpy array containing reference peak information, including retention time (RT), precursor, and fragments. Typically generated by the function "gen_ref_swath".
    ms2 (list): A list of MS2 scans, where each scan contains information about selected precursors and other MS2 data.
    precursor_ion_start_mass (float): The starting mass of the scan range for precursor ions. Default is 99.5.
    mz_overlap (float): The overlap between the fragment windows in mass-to-charge ratio (m/z) units. Default is 1.
    message (str): A message string for progress tracking, used with tqdm for displaying progress. Default is an empty string.

    Returns:
    pandas.DataFrame: A DataFrame containing the calculated peak areas for each fragment within the specified RT and precursor ranges. Each row corresponds to a fragment, with columns for retention time, m/z, area, and a raw index combining RT, m/z, and fragment number.
    """
    
    # 1. 获得所有selected precursors
    all_precursors = []
    for scan in ms2:
        all_precursors.append(round(scan.selected_precursors[0]['mz'], 1))
    precursors = list(set(all_precursors))
    precursors = sorted(precursors)
    
    # 2. 创建好接收scans的变量
    all_data = {}
    for precursor in precursors:
        name = 'ms' + str(precursor)
        locals()[name] = []
        all_data[precursor] = name
    # 3. 接收变量
    for scan in ms2:
        name = 'ms' + str(round(scan.selected_precursors[0]['mz'], 1))
        locals()[name].append(scan)
    
    # ======计算窗口大小=============
    
    precursor = precursors[0]
    # 第一个要手动
    ms_range = {}
    next_gap = precursors[0] - precursor_ion_start_mass
    ms_range[precursor] = [precursor - next_gap, precursor + next_gap]
    end_mz = round(precursor + next_gap, 1)
    for precursor in precursors[1:]:
        next_start_mz = round(end_mz - mz_overlap, 1)
        next_gap = precursor - next_start_mz
        end_mz = round(precursor + next_gap, 1)
        ms_range[precursor] = [next_start_mz, end_mz]
    
    # 开始分段提取
    peak_area_all = []
    x1 = 0.5
    items = list(ms_range.items())  # Convert dictionary items to a list for iteration
    for i, (k, v) in enumerate(items):
        message1 = message + 'ms1 range: ' + str(v) + '  '
        # Check if this is the last item in the dictionary
        if i == len(items) - 1:
            x1 = 0
        # Apply the range condition to peak_ref
        sep_peak_ref = peak_ref[np.where((peak_ref[:, 1] >= v[0] + 0.5) & (peak_ref[:, 1] < v[1] - x1))]
        sep_peak_ref = np.array(sorted(sep_peak_ref, key=lambda x: x[2]))
        target_ms2 = locals()['ms' + str(k)]
        
        # revise 1. 根据sep_peak_ref找到传统的rt_mz pair
        string_array_fast = np.apply_along_axis(lambda row: "_".join(row.astype(str)), 1, sep_peak_ref)
        # Adjusting the lambda function to only join the first and last elements of each row
        string_array_first_last = [i.split('_')[0].rstrip('0').rstrip('.')
                                   + '_' + i.split('_')[-1].rstrip('0').rstrip('.') for i in string_array_fast]
        
        raw_index_info = pd.DataFrame(index=string_array_fast, data=string_array_first_last, columns=['short_index'])
        # revise 2. 根据short_index去提取峰
        short_info = list(set(raw_index_info['short_index'].values))
        short_info_values = [[eval(i.split('_')[0]), eval(i.split('_')[1])] for i in short_info]
        ref_all = pd.DataFrame(short_info_values)
        ref_all.columns = ['rt', 'mz']
        peak_area = peak_checking_area_split(ref_all, target_ms2, 'peak_area', profile=profile, orbi=True,
                                             message=message1, sn_info=sn_info)
        # revise 3. 映射到raw_index_info
        raw_index_info['peak area'] = raw_index_info['short_index'].map(peak_area['peak_area'])
        if sn_info is True:
            raw_index_info['peak_area_S/N'] = raw_index_info['short_index'].map(peak_area['peak_area_S/N'])
            
            # 解决nan的情况
            raw_index_info['peak_area_S/N'] = raw_index_info['peak_area_S/N'].fillna(0)
        raw_index_info['peak area'] = raw_index_info['peak area'].fillna(1)
        peak_area_all.append(raw_index_info)
    return pd.concat(peak_area_all)


def gen_ref_swath_inner(data, rt_error=0.1, ms1_error=0.01, ms2_error=0.015):
    """
    Generates a reference list from a set of data points considering the given rt, ms1, and ms2 error tolerances.

    Args:
    data (np.array): The list of [[rt,mz,frag]...].
    rt_error (float): The error tolerance for retention time.
    ms1_error (float): The error tolerance for ms1.
    ms2_error (float): The error tolerance for ms2.

    Returns:
    list: A list of reference points that meet the error criteria.
    """
    
    # Calculate the range for rt, ms1, and ms2
    rt_range = np.ptp(data[:, 0])
    ms1_range = np.ptp(data[:, 1])
    ms2_range = np.ptp(data[:, 2])
    
    # Scale the tolerances relative to the range of each dimension
    scaled_rt_tol = rt_error / rt_range
    scaled_ms1_tol = ms1_error / ms1_range
    scaled_ms2_tol = ms2_error / ms2_range
    
    # Scale the data
    scaled_data = np.copy(data)
    scaled_data[:, 0] /= rt_range
    scaled_data[:, 1] /= ms1_range
    scaled_data[:, 2] /= ms2_range
    
    # Create a KDTree with scaled data
    tree = KDTree(scaled_data)
    
    # Initialize reference list and visited set
    reference_list = []
    visited = set()
    
    # Iterate over each point
    for idx, scaled_point in tqdm(enumerate(scaled_data),
                                  desc='Aligning all rt_mz pairs(inner)', leave=False, colour='Green'):
        if idx in visited:
            continue
        
        # Find neighbors within a spherical range
        neighbors = tree.query_ball_point(scaled_point, r=max(scaled_rt_tol, scaled_ms1_tol, scaled_ms2_tol))
        
        # Filter neighbors based on actual tolerances
        filtered_neighbors = [i for i in neighbors if
                              abs(data[i, 0] - data[idx, 0]) <= rt_error and
                              abs(data[i, 1] - data[idx, 1]) <= ms1_error and
                              abs(data[i, 2] - data[idx, 2]) <= ms2_error]
        
        # Mark neighbors as visited
        visited.update(filtered_neighbors)
        
        # Add the first neighbor to the reference list
        reference_list.append(list(data[idx]))
    
    return reference_list


def gen_ref_swath(files_excel, rt_error=0.1, ms1_error=0.01, ms2_error=0.015):
    """
    Generates a reference list from a set of data points considering the given rt, ms1, and ms2 error tolerances.

    Args:
    files_excel (list): The list of file paths to excel files.
    rt_error (float): The error tolerance for retention time.
    ms1_error (float): The error tolerance for ms1.
    ms2_error (float): The error tolerance for ms2.

    Returns:
    list: A list of reference points that meet the error criteria.
    """
    
    # Gather all data points from the files
    pairs_all = [
        [
            [df.loc[i, 'rt'], df.loc[i, 'mz'], frag]
            for i in tqdm(range(len(df)), leave=False, desc='Reading swath frag for alignment')
            for frag, intensity in eval(df.loc[i, 'MS2_spectra_swath_dict']).items()
        ]
        for file in files_excel
        for df in [pd.read_excel(file)]
    ]
    data = np.vstack(pairs_all)
    
    # Convert data to numpy array
    data = np.array(data)
    
    # Calculate the range for rt, ms1, and ms2
    rt_range = np.ptp(data[:, 0])
    ms1_range = np.ptp(data[:, 1])
    ms2_range = np.ptp(data[:, 2])
    
    # Scale the tolerances relative to the range of each dimension
    scaled_rt_tol = rt_error / rt_range
    scaled_ms1_tol = ms1_error / ms1_range
    scaled_ms2_tol = ms2_error / ms2_range
    
    # Scale the data
    scaled_data = np.copy(data)
    scaled_data[:, 0] /= rt_range
    scaled_data[:, 1] /= ms1_range
    scaled_data[:, 2] /= ms2_range
    
    # Create a KDTree with scaled data
    tree = KDTree(scaled_data)
    
    # Initialize reference list and visited set
    reference_list = []
    visited = set()
    
    # Iterate over each point
    for idx, scaled_point in tqdm(enumerate(scaled_data),
                                  desc='Aligning all rt_mz pairs(gen_ref_swath)', leave=False, colour='Green'):
        if idx in visited:
            continue
        
        # Find neighbors within a spherical range
        neighbors = tree.query_ball_point(scaled_point, r=max(scaled_rt_tol, scaled_ms1_tol, scaled_ms2_tol))
        
        # Filter neighbors based on actual tolerances
        filtered_neighbors = [i for i in neighbors if
                              abs(data[i, 0] - data[idx, 0]) <= rt_error and
                              abs(data[i, 1] - data[idx, 1]) <= ms1_error and
                              abs(data[i, 2] - data[idx, 2]) <= ms2_error]
        
        # Mark neighbors as visited
        visited.update(filtered_neighbors)
        
        # Add the first neighbor to the reference list
        reference_list.append(list(data[idx]))
    
    return reference_list


def eval2(input_string):
    """
    Converts a string representation of a series back into a pandas Series.

    Args:
    input_string (str): The string representation of the series.

    Returns:
    pd.Series: A pandas Series object.
    """
    # Check for empty series representation
    if input_string.strip() == 'Series([], dtype: float64)':
        return pd.Series(dtype='float64')
    
    # Process the string to convert it into a series
    try:
        # Splitting the string by new lines and then by spaces to separate index and value
        lines = input_string.strip().split('\n')
        index = []
        values = []
        for line in lines:
            if line.startswith('dtype'):  # Skip dtype line
                continue
            index_value = line.split()
            if len(index_value) == 2:
                index.append(float(index_value[0]))
                values.append(float(index_value[1]))
        return pd.Series(values, index=index, dtype='float64')
    except Exception as e:
        raise ValueError(f"Error converting string to series: {e}")


"""
========================================================================================================
3. Omics functions
========================================================================================================
"""


def PCA_analysis(data, additional_info=False):
    """
    Performs PCA analysis on the given final area data and returns a DataFrame
    containing the results.

    Parameters:
        data (pd.DataFrame): DataFrame containing the final area data.

    Returns:
        pd.DataFrame: DataFrame containing the PCA results.
    """
    scaled_data = preprocessing.scale(data.T)
    pca = PCA()
    pca.fit(scaled_data)
    pca_data = pca.transform(scaled_data)
    per_var = np.round(pca.explained_variance_ratio_ * 100, 1)
    labels = ['PC' + str(x) for x in range(1, len(per_var) + 1)]
    pca_df = pd.DataFrame(pca_data, index=data.columns.values, columns=labels)
    if additional_info:
        return pca_df, per_var
    else:
        return pca_df


def omics_final_area(path, names):
    """
    This function summarizes all the final area files, calculates the average value for each sample set, and returns a
    pandas DataFrame with the results.

    Args:
        path: A string specifying the path to the final area files.
        names: A list of strings specifying the names of the sample sets.

    Returns:
        A pandas DataFrame with the average final areas for each sample set.

    Raises:
        FileNotFoundError: If no files are found in the specified path.
        ValueError: If no final area files are found in the specified path.

    Examples:
        omics_final_area('path/to/final_area_files', ['SampleSet1', 'SampleSet2'])
             SampleSet1  SampleSet2
        0            10          20
        1            12          25
        2            15          30
    """
    
    # Get a list of all files in the specified path that have the name 'final_area' and an .xlsx extension.
    files = glob(os.path.join(path, '*.xlsx'))
    
    # Filter out any files that don't contain the specified sample set names.
    files = [file for file in files if 'final_area' in os.path.basename(file)]
    
    final_result = []
    for name in names:
        print(f'Processing name: {name}')
        name_files = [file for file in files if name in file]
        name_data = []
        for file in name_files:
            file_name1 = os.path.basename(file)
            print(f'     * reading file: {file_name1}')
            df = pd.read_excel(file, index_col='Unnamed: 0')
            name_data.append(df)
        name_s = pd.concat(name_data, axis=1).mean(axis=1)
        final_result.append(name_s)
    data = pd.concat(final_result, axis=1).fillna(1).astype(int)
    data.columns = names
    return data


def omics_index_dict(path, all_new_index, names, rt_threshold=0.2, mz_threshold=0.02):
    """
    Given a list of new_index values, this function checks if each value corresponds to a pair of
    retention time (rt) and mass-to-charge ratio (mz) values that are present in a set of Excel files
    containing omics data. For each sample set, the function returns a dictionary mapping sample set
    names to lists of new_index values that correspond to valid rt/mz pairs in the omics data files.

    Args:
        path (str): A string representing the path to the directory where the Excel files are located.
        all_new_index (list): A list of new_index values to check,usually from final_data.index.
        names (list): A list of names for the sample sets to process.

    Returns:
        dict: A dictionary with sample set names as keys and lists of new_index values as values.

    """
    
    files = glob(os.path.join(path, '*.xlsx'))
    # 把所有new_index转化成pair
    pair = [[eval(all_new_index[i].split('_')[0]), eval(all_new_index[i].split('_')[1])] for i in
            range(len(all_new_index))]
    pair_df = pd.DataFrame(np.array(pair))
    pair_df.columns = ['rt', 'mz']
    pair_df.index = all_new_index
    # 针对每一组样品进行处理
    final_dict = {}
    for name in names:
        print(f'Processing files name: {name}')
        name_files = [file for file in files if name in file]
        df_all = []
        for file in name_files:
            file_name1 = os.path.basename(file)
            print(f'   * reading {file_name1}')
            df = pd.read_excel(file)
            df_all.append(df)
        df_all_df = pd.concat(df_all, axis=0).reset_index(drop=True)
        index_check = []
        for i in tqdm(range(len(pair_df)), desc='Checking compounds for each new_index:'):
            rt, mz = pair_df.iloc[i, [0, 1]]
            new_index = pair_df.iloc[i].name
            check_result = df_all_df[(df_all_df.rt > rt - rt_threshold) & (df_all_df.rt < rt + rt_threshold) &
                                     (df_all_df.mz < mz + mz_threshold) & (df_all_df.mz > mz - mz_threshold)]
            if len(check_result) > 0:
                index_check.append(new_index)
        final_dict[name] = index_check
    return final_dict


def omics_filter(data, index_dict, mz_range=[100, 800], rt_range=[1, 18], area_threshold=5000):
    """
    This function can help you to reduce the datasize and so the clustermap can be generated;;(omics_3)

    Args:
        data: dataframe for clustermap
        index_dict: index dict for each sample set
        mz_range: mz range
        rt_range: rt range
        area_threshold: area threshold
    returns:
        a new dataframe
    """
    
    final_list = []
    if isinstance(index_dict, dict):
        for key, values in index_dict.items():
            if key in data.columns:
                s1 = data[key]
                s2 = s1.loc[values]
                final_list.append(s2)
    elif isinstance(index_dict, pd.DataFrame):
        df1 = remove_unnamed_columns(index_dict)
        for column in df1.columns:
            if column in data.columns:
                s1 = data[column]
                s2 = s1.loc[df1[column].dropna().values]
                final_list.append(s2)  # Append the new DataFrame to final_list
    else:
        raise TypeError("Input parameter must be a dict or a pandas DataFrame.")
    
    final_df = pd.concat(final_list, axis=1)  # Get the original data
    
    # Filter by peak area
    final_df[final_df < area_threshold] = np.nan
    index1 = final_df.dropna(how='all', axis=0).index.values
    final_df = pd.concat(final_list, axis=1)  # Get the original data again
    final_df = final_df.loc[index1]
    
    # Filter by mz and rt
    final_df.loc[:, 'index'] = final_df.index
    final_df.loc[:, 'rt'] = final_df['index'].apply(lambda x: eval(x.split('_')[0]))
    final_df.loc[:, 'mz'] = final_df['index'].apply(lambda x: eval(x.split('_')[1]))
    final_df = final_df[(final_df.mz > mz_range[0]) & (final_df.mz < mz_range[1]) & (final_df.rt > rt_range[0]) & (
            final_df.rt < rt_range[1])]
    final_df = final_df.drop(columns=['index', 'rt', 'mz']).fillna(1)
    return final_df


def map_values(df, range_dict):
    """
    Map the values in a given pandas DataFrame to new values based on the ranges specified in a dictionary.

    Args:
        df: pandas DataFrame
            The DataFrame to be mapped
        range_dict: dictionary
            A dictionary specifying the ranges and their corresponding new values. The keys are the lower bounds of the ranges,
            and the values are the new values to map the numbers within the range to. e.g., range_dict = {500: 1, 5000: 2, 20000: 3, 50000: 4, 100000: 5}

    Returns:

        The same pandas DataFrame with the values replaced.


    """
    
    def get_range(x):
        """
        Helper function to get the range that a number belongs to.
        """
        for k, v in range_dict.items():
            if x <= k:
                return v
        return v  # If the value is greater than all the keys in the dictionary, map it to the final value
    
    # Apply the get_range function to the DataFrame and replace the original values
    for i in range(len(df.columns)):
        df.iloc[:, i] = df.iloc[:, i].apply(get_range)
    
    return df


def omics_cmp_numbers(path, names, mode='pos'):
    """
    Use names (index) to collect the information about unique compounds numbers.

    Args:
        files: files to count compounds' numbers
        names: files series name
        mode: 'pos' or 'neg'

    returns:
        dataframe with number and error

    """
    files = glob(os.path.join(path, '*.xlsx'))
    
    numbers = {}
    numbers_error = {}
    
    for name in names:
        print(f'Processing {name}')
        files1 = [file for file in files if name in file]
        triplicates = []
        for file in files1:
            file_name = os.path.basename(file)
            print(f'    * reading file: {file_name}')
            df = pd.read_excel(file)
            triplicates.append(len(df))
        average = np.average(np.array(triplicates))
        error = np.std(np.array(triplicates))
        numbers[name] = int(average)
        numbers_error[name] = int(error)
    
    # concat data
    numbers_s = pd.Series(numbers)
    numbers_error_s = pd.Series(numbers_error)
    
    num_info = pd.concat([numbers_s, numbers_error_s], axis=1)
    
    if mode == 'pos':
        num_info.columns = ['pos_num', 'pos_num_error']
    else:
        num_info.columns = ['neg_num', 'neg_num_error']
    
    return num_info


def omics_cmp_total_area(files, names, mode='pos', column_name='area'):
    """
    Use names (index) to collect the information about unique compounds' total area.
    Args:
        files: files to count compounds' numbers
        names: files series name
        mode: 'pos' or 'neg'
        columns_name: target column's name (default:'area')
    :return: dataframe with number and error
    """
    area_info = {}
    area_error_info = {}
    for name in names:
        print(f'Processing {name}')
        files1 = [file for file in files if name in file]
        triplicates = []
        for file in files1:
            file_name = os.path.basename(file)
            print(f'    * reading file: {file_name}')
            df = pd.read_excel(file)
            total_area = df[column_name].sum()
            triplicates.append(total_area)
        
        average = np.average(np.array(triplicates))
        error = np.std(np.array(triplicates))
        area_info[name] = int(average)
        area_error_info[name] = int(error)
    
    area_info_s = pd.Series(area_info)
    area_error_info_s = pd.Series(area_error_info)
    final_area_info = pd.concat([area_info_s, area_error_info_s], axis=1)
    if mode == 'pos':
        final_area_info.columns = ['pos_total_area', 'pos_total_area_error']
    else:
        final_area_info.columns = ['neg_total_area', 'neg_total_area_error']
    
    return final_area_info


def omics_correcting_areas(path_for_final_area, path_for_files, istd_info, normalized_area):
    """
    Corrects the peak area values of metabolites in each sample file using internal standard normalization.

    Args:
        path_for_final_area (str): The path to the folder containing the final area files.
        path_for_files (str): The path to the folder containing the sample files.
        istd_info (list[float]): The retention time and m/z values of the internal standard as a list. e.g., [4.35, 212.1183]
        normalized_area (float): The area value of the internal standard used for normalization.

    Returns:
        None. Saves the corrected sample files in the same folder with the suffix '_istd_corrected'.

    """
    # Get file paths
    final_area_files = glob(os.path.join(path_for_final_area, '*.xlsx'))
    files = glob(os.path.join(path_for_files, '*.xlsx'))
    rt, mz = istd_info
    
    # Extract retention time and m/z values for internal standard
    final_area_df1 = pd.read_excel(final_area_files[0])
    columns_name = final_area_df1.columns
    final_area_df1 = final_area_df1.sort_values(by=columns_name[-1], ascending=False)
    final_area_df1['rt'] = final_area_df1['Unnamed: 0'].apply(lambda x: eval(x.split('_')[0]))
    final_area_df1['mz'] = final_area_df1['Unnamed: 0'].apply(lambda x: eval(x.split('_')[1]))
    istd_index = final_area_df1[(final_area_df1.rt > rt - 0.1) &
                                (final_area_df1.rt < rt + 0.1) &
                                (final_area_df1.mz < mz + 0.015) &
                                (final_area_df1.mz > mz - 0.015)]['Unnamed: 0'].values[0]
    print(f'The istd_index area: {istd_index}')
    
    # 第一步：处理final_area获得所有样品的峰面积
    istd_all = []
    for file in tqdm(final_area_files, desc='Reading final area files'):
        df = pd.read_excel(file, index_col='Unnamed: 0')
        s = df.loc[istd_index]
        istd_all.append(s)
    corr = pd.concat(istd_all)
    
    # 第二步：处理files
    for name in tqdm(corr.index):
        file = [file for file in files if name in file]
        if len(file) != 0:
            df = pd.read_excel(file[0])
            coeff = corr.loc[name] / normalized_area
            df.loc[:, 'area_corr'] = (df['area'] / coeff).astype(int)
            df = df[df.intensity > 500]
            df = df[df.area > 500]
            df = df.sort_values(by='intensity', ascending=False).reset_index(drop=True)
            df = remove_unnamed_columns(df)
            df.to_excel(file[0].replace('.xlsx', '_istd_corrected.xlsx'))


def check_istd_quality(istd_info, final_area_df):
    """
    Locates the internal standard in the final area dataframe and returns the final areas.

    Args:
        istd_info: A list of two values containing the retention time and mz values of the internal standard.
        final_area_df: A pandas dataframe containing final peak areas.

    Returns:
        A pandas series containing the file names and their corresponding final peak areas.
    """
    
    rt, mz = istd_info
    
    # Locate the internal standard index
    final_area_df.loc[:, 'new_index'] = final_area_df.index.values
    final_area_df.loc[:, 'rt'] = final_area_df['new_index'].apply(lambda x: eval(x.split('_')[0]))
    final_area_df.loc[:, 'mz'] = final_area_df['new_index'].apply(lambda x: eval(x.split('_')[1]))
    istd_index_df = final_area_df[(final_area_df['rt'] > rt - 0.1) &
                                  (final_area_df['rt'] < rt + 0.1) &
                                  (final_area_df['mz'] < mz + 0.015) &
                                  (final_area_df['mz'] > mz - 0.015)]['new_index']
    if len(istd_index_df) == 0:
        print(r'Error: istd not found')
        return None
    else:
        istd_index = istd_index_df.values[0]
        print(f'The istd_index: {istd_index}')
        final_area_df = final_area_df.drop(columns=['new_index', 'rt', 'mz'])
        result = final_area_df.loc[istd_index]
        return result


def KMD_cal(exact_mass, functional_group):
    """
    Calculate the Kendrick mass defect (KMD) of a given mass with respect to a specified functional group.

    Parameters:
    - exact_mass (float): The exact mass of the compound of interest.
    - functional_group (str): The functional group used as reference for the Kendrick mass scaling. Common choices are "CH2", "CF2", "Br", etc.

    Returns:
    - float: The Kendrick mass defect value.

    Raises:
    - ValueError: If the provided functional group is not in the known list of functional groups.

    Example:
    >>> kendrick_mass_defect(300.0932, "CF2")
    -0.11260158730158615

    Note:
    The function uses a predefined list of exact masses for functional groups. To support additional functional groups, they need to be added to the `functional_group_masses` dictionary.
    """
    
    # Dictionary of exact masses for common functional groups
    functional_group_masses = {
        "CH2": 14.01565,
        "CF2": 49.996806,
        "Br": 77.911061,
        # Add other functional groups here as needed
    }
    
    # Check if the functional group is in our dictionary
    if functional_group not in functional_group_masses:
        raise ValueError(f"Unknown functional group: {functional_group}")
    
    # Calculate Kendrick mass
    kendrick_mass = exact_mass * round(functional_group_masses[functional_group], 0) / functional_group_masses[
        functional_group]
    
    # Calculate Kendrick mass defect
    kmd = kendrick_mass - np.floor(kendrick_mass)
    
    return kmd


"""
========================================================================================================
4. FT-ICRMS data processing
========================================================================================================
"""


def draw_Van_Krevelen_diagrams(result, name='', path=None, dpi=300):
    """
    Draws Van Krevelen diagrams to visually classify and compare the elemental composition
    of organic compounds based on their hydrogen-to-carbon (H/C) and oxygen-to-carbon (O/C) ratios.
    This function differentiates between compounds containing only carbon, hydrogen, and oxygen (CHO),
    those also containing nitrogen (CHON), sulfur (CHOS), or both (CHONS), and plots them on the diagram
    with distinct markers. Additionally, it delineates stoichiometric regions associated with different
    compound classes such as lipids, proteins, lignins, carbohydrates, etc., on the diagram.

    Parameters:
        result (Pandas DataFrame): A DataFrame containing the columns 'C', 'H', 'O', 'N', and 'S'
                                   which represent the count of each element in the compounds. Must not
                                   contain NaN values in the 'C' column.
        name (str, optional): Title of the plot. Defaults to an empty string.
        path (str, optional): File path where the plot image will be saved. If None, the plot is shown
                              using plt.show(). Defaults to None.
        dpi (int, optional): The resolution of the saved plot image in dots per inch. Defaults to 300.

    Returns:
        None. Displays the Van Krevelen diagram or saves it as a file, depending on the 'path' parameter.

    Raises:
        ValueError: If the 'result' DataFrame does not contain the required columns ('C', 'H', 'O', 'N', 'S').

    Example usage:
        draw_Van_Krevelen_diagrams(result_df, name='Sample Van Krevelen Diagram', path='diagram.png', dpi=300)

    Note:
        - This function is specifically designed for analyzing and visualizing elemental compositions
          in organic geochemistry and may not be applicable for other types of data.
        - Ensure the 'result' DataFrame is preprocessed to remove NaN values in 'C' column and contains
          the necessary elemental columns before calling this function.
    """
    
    # 数据处理
    result1 = result[~result['C'].isna()]
    CHO = result1[(result1['N'] == 0) & (result1['S'] == 0)]
    CHO_OC = CHO['O/C']
    CHO_HC = CHO['H/C']
    CHON = result1[(result1['N'] != 0) & (result1['S'] == 0)]
    CHON_OC = CHON['O/C']
    CHON_HC = CHON['H/C']
    CHOS = result1[(result1['N'] == 0) & (result1['S'] != 0)]
    CHOS_OC = CHOS['O/C']
    CHOS_HC = CHOS['H/C']
    CHONS = result1[(result1['N'] != 0) & (result1['S'] != 0)]
    CHONS_OC = CHONS['O/C']
    CHONS_HC = CHONS['H/C']
    
    # Plotting the image
    fig, ax = plt.subplots()
    
    ax.scatter(CHO_OC, CHO_HC, color='#E64B35FF', s=15, marker='o', alpha=0.8, label='CHO')
    ax.scatter(CHON_OC, CHON_HC, color='#00A087FF', s=15, marker='^', alpha=0.8, label='CHON')
    ax.scatter(CHOS_OC, CHOS_HC, color='#F7C530FF', s=15, marker='s', alpha=0.8, edgecolor=None, label='CHOS')
    ax.scatter(CHONS_OC, CHONS_HC, color='#3C5488FF', s=15, marker='*', alpha=0.8, label='CHONS')
    
    ax.set_title(name)
    ax.set_xlabel('O/C', size=15)
    ax.set_ylabel('H/C', size=15)
    # Defining the stoichiometric ranges for each compound class
    regions = {
        'Lipids': {'H/C': (1.5, 2.0), 'O/C': (0, 0.3)},
        'Aliphatic/proteins': {'H/C': (1.5, 2.2), 'O/C': (0.3, 0.67)},
        'Lignins/CRAM-like structures': {'H/C': (0.7, 1.5), 'O/C': (0.1, 0.67)},
        'Carbohydrates': {'H/C': (1.5, 2.4), 'O/C': (0.67, 1.2)},
        'Unsaturated hydrocarbons': {'H/C': (0.7, 1.5), 'O/C': (0, 0.1)},
        'Aromatic structures': {'H/C': (0.2, 0.7), 'O/C': (0, 0.67)},
        'Tannins': {'H/C': (0.6, 1.5), 'O/C': (0.67, 1.0)}
    }
    
    # Add rectangles for each region
    for region, boundaries in regions.items():
        h_c_range = boundaries['H/C']
        o_c_range = boundaries['O/C']
        
        # The rectangle dimensions and location
        width = o_c_range[1] - o_c_range[0]
        height = h_c_range[1] - h_c_range[0]
        lower_left = (o_c_range[0], h_c_range[0])
        
        # Create a rectangle patch and add it to the axes
        rect = patches.Rectangle(lower_left, width, height, linewidth=1, edgecolor='black', facecolor='none')
        ax.add_patch(rect)
    
    label_coordinates = {
        'Lipids': (0.15, 1.75),
        'Aliphatic/proteins': (0.51, 2),
        'Lignins/CRAM-like structures': (0.95, 0.32),
        'Carbohydrates': (0.93, 1.75),
        'Unsaturated hydrocarbons': (0.32, 2.35),
        'Aromatic structures': (0.33, 0.35),
        'Tannins': (0.89, 1.3)
    }
    
    for region, boundaries in regions.items():
        label_coord = label_coordinates[region]
        if region == 'Lignins/CRAM-like structures':
            region = 'Lignins/CRAM-like\n structures'
        ax.text(label_coord[0], label_coord[1], region,
                horizontalalignment='center', verticalalignment='center',
                fontsize=12, color='black', bbox=dict(facecolor='white', alpha=0.45, edgecolor='none'))
    
    # 添加箭头
    x_start = 0.05
    y_start = 2.2
    x_end = 0.05
    y_end = 1.4
    # Calculate the length of the arrow
    x_length = x_end - x_start
    y_length = y_end - y_start
    # Add an arrow to the figure
    ax.arrow(x_start, y_start, x_length, y_length, head_width=0.02, head_length=0.15, fc='blue', ec='blue', lw=0.5)
    
    x_start = 0.6
    y_start = 0.45
    x_end = 0.6
    y_end = 1
    # Calculate the length of the arrow
    x_length = x_end - x_start
    y_length = y_end - y_start
    # Add an arrow to the figure
    ax.arrow(x_start, y_start, x_length, y_length, head_width=0.02, head_length=0.15, fc='blue', ec='blue', lw=0.5)
    x_start = 0.6
    y_start = 0.45
    x_end = 0.74
    y_end = 0.45
    # Calculate the length of the arrow
    x_length = x_end - x_start
    y_length = y_end - y_start
    # Add an arrow to the figure
    ax.arrow(x_start, y_start, x_length, y_length, head_width=0, head_length=0, fc='blue', ec='blue', lw=0.8)
    
    plt.xlim(0, 1.2)
    plt.ylim(0, 2.75)
    plt.tick_params(labelsize=12)
    plt.legend()
    if path is None:
        plt.show()
    else:
        plt.savefig(path, dpi=dpi)
        plt.close('All')


def FT_ICRMS_process(data_input, mode='neg', atoms=['C', 'H', 'O', 'N', 'S'],
                     atom_n=[[5, 60], [0, 150], [0, 50], [0, 10], [0, 3]], mz_error=1, mz_range=[150, 1000],
                     isotope_i_error=10, peak_threshold=15, peak_width=2):
    """
  This function processes FT-ICR-MS data to identify potential elemental formulas corresponding to the peaks in the raw mass spectrum.

  Args:
      data_input: Either a list containing [mzs, intensities] or a string representing a file path to .mzML or .xy data files.
      mode: 'pos' for positive mode electrospray ionization or 'neg' for negative mode.
          (default: 'neg')
      atoms: A list of elements to consider for formula generation. (default: ['C', 'H', 'O', 'N', 'S'])
      atom_n: A list of lists defining the allowed number of atoms for each element in `atoms`.
          Each inner list contains the minimum and maximum number of atoms allowed for the corresponding element.
      mz_error: The allowed mass error in ppm for peak matching. (default: 1)
      mz_range: The m/z range (in Da) to consider for formula generation. (default: [150, 1000])
      isotope_i_error: The allowed percentage error for isotope peak intensity matching. (default: 10)
      peak_threshold: The minimum intensity threshold for peak detection. (default: 15)
      peak_width: The peak width (m/z) used for peak detection. (default: 2)

  Returns:
      A Pandas DataFrame containing the following information for each peak:
          - obs_mass: The observed m/z value of the peak.
          - intensity: The intensity of the peak.
          - exact_mass: The calculated exact mass of the most likely formula.
          - formula: The most likely elemental formula for the peak.
          - hetero_atom_num: The number of heteroatoms (elements other than C, H, O, N) in the formula.
          - mz_error: The mass error (ppm) of the most likely formula.
          - mz_error_abs: The absolute value of the mass error.
          - isotope_peak (optional): 'yes' if the peak is identified as an isotope peak, 'no' otherwise.
          - iso_ratio_error(%) (optional): The percentage difference between the observed and expected isotope peak ratio.
    """
    try:
        if isinstance(data_input, list):
            mzs, intensities = data_input
        elif isinstance(data_input, str):
            if data_input.endswith('.mzML'):
                ms1, ms2 = sep_scans(data_input, 'Bruker')
                mzs = ms1[0].mz
                intensities = ms1[0].i
            elif data_input.endswith('.xy'):
                result = pd.read_csv(data_input, delimiter=' ')
                result.columns = ['mz', 'intensity']
                mzs = result['mz'].values
                intensities = result['intensity'].values
            else:
                raise ValueError("Unsupported data input format.")
        else:
            raise ValueError("Data input is neither a list nor a supported file path.")
    except ValueError as e:
        print(e)
    
    background = np.mean(intensities) * 2.5
    peak_idx, right, left = peak_finding(list(intensities), threshold=peak_threshold, width=peak_width)
    target_mzs, target_intensities = mzs[peak_idx], intensities[peak_idx]
    
    all_atoms = atoms  # 先存一个，避免被改
    
    # Function to generate chemical formula for a given row
    def generate_formula(row):
        formula = ''.join([f"{el}{int(row[el]) if row[el] > 1 else ''}" for el in atoms if row[el] > 0])
        return formula
    
    atom_mass_table1 = pd.Series(
        data={'C': 12.000000, 'Ciso': 13.003355, 'N': 14.003074, 'Niso': 15.000109, 'O': 15.994915, 'H': 1.007825,
              'Oiso': 17.999159, 'F': 18.998403, 'K': 38.963708, 'P': 30.973763, 'Cl': 34.968853,
              'S': 31.972072, 'Siso': 33.967868, 'Br': 78.918336, 'Na': 22.989770, 'Si': 27.976928,
              'Fe': 55.934939, 'Se': 79.916521, 'As': 74.921596, 'I': 126.904477, 'D': 2.014102,
              'Co': 58.933198, 'Au': 196.966560, 'B': 11.009305, 'e': 0.0005486
              })
    
    # step 1. 剥离[C, H, O,N]
    
    # Define the elements to be extracted for the first part
    elements_part1 = ['C', 'H', 'O', 'N']
    
    # Splitting the input into two parts based on the specified elements
    atoms1, atom_n1 = zip(*[(atom, ranges) for atom, ranges in zip(atoms, atom_n) if atom in elements_part1])
    atoms2, atom_n2 = zip(*[(atom, ranges) for atom, ranges in zip(atoms, atom_n) if atom not in elements_part1])
    
    # Converting tuples back to lists (for consistency with the input format)
    atoms1, atom_n1 = list(atoms1), list(atom_n1)
    atoms2, atom_n2 = list(atoms2), list(atom_n2)
    
    # step 2. 获得所有的组合
    
    atoms = atoms1
    atom_n = atom_n1
    # sort element list
    elements_sorted_list = ['C', 'H', 'O', 'N', 'S', 'Cl', 'Br', 'P', 'F', 'K', 'Na', 'Ciso', 'D', 'Oiso', 'Niso',
                            'Siso']
    
    atom_indices = {atom: i for i, atom in enumerate(atoms)}
    sorted_atoms_and_ranges = sorted(
        [(atom, atom_n[atom_indices[atom]]) for atom in atoms if atom in elements_sorted_list],
        key=lambda x: elements_sorted_list.index(x[0]))
    atoms, atom_n = zip(*sorted_atoms_and_ranges)
    # generate ranges
    ranges = [range(n[0], n[1] + 1) for n in atom_n]
    # generate patterns_list, this process is very fast
    patterns = np.array(list(itertools.product(*ranges)))
    
    # step3. 去除不太可能的
    # 条件1: H,O,N数量必须≥C
    # 条件2: H,O,N数量必须<2n+2 C
    # 条件3：N_count <= 1.3 * C_coun
    # 条件4：O_count <= 1.3 * C_coun
    # 条件5: O_count <= 1.2 * C_count
    # 条件6: H_count >= C_count + N_count/2 + O_count/2
    patterns1 = patterns[(patterns[:, 0] <= patterns[:, 1] + patterns[:, 2] + patterns[:, 3]) & (
            2 * patterns[:, 0] + 2 >= patterns[:, 1] + patterns[:, 2] + patterns[:, 3] * 2) & (
                                 1.3 * patterns[:, 0] >= patterns[:, 3]) & (1.2 * patterns[:, 0] >= patterns[:, 2])]
    
    # step 4. 添加剩下的
    atoms = atoms2
    atom_n = atom_n2
    # sort element list
    elements_sorted_list = ['C', 'H', 'O', 'N', 'S', 'Cl', 'Br', 'P', 'F', 'K', 'Na', 'Ciso', 'D', 'Oiso', 'Niso',
                            'Siso']
    
    atom_indices = {atom: i for i, atom in enumerate(atoms)}
    sorted_atoms_and_ranges = sorted(
        [(atom, atom_n[atom_indices[atom]]) for atom in atoms if atom in elements_sorted_list],
        key=lambda x: elements_sorted_list.index(x[0]))
    atoms, atom_n = zip(*sorted_atoms_and_ranges)
    # generate ranges
    ranges = [range(n[0], n[1] + 1) for n in atom_n]
    # generate patterns_list, this process is very fast
    patterns2 = np.array(list(itertools.product(*ranges)))
    
    # Step 5:整合在一起,生成最终的final_pattern
    all_pattern = []
    for pattern in patterns2:
        new_array = np.hstack((patterns1, pattern.reshape(1, -1).repeat(len(patterns1), axis=0)))
        all_pattern.append(new_array)
    final_pattern = np.vstack(all_pattern)
    
    # Step 6: 计算所有的值
    mzs = 0
    atoms = atoms1 + atoms2
    for i in range(len(atoms)):
        mzs += final_pattern[:, i] * atom_mass_table1[atoms[i]]
    mzs = mzs + atom_mass_table1['e'] if mode == 'neg' else mzs - atom_mass_table1['e']  # mzs 特指所有可能的质量
    
    # Step 7: 继续精简数据
    mz_range_idx = np.where(mzs[(mzs > mz_range[0]) & (mzs < mz_range[1])])
    final_pattern1 = final_pattern[mz_range_idx]
    mzs1 = mzs[mz_range_idx]
    
    # step 8: 开始做计算
    df_all = []
    hetero_atoms = [atom for atom in atoms if atom not in ['C', 'H', 'O', 'N']]
    for i in tqdm(range(len(target_mzs)), desc='Calculating the formula', leave=True):
        target_mz = target_mzs[i]
        target_intensity = target_intensities[i]
        index = np.where((mzs1 > target_mz * (1 - mz_error * 1e-6)) & (mzs1 < target_mz * (1 + mz_error * 1e-6)))
        if len(index[0]) == 0:
            s1 = pd.Series({'obs_mass': target_mz, 'intensity': target_intensity})
            df_all.append(s1)
        else:
            arr1 = final_pattern1[index]
            exact_mass = mzs1[index]
            # Reshape the array to make it 2-dimensional
            arr_2d = arr1.reshape(arr1.shape[0], -1)
            # Creating the DataFrame
            df = pd.DataFrame(arr_2d, columns=atoms)
            df.loc[:, 'obs_mass'] = target_mz
            df.loc[:, 'exact_mass'] = exact_mass
            df.loc[:, 'intensity'] = target_intensity
            df.loc[:, 'hetero_atom_num'] = df[hetero_atoms].sum(axis=1)
            df.loc[:, 'mz_error'] = round((df['exact_mass'] - target_mz) / target_mz * 1e6, 2)
            df.loc[:, 'mz_error_abs'] = df['mz_error'].abs()
            df.loc[:, 'formula'] = df.apply(generate_formula, axis=1)
            df1 = df.sort_values(by=['hetero_atom_num', 'mz_error_abs']).reset_index(drop=True)
            df_all.append(df1.iloc[0])
    result = pd.concat(df_all, axis=1).T.sort_values(by='intensity', ascending=False).reset_index(drop=True)
    
    # 开始处理同位素
    column_names = [i for i in result.columns if i not in ['obs_mass', 'intensity', 'exact_mass',
                                                           'mz_error', 'mz_error_abs']]
    isotope_idx = []
    isotope_df = []
    for i in tqdm(range(len(result)), desc='Processing isotope', leave=True):
        formula = result.loc[i, 'formula']
        obs_mz = result.loc[i, 'obs_mass']
        obs_intensity = result.loc[i, 'intensity']
        basic_info = result.loc[i, column_names].values  # 为了给后面匹配到的赋值
        if type(formula) is str:  # 如果有分子式，去找它的同位素
            # 先生成其同位素信息
            isotopes, distribution = formula_to_distribution(formula, adducts='-' if mode == 'neg' else '+', num=5)
            for j, iso_mz in enumerate(isotopes):
                if abs(1e6 * (obs_mz - iso_mz) / iso_mz) < 1:
                    pass
                else:
                    result1 = result[(result['obs_mass'] < iso_mz * (1 + mz_error * 1e-6)) & (
                            result['obs_mass'] > iso_mz * (1 - mz_error * 1e-6))].copy()
                    
                    if len(result1) != 0:
                        iso_intensity = result1['intensity'].values[0]  # isotope的intensity
                        iso_ratio = round(iso_intensity / obs_intensity * 100, 1)
                        iso_ratio_error = iso_ratio - distribution[j]  # 获得同位素峰响应的偏差
                        obs_mass_iso_candi = result1['obs_mass'].values[0]
                        idx1 = result1.index.values
                        result1.loc[:, column_names] = basic_info  # 先填充其他信息
                        result1.loc[idx1, 'exact_mass'] = iso_mz
                        real_mass_error = round((iso_mz - obs_mass_iso_candi) / obs_mass_iso_candi * 1e6, 2)
                        result1.loc[idx1, 'mz_error'] = real_mass_error
                        result1.loc[idx1, 'mz_error_abs'] = abs(real_mass_error)
                        result1.loc[idx1, 'isotope_peak'] = 'yes'
                        result1.loc[idx1, 'iso_ratio_error(%)'] = iso_ratio_error
                        # 搜集信息
                        if iso_ratio_error < isotope_i_error:
                            if idx1 not in isotope_idx:
                                isotope_idx.append(idx1)
                                isotope_df.append(result1)
    result_remaining = result.drop(index=np.hstack(isotope_idx), axis=0)
    isotope_result = pd.concat(isotope_df)
    final_result = pd.concat([result_remaining, isotope_result]).sort_index()
    
    # 计算其他参数
    final_result['S/N'] = (final_result['intensity'] / background).astype(float).round(2)
    final_result['O/C'] = (final_result['O'] / final_result['C']).astype(float).round(3)
    if mode == 'pos':
        x = 1
    elif mode == 'neg':
        x = -1
    else:
        x = 1
        print('mode set as positive')
    final_result['H/C'] = ((final_result['H'] - x) / final_result['C']).astype(float).round(3)
    final_result['DBE'] = 1 + 0.5 * (2 * final_result['C'] - (final_result['H'] - x) + final_result['N'])
    final_result['NOSC'] = 4 - (4 * final_result['C'] + (final_result['H'] - x)
                                - 3 * final_result['N'] - 2 * final_result['O'] - 2 * final_result['S']) / final_result[
                               'C']
    final_result['NOSC'] = final_result['NOSC'].astype(float).round(3)
    AI_denominator = final_result['C'] - 0.5 * final_result['O'] - final_result['S'] - final_result['N']
    AI_numerator = 1 + final_result['C'] - 0.5 * final_result['O'] - final_result['S'] - 0.5 * (final_result['H'] - x)
    AI = AI_numerator / (AI_denominator.sort_values() + 1 * 1e-6)
    final_result['AI'] = AI
    
    return final_result


"""
========================================================================================================
5. Ion mobility data processing
========================================================================================================
"""


def first_step_for_IMS(path, mz_range=[50, 2000], company='Waters', profile=True, lock_mass=556.2771, ms2_analysis=True,
                       frag_rt_error=0.05, dft_error=0.5,
                       split_n=20, long_rt_split_n=5, rt_overlap=1, mz_overlap=1, noise_threshold=0, threshold=15,
                       i_threshold=200,
                       SN_threshold=3, rt_error_alignment=0.1, mz_error_alignment=0.015, sat_intensity=False):
    """
    if select IMS, make sure you have install pyopenms and import properly：from pyopenms import MSExperiment, MzMLFile
    """
    
    files = glob(os.path.join(path, '*.mzML'))
    for file in files:
        # 1. 先分离，获得ms1，ms2和lockspray
        ms1, ms2, lockspray = sep_scans(file, company, tool='pyopenms')
        # 2. 获得矫正数据factor
        mz_corr_factors = []
        for scan in lockspray:
            mz, intensity = scan.get_peaks()
            s = pd.Series(data=intensity, index=mz)
            s1 = s.loc[(s.index > lock_mass - 0.2) & (s.index < lock_mass + 0.2)]
            lockmass_obs = s1.idxmax()
            factor = lock_mass / lockmass_obs
            mz_corr_factors.append(factor)
        factor = np.median(mz_corr_factors)
        
        # 3. 开始处理ms1
        peak_all1 = peak_picking_ion_mobility_DIA1(ms1, mz_range=mz_range, profile=profile, split_n=split_n,
                                                   long_rt_split_n=long_rt_split_n,
                                                   rt_overlap=rt_overlap, mz_overlap=mz_overlap,
                                                   noise_threshold=noise_threshold, threshold=threshold,
                                                   i_threshold=i_threshold, SN_threshold=SN_threshold,
                                                   rt_error_alignment=rt_error_alignment,
                                                   mz_error_alignment=mz_error_alignment, factor=factor)
        
        # 4. 开始处理ms2
        if (len(ms2) == 0) | (ms2_analysis == False):
            pass
        else:
            peak_all2 = peak_picking_ion_mobility_DIA1(ms2, mz_range=mz_range, profile=profile, split_n=split_n,
                                                       long_rt_split_n=long_rt_split_n,
                                                       rt_overlap=rt_overlap, mz_overlap=mz_overlap,
                                                       noise_threshold=noise_threshold, threshold=threshold,
                                                       i_threshold=i_threshold, SN_threshold=SN_threshold,
                                                       rt_error_alignment=rt_error_alignment,
                                                       mz_error_alignment=mz_error_alignment, factor=factor)
            
            for i in tqdm(range(len(peak_all1))):
                rt, mz, dft = peak_all1.loc[i, ['rt', 'mz', 'Drift Time']]
                frag_df = peak_all2[(peak_all2['rt'] > rt - frag_rt_error) & (peak_all2['rt'] < rt + frag_rt_error) & (
                        peak_all2['mz'] < mz + 1)]
                mz, intensities = frag_df['mz'].values, frag_df['intensity'].values
                s_frag = pd.Series(data=intensities, index=mz, name=dft).sort_index(ascending=False)
                d_frag = s_frag.to_dict()
                peak_all1.loc[i, 'ms2_spec'] = str(s_frag)
                peak_all1.loc[i, 'ms2_spec_dict'] = str(d_frag)
        peak_all1.to_excel(file.replace('.mzML', '.xlsx'))


def peak_picking_ion_mobility_DIA1(ms1, mz_range=[50, 2000], profile=True, split_n=20, long_rt_split_n=5, peak_width=1,
                                   rt_overlap=1, mz_overlap=1, noise_threshold=0, threshold=15, i_threshold=200,
                                   SN_threshold=3,
                                   rt_error_alignment=0.1, mz_error_alignment=0.015, factor=1, sat_intensity=False):
    # using the same factor
    
    # 1. put the information of mz, rt, intensity and ion mobility in one dict
    
    # Initialize an empty defaultdict of lists
    dict_name = defaultdict(list)
    
    # Iterate over each scan in ms1
    for scan in tqdm(ms1, desc='Reading each scan'):
        # Create a pandas Series for the current scan
        mzs, intensities = scan.get_peaks()
        mzs = mzs * factor
        drift_time = round(scan.getDriftTime(), 3)  # Assuming drift time is available
        s = pd.Series(index=mzs, data=intensities, name=drift_time)
        # Append the series to the list associated with its retention time in the dictionary
        rt = round(scan.getRT() / 60, 3)
        if len(s) != 0:
            dict_name[rt].append(s)
    
    # 2. combine all data if their retention is the same
    
    result = []
    for rt, series_list in tqdm(dict_name.items(), desc='Combine all drift data'):
        combined_series = pd.concat(series_list).groupby(level=0).sum()
        combined_series.name = rt
        result.append(combined_series)
    
    # 3. convert profile to centroid
    if profile is True:
        centroid_data = []
        for scan in tqdm(result, desc='Convert to centroid'):
            scan1 = ms_to_centroid(scan)
            centroid_data.append(scan1)
    else:
        centroid_data = result
    
    # 4. 横向分割
    
    # Calculate the length of each part
    total_spectra = len(centroid_data)
    part_length = total_spectra // long_rt_split_n
    overlap_spectra = int(rt_overlap / (centroid_data[1].name - centroid_data[
        0].name))  # calculate the number of spectra in 1 minute of retention time
    
    # Split the list into parts
    parts = []
    for i in range(long_rt_split_n):
        start_index = i * part_length - overlap_spectra
        start_index = max(start_index, 0)  # set start index to 0 if it is less than 0
        end_index = (i + 1) * part_length + overlap_spectra
        part = centroid_data[start_index:end_index]
        parts.append(part)
    
    # Add any remaining spectra to the last part
    if end_index < total_spectra:
        last_part = ms1[end_index:]
        parts[-1] += last_part
    
    # 5. 众向分割
    
    if long_rt_split_n == 1:
        peak_all = split_peak_picking2(centroid_data, mz_range=mz_range, i_threshold=i_threshold, peak_width=peak_width,
                                       SN_threshold=SN_threshold, split_n=split_n)
    else:
        # Calculate the length of each part
        total_spectra = len(centroid_data)
        part_length = total_spectra // long_rt_split_n
        overlap_spectra = int(rt_overlap / (centroid_data[1].name - centroid_data[
            0].name))  # calculate the number of spectra in 1 minute of retention time
        # Split the list into parts
        parts = []
        for i in range(long_rt_split_n):
            start_index = i * part_length - overlap_spectra
            start_index = max(start_index, 0)  # set start index to 0 if it is less than 0
            end_index = (i + 1) * part_length + overlap_spectra
            part = centroid_data[start_index:end_index]
            parts.append(part)
        
        # Add any remaining spectra to the last part
        if end_index < total_spectra:
            last_part = centroid_data[end_index:]
            parts[-1] += last_part
    
    parts1 = [centroid_data[i * part_length:(i + 1) * part_length] for i in
              range(long_rt_split_n)]  # find the cut point of the retention time.
    ranges = []
    for i, part in enumerate(parts1):
        rt_start = part[0].name
        rt_end = part[-1].name
        range1 = [rt_start, rt_end]
        ranges.append(range1)
    # to make sure there is no gap between each list.
    my_list = ranges
    ranges = [[my_list[i][0], my_list[i + 1][0]] for i in range(len(my_list) - 1)] + [my_list[-1]]
    
    # start to do peak picking for each part
    peak_list_all = []
    for n, part in enumerate(parts):
        peak_all = split_peak_picking2(part, mz_range=mz_range, i_threshold=i_threshold, peak_width=peak_width,
                                       SN_threshold=SN_threshold, split_n=split_n)
        peak_all = peak_all[(peak_all['rt'] > ranges[n][0]) & (peak_all['rt'] <= ranges[n][1])]
        peak_list_all.append(peak_all)
    
    peak_all = pd.concat(peak_list_all).reset_index(drop=True)
    
    # 对peak all进行排序
    peak_all = peak_all.sort_values(by='intensity', ascending=False).reset_index(drop=True)
    
    # 开始处理淌度数据
    # 1. 找到所有的RTs
    scan_times = []
    for k, v in dict_name.items():
        scan_times.append(k)
    
    # 2找到特定的rt，mz，并找到最高点作为漂移时间
    for i in tqdm(range(len(peak_all)), desc='Collecting drift time'):
        rt, mz = peak_all.loc[i, ['rt', 'mz']]
        rt_index = np.argmin(abs(scan_times - rt))
        # 2. 找到特定的scans，去看drift time
        target_rt = scan_times[rt_index]
        target_rt_scans = dict_name[target_rt]
        # 3. 获得eic和time
        drift_eic = np.array(
            [scan[(scan.index > mz * (1 - 50e-6)) & (scan.index < mz * (1 + 50e-6))].sum() for scan in target_rt_scans])
        drift_times = np.array([scan.name for scan in target_rt_scans])
        peak_all.loc[i, 'Drift Time'] = drift_times[np.argmax(drift_eic)]
    return peak_all


def split_peak_picking2(data, mz_range=[50, 2000], split_n=20, mz_overlap=1, peak_width=1,
                        noise_threshold=0, threshold=15, i_threshold=200,
                        SN_threshold=3, rt_error_alignment=0.1, mz_error_alignment=0.015):
    """
    Find peaks in the orginal Series list, analyze isotope and adduct information, and return a dataframe with
    information on the peaks including retention time, m/z value, intensity, and area. Note this is used for the data processed by pyopenms.

    Args:
        ms1 (scan list): generated from sep_scans(file.mzML).
        profile: A boolean indicating whether the data is in profile mode (True) or centroid mode (False)
        split_n (int): The number of pieces to split the large dataframe.
        threshold (int): Threshold for finding peaks.
        i_threshold (int): Threshold for peak intensity.
        SN_threshold (float): Signal-to-noise threshold.
        rt_error_alignment (float, optional): Retention time error alignment threshold.
        mz_error_alignment (float, optional): m/z error alignment threshold.
        mz_overlap (float,optional): The overlap between adjacent sections of data when splitting it.
        sat_intensity: The saturation intensity refers to the point where the intensity of an m/z value becomes so high that it may no longer be accurate. In such cases, the retention time can be adjusted to bring the intensity below the saturation intensity, thereby ensuring accurate measurement of the m/z value.
    Returns:
        pandas.DataFrame: A dataframe with information on the peaks including retention time, m/z value,
        intensity, and area.
    """
    
    # 定义变量名称
    all_data = []
    for j in range(split_n):
        name = 'a' + str(j + 1)
        locals()[name] = []
    
    # 对series进行切割
    ms_increase = int(mz_range[1] / split_n)
    for i in tqdm(range(len(data)), desc='Split series:'):
        s1 = data[i]
        low, high = 50, 50 + ms_increase
        for j in range(split_n):
            name = 'a' + str(j + 1)
            locals()[name].append(
                s1[(s1.index < high + mz_overlap) & (s1.index >= low - mz_overlap) & (s1.index > noise_threshold)])
            low += ms_increase
            high += ms_increase
    for j in range(split_n):
        name = 'a' + str(j + 1)
        all_data.append(locals()[name])
    
    # 开始分段提取
    all_peak_all = []
    for data in tqdm(all_data, desc='Split peak picking process'):
        df1 = pd.concat(data, axis=1)
        df1 = df1.fillna(0)
        if len(df1) == 0:
            pass
        else:
            peak_all = peak_picking(df1, isotope_analysis=False, threshold=threshold, peak_width=peak_width,
                                    i_threshold=i_threshold, SN_threshold=SN_threshold,
                                    rt_error_alignment=rt_error_alignment,
                                    mz_error_alignment=mz_error_alignment, enable_progress_bar=False, alignment=False)
            all_peak_all.append(peak_all)
    
    peak_all = pd.concat(all_peak_all).sort_values(by='intensity', ascending=False).reset_index(drop=True)
    
    # 做alignment
    print('\r Single file alignment...', end='')
    t1 = time.time()
    peak_p = np.array([peak_all.rt.values, peak_all.mz.values]).T
    indice = [
        peak_all[
            (peak_all.mz > peak_p[i][1] - mz_error_alignment) & (peak_all.mz < peak_p[i][1] + mz_error_alignment) &
            (peak_all.rt > peak_p[i][0] - rt_error_alignment) & (
                    peak_all.rt < peak_p[i][0] + rt_error_alignment)].sort_values(by='intensity').index[-1] for
        i in range(len(peak_p))]
    indice1 = np.array(list(set(indice)))
    peak_all = peak_all.loc[indice1, :].sort_values(by='intensity', ascending=False).reset_index(drop=True)
    t2 = time.time()
    t_ = round(t2 - t1, 1)
    print(f'\r *** Single file alignment finished: {t_} s')
    
    # 对同位素丰度进行记录
    print('\r Recording isotope information...', end='')
    raw_info_rts = [data1.name for data1 in data]
    rts = peak_all.rt.values
    mzs = peak_all.mz.values
    
    rt_keys = [argmin(abs(np.array(raw_info_rts) - i)) for i in rts]  # 基于上述rt找到ms的时间索引
    
    iso_info = [str(isotope_distribution(data[rt_keys[i]], mzs[i])) for i in range(len(mzs))]
    peak_all['iso_distribution'] = iso_info
    
    t3 = time.time()
    t_ = round(t3 - t2, 1)
    print(f'\r *** Recording isotope information finished: {t_} s')
    return peak_all


"""
========================================================================================================
6. other functions
========================================================================================================
"""


def rename_files(rename_info, files):
    """
    Rename files based on a mapping of old names to new names.

    Args:
        rename_info: A pandas DataFrame with columns 'new_name' and 'old_name'. The index of the DataFrame should be
            unique new names.
        files: A list of file paths to rename.

    Returns:
        None. The files are renamed in-place.
    """
    for i in tqdm(range(len(rename_info))):
        old_name_index = rename_info.loc[i, 'old_name']
        new_name_index = rename_info.loc[i, 'new_name']
        target_files = [file for file in files if old_name_index in file]
        if len(target_files) == 0:
            pass
        else:
            for old_file_name in target_files:
                new_file_name = old_file_name.replace(old_name_index, new_name_index)
                os.rename(old_file_name, new_file_name)


def get_ms2_from_DDA(ms2, rt, mz, DDA_rt_error=0.1, DDA_mz_error=0.015):
    """
    Get MS2 spectrum from DDA data.

    Args:
        ms2 (list): List of MS2 scans generated from sep_scans.
        rt (float): Target retention time of a compound.
        mz (float): Target precursor mass of a compound.
        DDA_rt_error (float, optional): Retention time error tolerance for DDA data. Defaults to 0.1.
        DDA_mz_error (float, optional): Precursor mass error tolerance for DDA data. Defaults to 0.015.

    Returns:
        List: List of MS2 scans with retention time and precursor mass within the specified tolerance.
    """
    
    target_scans = []
    for scan in ms2:
        if (scan.scan_time[0] > rt - DDA_rt_error
        ) & (scan.scan_time[0] < rt + DDA_rt_error
        ) & (scan.selected_precursors[0]['mz'] < mz + DDA_mz_error
        ) & (scan.selected_precursors[0]['mz'] > mz - DDA_mz_error):
            target_scans.append(scan)
    return target_scans


def extract_tic(ms1):
    """
    Extract total ion current (TIC) data from MS1 scans.

    Args:
        ms1 (list): List of MS1 scans.

    Returns:
        Tuple: A tuple of two lists containing the retention times and TIC values for each scan.
    """
    
    rt = [scan.scan_time[0] for scan in ms1]
    tic = [scan.TIC for scan in ms1]
    return rt, tic


def ms_bg_removal(background, target_spec1, i_threshold=500, mz_error=0.01):
    """
    Remove background signal from a target mass spectrum (centroid).

    Args:
        background (pd.Series): Background mass spectrum.
        target_spec (pd.Series): Target mass spectrum.
        i_threshold (float, optional): Intensity threshold for filtering. Defaults to 500.
        mz_error (float, optional): Mass tolerance window. Defaults to 0.01.

    Returns:
        pd.Series: Target mass spectrum with background removed.
    """
    
    target_spec1 = target_spec1[target_spec1 > i_threshold]
    bg = []
    if len(target_spec1) == 0:
        return None
    else:
        for i in target_spec1.index.values:
            index = argmin(abs(background.index.values - i))
            if background.index.values[index] - i < mz_error:
                bg.append([i, background.values[index]])
            else:
                bg.append([i, 0])
        bg_spec = pd.Series(np.array(bg).T[1], np.array(bg).T[0], name=target_spec1.name)
        spec_bg_removal = target_spec1 - bg_spec
        return spec_bg_removal[spec_bg_removal > i_threshold].sort_values()


def JsonToExcel(json_file):
    """
    Parses a MassBank JSON file and generates a pandas dataframe with compounds information.

    Args:
        json_file: Path to the MassBank JSON file.

    Returns:
        A pandas dataframe with compounds' information, including InChIKey, molecular formula, total exact mass,
        SMILES, CAS, PubChem CID, InChI, total_exact_mass, ionization mode, instrument type, collision energy,
        column, mass accuracy, precursor m/z, precursor type, and classification.
    """
    
    with open(json_file, 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    Inchikey, precursors, frags, formulas, smiles, ion_modes, instrument_types, collision_energies = [], [], [], [], [], [], [], []
    cases, pubchem_cids, inchis, total_exact_masses = [], [], [], []
    columns, mass_accuracies, precursor_mzs, precursor_types, ionization_modes = [], [], [], [], []
    kingdoms, superclasses, class1s, subclasses = [], [], [], []
    names = []
    frag_annotations = []
    num = len(json_data)
    for i in tqdm(range(num), desc='Extracting info', leave=True, colour='Green'):
        # 信息1:包括分子信息
        info1 = json_data[i]['compound'][0]['metaData']
        ik_info = [x['value'] for x in info1 if x['name'] == 'InChIKey']
        formula_info = [x['value'] for x in info1 if x['name'] == 'molecular formula']
        precursor_info = [x['value'] for x in info1 if x['name'] == 'total exact mass']
        smile_info = [x['value'] for x in info1 if x['name'] == 'SMILES']
        cas_info = [x['value'] for x in info1 if x['name'] == 'cas']  # 新增cas
        pubchem_cid_info = [x['value'] for x in info1 if x['name'] == 'pubchem cid']  # 新增pubchem_cid
        inchi_info = [x['value'] for x in info1 if x['name'] == 'InChI']  # 新增 inchi
        total_exact_mass_info = [x['value'] for x in info1 if x['name'] == 'total exact mass']  # 新增 total_exact_mass
        # 获得数据
        ik = None if len(ik_info) == 0 else ik_info[0]
        formula = None if len(formula_info) == 0 else formula_info[0]
        precursor = None if len(precursor_info) == 0 else precursor_info[0]
        smile = None if len(smile_info) == 0 else smile_info[0]
        cas = None if len(cas_info) == 0 else cas_info[0]
        pubchem_cid = None if len(pubchem_cid_info) == 0 else pubchem_cid_info[0]
        inchi = None if len(inchi_info) == 0 else inchi_info[0]
        total_exact_mass = None if len(total_exact_mass_info) == 0 else total_exact_mass_info[0]
        
        # 信息2:包括测试条件
        info2 = json_data[i]['metaData']
        ion_mode_info = [x['value'] for x in info2 if x['name'] == 'ionization mode']
        instrument_type_info = [x['value'] for x in info2 if x['name'] == 'instrument type']
        ce_info = [i for i in info2 if i['name'] == 'collision energy']
        columns_info = [x['value'] for x in info2 if x['name'] == 'column']  # 新增columns
        mass_accuracy_info = [x['value'] for x in info2 if x['name'] == 'mass accuracy']  # 新增mass_accuracy
        precursor_mz_info = [x['value'] for x in info2 if x['name'] == 'precursor m/z']  # 新增precursor_mz
        precursor_type_info = [x['value'] for x in info2 if x['name'] == 'precursor type']  # 新增precursor_type
        ionization_mode_info = [x['value'] for x in info2 if x['name'] == 'ionization mode']  # 新增ionization_mode
        
        # 获得数据
        ion_mode = None if len(ion_mode_info) == 0 else ion_mode_info[0]
        instrument_type = None if len(instrument_type_info) == 0 else instrument_type_info[0]
        ce = None if len(ce_info) == 0 else ce_info[0]['value']
        column = None if len(columns_info) == 0 else columns_info[0]
        mass_accuracy = None if len(mass_accuracy_info) == 0 else mass_accuracy_info[0]
        precursor_mz = None if len(precursor_mz_info) == 0 else precursor_mz_info[0]
        precursor_type = None if len(precursor_type_info) == 0 else precursor_type_info[0]
        ionization_mode = None if len(ionization_mode_info) == 0 else ionization_mode_info[0]
        
        # 信息3：包括分类
        info3 = json_data[i]['compound'][0]['classification'] if 'classification' in [k for k, v in
                                                                                      json_data[i]['compound'][
                                                                                          0].items()] else []
        if len(info3) == 0:
            kingdom_info, superclass_info, class1_info, subclass_info = [], [], [], []
        else:
            kingdom_info = [x['value'] for x in info3 if x['name'] == 'kingdom']  # 新增kingdom_info
            superclass_info = [x['value'] for x in info3 if x['name'] == 'superclass']  # 新增superclass_info
            class1_info = [x['value'] for x in info3 if x['name'] == 'class']  # 新增class1_info
            subclass_info = [x['value'] for x in info3 if x['name'] == 'subclass']  # 新增subclass_info
        # 获得数据
        kingdom = None if len(kingdom_info) == 0 else kingdom_info[0]
        superclass = None if len(superclass_info) == 0 else superclass_info[0]
        class1 = None if len(class1_info) == 0 else class1_info[0]
        subclass = None if len(subclass_info) == 0 else subclass_info[0]
        
        # 信息4： 名字
        name = json_data[i]['compound'][0]['names'][0]['name'] if len(
            json_data[i]['compound'][0]['names']) != 0 else np.nan
        
        # 信息5： spectrum
        spec1 = r'{' + json_data[i]['spectrum'].replace(' ', ',') + r'}'
        spec2 = pd.Series(eval(spec1))
        s1 = spec2.sort_values(ascending=False).iloc[:10]
        # 生成碎片的annotation
        frag = [i['name'] for i in json_data[i]['annotations']] if 'annotations' in [k for k, v in
                                                                                     json_data[i].items()] else []
        frag_mz = [i['value'] for i in json_data[i]['annotations']] if 'annotations' in [k for k, v in
                                                                                         json_data[i].items()] else []
        s2 = pd.Series(frag, frag_mz)
        s2 = s2[~s2.index.duplicated(keep='first')]
        # 合并成dataframe
        df1 = pd.concat([s1, s2], axis=1)
        
        df1.columns = ['ratio', 'frag']
        df2 = df1[~df1['ratio'].isna()].sort_values(by='ratio', ascending=False)
        spec3 = str(df2.loc[:, 'ratio'].to_dict())
        spec3_annotation = str(df2.loc[:, 'frag'].to_dict())  # 新增spec3——annotation
        
        # 搜集数据
        Inchikey.append(ik)
        precursors.append(precursor)
        formulas.append(formula)
        smiles.append(smile)
        ion_modes.append(ion_mode)
        instrument_types.append(instrument_type)
        frags.append(spec3)
        collision_energies.append(ce)
        # 新增信息
        cases.append(cas)
        pubchem_cids.append(pubchem_cid)
        inchis.append(inchi)
        total_exact_masses.append(total_exact_mass)
        columns.append(column)
        mass_accuracies.append(mass_accuracy)
        precursor_mzs.append(precursor_mz)
        precursor_types.append(precursor_type)
        ionization_modes.append(ionization_mode)
        kingdoms.append(kingdom)
        superclasses.append(superclass)
        class1s.append(class1)
        subclasses.append(subclass)
        names.append(name)
        frag_annotations.append(spec3_annotation)
    database = pd.DataFrame(
        np.array([Inchikey, precursors, frags, frag_annotations, formulas, smiles, ion_modes, collision_energies,
                  instrument_types,
                  cases, pubchem_cids, inchis, total_exact_masses, columns, mass_accuracies, precursor_mzs,
                  precursor_types,
                  ionization_modes, kingdoms, superclasses, class1s, subclasses, names]).T,
        columns=['Inchikey', 'Precursor', 'Frag', 'frag annotations', 'Formula', 'Smiles', 'ion_modes',
                 'collision_energies', 'instrument type',
                 'cas', 'pubchem_cid', 'Inchi', 'total_exact_mass', 'chromatogram column info', 'mass_accuracy (ppm)',
                 'precursor mz', 'precursor_types', 'ionization_mode', 'kingdom', 'superclass', 'class1s', 'subclasses',
                 'names'
                 ])
    return database


def calibration(path, mode='internal'):
    """
    Calibrate using internal or external standard method, must have 'all_area_df.xlsx', 'quan_info.xlsx',
    and 'alignment' files.
    :param path: path for excel files
    :param mode: external or internal
    :return: result dataframe
    How to do it?
    1. concat all "final area" files by using concat_alignment, include samples and standard curve;
    2. save this data as "all_area_df"
    3. modify the "quan_info.xlsx" file, to include the file names and sample types
    4. use function calibration.


    """
    # 测试使用，2如果可以用就删除
    print('-----------------------')
    print('Reading files...')
    print('-----------------------')
    files_excel = glob(os.path.join(path, '*.xlsx'))  # 拿到所有excel文件
    area_file = [file for file in files_excel if 'all_area_df' in file][0]  # 拿到所有final_area
    unique_files = [file for file in files_excel if 'unique_cmp' in file]  # 拿到所有final_area
    area_df = pd.read_excel(area_file, index_col='Unnamed: 0')
    quan_info_file = [file for file in files_excel if 'quan_info' in file][0]  # 拿到定量信息
    cmp_info = pd.read_excel(quan_info_file)  # 污染物信息
    file_info = pd.read_excel(quan_info_file, sheet_name=1)  # 样品信息
    print('-----------------------')
    print('Processing data...')
    print('-----------------------')
    # 开始处理
    std_df = file_info[file_info['sample_type'] == 'STD']  # 标准品信息
    # 给std_df排序
    one_cmp = [cmp for cmp in std_df.columns.values if (cmp != 'file_name') &
               (cmp != 'ISTD_fold') & (cmp != 'unit') & (cmp != 'sample_type')][0]  # 随机选一个污染物名称
    std_df1 = std_df.sort_values(by=one_cmp, ascending=False)
    
    # 找到area df，拿到所有的new index,在这里面找new_index去更新标线里面的index
    index_df1 = pd.DataFrame(area_df.index, columns=['index'])
    index_df1['rt'] = index_df1['index'].apply(lambda x: eval(x.split('_')[0]))
    index_df1['mz'] = index_df1['index'].apply(lambda x: eval(x.split('_')[1]))
    
    # 更新cmp_info的new_index
    for i in range(len(cmp_info)):
        mz, rt = cmp_info.loc[i, ['mz', 'rt']]
        x = index_df1[(index_df1.mz > mz - 0.015) & (index_df1.mz < mz + 0.015) &
                      (index_df1.rt > rt - 0.1) & (index_df1.rt < rt + 0.1)].reset_index(drop=True)
        if len(x) == 0:
            x = index_df1[(index_df1.mz > mz - 0.03) & (index_df1.mz < mz + 0.03) &
                          (index_df1.rt > rt - 0.2) & (index_df1.rt < rt + 0.2)].reset_index(drop=True)
            if len(x) > 1:
                x['error'] = (x['mz'] - mz).abs()
                x1 = x.sort_values(by='error').reset_index(drop=True)
                match_index = x1.iloc[0]['index']
            elif len(x) == 1:
                match_index = x['index'].values[0]
            else:
                match_index = np.nan
        elif len(x) == 1:
            match_index = x['index'].values[0]
        elif len(x) > 1:
            x['error'] = (x['mz'] - mz).abs()
            x1 = x.sort_values(by='error').reset_index(drop=True)
            match_index = x.iloc[0]['index']
        cmp_info.loc[i, 'new_index'] = match_index
    cmp_info = cmp_info[~cmp_info['new_index'].isna()].reset_index(drop=True)
    
    # 获得standard的峰面积
    std_indice = cmp_info.new_index
    std_area_df = area_df.loc[std_indice, std_df.file_name]
    
    if mode.lower() == 'internal':
        for i in range(len(cmp_info)):
            istd_mz, istd_rt = cmp_info.loc[i, ['ISTD_mz', 'ISTD_rt']]
            istd_index = index_df1[(index_df1.mz > istd_mz - 0.05) & (index_df1.mz < istd_mz + 0.05) &
                                   (index_df1.rt > istd_rt - 0.1) & (index_df1.rt < istd_rt + 0.1)].reset_index(
                drop=True).loc[0, 'index']
            cmp_info.loc[i, 'new_index_istd'] = istd_index
        
        # 获得STD文件中istd的峰面积
        istd_indice = cmp_info.new_index_istd
        istd_area_df = area_df.loc[istd_indice, std_df.file_name]
        
        # 根据标准曲线求RF
        for i in range(len(cmp_info)):  # 先选择不同的污染物
            RFs = []
            raw_data = []
            istd_conc_raw = cmp_info.loc[i, 'ISTD_conc']
            std_cmp_name = cmp_info.loc[i, 'compound']
            for j in range(len(std_df)):  # 以std_file name 作为索引
                area_sample = std_area_df.iloc[i].loc[std_df.file_name.values[j]]
                area_istd = istd_area_df.iloc[i].loc[std_df.file_name.values[j]]
                std_conc = std_df[std_df['file_name'] == std_df.file_name.values[j]][std_cmp_name].values[0]
                istd_conc = std_df.ISTD_fold.iloc[j] * istd_conc_raw
                RF = (area_sample / area_istd) * (istd_conc / std_conc)
                raw_data.append([area_sample, area_istd, std_conc, istd_conc])
                RFs.append(round(RF, 2))
            RF_mean = round(np.mean(RFs), 2)
            RF_error = round(np.std(RFs) / np.mean(RFs) * 100, 1)
            cmp_info.loc[i, ['RF_mean', 'RF_std', 'RFs_raw']] = RF_mean, RF_error, str(RFs)
        
        # 获得sample文件中sample的area和istd的area
        sample_df = file_info[file_info['sample_type'] == 'Sample']  # 样品信息
        sample_area_df = area_df.loc[
            std_indice, sample_df['file_name'].apply(lambda x: x.split('_unique_cmp')[0])]  # 样品峰面积
        istd_area_df = area_df.loc[
            istd_indice, sample_df['file_name'].apply(lambda x: x.split('_unique_cmp')[0])]  # 样品峰面积
        
        # 计算样品
        for i in range(len(sample_area_df.columns)):
            column_name = sample_area_df.columns[i]
            # 开始计算浓度
            for j in range(len(cmp_info)):
                istd_conc = cmp_info.loc[j, 'ISTD_conc']
                area_sample = sample_area_df.iloc[j].loc[column_name]
                area_istd = istd_area_df.iloc[j].loc[column_name]
                RF = cmp_info.loc[j, 'RF_mean']
                cmp_info.loc[j, column_name] = round((area_sample / area_istd) * (istd_conc / RF), 2)
        final_result = cmp_info
    
    else:
        # 开始外标法
        external_std_df = pd.concat([cmp_info, std_area_df.reset_index(drop=True)], axis=1)  # 二者合并
        for i in range(len(external_std_df)):
            cmp_index = external_std_df.loc[i, 'compound']
            conc = std_df1.loc[:, cmp_index]  # 在这里改浓度
            area = external_std_df.loc[i, std_df1.file_name].values.astype(float)
            slope, intercept, r_value, p_value, std_err = st.linregress(area, conc)
            name = 'cmp' + str(i)
            locals()[name] = [slope, intercept, r_value ** 2]
            external_std_df.loc[i, ['slop', 'intercept', 'R2']] = [slope, intercept, r_value ** 2]
        
        sample_df = file_info[file_info['sample_type'] == 'Sample']  # 样品信息
        sample_area_df = area_df.loc[std_indice, sample_df.file_name]  # 样品峰面积
        # 计算标线斜率和截距
        for i in range(len(sample_area_df)):
            name = 'cmp' + str(i)
            area1 = sample_area_df.iloc[i, :].values
            c = locals()[name][0] * area1 + locals()[name][1]
            sample_area_df.iloc[i, :] = c
        final_result = pd.concat([external_std_df, sample_area_df.round(3).reset_index(drop=True)], axis=1)
    
    # 将unique_cmp没有筛查出来的数据移除
    unique_files = [file for file in files_excel if 'unique_cmp' in file]
    unique_file_names = [os.path.basename(i).split('_unique_cmps')[0] for i in unique_files]
    path_s1 = pd.Series(data=unique_files, index=unique_file_names)
    final_result.index = final_result['new_index']
    std_index = final_result['new_index'].values
    for name in tqdm(final_result.columns, desc='Remove nondetectable cmps'):
        if name in path_s1.index.values:
            df_unique = pd.read_excel(path_s1.loc[name])
            unique_info = pd.DataFrame(np.array([df_unique.rt.values, df_unique.mz.values]).T, columns=['rt', 'mz'])
            set_0_index = []
            for index in std_index:
                rt, mz = index.split('_')
                rt = eval(rt)
                mz = eval(mz)
                result1 = unique_info[(unique_info.rt < rt + 0.1)
                                      & (unique_info.rt > rt - 0.1)
                                      & (unique_info.mz < mz + 0.015)
                                      & (unique_info.mz > mz - 0.015)]
                if len(result1) == 0:
                    set_0_index.append(index)
                else:
                    pass
            final_result.loc[set_0_index, name] = np.nan
    return final_result


def peak_checking_plot(df1, mz, rt1, path=None):
    """
    Evaluating/visualizing the extracted mz
    :param path: whether export to path
    :param df1: LC-MS dataframe, generated by the function gen_df()
    :param mz: Targeted mass for extraction
    :param rt1: expected rt for peaks
    :return:
    """
    plt.rcParams['font.sans-serif'] = 'Times New Roman'  # 设置全局字体
    fig = plt.figure(figsize=(12, 4))
    # 检查色谱图ax
    ax = fig.add_subplot(121)
    rt, eic = extract(df1, mz, 50)
    rt = np.array(rt)
    eic = np.array(eic)
    rt2 = rt[where((rt > rt1 - 3) & (rt < rt1 + 3))]
    eic2 = eic[where((rt > rt1 - 3) & (rt < rt1 + 3))]
    ax.plot(rt, eic)
    ax.set_xlabel('Retention Time(min)', fontsize=12)
    ax.set_ylabel('Intensity', fontsize=12)
    peak_index = np.argmin(abs(rt - rt1))
    peak_height = max(eic[peak_index - 2:peak_index + 2])
    ax.scatter(rt1, peak_height * 1.05, c='r', marker='*', s=50)
    # 计算背景
    bg = cal_bg(eic)
    bg1 = zeros(len(eic)) + bg
    ax.plot(rt, bg1)
    SN = round(peak_height / bg, 1)
    ax.set_title(f'SN:{SN}')
    ax.set_ylim(top=peak_height * 1.1, bottom=-peak_height * 0.05)
    
    # 开始画质谱图
    spec = spec_at_rt(df1, rt1)
    spec_mz, spec_i = spec.index.values, spec.values
    ax2 = fig.add_subplot(122)
    ax2.plot(spec_mz, spec_i)
    ax2.set_xlabel('m/z', fontsize=12)
    ax2.set_ylabel('Intensity', fontsize=12)
    
    if path is None:
        pass
    else:
        plt.savefig(path, dpi=1000)
        plt.close('all')


def final_result_filter(final_result, remove_list=None, match_num=2):
    """
    Filter the final result based on the minimum number of matched fragments and remove certain compounds if specified.

    Args:
        final_result (pd.DataFrame): The final result generated by summarize_pos_neg_result().
        remove_list (list, optional): A list of source names to be removed from the final result. Defaults to None.
        match_num (int, optional): The minimum number of matched fragments required for a compound to be included in the final result. Defaults to 2.

    Returns:
        pd.DataFrame: The filtered final result.
    """
    
    if remove_list is None:
        pass
    else:
        for remove_item in remove_list:
            final_result1 = final_result[~final_result['source'].fillna('-').str.contains(remove_item)]
    a = final_result1[final_result1['Confidence level'] == 1]
    c = final_result1[final_result1['Confidence level'] == 3]
    b_ = final_result1[final_result1['Confidence level'] == 2]
    b = b_[b_['match_num'] >= match_num]
    final_result2 = pd.concat([a, b, c], axis=0).reset_index(drop=True)
    for i in range(len(final_result2)):
        if type(final_result2.loc[i, 'Toxicity']) == float:
            pass
        else:
            x = eval(final_result2.loc[i, 'Toxicity'])
            for k, v in x.items():
                if (type(v) is float) | (v == '-'):
                    final_result2.loc[i, k] = v
                else:
                    final_result2.loc[i, k] = eval(v)
    return final_result2


def update_category(result, category_updates, good_category):
    """
    This function can transform old categories to new categories.
    :param category_updates: category updates information
    :param good_category: This category are doubtless，most of them are standards in our lab
    :return: new summarized results with new category
    """
    updates = category_updates[~category_updates['new category'].isna()].reset_index(drop=True)
    # 先做替换
    for i in range(len(result)):
        x = eval(result.loc[i, 'category'])
        if len(x) == 0:
            pass
        else:
            y = list(set([None if i not in updates['old category'].values else
                          updates[updates['old category'] == i]['new category'].values[0] for i in x]))
            if None in y:
                y.remove(None)
            result.loc[i, 'new_category'] = str(y)
    # 再将正确的替换
    ik_index = good_category['ik'].value_counts().index
    for ik in ik_index:
        ik_df = good_category[good_category.ik == ik]
        new_category = list(set(ik_df['category'].values))
        usage = list(set(ik_df['sub_category'].values))
        if np.nan in usage:
            usage.remove(np.nan)
        # 去找一下result里面是否有这个物质
        a = result[result['ik'] == ik]
        if len(a) != 0:
            index = a.index.values[0]
            if 'REACH' in str(result.loc[index, 'new_category']):  # 看一下原来的分类里，是否包含REACH
                new_category.append('REACH')
            result.loc[index, 'new_category'] = str(new_category)
            result.loc[index, 'usage'] = str(usage)
    return result


def draw_pie_chart(category_data_series, path=None, show=True, fraction=False, drop_list=None):
    """
    Draw a pie chart to represent the distribution of categories.

    Args:
        category_data_series (pandas Series): The data series containing the category data.
        path (str, optional): The file path to save the chart image. Default is None.
        show (bool, optional): Whether to display the chart. Default is True.
        fraction (bool, optional): Whether to display the percentage values as fractions. Default is False.
        drop_list (list, optional): A list of categories to remove from the chart. Default is None.

    Returns:
        None
    """
    data = category_data_series
    if isinstance(drop_list, list):
        drop_list = [category for category in drop_list if category in data.index]
        data = data.drop(drop_list)
    plt.rcParams['font.sans-serif'] = 'Times New Roman'
    plt.rcParams['font.size'] = 14
    
    # Define explode values - explode if value is less than 5%
    explode = (data / sum(data) < 0.05).map({True: 0.1, False: 0})
    
    # Plot
    fig1, ax1 = plt.subplots(figsize=(15, 6))
    
    # Define color palette
    colors = plt.cm.Set3(np.linspace(0, 1, len(data)))
    
    wedges, texts, autotexts = ax1.pie(data, explode=explode, labels=None, startangle=140, autopct='')
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')
    
    # Create custom legend handles
    legend_handles = [mpatches.Patch(color=colors[i], label=f'{data.index[i]} ({data.iloc[i]})') for i in
                      range(len(data))]
    
    # Set edge color for each legend handle
    for handle in legend_handles:
        handle.set_edgecolor('black')
    
    # Add legend with custom handles
    legend = plt.legend(handles=legend_handles,
                        loc="center left",
                        bbox_to_anchor=(0.7, 0.5),
                        frameon=False)
    
    # Place the percentage values outside the pie chart
    def autopct_format(value):
        return f'{value:.1f}%'
    
    if fraction is False:
        ax1.pie(data, explode=explode, labels=None, startangle=140, pctdistance=0.85, colors=colors, shadow=False)
    else:
        ax1.pie(data, explode=explode, labels=None, startangle=140, autopct=autopct_format, pctdistance=0.85,
                colors=colors, shadow=False)
    
    # Apply additional styling
    plt.setp(autotexts, size=10, weight="bold", color='white')
    plt.setp(texts, size=10)
    
    # Add a title
    plt.title("Distribution of Categories")
    
    if show is True:
        plt.show()
    
    if path is not None:
        bbox_extra_artists = [legend]  # Include legend in the bounding box calculation
        plt.savefig(path, dpi=500, bbox_inches='tight', bbox_extra_artists=bbox_extra_artists)
        plt.close('all')


def AIF_multi_ce(path, company='Agilent', profile=False, control_group=['Methanol'], collision_energies=[10, 20, 40],
                 filter_type=1, frag_rt_error=0.02, split_n=20, peak_width=1,
                 sat_intensity=False, long_rt_split_n=1, threshold=15, i_threshold=500, SN_threshold=3, orbi=False):
    """
    Processes AIF data when multiple collision energies are present.

    Args:
        path (str): The file path for the mzML files to be processed. Example, 'C:/Users/Desktop/my_HRMS_files'.
        company (str): The brand of the mass spectrometer used to gather the data. Acceptable options are 'Waters', 'Thermo', 'Sciex', 'Agilent'.
        profile (bool): Specifies whether the data is in profile or centroid mode. Set as True for profile mode, False for centroid mode.
        control_group (List[str]): List of labels that designate the control group, used when searching for relevant filenames.
        collision_energies (List[int]): List of different collision energies. Exclude 0 as it corresponds to MS1.
        filter_type (int): Set to 1 for data without triplicates where fold change is calculated as the ratio of sample area to the maximum control area.
                           Set to 2 for data with triplicates where the function computes p-values, and fold change as the ratio of the mean sample area to the mean control area.
        frag_rt_error (float): The retention time (RT) error for matching fragment peak to the precursor's peak.
        split_n (int): The mass range will be divided into n parts for easier processing.
        sat_intensity (bool): Specifies if the mass spectrometer has a saturated intensity. Default is False.
        long_rt_split_n (int): The retention time will be divided into n parts for easier processing.
        threshold (int): The noise level threshold for a peak. Default is 15.
        i_threshold (int): The intensity threshold for the peak picking step. Default is 500.
        SN_threshold (int): The signal to noise ratio threshold for the peak picking step. Default is 3.

    Returns:
        None. The processed data is saved to an output file.
    """
    
    collision_energies = sorted(collision_energies)
    
    files = glob(os.path.join(path, '*.mzML'))
    # 1. first step peak picking
    for file in files:
        if any(control.lower() in file.lower() for control in control_group):
            first_process(file, company, profile=profile, i_threshold=200, peak_width=peak_width,
                          SN_threshold=3, ms2_analysis=False, frag_rt_error=frag_rt_error, split_n=split_n,
                          sat_intensity=sat_intensity, long_rt_split_n=long_rt_split_n, orbi=orbi)
        else:
            ms_scans = [[] for _ in range(len(collision_energies) + 1)]
            run = pymzml.run.Reader(file)
            for scan in tqdm(run, desc='Separating Scans'):
                if scan.ms_level == 1:
                    ms_scans[0].append(scan)
                elif 'collision energy' in scan:
                    collision_energy = scan['collision energy']
                    if collision_energy in collision_energies:
                        index = collision_energies.index(collision_energy) + 1
                        ms_scans[index].append(scan)
            peak_alls = []
            for ms in ms_scans:
                peak_all = ultimate_peak_picking(ms, profile=profile, split_n=split_n, threshold=threshold,
                                                 peak_width=peak_width,
                                                 i_threshold=i_threshold, SN_threshold=SN_threshold,
                                                 rt_error_alignment=0.05, mz_error_alignment=0.015, mz_overlap=1,
                                                 sat_intensity=sat_intensity, long_rt_split_n=long_rt_split_n,
                                                 rt_overlap=1, orbi=orbi)
                peak_alls.append(peak_all)
            peak_all_ms1 = peak_alls[0]
            peak_alls_ms2 = peak_alls[1:]
            for j, each_ms2_peak_all in enumerate(peak_alls_ms2):
                frag_all, spec_all = get_frag_DIA(peak_all_ms1, each_ms2_peak_all, frag_rt_error=frag_rt_error)
                column_name1 = 'frag_DIA_' + str(collision_energies[j]) + 'V'
                column_name2 = 'Spec_DIA' + str(collision_energies[j]) + 'V'
                peak_all_ms1.loc[:, column_name1] = frag_all
                peak_all_ms1.loc[:, column_name2] = spec_all
            peak_all_ms1.to_excel(file.replace('.mzML', '.xlsx'))
    
    # 中间过程
    files_excel = glob(os.path.join(path, '*.xlsx'))
    peak_alignment(files_excel)
    ref_all = pd.read_excel(os.path.join(path, 'peak_ref.xlsx'), index_col='Unnamed: 0')
    
    # 第二部分
    for file in files:
        second_process(file, ref_all, company=company, profile=profile, long_rt_split_n=long_rt_split_n, orbi=orbi)
    
    # 第三部份，差异性分析
    # 第三个过程, 做fold change filter
    print('                                                                            ')
    print('============================================================================')
    print('Third process started...')
    print('============================================================================')
    print('                                                                            ')
    fold_change_filter(path, control_group=control_group, filter_type=filter_type)


def get_frag_DIA(peak_all, peak_all2, frag_rt_error=0.02):
    """
    This function assigns possible fragments from MS2 data (peak_all2) to the corresponding MS1 peaks in peak_all
    based on the retention time (rt) range defined by frag_rt_error.

    Args:
        peak_all (pd.DataFrame): A DataFrame of peaks generated by peak picking from MS1 data.
        peak_all2 (pd.DataFrame): A DataFrame of peaks generated by peak picking from MS2 data.
        frag_rt_error (float, optional): The retention time error tolerance for matching MS1 peaks to MS2 fragments.
                                         The default value is 0.02.

    Returns:
        tuple: Two lists containing fragment ions and spectra information, respectively. The fragment ions list
               consists of strings representing lists of m/z values. The spectra list contains strings representing
               Series of MS2 spectra with their intensity values, where each series is sorted by descending intensity
               and trimmed to the top 20 values.

    Note:
        The peak_all and peak_all2 dataframes should contain 'rt', 'mz', and 'intensity' columns.
    """
    
    frag_all = []
    spec_all = []
    for i in tqdm(range(len(peak_all)), desc='Assign DIA MS2 spectrum', leave=False, colour='Green'):
        rt = peak_all.loc[i, 'rt']
        df_DIA = peak_all2[(peak_all2['rt'] > rt - frag_rt_error)
                           & (peak_all2['rt'] < rt + frag_rt_error)].sort_values(
            by='intensity', ascending=False)
        # append fragments
        frag = str(list(df_DIA['mz'].values))
        frag_all.append(frag)
        # append ms2 spectra
        
        s = pd.Series(data=df_DIA['intensity'].values, index=df_DIA['mz'])
        # Convert the series to a DataFrame
        df = pd.DataFrame(s).reset_index()
        df.columns = ['m/z', 'intensity']
        
        # Sort the dataframe by 'm/z'
        df = df.sort_values(by='m/z')
        
        # Create a new column 'group' for data grouping
        df.loc[:, 'group'] = (df['m/z'].diff() > 0.5).cumsum()
        
        # Keep the row with max 'intensity' from each group
        df = df.loc[df.groupby('group')['intensity'].idxmax()]
        
        # Drop the 'group' column as it's no longer needed
        df = df.drop(columns=['group'])
        
        # Convert the DataFrame back to a Series
        result = pd.Series(df['intensity'].values, index=df['m/z']).astype(int)
        
        # Remove the name of the index
        result.index.name = None
        
        result = result.sort_values(ascending=False).iloc[:20]
        
        spec_all.append(str(result))
    
    return frag_all, spec_all


def build_molecular_network(data, parent_cmps,
                            frag_num_for_network=2,
                            insource_frag_RT_threshold=0.05,
                            parent_cmps_color='g',
                            insource_cmp_color='yellow',
                            tp_cmps_color='b',
                            parent_cmps_size=820,
                            insource_cmp_size=420,
                            tp_cmps_size=400,
                            default_color='g',
                            default_size=5,
                            default_edge_widths=0.8,
                            node_edge_width=1.0, node_edge_color='black', alpha=1,
                            network_type='random_layout',
                            with_labels=False, label_font_size=12, font_type='sans-serif', label_x_tight=0.88,
                            legend=True, other_cmps=[],
                            figsize=(12, 12), path=None, dpi=500):
    """
    Build and visualize a molecular network from provided data and parameters.

    Parameters:
    - data (DataFrame): The input data containing compound pairs, their shared fragment count,
        and fragment info.
    - parent_cmps (list of str): List of parent compounds to be considered.
    - frag_num_for_network (int, optional): Threshold for shared fragment count to identify TP compounds.
        Default is 2.
    - insource_frag_RT_threshold (float, optional): Threshold for difference in retention time to
        identify in-source fragments. Default is 0.1.
    - parent_cmps_color (str, optional): Color for parent compounds in the network. Default is 'r' (red).
    - insource_cmp_color (str, optional): Color for in-source fragments in the network. Default is 'g' (green).
    - tp_cmps_color (str, optional): Color for TP compounds in the network. Default is 'm' (magenta).
    - parent_cmps_size (int, optional): Size of parent compounds in the network. Default is 820.
    - insource_cmp_size (int, optional): Size of in-source fragments in the network. Default is 420.
    - tp_cmps_size (int, optional): Size of TP compounds in the network. Default is 400.
    - default_color (str, optional): Default color for nodes that don't fall into other categories.
        Default is 'g' (green).
    - default_size (int, optional): Default size for nodes that don't fall into other categories. Default is 5.
    - default_edge_widths (float, optional): Default edge width for the network. Default is 0.5.
    - network_type (str, optional): Layout of the network. Options are: 'random_layout', 'spring_layout',
        'circular_layout', 'kamada_kawai_layout', and 'shell_layout'. Default is 'random_layout'.
    - figsize (tuple of int, optional): Figure size for the molecular network visualization. Default is (5, 5).
    - path (str, optional): Path to save the visualization. If None, the visualization won't be saved. Default is None.
    - dpi (int, optional): Dots per inch for saved visualization. Default is 300.

    Returns:
    None. Displays or saves a visualization of the molecular network.
    """
    
    # data analysis
    # Identify pairs that contain at least one of the parent compounds
    parent_pairs = data[(data['cmp1'].isin(parent_cmps) | data['cmp2'].isin(parent_cmps)) & (
            data['same_frag_num'] >= frag_num_for_network)]
    
    # Extract target compounds from parent pairs
    target_cmp = set(parent_pairs['cmp1'].tolist() + parent_pairs['cmp2'].tolist())
    
    # find their relationships
    target_pairs = data[
        data['cmp1'].isin(target_cmp) & data['cmp2'].isin(target_cmp) & (data['same_frag_num'] >= frag_num_for_network)]
    
    # Extract RT values for parent compounds
    parent_RT_values = [float(cmp.split('_')[0]) for cmp in parent_cmps]
    
    # Identify in-source fragments based on RT difference
    insource_fragments = []
    for index, row in target_pairs.iterrows():
        cmp1_RT = float(row['cmp1'].split('_')[0])
        cmp2_RT = float(row['cmp2'].split('_')[0])
        
        for parent_RT in parent_RT_values:
            if abs(cmp1_RT - parent_RT) < insource_frag_RT_threshold:
                insource_fragments.append(row['cmp1'])
            if abs(cmp2_RT - parent_RT) < insource_frag_RT_threshold:
                insource_fragments.append(row['cmp2'])
    # Create the network graph
    G = nx.Graph()
    
    # add nodes
    # add parent nodes
    parent_num = 0
    for cmp in parent_cmps:
        G.add_node(cmp, color=parent_cmps_color, size=parent_cmps_size)
        parent_num += 1
    for cmp1 in other_cmps:
        G.add_node(cmp1, color=default_color, size=default_size)
        parent_num += 1
    # add in-source fragment nodes
    insource_num = 0
    for in_source_cmp in insource_fragments:
        if in_source_cmp not in G:
            G.add_node(in_source_cmp, color=insource_cmp_color, size=insource_cmp_size)
            insource_num += 1
    # add tp nodes
    tp_num = 0
    for _, row in parent_pairs.iterrows():
        if row['cmp1'] not in G:
            G.add_node(row['cmp1'], color=tp_cmps_color, size=tp_cmps_size)
            tp_num += 1
        if row['cmp2'] not in G:
            G.add_node(row['cmp2'], color=tp_cmps_color, size=tp_cmps_size)
            tp_num += 1
    
    # add edge
    for _, row in target_pairs.iterrows():
        G.add_edge(row['cmp1'], row['cmp2'], weight=row['same_frag_num'])
    
    # Visualization
    pos = None
    if network_type == 'random_layout':
        pos = nx.random_layout(G)
    elif network_type == 'spring_layout':
        pos = nx.spring_layout(G, iterations=100, k=0.5)
    elif network_type == 'circular_layout':
        pos = nx.circular_layout(G)
    elif network_type == 'kamada_kawai_layout':
        pos = nx.kamada_kawai_layout(G)
    elif network_type == 'shell_layout':
        pos = nx.shell_layout(G)
    
    colors = [G.nodes[node]['color'] for node in G.nodes()]
    sizes = [G.nodes[node]['size'] for node in G.nodes()]
    edge_widths = [default_edge_widths * G[u][v]['weight'] / 15 for u, v in G.edges()]
    
    plt.figure(figsize=figsize)
    
    nx.draw(G, pos, with_labels=False, node_color=colors, font_size=label_font_size,
            node_size=sizes, width=edge_widths,
            linewidths=node_edge_width, edgecolors=node_edge_color, alpha=alpha)
    
    if with_labels:
        x_min = min([v[0] for k, v in pos.items()])
        x_max = max([v[0] for k, v in pos.items()])
        x_middle = (x_max + x_min) / 2
        label_pos = {k: [x_middle + (v[0] - x_middle) * label_x_tight, v[1]] for k, v in pos.items()}
        nx.draw_networkx_labels(G, label_pos, font_size=label_font_size, font_family=font_type)
    # Create and show legend if `legend` is set to True
    if legend:
        # Creating legend entries
        red_patch = mpatches.Patch(color=parent_cmps_color, label=f'Parent Compounds({parent_num})')
        green_patch = mpatches.Patch(color=insource_cmp_color, label=f'In-source Fragments({insource_num})')
        magenta_patch = mpatches.Patch(color=tp_cmps_color, label=f'TP Compounds({tp_num})')
        
        # Adding the legend
        plt.legend(handles=[red_patch, green_patch, magenta_patch])
    
    if path is None:
        pass
    else:
        plt.savefig(path, dpi=dpi, bbox_inches='tight')


def ISTD_evaluation(files, istd_info, columns_for_name_rt_mz=['name', 'rt', 'mz'],
                    checking_list=['mz', 'rt', 'mz_opt', 'area', 'intensity', 'S/N'],
                    mz_error_threshold=0.015, rt_error_threshold=0.15):
    """
    Evaluate the quality of Internal Standards (ISTDs) from peak picking results.

    Parameters:
    - files (list of str): File paths of Excel results to evaluate.
    - istd_info (DataFrame): DataFrame with ISTD details, including name, RT, and m/z.
    - columns_for_name_rt_mz (list of str, optional): Column names for 'name', 'rt', and 'mz' in the ISTD info. Defaults to ['name', 'rt', 'mz'].
    - checking_list (list of str, optional): List of attributes to check in the results. Defaults to ['mz', 'rt', 'mz_opt', 'area', 'intensity', 'S/N'].
    - mz_error_threshold (float, optional): Tolerance for m/z discrepancies. Defaults to 0.015.
    - rt_error_threshold (float, optional): Tolerance for RT discrepancies. Defaults to 0.15.

    Returns:
    - list of DataFrames: Evaluated results for each attribute in `checking_list`.

    Notes:
    - If 'mz_opt' is present in the input data, it indicates the optimized m/z value.
    """
    
    final_data = []
    istd_df = istd_info.loc[:, columns_for_name_rt_mz]
    
    # Initialize dictionaries to store results for each attribute in checking_list
    for m in range(len(checking_list)):
        locals()['dict' + str(m)] = {}
    
    for file in tqdm(files):
        name = os.path.basename(file).replace('.xlsx', '')
        df = pd.read_excel(file)
        
        # Initialize lists to store ISTD attributes for the current file
        for n in range(len(checking_list)):
            locals()['box' + str(n)] = []
        
        # Extract relevant ISTD information from the data
        for i in range(len(istd_info)):
            rt = istd_info.loc[i, columns_for_name_rt_mz[1]]
            mz = istd_info.loc[i, columns_for_name_rt_mz[2]]
            
            # Filter rows matching the current ISTD based on rt and mz values
            df1 = df[
                (df['rt'] < rt + rt_error_threshold) &
                (df['rt'] > rt - rt_error_threshold) &
                (df['mz'] < mz + mz_error_threshold) &
                (df['mz'] > mz - mz_error_threshold)
                ]
            
            # If matching rows found, store the one with highest intensity
            if len(df1) > 0:
                df1 = df1.sort_values(by='intensity', ascending=False)
                s1 = df1.iloc[0]
                for j in range(len(checking_list)):
                    locals()['box' + str(j)].append(s1[checking_list[j]])
            else:
                for o in range(len(checking_list)):
                    locals()['box' + str(o)].append(None)
        
        # Store results for the current file in the dictionaries
        for m in range(len(checking_list)):
            locals()['dict' + str(m)][name] = locals()['box' + str(m)]
    
    # Combine the results into a final list of DataFrames for each attribute
    for q in range(len(checking_list)):
        df_q = pd.DataFrame(locals()['dict' + str(q)])
        final_df = pd.concat([istd_df, df_q], axis=1)
        final_data.append(final_df)
    
    return final_data


def formula_prediction(mz, mode, atoms=['C', 'H', 'O', 'N'],
                       atom_n=[[5, 30], [0, 50], [0, 30], [0, 10]], max_possible_num=2e7, mz_error=5, all_info=False):
    """
    Predicts the chemical formula based on the provided m/z value(s).

    Parameters:
        mz (float or list/np.ndarray): The mass-to-charge ratio(s). If a list or ndarray is provided,
                                       formulae for all values will be predicted.
        mode (str): The ionization mode ('pos' for positive or 'neg' for negative).
        atoms (list): List of chemical elements to consider. Defaults to ['C', 'H', 'O', 'N'].
        atom_n (list): Range for each atom to consider in the prediction. Defaults to [[5, 30], [0, 50], [0, 30], [0, 10]].
        max_possible_num (float): Maximum number of possible structures allowed. Defaults to 2e7.
        mz_error (float): Allowed error for the m/z value in parts per million (ppm). Defaults to 5.
        all_info (bool): If True, returns all possible formulas and their errors. If False, returns only the best match. Defaults to False.

    Returns:
        DataFrame or tuple: For a single m/z (float), returns a DataFrame of possible formulae.
                            For multiple m/z values (list/np.ndarray), returns a tuple of possible formulae and their corresponding errors.

    Raises:
        ValueError: If the number of possible structures exceeds the max_possible_num.
                    If the type of mz is unsupported.
    """
    atom_mass_table1 = pd.Series(
        data={'C': 12.000000, 'Ciso': 13.003355, 'N': 14.003074, 'Niso': 15.000109, 'O': 15.994915, 'H': 1.007825,
              'Oiso': 17.999159, 'F': 18.998403, 'K': 38.963708, 'P': 30.973763, 'Cl': 34.968853,
              'S': 31.972072, 'Siso': 33.967868, 'Br': 78.918336, 'Na': 22.989770, 'Si': 27.976928,
              'Fe': 55.934939, 'Se': 79.916521, 'As': 74.921596, 'I': 126.904477, 'D': 2.014102,
              'Co': 58.933198, 'Au': 196.966560, 'B': 11.009305, 'e': 0.0005486
              })
    
    # Function to generate chemical formula for a given row
    def generate_formula(row):
        formula = ''.join([f"{el}{int(row[el]) if row[el] > 1 else ''}" for el in atoms if row[el] > 0])
        return formula
    
    # sort element list
    elements_sorted_list = ['C', 'H', 'O', 'N', 'S', 'Cl', 'Br', 'P', 'F', 'K', 'Na', 'Ciso', 'D', 'Oiso', 'Niso',
                            'Siso']
    
    atom_indices = {atom: i for i, atom in enumerate(atoms)}
    sorted_atoms_and_ranges = sorted(
        [(atom, atom_n[atom_indices[atom]]) for atom in atoms if atom in elements_sorted_list],
        key=lambda x: elements_sorted_list.index(x[0]))
    atoms, atom_n = zip(*sorted_atoms_and_ranges)
    
    # generate ranges
    ranges = [range(n[0], n[1] + 1) for n in atom_n]
    # generate patterns_list, this process is very fast
    patterns_list = list(itertools.product(*ranges))
    
    if len(patterns_list) > max_possible_num:
        raise ValueError(
            "The number of possible structures is so large that processing may take an extended period on your computer, increase the max_possible_num may solve the issue.")
    else:
        # generate a np.array, this is time-consuming
        patterns = np.array(patterns_list)
        
        mzs = 0
        for i in range(len(atoms)):
            mzs += patterns[:, i] * atom_mass_table1[atoms[i]]
        mzs = mzs + atom_mass_table1['e'] if mode == 'neg' else mzs - atom_mass_table1['e']
    if isinstance(mz, float):
        target_mz = mz
        index = np.argwhere((mzs > target_mz * (1 - mz_error * 1e-6)) & (mzs < target_mz * (1 + mz_error * 1e-6)))
        if len(index) == 0:
            return pd.DataFrame()
        else:
            arr1 = patterns[index]
            exact_mass = mzs[index]
            # Reshape the array to make it 2-dimensional
            arr_2d = arr1.reshape(arr1.shape[0], -1)
            # Creating the DataFrame
            df = pd.DataFrame(arr_2d, columns=atoms)
            df['exact_mass'] = exact_mass
            hetero_atoms = [atom for atom in atoms if atom not in ['C', 'H', 'O', 'N']]
            df1 = df.sort_values(by=hetero_atoms).reset_index(drop=True)
            df1['mz_error'] = round((df1['exact_mass'] - target_mz) / target_mz * 1e6, 2)
            df1['formula'] = df1.apply(generate_formula, axis=1)
            return df1
    elif isinstance(mz, (list, np.ndarray)):
        possible_formulas = []
        errors = []
        for target_mz in tqdm(mz, desc='Calculating the formula', leave=False):
            index = np.argwhere((mzs > target_mz * (1 - mz_error * 1e-6)) & (mzs < target_mz * (1 + mz_error * 1e-6)))
            if len(index) == 0:
                possible_formulas.append(None)
                errors.append(None)
            else:
                arr1 = patterns[index]
                exact_mass = mzs[index]
                # Reshape the array to make it 2-dimensional
                arr_2d = arr1.reshape(arr1.shape[0], -1)
                # Creating the DataFrame
                df = pd.DataFrame(arr_2d, columns=atoms)
                df['exact_mass'] = exact_mass
                hetero_atoms = [atom for atom in atoms if atom not in ['C', 'H', 'O', 'N']]
                df1 = df.sort_values(by=hetero_atoms).reset_index(drop=True)
                df1['mz_error'] = round((df1['exact_mass'] - target_mz) / target_mz * 1e6, 2)
                df1['formula'] = df1.apply(generate_formula, axis=1)
                if all_info is False:
                    possible_formulas.append(df1.loc[0, 'formula'])
                    errors.append(df1.loc[0, 'mz_error'])
                else:
                    possible_formulas.append(str(list(df1['formula'].values)))
                    errors.append(str(list(df1['mz_error'].values)))
        return possible_formulas, errors
    else:
        raise ValueError(f"Unsupported type for mz: {type(mz)}")


def convert_db(df, relative_i_threshold=20, source='', source_info=''):
    """
    Convert a Massbank database from Excel to a format compatible with pyhrms.

    This function processes an Excel file (previously converted from a JSON file using the JsonToExcel function) to create a database suitable for use in pyhrms. It filters fragment masses based on a relative intensity threshold and adds metadata about the source of the database.

    Args:
        df (pandas.DataFrame): The dataframe created by reading the Excel file with pandas.
        relative_i_threshold (int): The relative intensity threshold. Fragments with an intensity above this threshold are kept. Defaults to 20.
        source (str): The origin of the database, e.g., 'Massbank'. Defaults to an empty string.
        source_info (str): The specific database name from Massbank. Defaults to an empty string.

    Returns:
        pandas.DataFrame: A dataframe containing the processed database information, formatted for use in pyhrms.

    The function processes each compound in the dataframe, filtering out fragment masses that do not meet the specified intensity threshold and are less than the precursor mass minus 5. It also formats ion modes and includes source information in the resulting dataframe.
    """
    iks = df['Inchikey'].value_counts().index.values
    info_all = []
    for ik in tqdm(iks, desc='Collecting MS2 info'):
        df1 = df[df['Inchikey'] == ik].reset_index(drop=True)
        target_df = df1.loc[0, ['Inchikey', 'Precursor', 'Formula', 'Smiles', 'ion_modes']]
        precursor = eval(df1['Precursor'].iloc[0]) if isinstance(df1['Precursor'].iloc[0], str) else \
            df1['Precursor'].iloc[0]
        # 1. 获得所有该化合物信息
        all_s = []
        for i in range(len(df1)):
            s = pd.Series(eval(df1.loc[i, 'Frag']))
            all_s.append(s)
        all_s_s = pd.concat(all_s)
        # 2. 去掉特别相似的质量，保留响应高的质量
        df2 = pd.DataFrame(all_s_s)
        df2['mz'] = df2.index.values.round(2)
        df2.columns = ['abundance', 'mz']
        df2 = df2.sort_values(by='abundance', ascending=False)
        df3 = df2.drop_duplicates(subset='mz', keep='first')
        # 筛选响应大于relative_i_threshold，质量小于precursor-5的
        df4 = df3[(df3['abundance'] > relative_i_threshold) & (df3['mz'] < precursor - 5)]
        final_frag = str(list(df3.index))
        target_df.loc[:, 'Frag'] = final_frag
        target_df.loc[:, 'Precursor'] = precursor
        info_all.append(target_df)
    database = pd.concat(info_all, axis=1).T.reset_index(drop=True)
    database.loc[:, 'ion_modes'] = database['ion_modes'].apply(
        lambda a: a.replace('positive', 'pos').replace('negative', 'neg'))
    database.loc[:, 'Source'] = source
    database.loc[:, 'Source info'] = source_info
    database.loc[:, 'rt'] = np.nan
    database = database.rename(columns={'ion_modes': 'mode'})
    return database


def find_name(soup, label_text):
    name_label = soup.find('td', string=label_text)
    if name_label:
        name_tag = name_label.find_next_sibling('td')
        if name_tag:
            return name_tag.get_text().strip()
    return ""


def get_chemical_name(query, language='both'):
    ua = UserAgent()  # 读取本地ua,避免ua报错
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.chemicalbook.com/"
    }
    url = f"https://www.chemicalbook.com/Search.aspx?_s=&keyword={query}"
    with requests.Session() as session:
        session.headers.update(headers)
        session.get("https://www.chemicalbook.com/")
        try:
            response = session.get(url, headers=headers)
            response.raise_for_status()
            page_content = response.text
            soup = BeautifulSoup(page_content, 'html.parser')
            # Fetch names based on language selection
            if language.lower() == 'both':
                english_name = find_name(soup, '英文名称：').capitalize()
                chinese_name = find_name(soup, '中文名称：')
                return english_name, chinese_name
            elif language.lower() == 'cn':
                return find_name(soup, '中文名称：')
            elif language.lower() == 'en':
                return find_name(soup, '英文名称：').capitalize()
            else:
                return ""
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return "" if language != 'both' else ("", "")
        except Exception as err:
            print(f"An error occurred: {err}")
            return "" if language != 'both' else ("", "")


def calculate_mass_percentage(formula, element):
    """ Calculate the mass percentage of an element in a chemical formula. """
    
    def parse_formula(formula):
        """ Parse the chemical formula into a dictionary of elements and their counts. """
        
        elements_counts = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
        return {element: int(count) if count else 1 for element, count in elements_counts}
    
    # Parse the formula
    formula_dict = parse_formula(formula)
    
    # Calculate the total molecular mass
    total_mass = sum(atom_mass_table[el] * count for el, count in formula_dict.items())
    
    # Calculate the mass of the specified element
    element_mass = atom_mass_table[element] * formula_dict.get(element, 0)
    
    # Calculate the mass percentage
    mass_percentage = (element_mass / total_mass) * 100
    
    return mass_percentage


def pubchem_search(file, sleep_time=1):
    """
    Searches PubChem database to fill missing information in a given Excel file.

    Args:
        file (str): The path to the Excel file.

    Returns:
        pandas.DataFrame: The updated DataFrame with missing information filled.

    The function reads an Excel file and searches PubChem using the InChIKey (ik) column
    to retrieve missing information such as compound name, formula, CAS number, and SMILES.

    If a compound's name, formula, or CAS number is missing, the function queries PubChem using
    the provided InChIKey and retrieves the information if available.

    Example:
        updated_data = pubchem_search('data.xlsx')
        print(updated_data.head())
    """
    
    import pubchempy as pcp
    df = pd.read_excel(file)
    
    # Ensure these columns exist
    for column in ['name', 'formula', 'CAS', 'Smile']:
        if column not in df.columns:
            df[column] = np.nan
    
    query_num = 0
    response_num = 0
    
    try:
        for i in tqdm(range(len(df)), desc='Searching in pubchem'):
            time.sleep(sleep_time)
            name, formula, cas, smile, ik = df.loc[i, ['name', 'formula', 'CAS', 'Smile', 'ik']]
            
            if pd.isna(name) or pd.isna(formula) or pd.isna(cas) or pd.isna(smile):
                query_num += 1
                try:
                    cmp_all = pcp.get_compounds(ik, namespace='inchikey')
                    cmp = cmp_all[0] if cmp_all else None
                    if cmp:
                        synonyms = cmp.synonyms
                        new_smi = cmp.isomeric_smiles
                        new_formula = cmp.molecular_formula
                        cas_number = None
                        first_name = None
                        
                        for item in synonyms:
                            if re.match(r'^\d{2,}-\d{2,}-\d{1,}$', item) and not cas_number:
                                cas_number = item
                            elif not re.match(r'^\d{2,}-\d{2,}-\d{1,}$', item) and not first_name:
                                first_name = item
                            if cas_number and first_name:
                                break
                        
                        df.loc[i, ['name', 'formula', 'Smile', 'CAS']] = first_name, new_formula, new_smi, cas_number
                        response_num += 1
                except Exception as e:
                    print(f"Error at index {i}: {e}")
    
    except (KeyboardInterrupt, TimeoutError):
        print("Interrupted! Returning partial results.")
    
    print(
        f'Total query number = {query_num}; Total response number = {response_num}, Response rate = {round(response_num / query_num * 100, 2) if query_num else 0} %')
    return df


def get_correction_factor_waters(file, lock_mass=556.2771):
    """
    Calculate the correction factor for Waters LC-TOF-MS data based on the lockmass value.

    Parameters:
    - file (str): Path to the mzML file containing the LC-TOF-MS data.
    - lockmass (float, optional): The lockmass value used for correction. Default values are
      556.2771 for positive mode and 554.2615 for negative mode.

    Returns:
    tuple: A tuple containing two elements:
        - factor_median (float): The median of the calculated correction factors.
        - factor_mean (float): The mean of the calculated correction factors.

    The function reads the provided mzML file, identifies the lockmass peaks, and calculates the
    correction factors for mass-to-charge (m/z) values. The median and mean of these factors are
    then returned.
    """
    run = pymzml.run.Reader(file)
    function_nums = [scan.id_dict['function'] for scan in run]
    func_num_max = max(function_nums)
    lockspray = [scan for scan in run if scan.id_dict['function'] == func_num_max]
    mz_corr_factors = []
    for scan in lockspray:
        mz, intensity = scan.mz, scan.i
        s = pd.Series(data=intensity, index=mz)
        if len(s) == 0:
            pass
        else:
            s1 = s.loc[(s.index > lock_mass - 0.2) & (s.index < lock_mass + 0.2)]
            lockmass_obs = s1.idxmax()
            factor = lock_mass / lockmass_obs
            mz_corr_factors.append(factor)
    factor_median = np.median(mz_corr_factors)
    factor_mean = np.mean(mz_corr_factors)
    return factor_median, factor_mean


def compare_ms_spectra(spec_db, spec_obs, error=0.015):
    """
    Calculate the matching score between two mass spectrometry spectra.

    This function computes a similarity score based on the overlap and difference in intensity values
    between a reference spectrum (spec_db) and an observed spectrum (spec_obs) within a specified
    mass error tolerance (error).

    Args:
        spec_db (pandas.Series): The reference spectrum, with mass-to-charge ratios as index and intensity values as data.
        spec_obs (pandas.Series): The observed spectrum to compare, formatted like `spec_db`.
        error (float, optional): The mass error tolerance for matching peaks in the spectra. Default is 0.015.

    Returns:
        float: A similarity score ranging from 0 (no match) to 1 (perfect match) between the two spectra.
    """
    s1 = spec_db
    s2 = spec_obs
    s_all = []
    for index in s1.index:
        s = s2[(s2.index > index - error) & (s2.index < index + error)]
        if len(s) != 0:
            s_all.append(s.sort_values(ascending=False).head(1))
        else:
            s_all.append(pd.Series(index=[index], data=[0]))
    s2_new = pd.concat(s_all)
    
    s1_nor = s1 / max(s1.values)
    index_max = s2_new.sort_values(ascending=False).head(1).index[0]
    index_value = s1_nor.values[np.argmin(abs(s1_nor.index.values - index_max))]
    s2_nor = s2_new / max(s2_new) * index_value if max(s2_new) != 0 else s2_new
    if max(s2_new) == 0:
        score = 0
    else:
        diff = sum([abs(s1_nor.values[i] - s2_nor.values[i]) for i in range(len(s1_nor))]) / s1_nor.sum()
        score = 1 - diff
    return score


def one_step_process_ms2(path, company, profile=True, control_group=['lab_blank', 'methanol'], threshold=10,
                         i_threshold=500, SN_threshold=3,
                         area_threshold=500, height_threshold=500, rt_error_alignment=0.1, mz_error_alignment=0.015,
                         mz_overlap=1,
                         split_n=20, peak_width=1, filter_type=1, sat_intensity=False, long_rt_split_n=1, rt_overlap=1,
                         step_size=0.02,
                         isotope_analysis=True, orbi=False, noise_threshold=0):
    """
    Processes mzML data in a single-step procedure that includes peak picking and data comparison
    between sample and control groups, and generates an Excel summary of the differences. This
    function handles both MS1 and MS2 data processing.

    Args:
        path (str): File path for the mzML files to be processed, e.g., '../Users/Desktop/my_HRMS_files'.
        company (str): Manufacturer of the mass spectrometer, e.g., 'Waters', 'Thermo', 'Sciex', 'Agilent'.
        profile (bool): True if data is in profile mode, False for centroid mode.
        control_group (list[str]): Labels identifying the control group files.
        peak_width (int): The expected width of peaks used in peak detection algorithms.
        threshold (int): Intensity threshold for peak detection.
        filter_type (int): Operational mode for data analysis.
            - 1: Computes fold change as the ratio of the sample area to the maximum control area.
            - 2: For data with triplicates, calculates p-values and fold change as the ratio of
              mean sample area to mean control area.
        split_n (int): Number of segments to split the dataframe for processing.
        sat_intensity (bool): Adjusts for saturation intensity in peak measurements.
        long_rt_split_n (int): Number of segments for handling long retention times.
        orbi (bool): True for Orbitrap data, False for Time-of-Flight (TOF) data.

    Returns:
        None: Outputs Excel files summarizing differences between control and sample sets.

    Note:
        Ensure the mzML and Excel handling libraries are installed and properly configured. Calls
        several other functions (`first_process_ms2`, `second_process_ms2`, etc.) that need to be defined
        and correctly functioning for this script to work.




        def first_process(file, company, profile=True, control_group=['methanol_blank', 'control', 'lab_blank'], threshold=10,
                  i_threshold=200, SN_threshold=3,peak_width=1,area_threshold = 500,height_threshold = 500,rt_error_alignment=0.05,
                  mz_error_alignment=0.015, mz_overlap=1,ms2_analysis=True, frag_rt_error=0.02, split_n=20, sat_intensity=False,
                  long_rt_split_n=1,rt_overlap=1,step_size = 0.02,orbi=False, message = '',max_frag_num = 50)
    """
    
    move_files(path)
    # Log function details
    func_name = inspect.currentframe().f_code.co_name
    func_params = inspect.getargvalues(inspect.currentframe()).locals
    log_function_details(path, func_name, func_params)
    print('                                                                            ')
    print('============================================================================')
    print('First process...')
    print('============================================================================')
    print('                                                                            ')
    
    files_mzml = glob(os.path.join(path, '*.mzML'))
    
    files_mzml = [file for file in files_mzml if 'DDA' not in os.path.basename(file)]
    for j, file in enumerate(files_mzml):
        ms1, ms2 = sep_scans(file, company=company, message=f'No. {j + 1}_ms2 : ')
        # 针对ms1进行处理
        peak_all1 = ultimate_peak_picking(ms1, profile=profile, split_n=split_n, threshold=threshold,
                                          i_threshold=i_threshold, SN_threshold=SN_threshold,
                                          peak_width=peak_width, area_threshold=area_threshold,
                                          height_threshold=height_threshold,
                                          noise_threshold=noise_threshold, rt_error_alignment=rt_error_alignment,
                                          mz_error_alignment=mz_error_alignment,
                                          mz_overlap=mz_overlap, sat_intensity=sat_intensity,
                                          long_rt_split_n=long_rt_split_n, rt_overlap=rt_overlap,
                                          orbi=orbi, step_size=step_size, message=f'No. {j + 1}_ms1 : ',
                                          isotope_analysis=isotope_analysis)
        peak_all1.to_excel(file.replace('.mzML', '.xlsx'))
        # 针对ms2进行处理
        peak_all2 = ultimate_peak_picking(ms2, profile=profile, split_n=split_n, threshold=threshold,
                                          i_threshold=i_threshold, SN_threshold=SN_threshold,
                                          peak_width=peak_width, area_threshold=area_threshold,
                                          height_threshold=height_threshold,
                                          noise_threshold=noise_threshold, rt_error_alignment=rt_error_alignment,
                                          mz_error_alignment=mz_error_alignment,
                                          mz_overlap=mz_overlap, sat_intensity=sat_intensity,
                                          long_rt_split_n=long_rt_split_n, rt_overlap=rt_overlap,
                                          orbi=orbi, step_size=step_size, message=f'No. {j + 1}_ms2 : ',
                                          isotope_analysis=isotope_analysis)
        peak_all2.to_excel(file.replace('.mzML', '_ms2_data.xlsx'))
    
    # 中间过程
    files_excel = glob(os.path.join(path, '*.xlsx'))
    peak_alignment(files_excel)
    ref_all = pd.read_excel(os.path.join(path, 'peak_ref.xlsx'), index_col='Unnamed: 0')
    
    # 第二个过程
    print('                                                                            ')
    print('============================================================================')
    print('Second process...')
    print('============================================================================')
    print('                                                                            ')
    for j, file in enumerate(files_mzml):
        ms1, ms2 = sep_scans(file, company, message=f'No. {j + 1}_ms2 : ')
        name1 = os.path.basename(file).split('.mzML')[0]
        # 　处理ms1
        final_result1 = ultimate_checking_area(ref_all, ms1, name1, profile=profile,
                                               rt_overlap=1, long_rt_split_n=long_rt_split_n, orbi=orbi,
                                               message=f'No. {j + 1}_ms2 : ')
        final_result1.to_excel(file.replace('.mzML', '_final_area.xlsx'))
        # 　处理ms2
        final_result2 = ultimate_checking_area(ref_all, ms2, name1, profile=profile,
                                               rt_overlap=1, long_rt_split_n=long_rt_split_n, orbi=orbi,
                                               message=f'No. {j + 1}_ms2 : ')
        final_result2.to_excel(file.replace('.mzML', '_ms2_data_final_area.xlsx'))
    
    # 第三个过程, 做fold change filter
    print('                                                                            ')
    print('============================================================================')
    print('Third process...')
    print('============================================================================')
    print('                                                                            ')
    
    # 创建文件夹路径
    ms1_path = os.path.join(path, 'data_for_ms1')
    ms2_path = os.path.join(path, 'data_for_ms2')
    # 创建文件夹
    if not os.path.exists(ms1_path):
        os.makedirs(ms1_path)
    if not os.path.exists(ms2_path):
        os.makedirs(ms2_path)
    
    # 先把ms2的文件的弄进去
    excel_files = glob(os.path.join(path, '*.xlsx'))
    ms2_names = ['_ms2_data.xlsx', '_ms2_data_alignment.xlsx', '_ms2_data_final_area.xlsx']
    for file in excel_files:
        if any([file.endswith(name) for name in ms2_names]):
            shutil.move(file, os.path.join(ms2_path, os.path.basename(file)))
    
    # 再把剩下所有的弄进去
    excel_files = glob(os.path.join(path, '*.xlsx'))
    for file in excel_files:
        shutil.move(file, os.path.join(ms1_path, os.path.basename(file)))
    
    # 分批处理fold change
    fold_change_filter(ms1_path, control_group=control_group, filter_type=filter_type)
    fold_change_filter(ms2_path, control_group=control_group, filter_type=filter_type)


def log_function_details(path, func_name, func_params):
    """
    Logs the function name and its parameters to a text file named "Processing parameters.txt".

    Args:
        path (str): The path where the log file will be saved.
        func_name (str): The name of the function.
        func_params (dict): The parameters and their values.
    """
    file_path = os.path.join(path, "Processing parameters.txt")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(file_path, 'w') as file:
        file.write(f"Function Name: {func_name}\n")
        file.write(f"Processing Date and Time: {current_time}\n")
        file.write("Parameters:\n")
        for key, value in func_params.items():
            file.write(f"{key}: {value}\n")


def convert_df_to_mgf(df, output_path, ms2_info_column, charge, max_num=None):
    """
    Converts a DataFrame containing MS2 spectra information into an MGF (Mascot Generic Format) file.

    Args:
        df (DataFrame): DataFrame containing unique compounds and their associated MS2 spectra. Each row represents a unique compound.
        output_path (str): The path where the resulting MGF file will be saved.
        ms2_info_column (str): Column name in the DataFrame where MS2 spectrum information is stored. This column should contain data structured as series.
        charge (int): Precursor charge state (e.g., 1, -1) to be recorded in the MGF file.
        max_num (int, optional): Maximum number of spectra to include in the MGF file. If None, all spectra in the DataFrame will be included.

    Returns:
        None: The function writes an MGF file to the specified output path, containing the spectra data formatted according to the MGF specifications.

    Note:
        The function relies on the DataFrame structure where each row contains MS2 data for different compounds, including retention time ('rt'), precursor m/z ('mz'), and intensity values.
    """
    
    def create_mgf_file(spectra, file_name=output_path):
        with open(file_name, 'w') as file:
            for spectrum in spectra:
                file.write("BEGIN IONS\n")
                file.write(f"TITLE={spectrum['title']}\n")
                pepmass = spectrum['pepmass'][0] if spectrum['pepmass'][
                                                        1] is None else f"{spectrum['pepmass'][0]} {spectrum['pepmass'][1]}"
                file.write(f"PEPMASS={pepmass}\n")
                file.write(f"CHARGE={spectrum['charge']}+\n")
                if 'rtinseconds' in spectrum:
                    file.write(f"RTINSECONDS={spectrum['rtinseconds']}\n")
                for mz, intensity in zip(spectrum['mz_values'], spectrum['intensities']):
                    file.write(f"{mz} {intensity}\n")
                file.write("END IONS\n")
    
    spectra = []
    for i in tqdm(range(len(df))):
        s1 = eval2(df.loc[i, ms2_info_column])
        
        if len(s1) != 0:
            mz_list = list(s1.index)
            intensities = list(s1.values)
            rt_in_second = df.loc[i, 'rt'] * 60
            precursor = df.loc[i, 'mz']
            dict2 = {
                'title': f'MS/MS_of_{precursor},_{charge}_at_{round(rt_in_second / 60, 3)}min',
                'pepmass': (precursor, None),  # (precursor m/z, intensity)
                'charge': charge,  # Precursor charge state
                'mz_values': mz_list,
                'intensities': intensities,
                'rtinseconds': rt_in_second  # Optional retention time in seconds
            }
            spectra.append(dict2)
    if max_num is None:
        create_mgf_file(spectra)
    else:
        create_mgf_file(spectra[:max_num])


def move_files(path):
    """
    Move files from the given directory to a new subdirectory named 'other_files_<timestamp>'.

    This function creates a new subdirectory with the current timestamp in its name and moves all files
    (except those with a .mzML extension) from the given directory to the new subdirectory. If a file
    cannot be moved (e.g., because it is open), an error message will be printed.

    Args:
        path (str): The path to the directory containing the files to be moved.

    Returns:
        None
    """
    # Get the current date and time
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Create a new folder name
    new_folder_name = f"other_files_{current_time}"
    new_folder_path = os.path.join(path, new_folder_name)
    
    # Create the new folder
    os.makedirs(new_folder_path, exist_ok=True)
    
    # Iterate over all files and folders in the path
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        
        # If it is a file and not a folder, and the file extension is not .mzML
        if os.path.isfile(item_path) and not item.endswith(".mzML"):
            try:
                # Move the file to the new folder
                shutil.move(item_path, new_folder_path)
            except Exception as e:
                print(f"Error: Unable to move '{item}'. It may be open. Details: {e}")


def fingerprints_generation(data_all, index_dict, source_info, fold_change=5, area_threshold=5000, blank_names=None):
    '''
    Generates unique molecular fingerprints for each source by identifying significant and source-specific peak areas.

    Parameters:
    ----------
    data_all : DataFrame
        A DataFrame containing the concatenated peak areas for all compounds across multiple samples.
        This should be generated using the `omics_final_area` function.
    index_dict : dict
        A dictionary mapping sample names to lists of unique indices, typically generated using the `omics_index_dict` function.
    source_info : dict
        A dictionary where keys are source names and values are lists of sample names corresponding to that source.
        Example:
        source_info = {'WWTP': ['LC-2024-3-18-pos-WWTP-100'],
            'ROAD Runoff': ['LC-2024-3-18-pos-ROAD-100'],
            'Drug Wastewater': ['LC-2024-3-18-pos-Drug-100']}
    fold_change : float, optional, default=5
        The minimum fold change required for a compound's peak area in the target source to be considered significantly
        greater than its peak areas in other sources or blanks.
    area_threshold : float, optional, default=5000
        The minimum peak area required for a compound to qualify as a unique fingerprint.
    blank_names : list, optional
        A list of sample names corresponding to blank samples. These are treated as additional sources when identifying
        unique fingerprints.

    Returns:
    -------
    target_source_fp : dict
        A dictionary where each key is a source name, and the value is a list of unique fingerprint indices for that source.
        The fingerprints meet the specified fold change and area threshold criteria.
    '''
    
    target_source_fp = {}
    for source_name, source in source_info.items():
        # 1. 获得其他源的信息
        other_sources = []
        for other_source_name, other_source in source_info.items():
            if other_source_name != source_name:
                other_sources.extend(other_source)
        if blank_names is not None:
            other_sources.extend(blank_names)
        
        # 2. 现在index_dict合并本身的源
        source_new_index = list(set([i for j in source for i in index_dict[j]]))
        # 3. 现在合并其他源
        other_source_index = list(set([i for j in other_sources for i in index_dict[j]]))
        # 4.找到只在这个源有，其他源没有的
        source_fp = np.setdiff1d(np.array(source_new_index), np.array(other_source_index))
        # 5. 比较污染源中，要比其他所有源包括空白，峰面积大于fold change的
        index_compare = data_all.loc[source_fp, source].min(axis=1) > data_all.loc[source_fp, other_sources].max(
            axis=1) * fold_change
        final_area_df_min = data_all.loc[source_fp, source][index_compare].min(axis=1)  # 获得分子指纹最小值
        # 5 峰面积最小值要大于area_threshold
        fps = final_area_df_min[final_area_df_min > area_threshold].index.values
        target_source_fp[source_name] = fps
    return target_source_fp


def fingerprints_application(data_all, index_dict, source_fps, source_info, target_sample_names=[]):
    '''
    Identifies the source composition of target samples by comparing their peak areas to fingerprints from various sources.

    Parameters:
    ----------
    data_all : DataFrame
        A DataFrame containing concatenated final peak areas for all compounds across multiple samples.
        This data should be generated using the `omics_final_area` function.
    index_dict : dict
        A dictionary mapping each sample name to a list of unique indices.
        Typically generated using the `omics_index_dict` function.
    source_fps : dict
        A dictionary of source fingerprints, where each key is a source name and each value is a list of fingerprint indices.
        This should be generated using the `fingerprints_generation` function.
    source_info : dict
        A dictionary that maps source names to their corresponding sample file names.
        Example:
        source_info = {
            'WWTP': ['LC-2024-3-18-pos-WWTP-100', 'LC-2024-3-18-pos-WWTP-40'],
            'ROAD Runoff': ['LC-2024-3-18-pos-ROAD-100', 'LC-2024-3-18-pos-ROAD-40'],
            'Drug Wastewater': ['LC-2024-3-18-pos-Drug-100', 'LC-2024-3-18-pos-Drug-40']
        }
    target_sample_names : list, optional
        A list of target sample names for which the source composition is to be identified.
        These names must correspond to entries in `index_dict` and `data_all`.
        If left empty, the function will prompt the user to provide valid sample names.

    Returns:
    -------
    result_info : dict
        A dictionary where each key represents a target sample, and the value is a nested dictionary containing:
            - `common_fps`: The indices of common fingerprints between the target sample and the source.
            - `num`: The number of common fingerprints.
            - `correlation_info`: A dictionary of correlation coefficients and p-values for peak areas between the target sample
              and the source samples.

    Notes:
    -----
    - If `target_sample_names` is not provided or is empty, the function will print a message prompting the user to provide them.
    - The correlation information includes Pearson correlation coefficients and p-values between the peak areas of the target
      sample and the source samples.
    '''
    
    result_info = {}
    if len(target_sample_names) == 0:
        print(r'Please input the target_sample_names')
    else:
        for target_sample_name in target_sample_names:
            sample_info = {}
            for source_name, target_source_fp in source_fps.items():
                source_composition_info = {}
                common_index_in_name = np.intersect1d(target_source_fp, index_dict[target_sample_name])
                source_composition_info['common_fps'] = common_index_in_name  # 1. 获得source_fp信息
                source_composition_info['num'] = len(common_index_in_name)
                # 这里要用source_info[source_name]找到当初建立指纹的文件名称，才能获得峰面积
                data_area = data_all.loc[common_index_in_name, [target_sample_name] + source_info[source_name]]
                
                if len(data_area) > 10:
                    corr_info = {}
                    sample_area = data_area.iloc[:, 0].values
                    for n1 in range(len(data_area.columns) - 1):
                        source_file_name = data_area.columns[n1 + 1]
                        source_area = data_area.iloc[:, n1 + 1].values
                        pearsonr_result = pearsonr(source_area, sample_area)
                        corr = round(pearsonr_result[0], 2)
                        p_value = "{:.2e}".format(pearsonr_result[1])
                        corr_info[source_file_name] = [corr, p_value]
                else:
                    corr_info = {}
                source_composition_info['correlation_info'] = str(corr_info)  # 2. correlation
                sample_info[f'{source_name}_origin'] = source_composition_info
            result_info[f'{target_sample_name}_composition'] = sample_info
    return result_info


def fingerprints_generation_precursor_frag(sources, source_names, ms1_error=0.01, ms2_error=0.015):
    """
    Generate fingerprints for each source by comparing them with each other.

    Args:
        sources (list): A list of source information arrays generated by
                        `swath_extract_precursor_frag_info`. These arrays should have been
                        compared to blanks and filtered with appropriate fold changes.
        source_names (list): A list of names corresponding to each source.
        ms1_error (float, optional): Tolerance for precursor mass error. Default is 0.01.
        ms2_error (float, optional): Tolerance for fragment mass error. Default is 0.015.

    Returns:
        dict: A dictionary mapping each source name to its generated fingerprints.
    """
    
    sources = [i if isinstance(i, np.ndarray) else np.array(i) for i in sources]
    source_ids = [i for i in range(len(sources))]
    new_source_fps = []
    for source_id in source_ids:
        other_sources_ids = [i for i in source_ids if i != source_id]
        source = sources[source_id]
        source = drop_duplicate_precursor_frag_pair(source, ms1_error=ms1_error, ms2_error=ms2_error)  # 去除重复的
        for other_source_id in other_sources_ids:
            other_source = sources[other_source_id]
            updated_source = []
            for pair in tqdm(source, desc=f'Update source {source_id + 1}', leave=False):
                precursor, frag = pair[1], pair[2]
                matched_result = other_source[(other_source[:, 1] > precursor - ms1_error
                                               ) & (other_source[:, 1] < precursor + ms1_error
                                                    ) & (other_source[:, 2] > frag - ms1_error
                                                         ) & (other_source[:, 2] < frag + ms1_error)]
                if len(matched_result) == 0:
                    updated_source.append(pair)
            source = updated_source
        new_source_fps.append(source)
    fp_result = dict(zip(source_names, new_source_fps))
    return fp_result


def fingerprints_precursor_frag_application(source_fps, sample_info_list, sample_name_list, ms1_error=0.01,
                                            ms2_error=0.015):
    """
    Apply source fingerprints to identify their presence in each sample and return results,
    including common fingerprints, correlation, and p-value.

    Args:
        source_fps (dict): Source fingerprints generated by `fingerprints_generation_precursor_frag`.
        sample_info_list (list): A list of sample information arrays generated by
                                 `swath_extract_precursor_frag_info`. Ensure that these arrays
                                 are compared to blanks using appropriate fold changes.
        sample_name_list (list): A list of names corresponding to each sample.
        ms1_error (float, optional): Tolerance for precursor mass error. Default is 0.01.
        ms2_error (float, optional): Tolerance for fragment mass error. Default is 0.015.

    Returns:
        dict: A dictionary containing fingerprint matches, correlation values, and p-values
              for each sample composition.
    """
    
    sample_info_list = [i if isinstance(i, np.ndarray) else np.array(i) for i in sample_info_list]
    final_result = {}
    for index, sample_info in enumerate(sample_info_list):
        sample_info = drop_duplicate_precursor_frag_pair(sample_info, ms1_error=ms1_error, ms2_error=ms2_error)
        sample_info = np.array(sample_info) if isinstance(sample_info, list) else sample_info
        source_matched_pairs = {}
        for k, v in source_fps.items():
            matched_pairs_info = {}
            matched_pairs = []
            for pair in tqdm(v, desc=f'Matching for source {k}', leave=False):
                precursor, frag = pair[1], pair[2]
                sample_info1 = sample_info[(sample_info[:, 1] > precursor - ms1_error
                                            ) & (sample_info[:, 1] < precursor + ms1_error
                                                 ) & (sample_info[:, 2] > frag - ms1_error
                                                      ) & (sample_info[:, 2] < frag + ms1_error)]
                
                if len(sample_info1) > 1:
                    sample_info1 = sample_info1[sample_info1[:, -1].argsort()][-1]
                    matched_pairs.append([pair, list(sample_info1)])
                elif len(sample_info1) == 1:
                    matched_pairs.append([pair, list(sample_info1[0])])
            matched_pairs_info['common_fps_pairs'] = matched_pairs
            # calculate pearsonr relationship
            x = [i[0][-1] for i in matched_pairs]
            y = [i[1][-1] for i in matched_pairs]
            if len(x) < 10:
                corr, p_value = '-', '-'
            else:
                corr, p_value = pearsonr(x, y)
                corr = round(corr, 2)
                p_value = "{:.2e}".format(p_value)
            matched_pairs_info['correlation'] = corr
            matched_pairs_info['p_value'] = p_value
            source_matched_pairs[k] = matched_pairs_info
        final_result[f'{sample_name_list[index]}_composition'] = source_matched_pairs
    return final_result


def drop_duplicate_precursor_frag_pair(precursor_frag_info, ms1_error=0.01, ms2_error=0.015):
    """
    Remove duplicate precursor-fragment pairs from the given information.

    Args:
        precursor_frag_info (array-like): Precursor and fragment information array generated
                                          by `swath_extract_precursor_frag_info`.
        ms1_error (float, optional): Tolerance for precursor mass error. Default is 0.01.
        ms2_error (float, optional): Tolerance for fragment mass error. Default is 0.015.

    Returns:
        list: A list of unique precursor-fragment pairs.
    """
    
    if isinstance(precursor_frag_info, list):
        precursor_frag_info = np.array(precursor_frag_info)
    data = precursor_frag_info[:, [1, 2]]
    aligned_data = gen_ref_precursor_frag(data, ms1_error=ms1_error, ms2_error=ms2_error)
    precursor_frag_fp = []
    for pair in tqdm(aligned_data, desc='Align precursor & frags', leave=False):
        precursor, frag = pair
        matched_result = precursor_frag_info[(precursor_frag_info[:, 1] < precursor + ms1_error
                                              ) & (precursor_frag_info[:, 1] > precursor - ms1_error
                                                   ) & (precursor_frag_info[:, 2] < frag + ms2_error
                                                        ) & (precursor_frag_info[:, 2] > frag - ms2_error)]
        if (len(matched_result) == 1) & (matched_result[0][1] > matched_result[0][2] + 5):  # 如果有重复的峰，就先不要？
            precursor_frag_fp.extend(matched_result)
    return [list(i) for i in precursor_frag_fp]


def gen_ref_precursor_frag(data, ms1_error=0.01, ms2_error=0.015):
    """
    Align precursor and fragment data to generate a reference set of unique pairs.

    Args:
        data (np.array): A 2D array containing precursor and fragment data.
        ms1_error (float, optional): Tolerance for precursor mass error. Default is 0.01.
        ms2_error (float, optional): Tolerance for fragment mass error. Default is 0.015.

    Returns:
        np.array: An array of unique aligned precursor-fragment pairs.
    """
    
    # Scale the tolerances relative to the range of each dimension
    rt_range = np.ptp(data[:, 0])
    mz_range = np.ptp(data[:, 1])
    scaled_ms1_tol = ms1_error / rt_range
    scaled_ms2_tol = ms2_error / mz_range
    
    # Create a KDTree with scaled data
    scaled_data = np.copy(data)
    scaled_data[:, 0] /= rt_range
    scaled_data[:, 1] /= mz_range
    tree = KDTree(scaled_data)
    
    reference_list = []
    visited = set()
    
    for idx, scaled_pair in tqdm(enumerate(scaled_data), desc='Aligning all rt_mz pairs(precursor_frag)', leave=False,
                                 colour='Green'):
        if idx in visited:
            continue
        
        # Find neighbors within a spherical range that's sure to encompass the rectangular range
        neighbors = tree.query_ball_point(scaled_pair, r=max(scaled_ms1_tol, scaled_ms2_tol))
        
        # Filter these neighbors based on the actual tolerances
        filtered_neighbors = [i for i in neighbors if abs(data[i, 0] - data[idx, 0]) <= ms1_error
                              and abs(data[i, 1] - data[idx, 1]) <= ms2_error]
        
        # Mark these neighbors as visited and add the first one to the reference list
        visited.update(filtered_neighbors)
        reference_list.append(data[idx])
    
    return np.array(reference_list)


def swath_extract_precursor_frag_info(df, i_threshold=1000, fold_change=5):
    """
    Extract precursor and fragment information from a DataFrame based on intensity
    threshold and fold change.

    Args:
        df (DataFrame): A DataFrame containing the results from unique compound files.
        i_threshold (int, optional): Intensity threshold for filtering fragments. Default is 1000.
        fold_change (int, optional): Fold change value for comparison with blanks. Default is 5.

    Returns:
        list: A list of extracted precursor-fragment information.
    """
    
    df = df[(df.loc[:, [i for i in df.columns if 'fold_change' in i]] > fold_change).all(axis=1)].reset_index(drop=True)
    info = []
    for i in range(len(df)):
        rt = df.loc[i, 'rt']
        mz = df.loc[i, 'mz']
        dict_column_name = [i for i in df.columns if '_dict' in i][0]
        ms2_spectra_dict = eval(df.loc[i, dict_column_name])
        if len(ms2_spectra_dict) > 0:
            s1 = pd.Series(ms2_spectra_dict)
            s2 = s1[s1 > i_threshold]
            s3 = s2[s2.index < mz]
            cmp_info = [[rt, mz, s1.index[i], s1.values[i]] for i in range(len(s1))]
            info.extend(cmp_info)
    return info


def fingerprints_precursor_frag_draw(path, result):
    for sample, sample_info in tqdm(result.items()):
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        colors = [None, 'r', 'g', 'm']
        i = 0
        for source_name, source_info in sample_info.items():
            pairs = source_info['common_fps_pairs']
            corr = source_info['correlation']
            p_value = source_info['p_value']
            x = [i[1][1] for i in pairs]
            y = [i[1][2] for i in pairs]
            num = len(pairs)
            ax.scatter(x, y, color=colors[i], s=50, alpha=0.8, edgecolor='k',
                       label=f'{source_name}(Num:{num},Corr:{corr},p_value:{p_value})')
            ax.set_xlabel('Precursor (m/z)')
            ax.set_ylabel('Fragments (m/z)')
            ax.set_xlim([0, 800])
            ax.set_ylim([0, 800])
            i += 1
        plt.title(sample)
        plt.legend(fontsize=10)
        file_path = os.path.join(path, f'{sample}.png')
        plt.savefig(file_path, dpi=300)
        plt.close('all')


def fingerprints_draw(path, result_info):
    for sample_name, info1 in tqdm(result_info.items()):
        sample_name1 = sample_name.replace('__composition', '')
        fig = plt.figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        colors = [None, 'r', 'g', 'm']
        i = 0
        for source_name, info2 in info1.items():
            source_name1 = source_name.replace('__origin', '')
            rts = [eval(i.split('_')[0]) for i in info2['common_fps']]
            mzs = [eval(i.split('_')[1]) for i in info2['common_fps']]
            num = info2['num']
            corr = info2['correlation']
            p_value = info2['p_value']
            
            ax.scatter(rts, mzs, color=colors[i], s=50, alpha=0.8, edgecolor='k',
                       label=f'{source_name1}(Num:{num},Corr:{corr},p_value:{p_value})')
            ax.set_xlabel('Retention time (min)')
            ax.set_ylabel('m/z')
            ax.set_xlim([0, 23])
            ax.set_title(sample_name1)
            i += 0
        plt.legend(fontsize=5)
        file_path = os.path.join(path, f'{sample_name1}.png')
        plt.savefig(file_path, dpi=300)
        plt.close('all')


# ========================================================================
# 定量溯源组件
# ========================================================================

# 模型函数
def linear_model(x, a, b):
    return a * x + b


def quadratic_model(x, a, b, c):
    return a * x ** 2 + b * x + c


def calculate_r2(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)


def inverse_linear(y, a, b):
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero for linear inversion.")
    return round((y - b) / a, 4)


def inverse_quadratic(y, a, b, c):
    discriminant = b ** 2 - 4 * a * (c - y)
    if discriminant < 0:
        # print(f"Warning: No real solution for peak area {y:.2f}.")
        return np.nan
    root1 = round((-b + np.sqrt(discriminant)) / (2 * a), 4)
    root2 = round((-b - np.sqrt(discriminant)) / (2 * a), 4)
    return root1 if root1 > 0 else root2

def fit_model(concentration, peak_area, model='linear', weight='1/x'):
    concentration = np.array(concentration)
    peak_area = np.array(peak_area)
    
    if weight == '1/x':
        sigma = 1 / (concentration + 1e-10)
    elif weight == '1/x^2':
        sigma = 1 / (concentration ** 2 + 1e-10)
    else:
        sigma = None
    
    if model == 'linear':
        initial_guess = [1.0, 0.0]
        try:
            popt, pcov = curve_fit(
                linear_model, concentration, peak_area, p0=initial_guess,
                sigma=sigma, absolute_sigma=True, maxfev=10000
            )
            fit_func = lambda x: linear_model(x, *popt)
            inverse_func = lambda y: inverse_linear(y, *popt)
        except RuntimeError as e:
            print(f"Error: {e}. Try adjusting initial parameters or weights.")
            return None, None, None, None, None

    elif model == 'quadratic':
        initial_guess = [0.0, 1.0, 0.0]
        try:
            popt, pcov = curve_fit(
                quadratic_model, concentration, peak_area, p0=initial_guess,
                sigma=sigma, absolute_sigma=True, maxfev=10000
            )
            fit_func = lambda x: quadratic_model(x, *popt)
            inverse_func = lambda y: inverse_quadratic(y, *popt)
        except RuntimeError as e:
            print(f"Error: {e}. Try adjusting initial parameters or weights.")
            return None, None, None, None, None

    else:
        raise ValueError("Model must be 'quadratic' or 'linear'")

    y_pred = fit_func(concentration)
    r2 = calculate_r2(peak_area, y_pred)

    return fit_func, popt, r2, inverse_func, lambda areas: [inverse_func(area) for area in areas]


def generate_source_apportionment_calibration_info(groups, data_all, index_dict, fold_change=10, area_threshold=5000,
                                                   r2_threshold=0.98):
    """
    Generate source apportionment calibration information based on pollution source dilution curves.

    This function processes provided pollution source data to generate calibration curves for
    source apportionment. It follows these main steps:

    1. Identify pollution sources from the given group data.
    2. Extract sources with 100% concentration as reference points.
    3. Identify control (blank) groups if available.
    4. Generate qualitative fingerprints using the extracted source data.
    5. Compute dilution curves for each identified source and evaluate calibration performance.

    Args:
        groups (dict): A dictionary mapping pollution sources to their respective dilution curve data.
                       - Positive values represent dilution curve concentrations.
                       - `-1` indicates control groups.
                       - `-2` indicates sample groups.
        data_all (pd.DataFrame): A DataFrame containing peak area data indexed by compound identifiers.
        index_dict (dict): A dictionary mapping compound identifiers to their corresponding indices.
        fold_change (int, optional): The minimum fold change for selecting significant features. Default is 10.
        area_threshold (int, optional): The minimum peak area required for a compound to be considered. Default is 5000.
        r2_threshold (float, optional): The minimum R² value for a valid calibration curve. Default is 0.98.

    Returns:
        dict: A nested dictionary containing calibration information for each pollution source.
              - Keys are source names.
              - Values are dictionaries mapping compound identifiers to their respective calibration curves.
                Each calibration curve entry includes:
                - `area_to_conc`: Function for converting peak area to concentration.
                - `conc_to_area`: Function for converting concentration to peak area.
                - `params`: Fitted model parameters.
                - `r2`: R² value of the fit.
                - `calculated_conc`: Predicted concentrations.
                - `calculated_conc_accuracy`: Accuracy of concentration predictions.
                - `length`: Number of data points used in calibration.
                - `type`: Model type (`linear` or `quadratic`).
                - `weight`: Weighting method used (`None` or `1/x`).

    Example:
        groups = {
            'Industrial Wastewater': {'Sample-0_1': 0.1, 'Sample-1': 1, 'Sample-2': 2, 'Sample-100': 100},
            'Control': {'Blank-0': -1, 'Blank-1': -1}
        }
        index_dict = {...}  # Dictionary mapping compound identifiers
        data_all = pd.DataFrame(...)  # DataFrame containing peak area data
        curve_info = generate_source_apportionment_calibration_info(groups, data_all, index_dict)
    """
    # 第1步： 选出污染源，
    source_group = {group: {k: v for k, v in items.items() if v >= 0} for group, items in groups.items()}
    source_group1 = {k: v for k, v in source_group.items() if len(v) > 0}
    
    # 第2步：找出污染源，这里需要要求用户，需要有100%的污染源，不然无法计算
    source_info = {}
    for k, v in source_group1.items():
        for k1, v1 in v.items():
            if v1 == 100:
                source_info[k] = [k1]
    
    # 第3步： 找到对照组，如果有的话。
    blank_names = []
    for k, v in source_group1.items():
        for k1, v1 in v.items():
            if v1 == -1:
                blank_names.append(k1)
    
    # 第4步：生成定性指纹
    fps = fingerprints_generation(data_all, index_dict, source_info, fold_change=fold_change,
                                  area_threshold=area_threshold, blank_names=blank_names)
    
    # 第5步：遍历污染源，生成污染源稀释曲线数据，并存储
    all_source_curve_info = {}
    for s1, s1_info in source_group1.items():
        curve_names = list(s1_info.keys())  # 获得污染稀释曲线文件名称
        curve_conc = np.array(list(groups[s1].values()))  # 获得污染稀释曲线浓度
        sourec_new_index = fps[s1]  # 获取污染源特征指纹化合物
        s1_df = data_all.loc[sourec_new_index, curve_names]  # 获得（1）该污染源（2）所有特征化合物的稀释曲线峰面积
        
        #  建立字典去一个个评估每个化合物
        curve_info_df_all = {}
        for index in tqdm(s1_df.index, desc=f'Evaluate all compounds for source: {s1}'):
            all_curve_info = []
            # 第一步，linear，weight None
            curve_conc = np.array(list(groups[s1].values()))  # 获得污染稀释曲线浓度
            peak_areas = s1_df.loc[index, curve_names].values
            while len(peak_areas) >= 4:
                fit_func, params, r2, inverse_func, predict_concentration = fit_model(curve_conc, peak_areas,
                                                                                      model='linear', weight=None)
                calculated_conc = predict_concentration(peak_areas)
                calculated_conc_accuracy = abs(calculated_conc - curve_conc) / curve_conc
                calculated_conc_accuracy = calculated_conc_accuracy.round(3)
                all_curve_info.append(
                    [inverse_func, fit_func, params, r2, calculated_conc, calculated_conc_accuracy, len(peak_areas),
                     'linear', 'None'])
                # 删除最高点（最后一个值）
                peak_areas = peak_areas[:-1]
                curve_conc = curve_conc[:-1]
            
            # 第二步，linear，weight 1/x
            curve_conc = np.array(list(groups[s1].values()))
            peak_areas = s1_df.loc[index, curve_names].values
            while len(peak_areas) >= 4:
                fit_func, params, r2, inverse_func, predict_concentration = fit_model(curve_conc, peak_areas,
                                                                                      model='linear', weight='1/x')
                calculated_conc = predict_concentration(peak_areas)
                calculated_conc_accuracy = abs(calculated_conc - curve_conc) / curve_conc
                calculated_conc_accuracy = calculated_conc_accuracy.round(3)
                all_curve_info.append(
                    [inverse_func, fit_func, params, r2, calculated_conc, calculated_conc_accuracy, len(peak_areas),
                     'linear', '1/x'])
                
                # 删除最高点（最后一个值）
                peak_areas = peak_areas[:-1]
                curve_conc = curve_conc[:-1]
            
            # 第三步，quadradic，weight None
            curve_conc = np.array(list(groups[s1].values()))
            peak_areas = s1_df.loc[index, curve_names].values
            while len(peak_areas) >= 4:
                fit_func, params, r2, inverse_func, predict_concentration = fit_model(curve_conc, peak_areas,
                                                                                      model='quadratic', weight=None)
                calculated_conc = predict_concentration(peak_areas)
                calculated_conc_accuracy = abs(calculated_conc - curve_conc) / curve_conc
                calculated_conc_accuracy = calculated_conc_accuracy.round(3)
                all_curve_info.append(
                    [inverse_func, fit_func, params, r2, calculated_conc, calculated_conc_accuracy, len(peak_areas),
                     'quadratic', 'None'])
                # 删除最高点（最后一个值）
                peak_areas = peak_areas[:-1]
                curve_conc = curve_conc[:-1]
            
            # 第四步，quadradic，weight 1/x
            curve_conc = np.array(list(groups[s1].values()))
            peak_areas = s1_df.loc[index, curve_names].values
            while len(peak_areas) >= 4:
                fit_func, params, r2, inverse_func, predict_concentration = fit_model(curve_conc, peak_areas,
                                                                                      model='quadratic', weight='1/x')
                calculated_conc = predict_concentration(peak_areas)
                calculated_conc_accuracy = abs(calculated_conc - curve_conc) / curve_conc
                calculated_conc_accuracy = calculated_conc_accuracy.round(3)
                all_curve_info.append(
                    [inverse_func, fit_func, params, r2, calculated_conc, calculated_conc_accuracy, len(peak_areas),
                     'quadratic', '1/x'])
                # 删除最高点（最后一个值）
                
                peak_areas = peak_areas[:-1]
                curve_conc = curve_conc[:-1]
            curve_info_df = pd.DataFrame(all_curve_info)
            curve_info_df.columns = ['area_to_conc', 'conc_to_area', 'params', 'r2', 'calculated_conc',
                                     'calculated_conc_accuracy', 'length', 'type', 'weight']
            curve_info_df = curve_info_df[curve_info_df['r2'] > r2_threshold]
            if len(curve_info_df) > 0:
                curve_info_df_all[index] = curve_info_df.sort_values(by=['length', 'r2'],
                                                                     ascending=[False, False]).reset_index(drop=True)
        # 把每个源的curve信息存储
        all_source_curve_info[s1] = curve_info_df_all
    return fps, all_source_curve_info


def source_apportionment_application(groups, fps, curve_info, data_all, sample_name, source_name,
                                     Cal_accuracy_threshold=0.3, remove_outlier=True):
    source_fps_index = fps[source_name]
    sample_df = data_all.loc[source_fps_index, sample_name]  # 获取样品信息，特定污染源指纹化合物峰面积
    # 第一步，先猜测初始的浓度
    initial_guess = []
    for new_index in tqdm(source_fps_index, desc='Initial Guess: processing each feature'):
        if new_index in curve_info[source_name].keys():
            new_index_df = curve_info[source_name][new_index]  # 获得其稀释规律
            target_area = float(sample_df.loc[new_index])  # 获得其在mix样品中的峰面积
            func1 = new_index_df.loc[0, 'area_to_conc']  # 找到最好的一个拟合曲线，也是点最多的
            calculated_conc = func1(target_area)
            if not np.isnan(calculated_conc):
                initial_guess.append(calculated_conc)
    if remove_outlier is True:
        initial_guess = np.array(initial_guess)
        Q1, Q3 = np.percentile(initial_guess, [25, 75])
        IQR = Q3 - Q1
        initial_guess = initial_guess[(initial_guess >= Q1 - 1.5 * IQR) & (initial_guess <= Q3 + 1.5 * IQR)]
        initial_guess_conc = np.median(initial_guess)
    else:
        initial_guess_conc = np.median(initial_guess)
    
    # 第二步，根据初始浓度去找那些accuracy不大的
    curve_conc = np.array(list(groups[source_name].values()))  # 根据用户输入的source name，再读取一次curve_conc
    target_cal_conc_index = argmin(abs(curve_conc - initial_guess_conc))  # 找到标线中和initial guess最接近的index
    final_guess = []  # 将上面的数据重置
    for new_index in tqdm(source_fps_index, desc='Source prediction: processing each feature'): \
            # 针对这个new_index
        if new_index in curve_info[source_name].keys():
            new_index_df = curve_info[source_name][new_index]  # 获得其稀释规律
            target_area = float(sample_df.loc[new_index])  # 获得其在mix样品中的峰面积
            # 很重要，要对标线的选择进行一个筛选，从数量从低到高,如果数量一样，优先线性
            new_index_df = new_index_df.sort_values(by=['length', 'type'], ascending=[True, True]).reset_index(drop = True)
            
            # 重要的一步，评估accuracy，如果不满足，就不计算
            for i in range(len(new_index_df)):
                calculated_conc_accuracy = new_index_df.loc[i, 'calculated_conc_accuracy']
                if len(calculated_conc_accuracy) > target_cal_conc_index and (
                        calculated_conc_accuracy[target_cal_conc_index] < Cal_accuracy_threshold):
                    func1 = new_index_df.loc[i, 'area_to_conc']  # 找到最符合条件，并且最多的？
                    calculated_conc = func1(target_area)
                    if not np.isnan(calculated_conc):
                        final_guess.append(calculated_conc)
                        break
    
    # 是否去除outlier:
    if remove_outlier is True:
        final_guess = np.array(final_guess)
        Q1, Q3 = np.percentile(final_guess, [25, 75])
        IQR = Q3 - Q1
        final_guess = final_guess[(final_guess >= Q1 - 1.5 * IQR) & (final_guess <= Q3 + 1.5 * IQR)]
        final_guess_conc = np.median(final_guess)
    else:
        final_guess_conc = np.median(final_guess)
    
    return initial_guess_conc, initial_guess, final_guess_conc, final_guess


# ========================================================================
# End of 定量溯源组件
# ========================================================================


if __name__ == '__main__':
    pass
# %config InlineBackendlineBackend.figure_format ='retina'
#  plt.rcParams['font.sans-serif'] = 'Times New Roman'  # 设置全局字体

# DeprecationWarning: 'scipy.integrate.simps' is deprecated in favour of 'scipy.integrate.simpson' and will be removed in SciPy 1.14.0

