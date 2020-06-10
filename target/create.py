# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 20:59:18 2020

@author: qtckp
"""

from heatmap import save_heatmaps
from get_data_from_file import get_all_data


def create_maps(filename, dpi = 350):
    data, x, y, t = get_all_data(filename)

    print(f'data.shape = {data.shape}')
    print(f'x axis: min = {x.min()}, max = {x.max()}, count = {len(x)}\n')
    print(f'y axis: min = {y.min()}, max = {y.max()}, count = {len(y)}\n')
    print(f'time: min = {t.min()}, max = {t.max()}, count = {len(t)}\n')

    every = int(input('Show every (how much?) time sample: '))

    save_heatmaps(data, x, y, t, every = every, dpi = dpi)
    
    
if __name__ == '__main__':
    
    with open('path.txt') as f:
        filename = f.readline().strip()
    
    create_maps(filename)





