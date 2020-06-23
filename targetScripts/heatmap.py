# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 17:51:00 2020

@author: qtckp
"""


import matplotlib.pyplot as plt
import numpy as np
from get_data_from_file import get_all_data
from matplotlib.ticker import MaxNLocator

def heatmap2d(arr: np.ndarray):
    plt.imshow(arr, cmap='viridis')
    plt.colorbar()
    plt.show()


def save_heatmaps(data, xnet, ynet,  timenet, every = 20, dpi = 350, out_file = 'times.txt', quantile = 0.001, cmap = 'PiYG'):
        
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
    cmap = plt.get_cmap(cmap)
    
    tmp = 0
    print('Start creating and saving heatmaps...')
    for t in range(0, len(timenet), every):
    
        figure, axes = plt.subplots()
        
        #c = axes.pcolormesh(a, b, data[t,:,:], cmap='copper', vmin=l_c, vmax=r_c)
        c = axes.contourf(a, b, data[t,:,:], cmap=cmap, levels = levels, vmin=l_c, vmax=r_c)
        
        name = 'time = {:.8f}'.format(timenet[t])
        axes.set_title(name)
        axes.axis([l_a, r_a, l_b, r_b])
        figure.colorbar(c)
        
        #plt.show()
        
        figure.savefig(f'{name}.png', dpi = dpi)
        
        #figure.clf()
        plt.close(figure)
        
        tmp+=1
        if tmp%10 == 0:
            print("{:.2%}".format(t/len(timenet)))
    
    
    print(f"Saving names...")
    with open(out_file, 'w') as f:
        for t in range(0, len(timenet), every):
            f.write('time = {:.8f}.png\n'.format(timenet[t]))
        
        








#filename = r"D:\svd_to_animation\Scan_time_10-30_area_hann7_143kHz.svd"

#data, x, y, t = get_all_data(filename)

#save_heatmaps(data, x, y, t)


#tmp = data[500,:,:]


# heatmap2d(tmp)



# a, b = np.meshgrid(x,y)

# c = tmp
# l_a=a.min()
# r_a=a.max()
# l_b=b.min()
# r_b=b.max()
# l_c,r_c  = -np.abs(c).max(), np.abs(c).max()

# figure, axes = plt.subplots()

# c = axes.pcolormesh(a.T, b.T, c, cmap='copper', vmin=l_c, vmax=r_c)
# axes.set_title('Heatmap')
# axes.axis([l_a, r_a, l_b, r_b])
# figure.colorbar(c)

# plt.show()

# figure.savefig('r.png',dpi = 350)





# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from matplotlib.ticker import LinearLocator

# # generate example data
# import numpy as np
# x, y = np.meshgrid(np.linspace(-1,1,15),np.linspace(-1,1,15))
# z = np.cos(x*np.pi)*np.sin(y*np.pi)

# # actual plotting example
# fig = plt.figure()
# ax1 = fig.add_subplot(121, projection='3d')
# ax1.plot_surface(x,y,z,rstride=1,cstride=1,cmap='viridis')
# ax2 = fig.add_subplot(122)
# cf = ax2.contourf(x,y,z,51,vmin=-1,vmax=1,cmap='viridis')
# cbar = fig.colorbar(cf)
# cbar.locator = LinearLocator(numticks=11)
# cbar.update_ticks()

# for ax in {ax1, ax2}:
#     ax.set_xlabel(r'$x$')
#     ax.set_ylabel(r'$y$')
#     ax.set_xlim([-1,1])
#     ax.set_ylim([-1,1])
#     #ax.set_aspect('equal')

# ax1.set_zlim([-1,1])
# #ax1.set_zlabel(r'$\cos(\pi x) \sin(\p    i y)$')

# plt.show()

























