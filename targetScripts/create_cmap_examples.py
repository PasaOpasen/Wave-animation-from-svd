# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 17:09:25 2020

@author: qtckp
"""


import matplotlib.pyplot as plt
import numpy as np
from get_data_from_file import get_all_data
from matplotlib.ticker import MaxNLocator


def save_heatmap_cmap(data, xnet, ynet,cmaps, which=400, dpi = 350, quantile = 0.001):
        
    a, b = np.meshgrid(xnet, ynet)
    
    a = a.T
    b = b.T
    
    l_a=a.min()
    r_a=a.max()
    l_b=b.min()
    r_b=b.max()
        
    l_c, r_c  = data.min(), data.max()
    
    print(f"Min Z val = {l_c}, Max Z val = {r_c}")
    
    d = quantile
    l_c = np.quantile(data, d)
    r_c = np.quantile(data, 1-d)
    print(f'{d} and {1-d} quantiles: {l_c}, {r_c}')
    
    levels = MaxNLocator(nbins=15).tick_values(l_c, r_c)
    
    for mp in cmaps: 
        
        cmap = plt.get_cmap(mp)
    
        figure, axes = plt.subplots()
        
        c = axes.contourf(a, b, data[which,:,:], cmap=cmap, levels = levels, vmin=l_c, vmax=r_c)
        
        name = f'cmap = {mp}'
        axes.set_title(name)
        axes.axis([l_a, r_a, l_b, r_b])
        figure.colorbar(c)
        
        #plt.show()
        
        figure.savefig(f'{name}.png', dpi = dpi)
        
        #figure.clf()
        plt.close(figure)
        

filename = r"D:\svd_to_animation\Scan_time_10-30_area_hann7_143kHz.svd"

data, x, y, _ = get_all_data(filename)


from heatmap import heatmap2d

heatmap2d(data[560,:,:])

save_heatmap_cmap(data, x, y, [
    'viridis', 'plasma', 'inferno', 'magma', 'cividis',
    
    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
    'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper',
        'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
            'twilight', 'twilight_shifted', 'hsv',
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
                        'Dark2', 'Set1', 'Set2', 'Set3',
                        'tab10', 'tab20', 'tab20b', 'tab20c',
                        
                         'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'
    ], 450)









