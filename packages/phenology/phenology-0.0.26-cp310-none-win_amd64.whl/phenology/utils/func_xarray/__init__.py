import xarray as xr


def swap_longtitude(ds:xr.Dataset, **kwargs):
    '''
    Converts longitudes based on the input dataset's longitude range:
    - If the input dataset's longitude range is -180 to 180 degrees, it converts to 0-360 degrees.
    - If the input dataset's longitude range is 0-360 degrees, it converts to -180 to 180 degrees.

    Parameters:
    - ds (xarray.Dataset): Input dataset.
    - lon_dim (str, optional): The dimension representing longitudes. Default is 'longitude'.

    Returns:
    xarray.Dataset: Dataset with longitudes converted based on the specified conditions and sorted by latitude and longitude.
    '''

    lon_dim = kwargs.get('lon_dim', 'lon')
    swap_type = kwargs.get('swap_type', '180')
    dims = list(ds.dims)
    if not lon_dim in dims:
        for item in ['longitude', 'x', 'Lon', 'Longitude']:
            if item in dims:
                lon_dim = item
                break
    if not lon_dim in dims:
        lon_dim = max(dims, key=dims.get)

    lon_arr = ds[lon_dim].values
    if swap_type == '180' and max(ds[lon_dim].values) > 300:
        lon_arr[lon_arr > 180] = lon_arr[lon_arr > 180] - 360
    elif swap_type == '360' and min(ds[lon_dim].values) < 0:
        lon_arr[lon_arr < 0] = lon_arr[lon_arr < 0] + 360

    ds[lon_dim] = lon_arr

    return ds.sortby(lon_dim)
