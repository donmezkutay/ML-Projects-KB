####### Utils for Data Post-processing #######

# math-df libraries
import numpy as np

# df libraries
import pandas as pd
import xarray as xr

def pd_to_xr(df_with_na, df_pred, lon_name, lat_name):
    
    df_pred_with_na = df_with_na.merge(df_pred[['pred', 'lat_lon']], how='left')
    df_pred_with_na.set_index([lat_name, lon_name], inplace=True)
    ds_pred = df_pred_with_na.to_xarray()
    
    return ds_pred