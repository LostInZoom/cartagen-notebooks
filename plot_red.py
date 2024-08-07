# Importing libraries

from matplotlib import pyplot as plt # for ploting results, especially maps
import cartagen4py as c4 # the main library, containing cartographic generalization algorithms
import geopandas as gp # used to import and manipulate geographic data
import pandas as pd # used to concatenate datas
import ipywidgets # creation of interactive plots
import os # navigation within the environnement
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar # adding scalebar to the maps
import matplotlib.colors as matcol # generating color palettes
#from matplotlib.path import Path  # Plot generation
#from matplotlib.patches import PathPatch # Plot generation
from matplotlib.figure import Figure # Plot generation
from mpl_toolkits.axisartist.axislines import Subplot # Plot generation
from shapely.geometry import Point, Polygon, LineString, MultiPolygon # Create and manipulate geometries
from shapely.wkt import loads # Create and manipulate geometries
from tqdm.notebook import tqdm # Creating loading bar
from time import sleep # Creating loading bar
import numpy as np # Using mathematical operations in Python
import re # regex
from IPython.display import clear_output, Image # used to delete widgets


from matplotlib.path import Path
from matplotlib.patches import PathPatch

import warnings # Remove warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*GeoDataFrame you are attempting to plot is empty.*") # Remove user warning 
warnings.filterwarnings("ignore", category=UserWarning, message=".*CRS not set for some of the concatenation inputs.*.")


def bf_af_4(SCREEN, scale, gdf_bckgrnd, area_built, build_base, SYMBO_PARAM, train, sport, vegetation, water, commune, roads_base, road, veget_gen):

    fig = plt.figure(figsize=(SCREEN[scale]))
    ax1 = fig.add_subplot(111)
    plt.xlim(668198, 669411)
    plt.ylim(6860147, 6860869)	
    plt.title("Before")	
    scalebar = AnchoredSizeBar(ax1.transData,
                                        250,  
                                        '250 m',  
                                        'lower left',  
                                        pad=0.5,
                                        color='black',
                                        frameon=True,
                                        size_vertical=1)
    ax1.add_artist(scalebar)
    ax1.axes.get_xaxis().set_visible(False)
    ax1.axes.get_yaxis().set_visible(False)
    
    fig2 = plt.figure(figsize=SCREEN[scale])
    ax2 = fig2.add_subplot(111)
    plt.xlim(668198, 669411)
    plt.ylim(6860147, 6860869)
    plt.title("After")	
    scalebar = AnchoredSizeBar(ax2.transData,
                                        250,  
                                        '250 m',  
                                        'lower left',  
                                        pad=0.5,
                                        color='black',
                                        frameon=True,
                                        size_vertical=1)
    ax2.add_artist(scalebar)	
    ax2.axes.get_xaxis().set_visible(False)
    ax2.axes.get_yaxis().set_visible(False)	
    
    gdf_bckgrnd.plot(ax=ax2, color = SYMBO_PARAM['bckgrnd_col'])
    gdf_bckgrnd.plot(ax=ax1, color = SYMBO_PARAM['bckgrnd_col'])
        
    area_built.plot(ax = ax2, color = SYMBO_PARAM['residential_col']) 
        
    col_buildings = matcol.LinearSegmentedColormap.from_list('colbuildings',
                                                            [SYMBO_PARAM['agricultural_col'], SYMBO_PARAM['annex_col'],SYMBO_PARAM['com_serv_col'], SYMBO_PARAM['other_col'],SYMBO_PARAM['religious_col'],SYMBO_PARAM['residential_col'],SYMBO_PARAM['sports_field_col']])       
    build_base.plot(ax=ax1, column = 'usage_1', cmap = col_buildings)
        
    train.plot(ax=ax1, color = SYMBO_PARAM['trainline_col'], linewidth = SYMBO_PARAM['trainline_width'])
    train.plot(ax=ax2, color = SYMBO_PARAM['trainline_col'], linewidth = SYMBO_PARAM['trainline_width'])    
    
    sport.plot(ax=ax1, color = SYMBO_PARAM['sports_field_col']) 
    sport.plot(ax=ax2, color = SYMBO_PARAM['sports_field_col'])
    
    vegetation.plot(ax=ax1, color = SYMBO_PARAM['vegetation_col']) 
    veget_gen.plot(ax=ax2, color = SYMBO_PARAM['vegetation_col'])
        
    water.plot(ax=ax1, color = SYMBO_PARAM['water_col'])
    water.plot(ax=ax2, color = SYMBO_PARAM['water_col'])
    
         
    for i in reversed(range(2,7)):
        roads_base[(roads_base.importance == f"{i}")].plot(ax=ax1, color = "#1f2232", linewidth = SYMBO_PARAM[f'road_width_{i}']+1)
        roads_base[(roads_base.importance == f"{i}")].plot(ax=ax1, color = SYMBO_PARAM[f'road_col_{i}'], linewidth = SYMBO_PARAM[f'road_width_{i}'])
        
        road[(road.importance == f"{i}")].plot(ax=ax2, color = "#1f2232", linewidth = SYMBO_PARAM[f'road_width_{i}']+1)
        road[(road.importance == f"{i}")].plot(ax=ax2, color = SYMBO_PARAM[f'road_col_{i}'], linewidth = SYMBO_PARAM[f'road_width_{i}'])
 
    commune.plot(ax=ax1, facecolor = 'None', edgecolor = SYMBO_PARAM['communes_col'], linewidth = SYMBO_PARAM['communes_width'],linestyle=(0,(5,10)), alpha = 0.5)
    commune.plot(ax=ax2, facecolor = 'None', edgecolor = SYMBO_PARAM['communes_col'], linewidth = SYMBO_PARAM['communes_width'],linestyle=(0,(5,10)), alpha = 0.5)