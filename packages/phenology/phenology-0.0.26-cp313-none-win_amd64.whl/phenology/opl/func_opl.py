import numpy as np
from tqdm import tqdm
from datetime import datetime, timedelta
from joblib import Parallel, delayed
from scipy.signal import detrend


def par_corr_npy(data, threshold=0.5):
    rows, cols = data.shape
    data = data[~np.isnan(data).any(axis=1)]
    if data.shape[0] < rows*threshold:
        return np.full(cols-1, np.nan)
    
    data = detrend(data, axis=0)
    # data = zscore(data, axis=0)
    corr_matrix = np.corrcoef(data, rowvar=False)
    inv_matrix = np.linalg.inv(corr_matrix)
    r = np.array([-inv_matrix[0, col] / np.sqrt(inv_matrix[0, 0] * inv_matrix[col, col]) for col in range(1, cols)])
    return r


def partial_corr(x, y, threshold=0.5, n_jobs=-1):
    data = np.concatenate([y[..., np.newaxis], x], axis=-1) # (660000, 21, 4)
    result = np.array(Parallel(n_jobs=n_jobs)(delayed(par_corr_npy)(data[i], threshold) for i in range(data.shape[0]))) # (660000, 3)
    return result



def get_opl(y:np.ndarray, x:np.ndarray, **kwargs):
    """
    Calculate the optimal pre-season length for specified variables.

    Parameters:
    - y: np.ndarray, shape (rows, cols, years, ) 
      Target variable data over the years. such as phenological data at an annual scale.

    - x: np.ndarray, shape (rows, cols, months, xvars)
      Explanatory variables data at a monthly scale, covering one more year than y data (months = 12 * (years + 1)).

    Keyword Arguments (kwargs):
    - n_jobs: int, default --> mp.cpu_count()
      number of jobs to run in parallel. 
    
    - max_month: int, default 6
      Maximum pre-season length calculated forward from the current month.


    Returns: 
    - for multiple data (eg. x.ndim == 4)
      result: np.ndarray, shape (rows, cols, xvars) the value of opl for each variable.
    """
    n_jobs = kwargs.get('n_jobs', -1)
    max_month = kwargs.get('max_month', 6)
    threshold = kwargs.get('threshold', 0.5)
    
    # 形状适配
    y = y.squeeze()
    x = x.squeeze()
    if x.ndim == 2:
        x = x[np.newaxis, np.newaxis, :, :]  # (1, 1, months, xvars)
        y = y[np.newaxis, np.newaxis, :]  # (1, 1, years)

    elif x.ndim == 3:
        x = x[np.newaxis, :, :, :]  # (1, cols, months, xvars)
        y = y[np.newaxis, :, :]  # (1, cols, years)
        
    
    rows, cols, months, xvars = x.shape
    _, _, years = y.shape

    mask_y = np.sum(~np.isnan(y), axis=2) >= years*threshold # (600, 3600)
    mask_x = np.sum(~np.isnan(x), axis=2) >= months*threshold # (600, 3600, 3)
    mask_x = np.sum(mask_x, axis=2) == xvars # (600, 3600)
    mask = mask_y & mask_x # (600, 3600)

    y = y[mask] # (660000, 21)
    x = x[mask] # (660000, 264, 3)

    # 获取多年平均物候期所在月份
    y_mean = np.nanmean(y, axis=-1) # (660000, )
    y_mean = np.array([(datetime(2023, 1, 1) + timedelta(days=int(round(day)))).month for day in y_mean])
    y_mean = np.expand_dims(y_mean, axis=-1).astype(int) # (660000, 1) 全是5月


    indices1 = np.arange(years) * 12 + y_mean - 1  # (660000, 21)
    indices0 = np.arange(x.shape[0])[:, np.newaxis]

    x_list = [x[:, 12-i:-i if i!= 0 else None, :] for i in range(max_month)]
    x_list = [np.mean(x_list[:i+1], axis=0)[indices0, indices1, :] for i in range(max_month)]

    
    result = [partial_corr(x, y, threshold, n_jobs) for x in tqdm(x_list)]
    result = np.abs(np.array(result)) # (6, 660000, 3)
    result = np.argmax(result, axis=0) # (660000, 3)
    

    result_mask = np.full((rows, cols, xvars), np.nan)
    result_mask[mask] = result
    result_mask = result_mask.squeeze()
    
    return result_mask



# -------------------------------------------------------------------------- #

    
def single_mean(x, opl, pheno):
    """
    x: shape (months, )
    opl: number
    pheno: number
    """
    k_indices = np.arange(12, len(x), 12) # (months//12-1, )
    start_indices = (k_indices + pheno - opl - 1).astype(int) # (months//12-1, )
    end_indices = (k_indices + pheno).astype(int) # (months//12-1, )
    mask = (np.arange(len(x)) >= start_indices[:, np.newaxis]) & (np.arange(len(x)) < end_indices[:, np.newaxis])
    x_masked = np.where(mask, x, np.nan) 
    resarr = np.nanmean(x_masked, axis=1) # shape (months//12-1, )
    
    return resarr


def seasonal_mean(x_arr: np.ndarray, opl_arr: np.ndarray, pheno_arr: np.ndarray):
    """
    Calculate pre-seasonal mean from input arrays.

    Parameters:
    - x_arr (np.ndarray): Climate variable array (months, rows, cols), where months is a multiple of 12.
    - opl_arr (np.ndarray): The optimal preseason length (rows, cols).
    - pheno_arr (np.ndarray): Phenological dates (rows, cols), typically multi-year average in day of year (1-365) or month (1-12).

    Returns:
    - result (np.ndarray): Pre-seasonal mean (months//12-1, rows, cols).

    """

    if np.nanmax(pheno_arr) > 12: # if the value of pheno_arr is the "day of year" (1-365), then convert it to the month
        pheno_arr[~np.isnan(pheno_arr)] = np.array([(datetime(2023, 1, 1) + timedelta(days=eos - 1)).month for eos in pheno_arr[~np.isnan(pheno_arr)]])

    months, rows, cols = x_arr.shape
 
    nn_indices = np.where(~np.isnan(opl_arr) & ~np.isnan(pheno_arr)) # nn_indices, means the indices of non-NaN elements
    nn_opl = opl_arr[nn_indices] # shape (806542,)
    nn_pheno = pheno_arr[nn_indices] # shape (806542,)
    nn_x = x_arr[:, nn_indices[0], nn_indices[1]] # shape (504, 806542)

    # slice the data
    args_list = [(nn_x[:, i], nn_opl[i], nn_pheno[i]) for i in range(nn_opl.shape[0])]
    res = np.array(Parallel(n_jobs=-1)(delayed(single_mean)(x, opl, pheno) for x, opl, pheno in tqdm(args_list))) # shape (806542, 41)
    result = np.full((months//12-1, rows, cols), np.nan)
    result[:, nn_indices[0], nn_indices[1]] = res.swapaxes(0, 1)

    return result
 
    

    
            
