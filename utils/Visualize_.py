import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import salem
import proplot as plot
import proplot
import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER , LATITUDE_FORMATTER
import matplotlib as mpl
from netCDF4 import Dataset
import matplotlib.colors as mcolors
from datetime import datetime, timedelta
import matplotlib.patheffects as PathEffects
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import cartopy.io.shapereader as shpreader
import rioxarray
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import geopandas as gpd
from matplotlib.colors import BoundaryNorm
from shapely.geometry import mapping



def define_figure(projection):
    # Create Figure -------------------------
    fig_array = [[1,1,]]
    fig, axs = proplot.subplots(fig_array, 
                                aspect=10, axwidth=5, proj=projection,
                                hratios=(1,), includepanels=True)
    ax = axs[0]
    return fig, ax
    
def clip_extent(ax, lonlim, latlim):
    ax.format(lonlim=lonlim, latlim=latlim, labels=False, longrid=False, latgrid = False)

def handle_shapefiles(ax, projection, shp_prov):
    
    # Turkey shapefile
    shape_feature_turkey = ShapelyFeature(Reader(shp_prov).geometries(),
                                          projection, facecolor='none',
                                          edgecolor = 'black', linewidth = 0.2, zorder = 0.3)
    

    ax.add_feature(shape_feature_turkey)
        
        
    # shapefiles except for Turkey
    shpfilename = shpreader.natural_earth(resolution='10m',
                                          category='cultural',
                                          name='admin_0_countries')

    countries = ['Syria', 'Iraq',
                 'Iran', 'Azerbaijan',
                 'Armenia', 'Russia',
                 'Georgia', 'Bulgaria',
                 'Greece', 'Cyprus',
                 'Northern Cyprus']
    
    
    for country in shpreader.Reader(shpfilename).records():

        if country.attributes['ADMIN'] in countries:
            
            count_shp = country.geometry
            ax.add_geometries([count_shp], projection,
                               facecolor='white', edgecolor = 'black',
                               linewidth = 0.1, zorder = 2.2,)


        elif country.attributes['ADMIN'] == 'Turkey':
            count_shp = country.geometry
            ax.add_geometries([count_shp], projection,
                              facecolor='none', edgecolor='black',
                              linewidth=0.8, zorder=3)
            

def handle_cmap(fig, mesh, ticks, cbar_name):
    # CMAP ----------------------

    cbar = fig.colorbar(mesh, ticks=ticks,
                        loc='b', drawedges = False,
                        shrink=1, space = 0.8,
                        aspect = 30)
    
    cbar.set_label(label='{}'.format(cbar_name),
                   size=11, loc = 'center',
                   y=0.35, weight = 'bold')
    
    cbar.ax.tick_params(labelsize=10)
    cbar.outline.set_linewidth(2)
    cbar.minorticks_off()
    cbar.ax.get_children()[4].set_color('black')
    cbar.solids.set_linewidth(1)
    
def plot_names(ax, shp_prov, crs):
    
    shp_dt = gpd.read_file(shp_prov)
    x = shp_dt.geometry.centroid.x.values
    y = shp_dt.geometry.centroid.y.values
    names = shp_dt['İl'].values
    
    for i,j,k in zip(x,y,names):
        
        # adjust
        if k == 'Antalya':
            ax.text(i, j+0.15, k, color='black', size=4,
                        ha='center', weight='bold', va='center',
                        transform=crs, zorder = 12,
                        path_effects=[PathEffects.withStroke(linewidth=2,
                                                             foreground="white",
                                                             alpha=.8)]
                       )
        else:
            ax.text(i, j, k, color='black', size=4,
                        ha='center', weight='bold', va='center',
                        transform=crs, zorder = 12,
                        path_effects=[PathEffects.withStroke(linewidth=2,
                                                             foreground="white",
                                                             alpha=.8)]
                       )
            
            
def plot_whole(ds_pred, cmap, vmin, vmax, ticks,
               variable, crs, shp_prov, lon_name,
               lat_name, cbar_name):
    
    # norm
    norm = BoundaryNorm(np.arange(vmin, vmax+0.1, 1),
                        ncolors=cmap.N,
                        clip=True)

    # fig, ax
    fig, ax = define_figure(cartopy.crs.Mercator(29))
    # set extent
    clip_extent(ax, lonlim=(26, 45), latlim=(35, 43))
    # add shapefile
    handle_shapefiles(ax, crs, shp_prov) 

    # plot data
    mesh = ax.pcolormesh(ds_pred[lon_name].values,
                         ds_pred[lat_name].values,
                         ds_pred[variable].values, 
                         cmap=cmap, norm=norm,
                         vmin=vmin, vmax=vmax,
                         transform=crs, 
                         zorder = 0.1)
    ax.patch.set_facecolor('lightblue')

    # cmap
    handle_cmap(fig, mesh, ticks, cbar_name)
    # province names
    plot_names(ax, shp_prov, crs)