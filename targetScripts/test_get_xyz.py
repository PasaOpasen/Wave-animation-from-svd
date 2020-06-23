# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 14:32:01 2020

@author: qtckp
"""

from win32com.client import Dispatch
import numpy as np

# XYZ = GetXYZCoordinates(filename, point)
# ----------------------------------------
# Gets XYZ coordinates of the scan points from a polytec file.
#
# This is only possible for files containing 3D geometry or that have
#   a distance to the object specified. Otherwise there will be an
#   error message.
#
# filename is the path of the .svd file
# 
# point is the (1-based) index of the point to get the coordinates from. If point is
#   0 the coordiantes of all points will be returned. XYZ will contain the data of
#   point i at row index i.
#
# returns the xyz coordinates. columns correspond to the geometry X, Y, Z
#   in meter, rows to the point index.
#
#function XYZ = GetXYZCoordinates(filename, point)
#

point = 0
filename = r"D:\svd_to_animation\3Lines_scan_pulse_1mus_70Vpp.svd"


file = Dispatch('PolyFile.PolyFile') 
try:
    file.Open(filename) 
    measpoints = file.Infos.MeasPoints 
 
    if (point == 0):
        XYZ=np.zeros((measpoints.count,3)) 
        for i in range(1, measpoints.count+1):
            measpoint=measpoints.Item(i) 
            X,Y,Z =measpoint.CoordXYZ() 
            XYZ[i-1,:]= X,Y,Z                
         
    else:
        measpoint=measpoints.Item(point) 
        X,Y,Z = measpoint.CoordXYZ() 
        XYZ= X,Y,Z 
     
    file.Close() 
    del file
except:
    if file.IsOpen:
        file.Close() 
     
    del file
 

