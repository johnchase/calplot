#!/usr/bin/env python

import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import calendar
import numpy as np
import itertools
import matplotlib.patches as patches


def scale(values, start=0, end=100):
    '''Scale a set of values to a range with a specified start and end.
    Parameters
    ----------
    values : list or array
        The values to be scaled
    start : int
        The lower bound of the output scale
    end : int
        The upper bound of the output scale
    Returns
    -------
    scaled range : list
        A list of the scaled values
    Examples
    -------
    >>> scale([0, 2, 10], 0, 100)
        [0.0, 20.0, 100.0]
   '''

    old_min = min(values)
    old_range = max(values) - old_min
    new_range = end - start

    def f(x):
        return (((x - old_min) * new_range) / old_range) + start
    return [f(e) for e in values]

def get_color_map(sample_md, continuous=False, colormap=None):
    """Create a colormap from a `pd.Series of categorical or continous data
    Parameters
    ----------
    sample_md: pd.Series
        a pandas series containing the sample id as the index and the values
         as the metadata category to color by
    continuous: bool, optional
        Pass True if the data is continuous. Default False
    colormap: str
        A string of the colormap. Valid entries can be found here:
        http://matplotlib.org/examples/color/colormaps_reference.html default
        is 'viridis' for continuous colormaps and 'Set1' for categorical
    Returns
    -------
    color_series: pd.Series
        pandas series containing the colors that should be plotted. The index
        of the series should match the index of the sample_md. default is None.
        if None is passed a color map will be generated.
    Examples
    --------
    >>> sample_md = pd.Series(list('abcd'), index=['s1', 's2', 's3', 's4'])
    >>> colors = get_color_map(sample_md)
    """
    if continuous:
        n_colors = 101
        if colormap is None:
            colormap = 'viridis'

        palette = sns.color_palette(colormap, n_colors).as_hex()
        scaled_vals = scale(sample_md, 0, 100)
        colors = [palette[int(e)] for e in scaled_vals]
        color_series = pd.Series(colors, index=sample_md.index)

    else:
        n_colors = len(sample_md.unique())
        if colormap is None:
            if n_colors > 13:
                raise ValueError('Column contains more than 13 categories, if '
                                 'data is continuous use `continuous=True` or '
                                 'pass a custom color map')
            colormap = 'Set1'

        palette = sns.color_palette(colormap, n_colors).as_hex()
        color_dict = dict(zip(sample_md.unique().tolist(), palette))
        color_series = sample_md.replace(color_dict)

    return color_series

def date_to_coords(date):
    week_day = (date.weekday() + 1) % 7
    end_date = pd.datetime(date.year, 
                             date.month, 
                             calendar.mdays[date.month])

    offset = 6 - ((end_date.weekday() + 1) % 7)
    week = (end_date.day - (date.day - offset)) // 7
    return(week_day, week)


def format_dates(date_series, color_map='viridis'):
    month = date_series.index[1].month 
    year = date_series.index[1].year
    dates = pd.date_range(pd.datetime(year, month, 1), 
                          pd.datetime(year, month, 
                                      calendar.mdays[month]))
    date_series = date_series.reindex(dates,
                        fill_value=0)
    return bpl.get_color_map(date_series, 
                              continuous=True, 
                              colormap=color_map)
    

def plot_month(date_series, ax, text_color='k'):
    date_series = get_color_map(date_series, continuous=True)
    for day_of_month, id_ in enumerate(date_series.index):
        coords = date_to_coords(id_)
        patch = patches.Rectangle(coords, 1, 1, 
                                  facecolor=date_series[id_], 
                                  edgecolor='#ffffff')
        ax.add_patch(patch)
        
        x = coords[0] + .1
        y = coords[1] + .675
        ax.annotate(day_of_month + 1, 
                    xy=(x, y),
                    color=text_color,
                   size=12)
        
    coords = np.array(list(map(date_to_coords, date_series.index)))
    n_weeks = coords.T[1].max() + 1
    
    ax.set_xlim(0, 7)
    ax.set_ylim(0, n_weeks)
    ax.set_xticklabels(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], rotation=45)
    ax.xaxis.tick_top()
    ax.set_xticks(np.arange(0.6, 7.6, 1))
    ax.set_yticklabels('')
    return ax
