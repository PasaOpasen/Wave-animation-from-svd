# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 20:59:18 2020

@author: qtckp
"""

from heatmap import save_heatmaps
from get_data_from_file import get_all_data
import os
import sys


def create_maps(filename, positions=[], dpi = 350, quantile = 0.001, cmap = 'twilight'):
    
    data, x, y, t = get_all_data(filename)
    
    if len(positions)>0:
        s1 = slice(positions[0],positions[1]+1)
        s2 = slice(positions[2],positions[3]+1)
        s3 = slice(positions[4],positions[5]+1)
        x = x[s1]
        y = y[s2]
        t = t[s3]
        data = data[s3,s1,s2]
        

    print(f'data.shape = {data.shape}\n')
    print(f'x axis: min = {x.min()}, max = {x.max()}, count = {len(x)}\n')
    print(f'y axis: min = {y.min()}, max = {y.max()}, count = {len(y)}\n')
    print(f'time: min = {t.min()}, max = {t.max()}, count = {len(t)}\n')

    every = int(input('Show every (how much?) time sample: '))

    save_heatmaps(data, x, y, t, every = every, dpi = dpi, quantile = quantile, cmap = cmap)
    
    
if __name__ == '__main__':
    
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    with open('path.txt') as f:
        filename = f.readline().strip()
    
    if len(sys.argv)>2:
        print(f"I see arguments {sys.argv[1:]}")
    
    create_maps(filename, positions = [int(a) for a in sys.argv[1:]])





