import numpy as np
import pandas as pd
import multiprocessing as mp
from tqdm import tqdm



def opl_for_parallel(args):
    from .api_opl_v1 import opl_api
    y, x, max_month, target_vars, index = args
    result = opl_api(y, x, max_month=max_month, target_vars=target_vars, index=index)
    return result
  

def get_opl_v1(y:np.ndarray, x:np.ndarray, **kwargs):
    """
    Calculate the optimal pre-season length for specified variables.

    Parameters:
    - y: np.ndarray, shape (rows, cols, years, 1) or (years, 1)
      Target variable data over the years. such as phenological data at an annual scale.

    - x: np.ndarray, shape (rows, cols, months, vars) or (months, vars)
      Explanatory variables data at a monthly scale, covering one more year than y data (months = 12 * (years + 1)).

    Keyword Arguments (kwargs):
    - n_jobs: int, default --> mp.cpu_count()
      number of jobs to run in parallel. 
    
    - max_month: int, default 6
      Maximum pre-season length calculated forward from the current month.

    - target_vars: list, default None
      variable names for calculating optimal pre-season length. Default --> x.columns.to_list().

    Returns: 
    - for multiple data (eg. x.ndim == 4)
      result: np.ndarray, shape (rows, cols, 6, len(target_vars))
      In the 3rd dimension of result, the 6 elements are ['n', 'r', 'ci95lower', 'ci95upper', 'p-val', 'opl'], where opl is the optimal pre-season length.
      
    - for single data (eg. x.ndim == 2)
      result: pd.DataFrame
      Columns: ['n', 'r', 'CI95%', 'p-val', 'opl', 'var', 'index'], where opl is the optimal preseason length.
    """
    

    n_jobs = kwargs.get('n_jobs', mp.cpu_count())
    max_month = kwargs.get('max_month', 6)
    target_vars = kwargs.get('target_vars', [f'x{i}' for i in range(x.shape[-1])])
    
    
    if x.ndim == 2:
        from .api_opl_v1 import opl_api
        if y.ndim == 1:
            y = y.reshape((-1, 1))
        return opl_api(y, x, max_month=max_month, target_vars=target_vars)
    

    rows, cols, months, vars  = x.shape
    x = x.reshape((rows * cols, months, vars)) 
    y = y.reshape((rows * cols, -1, 1))

    args_list = [[y[index], x[index], max_month, target_vars, index] for index in range(rows * cols)]
    
    print('Start parallel computation, parallel processing cores: ', n_jobs)
    
    result = []
    with mp.Pool(processes=n_jobs) as pool:
        for res in tqdm(pool.imap_unordered(opl_for_parallel, args_list), ncols=100, total=len(args_list)):
            result.append(res)
    
    result = pd.concat(result, axis=0)
    
    # Split CI95% column
    result[['ci95lower', 'ci95upper']] = pd.DataFrame(result['CI95%'].tolist(), index=result.index)
    result.drop('CI95%', axis=1, inplace=True)
    
    # Identify missing rows
    missing_rows = pd.DataFrame(columns=result.columns)
    missing_rows['index'] = list(set(range(rows * cols)).difference(result['index']))

    var_list = result['var'].unique()

    result_list = [result] + [missing_rows.assign(var=i) for i in var_list]
    res_grouped = pd.concat(result_list).groupby('var')

    result = np.stack([group_data.sort_values('index')[['n', 'r', 'ci95lower',	'ci95upper', 'p-val', 'opl']].values
                       .reshape(rows, cols, -1)
                       .astype(np.float32)
                       for group_id, group_data in res_grouped
                       ], axis=-1
                      )
    return result

