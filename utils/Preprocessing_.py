####### Utils for Data Pre-processing #######

# math-df libraries
import numpy as np

# df libraries
import pandas as pd
import xarray as xr
import geopandas as gpd
from shapely.geometry import mapping

def kelvin_to_celcius(ds, var):
    ds[var] = ds[var] - 273.15
    ds[var].attrs['units'] = 'C'
    
    return ds


def interpolate_xy(data, lon_name, lat_name, interp_size):
    
    # new lon and lat info
    new_lon = np.linspace(data[lon_name][0], data[lon_name][-1], len(data[lon_name]) * interp_size)
    new_lat = np.linspace(data[lat_name][0], data[lat_name][-1], len(data[lat_name]) * interp_size)
    
    # interpolate the data
    new_parameters = {lon_name:new_lon,
                      lat_name:new_lat}
    interp_data = data.interp(new_parameters)
    
    return interp_data


def write_crs_info(data, projection):
    return data.rio.write_crs(projection)


def clip_area(data, shp_path, lon_name, lat_name):
    
    # open shapefile data
    shp_data = gpd.read_file(shp_path, encoding='UTF-8')
    
    # set spatial dims
    data = data.rio.set_spatial_dims(x_dim=lon_name, y_dim=lat_name)
    
    # clip data into shapefile
    clip_data = data.rio.clip(shp_data.geometry.apply(mapping), shp_data.crs)
    
    return clip_data


def xr_to_pd(data, lon_name, lat_name, with_na=False):
    
    df_with_na = data.to_dataframe().reset_index().drop(columns=['spatial_ref'])
    df_with_na['lat_lon'] = df_with_na[lat_name].astype(str) + ' | ' + df_with_na[lon_name].astype(str)
    df = df_with_na.dropna().reset_index(drop=True)    
    
    if with_na:
        return df_with_na
    
    return df