import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from shapely.geometry import Point
from pyproj import CRS
from scipy import stats
from typing import Dict
from collections import Counter
import math



def calculate_evenness(matrix):
    """
    计算一个100x100矩阵的多种均匀度指数的平均值，忽略NaN值。
    支持植被类型在1到11之间的计算，返回一个单一数值。

    Parameters:
    - matrix (numpy.ndarray): 100x100的矩阵，可以包含NaN值，值应在1到11之间。

    Returns:
    - average_evenness (float): 各种均匀度指数的平均值。
    """

    valid_values = matrix[matrix>0]
    if valid_values.size == 0:
        return np.nan, np.nan, np.nan, np.nan


    type_counts = Counter(valid_values)
    total_count = sum(type_counts.values())
    proportions = [count / total_count for count in type_counts.values()]

    # 计算香农均匀度
    shannon_entropy = -sum(p * math.log(p) for p in proportions if p > 0)
    max_entropy = math.log(len(type_counts)) if len(type_counts) > 0 else 0
    shannon_evenness = shannon_entropy / max_entropy if max_entropy > 0 else 0

    # 计算辛普森均匀度
    simpson_index = sum(p ** 2 for p in proportions)
    simpson_evenness = (1 / simpson_index) / len(type_counts) if simpson_index > 0 else 0

    # 计算Gini-Simpson指数
    gini_simpson_index = 1 - simpson_index

    # 计算希尔均匀度 (q=2)
    hill_number_q2 = 1 / simpson_index if simpson_index > 0 else 0
    hill_evenness_q2 = hill_number_q2 / len(type_counts) if len(type_counts) > 0 else 0

    # 计算种类数
    species_count = len(type_counts)

    return species_count, shannon_evenness, simpson_evenness, gini_simpson_index, hill_evenness_q2


def compare_two_groups(x, y, label, alpha=0.05, alternative='two-sided', extra_d_when_nonparam=True):
    """
    Compare two numeric datasets by checking normality (Shapiro-Wilk) and homogeneity 
    of variances (Levene), then automatically select either an independent t-test 
    (equal variances or Welch) or the Mann-Whitney U test. Returns a one-row DataFrame 
    with sample sizes, descriptive statistics, chosen test, p-values (raw and formatted), 
    and effect size (Cohen's d or rank-biserial correlation).
    
    If extra_d_when_nonparam is True, an additional Cohen's d is computed in the non-normal branch.
    
    Parameters
    ----------
    x, y : array-like
        Two arrays of numeric data (e.g. list, np.ndarray, pd.Series).
    label : str
        Identifier stored in the "#" column.
    alpha : float, optional
        Significance level for the normality and variance tests (default 0.05).
    alternative : {'two-sided', 'less', 'greater'}, optional
        Alternative hypothesis for the tests (default 'two-sided').
    extra_d_when_nonparam : bool, optional
        Whether to compute an extra Cohen's d when using the Mann-Whitney U test.
    
    Returns
    -------
    pd.DataFrame
        A single-row DataFrame with columns including sample sizes, means, medians,
        normality and variance test results, test used, test statistic, p-values (raw 
        and formatted), and effect size.
    """
    # ---------- Helper: Format very small p-values ----------
    def fp(p, th=1e-16):
        """If p < th, return '< 1.0e-16'; otherwise, return in scientific notation."""
        if np.isnan(p):
            return "nan"
        return f"< {th:.1e}" if p < th else f"{p:.3g}"
    
    # ---------- Helper: Compute Cohen's d ----------
    def cohen_d(a, b):
        va, vb = np.var(a, ddof=1), np.var(b, ddof=1)
        pooled_std = np.sqrt(((len(a) - 1) * va + (len(b) - 1) * vb) / (len(a) + len(b) - 2))
        return (np.mean(a) - np.mean(b)) / pooled_std
    
    # ---------- Data cleaning: Convert to numpy arrays and remove NaNs ----------
    arr1 = np.array(x, dtype=float); arr1 = arr1[~np.isnan(arr1)]
    arr2 = np.array(y, dtype=float); arr2 = arr2[~np.isnan(arr2)]
    n1, n2 = len(arr1), len(arr2)
    
    if n1 < 2 or n2 < 2:
        return pd.DataFrame([{"#": label, 
                               "Error": "Insufficient sample size for statistical testing.", 
                               "Sample Sizes": (n1, n2)}])
    
    # ---------- Shapiro-Wilk Test for Normality ----------
    statn1, pn1 = stats.shapiro(arr1) if n1 >= 3 else (np.nan, np.nan)
    statn2, pn2 = stats.shapiro(arr2) if n2 >= 3 else (np.nan, np.nan)
    normality = (pn1 > alpha) and (pn2 > alpha) if not (np.isnan(pn1) or np.isnan(pn2)) else False
    
    # ---------- Levene's Test for Homogeneity of Variances ----------
    statv, pv = stats.levene(arr1, arr2)
    var_eq = (pv > alpha)
    
    # ---------- Initialize result dictionary ----------
    rd = {
        "#": label,
        "Sample Sizes": (n1, n2),
        "Mean (Group1)": arr1.mean(),
        "Mean (Group2)": arr2.mean(),
        "Median (Group1)": np.median(arr1),
        "Median (Group2)": np.median(arr2),
        "Var (Group1)": arr1.var(),
        "Var (Group2)": arr2.var(),
        # Shapiro-Wilk test results
        "Shapiro-Wilk p": (pn1, pn2),
        "Shapiro-Wilk p_str": (fp(pn1), fp(pn2)),

        # Levene test results
        "Levene p": pv,
        "Levene p_str": fp(pv),

        "Normality": normality,
        "VarEqual": var_eq,
        
    }
    
    # ---------- Choose test and compute effect size ----------
    if normality:
        # If data are normal -> use t-test (independent or Welch)
        if var_eq:
            t_stat, p_val = stats.ttest_ind(arr1, arr2, equal_var=True, alternative=alternative)
            test_used = "Independent t-test (equal var)"
        else:
            t_stat, p_val = stats.ttest_ind(arr1, arr2, equal_var=False, alternative=alternative)
            test_used = "Welch t-test (unequal var)"
        
        rd.update({
            "Test Used": test_used,
            "Test Statistic": t_stat,
            "p-value": p_val,
            "p-value_str": fp(p_val),
            "Cohen's d": cohen_d(arr1, arr2)
        })
    else:
        # If data are non-normal -> use Mann-Whitney U test
        u_stat, p_val = stats.mannwhitneyu(arr1, arr2, alternative=alternative)
        rb = 1 - 2 * min(u_stat, n1 * n2 - u_stat) / (n1 * n2)
        rd.update({
            "Test Used": "Mann-Whitney U",
            "Test Statistic": u_stat,
            "p-value": p_val,
            "p-value_str": fp(p_val),
            "Rank-biserial correlation": rb
        })
        if extra_d_when_nonparam:
            rd["Extra Cohen's d"] = cohen_d(arr1, arr2)
    
    return pd.DataFrame([rd]).T



def df2shp(output_file, df, lat_name='lat', lon_name='lon', max_length=10):
    """
    Truncate DataFrame column names to a maximum length (default 10 characters) ensuring uniqueness,
    and convert the DataFrame to a shapefile.

    If the absolute longitude values exceed 190, adjust longitudes by subtracting 360 for those > 180.
    The function creates a GeoDataFrame using the specified longitude and latitude columns, sets the CRS
    to EPSG:4326, and writes the shapefile to the given output_file path.

    Parameters:
        output_file (str): Path where the shapefile will be saved.
        df (pd.DataFrame): Input DataFrame.
        lat_name (str): Name of the latitude column (default 'lat').
        lon_name (str): Name of the longitude column (default 'lon').
        max_length (int): Maximum length for truncated column names (default 10).

    Returns:
        None
    """
    # Truncate column names and ensure uniqueness
    new_columns = []
    for col in df.columns:
        truncated = col[:max_length]
        suffix = 1
        # Ensure the truncated name is unique among already processed columns.
        while truncated in new_columns:
            truncated = col[:max_length - len(str(suffix))] + str(suffix)
            suffix += 1
        new_columns.append(truncated)
    df.columns = new_columns

    # Adjust longitude values if necessary: if any absolute value exceeds 190, 
    # subtract 360 from values greater than 180.
    longs = df[lon_name].values
    if np.nanmax(np.abs(longs)) > 190:
        # Use boolean indexing for efficient adjustments.
        df.loc[df[lon_name] > 180, lon_name] -= 360

    # Create a geometry column using longitude and latitude
    df.loc[:, 'geometry'] = [Point(lon, lat) for lon, lat in zip(df[lon_name], df[lat_name])]
    
    # Create GeoDataFrame and set CRS to EPSG:4326
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.crs = CRS.from_epsg(4326)
    
    # Save the GeoDataFrame as a shapefile
    gdf.to_file(output_file)



def get_summary(correlations, p_values):
    """
    Analyze statistically significant correlations across p-value thresholds.

    Processes input arrays through:
    1. Data validation: Filters non-NaN correlations with valid p-values (0-1)
    2. Threshold analysis: For each p-value cutoff (0.01, 0.05, 0.10, Total):
       a. Filters correlations meeting significance criteria
       b. Categorizes into positive/neutral/negative
       c. Calculates counts and percentages (relative to total and significant)
    3. Returns formatted comparison table

    Parameters:
        correlations (np.ndarray): Correlation coefficients array (-1 to 1)
        p_values (np.ndarray): Corresponding p-values array (0 to 1)

    Returns:
        pd.DataFrame: Summary table with columns:
            - Significance Level: Threshold (p < X) or 'Total'
            - Positive: Count (percentage of total)
            - Neutral: Count (percentage of total)
            - Negative: Count (percentage of total)
            - Pos/Neg Ratio: Ratio (significant positives vs negatives)

    Percentages show both:
    - Absolute %: Relative to all valid data points
    - Relative %: Within significant results (Pos/Neg ratio calculation)
    """
    # Validate and filter input data
    valid_mask = ~np.isnan(correlations) & (p_values >= 0) & (p_values <= 1)
    filtered_corrs = correlations[valid_mask]
    filtered_pvals = p_values[valid_mask]
    total_valid = len(filtered_corrs)

    results = []
    ANALYSIS_LEVELS = [
        ('0.01', 0.01), 
        ('0.05', 0.05), 
        ('0.10', 0.10), 
        ('1.01', 1.01)  # Special case for total
    ]

    for threshold_str, p_cutoff in ANALYSIS_LEVELS:
        # Apply p-value filter
        significant_corrs = filtered_corrs.copy()
        if p_cutoff <= 0.1:
            significant_corrs[filtered_pvals >= p_cutoff] = np.nan
        
        # Remove non-significant values (except for total case)
        analyzed_corrs = significant_corrs[~np.isnan(significant_corrs)]

        # Categorize correlations
        positive = np.sum(analyzed_corrs > 0)
        neutral = np.sum(analyzed_corrs == 0)
        negative = np.sum(analyzed_corrs < 0)
        total_significant = positive + negative

        # Calculate percentages relative to total valid
        positive_pct = positive / total_valid * 100
        neutral_pct = neutral / total_valid * 100
        negative_pct = negative / total_valid * 100

        # Calculate relative distribution (excluding neutral)
        denominator = total_significant if total_significant > 0 else 1
        positive_ratio_pct = positive / denominator * 100
        negative_ratio_pct = negative / denominator * 100

        # Safely format ratio
        if negative_ratio_pct == 0:
            ratio_str = "Inf" if positive_ratio_pct > 0 else "N/A"
        else:
            ratio_str = f"{positive_ratio_pct/negative_ratio_pct:.2f}"

        # Format output row
        level_label = 'Total' if threshold_str == '1.01' else f'p < {threshold_str}'
        results.append(pd.DataFrame({
            'Significance Level': [level_label],
            'Positive': [f"{positive} ({positive_pct:.2f}%)"],
            'Neutral': [f"{neutral} ({neutral_pct:.2f}%)"],
            'Negative': [f"{negative} ({negative_pct:.2f}%)"],
            'Pos/Neg Ratio': [f"{ratio_str} = {positive_ratio_pct:.2f}% : {negative_ratio_pct:.2f}%"]
        }))

    return pd.concat(results).reset_index(drop=True)



def fit_ols_model(x, y, degree):
    """
    Fit a polynomial Ordinary Least Squares (OLS) regression model to the data.
    
    This function creates polynomial features of a specified degree from the input predictor x,
    fits an OLS regression model to predict the response variable y, and computes various model statistics.
    It returns a range of x values for plotting the fitted curve, predicted y values over that range,
    along with key statistics including the coefficient, p-value, intercept, R-squared value, the fitted model,
    and the confidence interval bounds for the predictions.
    
    Parameters:
        x (np.ndarray): 1D array of predictor values.
        y (np.ndarray): 1D array of response values.
        degree (int): Degree of the polynomial to fit.
        
    Returns:
        tuple: A tuple containing:
            - x_range (np.ndarray): A linearly spaced array covering the range of x values.
            - y_range (np.ndarray): Predicted y values corresponding to x_range.
            - coef (float): Coefficient of the first polynomial feature (slope component).
            - p_val (float): p-value for the first predictor coefficient.
            - intercept (float): Intercept of the fitted model.
            - r2 (float): R-squared value of the model fit.
            - model: The fitted OLS model object.
            - ci_low (np.ndarray): Lower bounds of the confidence intervals for predictions.
            - ci_high (np.ndarray): Upper bounds of the confidence intervals for predictions.
    
    Example:
        >>> import numpy as np
        >>> x = np.linspace(0, 10, 50)
        >>> y = 3 * x + np.random.randn(50)
        >>> x_range, y_range, coef, p_val, intercept, r2, model, ci_low, ci_high = fit_ols_model(x, y, degree=1)
    """
    # Fit the polynomial transformation of x
    poly = PolynomialFeatures(degree=degree)
    x_poly = poly.fit_transform(x.reshape(-1, 1))
    
    # Add a constant term and fit the OLS model
    X = sm.add_constant(x_poly)
    model = sm.OLS(y, X).fit()
    
    # Extract key statistics from the model
    r2 = model.rsquared
    p_val = model.pvalues[1]
    coef = model.params[1]
    intercept = model.params[0]
    
    # Generate a range of x values for plotting predictions
    x_range = np.linspace(x.min(), x.max(), 100)
    x_poly_range = poly.fit_transform(x_range.reshape(-1, 1))
    
    # Get predicted y values and confidence intervals
    y_range = model.predict(sm.add_constant(x_poly_range))
    predictions = model.get_prediction(sm.add_constant(x_poly_range))
    ci_low, ci_high = predictions.conf_int().T  # confidence intervals
    
    return x_range, y_range, coef, p_val, intercept, r2, model, ci_low, ci_high



def remove_outliers(data, threshold=3, use_percentile_clip=True):
    """
    Function to remove outliers from a given data array.

    Parameters:
    - data: One-dimensional or multi-dimensional data array, can be a pandas Series, NumPy array, or xarray.DataArray.
    - threshold: Threshold for outliers in terms of the data standard deviation. Default is 3.
    - use_percentile_clip: Whether to clip extreme values using the 0.01 and 99.99 percentiles. Default is True.

    Returns:
    - Processed data array with outliers beyond the threshold replaced with NaN.

    Note:
    - For NumPy arrays, the function directly modifies the input array, replacing outliers with NaN.
    - For xarray.DataArray, a new array is generated where outliers are replaced with NaN, and the original array remains unaffected.
    - If the input is a pandas Series, a new Series is generated with outliers replaced with NaN, and the original Series remains unaffected.

    """
    
    # Calculate the standard deviation, mean, and center the data
    data[~np.isfinite(data)] = np.nan
    # 千分位的值
    if use_percentile_clip:
        data_p999 = np.nanpercentile(data, 99.99) # 99.99%
        data_p001 = np.nanpercentile(data,  0.01) #  0.01%
        data[data>data_p999] = np.nan
        data[data<data_p001] = np.nan

    data_std = np.nanstd(data)
    data_mean = np.nanmean(data)
    data_centered = np.abs(data - data_mean)
    
    # Remove outliers based on the threshold and data type
    if isinstance(data, xr.DataArray):
        data = xr.where(data_centered > threshold*data_std, np.nan, data)
    else:
        data[data_centered > threshold*data_std] = np.nan

    return data



def summarize_coeff_stats(files_dict: Dict[str, str], r_name='r', pval_name='p-val') -> pd.DataFrame:
    """

    汇总多个模型输出文件中的系数统计信息。

    支持的输入格式：
      - NetCDF (.nc)：文件中需包含变量 `r_name` 和 `pval_name`  
      - CSV (.csv)：表头需包含列 `r_name` 和 `pval_name`

    参数
    ----
    files_dict : Dict[str, str]
        键为用户自定义的标识符, 值为文件路径。
    r_name : str, 可选
        系数字段名称, 默认 'r'。
    pval_name : str, 可选
        P-value 字段名称, 默认 'p-val'。

    返回
    ----
    pd.DataFrame
        包含以下列:
        - key : 文件名中 .vs. 后、.control 前的关键字
        # —— 数量统计 (按正/中性/负分组)  —— 
        - count_total        : 总像元数
        - count_pos          : 正相关数量
        - count_pos_sig      :   └ 显著正相关数量 (p < 0.05)
        - count_pos_nonsig   :   └ 非显著正相关数量
        - count_neutral      : 中性 (r == 0) 数量
        - count_neg          : 负相关数量
        - count_neg_sig      :   └ 显著负相关数量 (p < 0.05)
        - count_neg_nonsig   :   └ 非显著负相关数量

        # —— 比例统计 (按正/中性/负分组)  —— 
        - ratio_pos_total         : 正相关／总体
        - ratio_pos_sig_total     :   └ 显著正相关／总体
        - ratio_pos_nonsig_total  :   └ 非显著正相关／总体
        - ratio_pos_sig_within_sig:   └ 显著正相关／所有显著像元
        - ratio_neutral_total     : 中性／总体
        - ratio_neg_total         : 负相关／总体
        - ratio_neg_sig_total     :   └ 显著负相关／总体
        - ratio_neg_nonsig_total  :   └ 非显著负相关／总体
        - ratio_neg_sig_within_sig:   └ 显著负相关／所有显著像元

        # —— 均值统计 —— 
        - mean_r_total      : 全部 r 的均值
        - mean_r_sig        : 所有显著 (p<0.05) r 的均值
        - mean_r_pos_sig    : 显著正相关 r 的均值
        - mean_r_neg_sig    : 显著负相关 r 的均值

        # —— 标准差统计 —— 
        - std_r_total       : 全部 r 的标准差
        - std_r_sig         : 所有显著 r 的标准差
        - std_r_pos_sig     : 显著正相关 r 的标准差
        - std_r_neg_sig     : 显著负相关 r 的标准差
    """
    cols = [
        'key',

        # —— 数量统计 (按正/中性/负分组)  —— 
        'count_total',        # 总像元数
        # 正相关组
        'count_pos',          # 正相关数量
        'count_pos_sig',      #   └ 显著正相关数量
        'count_pos_nonsig',   #   └ 非显著正相关数量
        # 中性
        'count_neutral',      # 中性 (r == 0) 数量
        # 负相关组
        'count_neg',          # 负相关数量
        'count_neg_sig',      #   └ 显著负相关数量
        'count_neg_nonsig',   #   └ 非显著负相关数量

        # —— 比例统计 (按正/中性/负分组)  —— 
        # 正相关组
        'ratio_pos_total',         # 正相关／总体
        'ratio_pos_sig_total',     #   └ 显著正相关／总体
        'ratio_pos_nonsig_total',  #   └ 非显著正相关／总体
        'ratio_pos_sig_within_sig',#   └ 显著正相关／所有显著
        # 中性
        'ratio_neutral_total',     # 中性／总体
        # 负相关组
        'ratio_neg_total',         # 负相关／总体
        'ratio_neg_sig_total',     #   └ 显著负相关／总体
        'ratio_neg_nonsig_total',  #   └ 非显著负相关／总体
        'ratio_neg_sig_within_sig',#   └ 显著负相关／所有显著

        # —— 均值统计 —— 
        'mean_r_total',       # 全部 r 的均值
        'mean_r_sig',         # 所有显著 r 的均值
        'mean_r_pos_sig',     # 显著正相关 r 的均值
        'mean_r_neg_sig',     # 显著负相关 r 的均值

        # —— 标准差统计 —— 
        'std_r_total',        # 全部 r 的标准差
        'std_r_sig',          # 所有显著 r 的标准差
        'std_r_pos_sig',      # 显著正相关 r 的标准差
        'std_r_neg_sig'       # 显著负相关 r 的标准差
    ]
    df = pd.DataFrame(columns=cols)

    for i, (key, file) in enumerate(files_dict.items()):
        if file.endswith('.nc'):
            ds = xr.open_dataset(file)
        elif file.endswith('.csv'):
            ds = pd.read_csv(file)
        else:
            raise ValueError('Invalid input file format.')
        r_arr = ds[r_name].values
        p_arr = ds[pval_name].values

        # 去除 NaN 和 inf
        mask = np.isfinite(r_arr) & np.isfinite(p_arr)
        r = r_arr[mask]
        p = p_arr[mask]

        # 数量统计
        count_total       = r.size
        pos_mask          = r > 0
        neg_mask          = r < 0
        neu_mask          = r == 0
        pos_sig_mask      = pos_mask & (p < 0.05)
        neg_sig_mask      = neg_mask & (p < 0.05)

        count_pos         = pos_mask.sum()
        count_neutral     = neu_mask.sum()
        count_neg         = neg_mask.sum()
        count_pos_sig     = pos_sig_mask.sum()
        count_neg_sig     = neg_sig_mask.sum()
        count_pos_nonsig  = count_pos - count_pos_sig
        count_neg_nonsig  = count_neg - count_neg_sig
        sig_count         = count_pos_sig + count_neg_sig

        # 比例统计
        ratio_pos_total         = count_pos        / count_total
        ratio_pos_sig_total     = count_pos_sig    / count_total
        ratio_pos_nonsig_total  = count_pos_nonsig / count_total
        ratio_pos_sig_within_sig= (count_pos_sig / sig_count) if sig_count else np.nan

        ratio_neutral_total     = count_neutral    / count_total

        ratio_neg_total         = count_neg        / count_total
        ratio_neg_sig_total     = count_neg_sig    / count_total
        ratio_neg_nonsig_total  = count_neg_nonsig / count_total
        ratio_neg_sig_within_sig= (count_neg_sig / sig_count) if sig_count else np.nan

        # 均值统计
        mean_r_total    = np.nanmean(r)
        sig_vals        = r[p < 0.05]
        mean_r_sig      = np.nanmean(sig_vals)     if sig_vals.size else np.nan
        mean_r_pos_sig  = np.nanmean(r[pos_sig_mask]) if pos_sig_mask.any() else np.nan
        mean_r_neg_sig  = np.nanmean(r[neg_sig_mask]) if neg_sig_mask.any() else np.nan

        # 标准差统计
        std_r_total     = np.nanstd(r)
        std_r_sig       = np.nanstd(sig_vals)      if sig_vals.size else np.nan
        std_r_pos_sig   = np.nanstd(r[pos_sig_mask]) if pos_sig_mask.any() else np.nan
        std_r_neg_sig   = np.nanstd(r[neg_sig_mask]) if neg_sig_mask.any() else np.nan

        df.loc[i] = [
            key,
            count_total,
            count_pos,
            count_pos_sig,
            count_pos_nonsig,
            count_neutral,
            count_neg,
            count_neg_sig,
            count_neg_nonsig,
            ratio_pos_total,
            ratio_pos_sig_total,
            ratio_pos_nonsig_total,
            ratio_pos_sig_within_sig,
            ratio_neutral_total,
            ratio_neg_total,
            ratio_neg_sig_total,
            ratio_neg_nonsig_total,
            ratio_neg_sig_within_sig,
            mean_r_total,
            mean_r_sig,
            mean_r_pos_sig,
            mean_r_neg_sig,
            std_r_total,
            std_r_sig,
            std_r_pos_sig,
            std_r_neg_sig
        ]

    return df