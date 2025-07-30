import numpy as np
import pandas as pd
from tqdm import tqdm
from scipy import stats
from typing import Union, List
from joblib import Parallel, delayed
from numpy.lib.stride_tricks import sliding_window_view
from scipy.stats import t

def aggregate2D(x, exc_shape, ignore_nodata=None):
    """
    x: 2D array
    exc_shape: tuple of (rows, cols)
    return: 2D array
    """
    from .api_resample import resample_2D_mean
    
    cur_rows, cur_cols = x.shape
    exc_rows, exc_cols = exc_shape
    rw = cur_rows / exc_rows
    cw = cur_cols / exc_cols
    
    x = np.pad(x, ((0, int(rw+1)), (0, int(cw+1))), 'constant', constant_values=np.nan)
    x[np.isinf(x)] = np.nan
    
    if ignore_nodata is not None:
        x[x==ignore_nodata] = np.nan
    
    x_min = np.nanmin(x)-1
    x = x - x_min # x >= 1

    x[np.isnan(x)] = 0 # 0 is the missing value
    x = x.astype(np.float64)
    y = np.full(exc_shape, np.nan).astype(np.float64)
    y = resample_2D_mean(x, y, rw, cw, exc_rows, exc_cols, 0) # 0 is the missing value
    y = np.asarray(y) + x_min
    
    return y



def aggregate3D_v1(data, exc_shape, n_jobs=-1):
    res = Parallel(n_jobs)(delayed(aggregate2D)(data_i, exc_shape) for data_i in data)
    res = np.array(res)
    return res



def aggregate3D_v2(x, exc_shape, ignore_nodata=None):
    """
    x: 2D array
    exc_shape: tuple of (rows, cols)
    return: 2D array
    """
    from .api_resample import resample_3D_mean
    cur_times, cur_rows, cur_cols = x.shape
    exc_times, exc_rows, exc_cols = exc_shape
    rw = cur_rows / exc_rows
    cw = cur_cols / exc_cols
    
    x = np.pad(x, (0, (0, int(rw+1)), (0, int(cw+1))), 'constant', constant_values=np.nan)
    x[np.isinf(x)] = np.nan
    
    if ignore_nodata is not None:
        x[x==ignore_nodata] = np.nan
    
    x_min = np.nanmin(x)-1
    x = x - x_min # x >= 1

    x[np.isnan(x)] = 0 # 0 is the missing value
    x = x.astype(np.float64)
    y = np.full(exc_shape, np.nan).astype(np.float64)
    y = resample_3D_mean(x, y, rw, cw, exc_times, exc_rows, exc_cols, 0) # 0 is the missing value
    y = np.asarray(y) + x_min
    
    return y



def sliding_grid_partition(data: np.ndarray, target_row_blocks: int, target_col_blocks: int) -> np.ndarray:
    """
    Partition a 2D or 3D array into a grid of fixed-size blocks along its last two dimensions using a sliding window approach.
    
    For a 2D array (shape: (rows, cols)), the array is first expanded to (1, rows, cols) and then partitioned into
    target_row_blocks x target_col_blocks blocks. The output shape is:
        - For 2D input: (target_row_blocks, target_col_blocks, block_height, block_width)
        - For 3D input: (D, target_row_blocks, target_col_blocks, block_height, block_width)
    
    If the number of rows and columns can be evenly divided by the target block counts, the function uses reshape
    and transpose for efficient extraction. Otherwise, it computes a fixed block size (using ceiling division) and
    extracts blocks using sliding_window_view based on computed centers, ensuring blocks do not exceed array bounds.
    
    Parameters:
        data (np.ndarray): Input array, either a 2D array (rows, cols) or a 3D array (D, rows, cols), where D typically 
                           represents the number of slices (e.g., channels, time frames, etc.).
        target_row_blocks (int): Desired number of blocks along the row dimension.
        target_col_blocks (int): Desired number of blocks along the column dimension.
        
    Returns:
        np.ndarray: The grid-partitioned array using a sliding window approach. For 2D input, the shape is 
                    (target_row_blocks, target_col_blocks, block_height, block_width), and for 3D input, 
                    the shape is (D, target_row_blocks, target_col_blocks, block_height, block_width).
    """
    # If the input is a 2D array, expand it to 3D for uniform processing; mark to squeeze output later.
    squeeze_output = False
    if data.ndim == 2:
        data = data[np.newaxis, ...]
        squeeze_output = True
    elif data.ndim != 3:
        raise ValueError("Input data must be a 2D array (rows, cols) or a 3D array (D, rows, cols).")
    
    num_slices, orig_rows, orig_cols = data.shape
    row_scale = orig_rows / target_row_blocks
    col_scale = orig_cols / target_col_blocks

    # If the dimensions are evenly divisible, use reshape and transpose for fast extraction.
    if row_scale.is_integer() and col_scale.is_integer():
        block_row_size, block_col_size = int(row_scale), int(col_scale)
        partitioned = data.reshape(num_slices, target_row_blocks, block_row_size, target_col_blocks, block_col_size)
        partitioned = partitioned.transpose(0, 1, 3, 2, 4)
    else:
        # Compute block size with ceiling division.
        block_row_size = int(np.ceil(row_scale))
        block_col_size = int(np.ceil(col_scale))
        
        # Calculate offsets to ensure blocks do not exceed array bounds.
        offset_row_left = block_row_size // 2
        offset_row_right = block_row_size - offset_row_left
        offset_col_top = block_col_size // 2
        offset_col_bottom = block_col_size - offset_col_top
        
        # Compute the center positions for blocks along rows and columns.
        row_centers = np.linspace(offset_row_left, orig_rows - offset_row_right, target_row_blocks).round().astype(int)
        col_centers = np.linspace(offset_col_top, orig_cols - offset_col_bottom, target_col_blocks).round().astype(int)
        
        # Determine the starting indices of each block.
        row_starts = row_centers - offset_row_left
        col_starts = col_centers - offset_col_top
        
        # Use sliding_window_view to generate all possible windows of fixed block size.
        windows = sliding_window_view(data, (block_row_size, block_col_size), axis=(1, 2))
        # Create a grid to select the desired windows based on the computed starting indices.
        grid_row, grid_col = np.meshgrid(row_starts, col_starts, indexing='ij')
        partitioned = windows[:, grid_row, grid_col, :, :]
    
    if squeeze_output:
        partitioned = partitioned[0]
    return partitioned



def get_stats(data: np.ndarray, alpha: float = 0.05) -> pd.DataFrame:
    """
    Compute a comprehensive descriptive statistics summary for the input numerical data,
    adding standard error (SE) and confidence interval (CI).

    Parameters:
        data (np.ndarray): A numerical 1D or multi-dimensional array that may contain NaN values.
        alpha (float): Significance level for CI, default 0.05 for 95% CI.

    Returns:
        pd.DataFrame: A single-row DataFrame containing:
            - Minimum, Mean, Maximum, Median
            - StdDev, Variance
            - SE (standard error)
            - Skewness, Kurtosis
            - Range, IQR
            - 1%, 5%, 10%, 90%, 95%, 99% Percentiles
            - Mean-3σ, Mean+3σ
            - Sum, Count, NaN Count
            - CI_lower, CI_upper
    """
    flat = np.ravel(data)
    nan_count = np.isnan(flat).sum()
    clean = flat[~np.isnan(flat)]
    n = clean.size
    if n < 2:
        raise ValueError("Need at least two non-NaN values to compute stats.")
        
    mean = clean.mean()
    std = clean.std(ddof=1)
    var = clean.var(ddof=1)
    se = std / np.sqrt(n)
    dfree = n - 1
    t_crit = t.ppf(1 - alpha/2, dfree)
    ci_lower = mean - t_crit * se
    ci_upper = mean + t_crit * se
    
    med = np.median(clean)
    mn = clean.min()
    mx = clean.max()
    skew = stats.skew(clean)
    kurt = stats.kurtosis(clean)
    data_range = mx - mn
    pct = np.percentile(clean, [1, 5, 10, 90, 95, 99])
    iqr = np.percentile(clean, 75) - np.percentile(clean, 25)
    
    stats_dict = {
        'Minimum': mn,
        'Mean': mean,
        'Maximum': mx,
        'Median': med,
        'StdDev': std,
        'Variance': var,
        'SE': se,
        'CI_lower': ci_lower,
        'CI_upper': ci_upper,
        'Skewness': skew,
        'Kurtosis': kurt,
        'Range': data_range,
        'IQR': iqr,
        '1%': pct[0],
        '5%': pct[1],
        '10%': pct[2],
        '90%': pct[3],
        '95%': pct[4],
        '99%': pct[5],
        'Mean-3σ': mean - 3*std,
        'Mean+3σ': mean + 3*std,
        'Sum': clean.sum(),
        'Count': n,
        'NaN Count': nan_count
    }
    return pd.DataFrame([stats_dict])



class Aggregate:

    def __init__(self, data: np.ndarray, exc_shape:tuple):
        '''
        Initialize Aggregator object.

        Parameters:
        data (numpy.ndarray): The input data to be aggregated.
        exc_shape (tuple): The expected shape of the output data.
        '''
        self.data = data
        self.exc_shape = exc_shape
        self.exc_rows, self.exc_cols = self.exc_shape
        self.cur_rows, self.cur_cols = self.data.shape
        self.r_res, self.c_res = self.cur_rows/self.exc_rows, self.cur_cols/self.exc_cols

        pass
        
    def mode(self): return self.fit('mode')
    def mean(self): return self.fit('mean')

    
    def fit(self, operation: str = 'mode'):
        '''
        Aggregate the data using mode operation.

        Returns:
        numpy.ndarray: The aggregated data.
        '''
       
        if self.r_res.is_integer() and self.c_res.is_integer():
            self.data = self.data.reshape(self.exc_rows, int(self.r_res), self.exc_cols, int(self.c_res))
            self.data = self.data.transpose(0, 2, 1, 3).reshape(self.exc_rows, self.exc_cols, -1)
            if operation == 'mode':
                return self._mode_exa_div()
            elif operation == 'mean':
                return np.nanmean(self.data, axis=-1)
            else:
                raise ValueError("Invalid operation")
            
        else:
            return self._mode_not_div(operation)




    def _get_boundary(self, r, ratio):
        r_sta = r*ratio
        r_end = (r+1)*ratio

        rmin = int(r_sta)
        rmax = np.ceil(r_end)

        offset_1 = np.ceil(r_sta) - r_sta # 上/左 偏移量
        offset_2 = r_end - int(r_end) # 下/右 偏移量
        # return rmin, rmax, offset_1, offset_2
        return rmin, int(rmax), int(offset_1), int(offset_2)
    


    def _get_area(self, win_shape, offsets):

        offset_1, offset_2, offset_3, offset_4 = offsets # 上下左右
        areas = np.full(win_shape, 1, dtype=float)
        if offset_1 > 0: areas[ 0, :] = offset_1 
        if offset_2 > 0: areas[-1, :] = offset_2
        if offset_3 > 0: areas[:,  0] = offset_3 * areas[:,  0]
        if offset_4 > 0: areas[:, -1] = offset_4 * areas[:, -1]

        return areas



    def _mode_not_div(self, operation):
        result = np.full(self.exc_shape, np.nan)
        for r in tqdm(range(self.exc_rows)):
            rmin, rmax, offset_1, offset_2 = self._get_boundary(r, self.r_res)
            
            for c in range(self.exc_cols):
                cmin, cmax, offset_3, offset_4 = self._get_boundary(c, self.c_res)
                data_win = self.data[rmin:rmax, cmin:cmax]
                mask = ~np.isnan(data_win)
                if not mask.any():
                    continue

                area_win = self._get_area(data_win.shape, (offset_1, offset_2, offset_3, offset_4))
                data_ij = data_win[mask].astype(np.int64)
                area_ij = area_win[mask]

                if operation == 'mode':
                    counts = np.bincount(data_ij, weights=area_ij)*1e9
                    result[r, c] = np.argmax(counts.astype(np.int64)) # areas整型或浮点型 对np.argmax(areas)的结果有影响。具体影响在于当多个val并列第一的时候, 该取哪一个? 据简单观测, 整型-->取最小的, 浮点型-->取最大
                elif operation == 'mean':
                    result[r, c] = np.sum(data_ij*area_ij)/np.sum(area_ij)
        
        return result


    def _mode_exa_div(self,):
        mask = np.any(~np.isnan(self.data), axis=-1)
        result = np.full(mask.shape, np.nan)
        result[mask] = np.apply_along_axis(lambda x: np.argmax(np.bincount(np.int64(x[~np.isnan(x)]))), axis=-1, arr=self.data[mask])
        return result
    


class SlidingWindowAnalysis: # sliding window analysis
    def __init__(self, step=10, window_size=10):
        self.step = step
        self.winsize = window_size
        self.l_ws = window_size // 2
        self.r_ws = window_size - self.l_ws
        self.data = None
        self.res = None
        self.concatenate_axis = 1

        
    def _pad(self, data):
        pad_width = [(self.r_ws, self.l_ws)]*2 + [(0, 0)]*(data.ndim - 2)
        if self.concatenate_axis is not None:
            if self.concatenate_axis != 1:
                data = np.swapaxes(data, self.concatenate_axis, 1)
            data = np.concatenate((data[:, -self.r_ws:], data, data[:, :self.l_ws]), axis=1) # 左右填充
            if self.concatenate_axis != 1:
                data = np.swapaxes(data, self.concatenate_axis, 1)
            pad_width[1] = (0, 0)
        data = np.pad(data, pad_width, mode='constant', constant_values=np.nan)
        return data


    def slide(self, data):
        data_list = []
        height, width, bands = data.shape # (500, 400, 3)
        x_range = np.arange(self.l_ws, height + self.l_ws, self.step).astype(int)
        y_range = np.arange(self.l_ws, width + self.l_ws, self.step).astype(int)
        data = self._pad(data)
        for i in x_range:
            i_start = i - self.l_ws
            i_end = i + self.r_ws
            for j in y_range:
                j_start = j - self.l_ws
                j_end = j + self.r_ws
                data_list.append(data[i_start:i_end, j_start:j_end])
        self.slide_data = np.array(data_list).reshape(len(x_range), len(y_range), self.winsize, self.winsize, bands)
        return self.slide_data
    
    def pcorr():
        pass




def split_array(array:np.ndarray, num_chunks=None, chunk_size=None) -> list[np.ndarray]:
    """
    Split an input array into chunks by specified number of chunks or fixed chunk size.

    Parameters:
    ----------
    array : np.ndarray
        Input multidimensional array to be split. Must have at least 1 dimension.
    num_chunks : int, optional
        Number of chunks to create. If specified:
        - Prioritizes chunk count over chunk size
        - Last chunk may contain more samples if array length isn't divisible
        - Mutually exclusive with chunk_size parameter
    chunk_size : int, optional
        Number of samples per chunk. If specified:
        - Splits array into chunks of fixed size
        - Last chunk may be smaller than specified size
        - Mutually exclusive with num_chunks parameter

    Returns:
    ----------
    list[np.ndarray]
        List of array chunks. Each element is a view of the original array.

    """
    total_size = array.shape[0]

    if num_chunks is not None:
        chunk_size = total_size // num_chunks
        chunks = [array[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks - 1)]
        last_chunk = array[(num_chunks - 1) * chunk_size:]
        chunks.append(last_chunk)
    elif chunk_size is not None:
        num_chunks = total_size // chunk_size + (1 if total_size % chunk_size != 0 else 0)
        chunks = [array[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]
    else:
        raise ValueError("Must specify either num_chunks or chunk_size")

    return chunks



def sequence_split(sequence: Union[np.ndarray, list], num_chunks: int = None,  chunk_size: int = None) -> List[Union[np.ndarray, list]]:
    """
    Split an input sequence (array or list) into chunks by specified number of chunks 
    or fixed chunk size. Automatically detects input type and returns corresponding chunks.

    Parameters:
    ----------
    sequence : Union[np.ndarray, list]
        Input sequence to be split. For numpy arrays, must have at least 1 dimension.
    num_chunks : int, optional
        Number of chunks to create. If specified:
        - Prioritizes chunk count over chunk size
        - Last chunk may contain more samples if sequence length isn't divisible
        - Mutually exclusive with chunk_size parameter
    chunk_size : int, optional
        Number of samples per chunk. If specified:
        - Splits sequence into fixed-size chunks
        - Last chunk may be smaller than specified size
        - Mutually exclusive with num_chunks parameter

    Returns:
    ----------
    List[Union[np.ndarray, list]]
        List of sequence chunks. Returns same type as input.
    """
    total_size = len(sequence)

    if num_chunks is not None:
        chunk_size = total_size // num_chunks
        chunks = [sequence[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks - 1)]
        last_chunk = sequence[(num_chunks - 1) * chunk_size:]
        chunks.append(last_chunk)
    elif chunk_size is not None:
        num_chunks = total_size // chunk_size + (1 if total_size % chunk_size != 0 else 0)
        chunks = [sequence[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]
    else:
        raise ValueError("Must specify either num_chunks or chunk_size")

    return chunks

