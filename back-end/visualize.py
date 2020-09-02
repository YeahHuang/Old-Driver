from bokeh.plotting import figure, output_notebook, show
#new :36
from collections import Iterator
from io import BytesIO
import numba as nb
import toolz as tz
import xarray as xr
from PIL.Image import fromarray
# new end
import numpy as np # linear algebra
import pandas as pd
import datashader as ds
from datashader import transfer_functions as tr_fns
from datashader.colors import Greys9
from datashader.bokeh_ext import InteractiveImage
from functools import partial
from datashader.utils import export_image
from datashader.colors import colormap_select, Greys9, Hot, viridis, inferno

plot_width = int(750)
plot_height = int(plot_width//1.2)
NYC = x_range, y_range = ((-74.05, -73.7), (40.6, 40.9))
def base_plot(tools='pan, wheel_zoom, reset', plot_width=plot_width, plot_height=plot_height, **plot_args):
    p = figure(tools=tools, plot_width=plot_width, plot_height=plot_height,
              x_range=x_range, y_range=y_range, outline_line_color=None,
              min_border=0, min_border_left=0, min_border_right=0,
              min_border_top=0, min_border_bottom=0, **plot_args)  
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    return p
    
df = pd.read_csv('train_filter.csv',
                 usecols=['pickup_datetime', 'dropoff_datetime', 'passenger_count', 'pickup_longitude', 'pickup_latitude',
                          'dropoff_longitude', 'dropoff_latitude',  'trip_duration'])
df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"])


df = df[(df.pickup_datetime.dt.hour.between(16,17,inclusive = True))]

cvs = ds.Canvas(plot_width=plot_width, plot_height=plot_height, x_range=x_range, y_range=y_range)
agg = cvs.points(df, 'dropoff_longitude', 'dropoff_latitude', ds.count('passenger_count'))
img = tr_fns.shade(agg, cmap=["white", 'darkblue'], how='linear')



background = "black"
export = partial(export_image, export_path="export", background=background)
cm = partial(colormap_select, reverse=(background=="black"))

def create_image(x_range, y_range, w=plot_width, h=plot_height):
    cvs = ds.Canvas(plot_width=w, plot_height=h, x_range=x_range, y_range=y_range)
    agg = cvs.points(df, 'dropoff_longitude', 'dropoff_latitude', ds.count('passenger_count'))
    img = tr_fns.shade(agg, cmap=Hot, how='eq_hist')
    return tr_fns.dynspread(img, threshold=0.5, max_px=4)

p = base_plot(background_fill_color=background)
export(create_image(*NYC), "NYCT_hot_16m")
InteractiveImage(p, create_image)
