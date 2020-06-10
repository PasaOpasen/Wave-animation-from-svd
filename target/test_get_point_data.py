# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 11:52:33 2020

@author: qtckp
"""

# [x,y,usd] = GetPointData(filename, domainname, channelname, signalname, displayname,
#   point, frame)
# 
# Gets original or user defined data from a polytec file.
#
# filename is the path of the .pvd or .svd file
# domainname is the name of the domain, e.g. 'FFT' or 'Time'
# channelname is the name of the channel, e.g. 'Vib' or 'Ref1' or 'Vib &
#   Ref1' or 'Vib X' or 'Vib Y' or 'Vib Z'.
# signalname is the name of the signal, e.g. 'Velocity' or 'Displacement'
# displayname is the name of the display, e.g. 'Real' or 'Magnitude' or
#   'Samples'. If the display name is 'Real & Imag.' the data is returned
#   as complex values.
# point is the (1-based) index of the point to get data from. If point is
#   0 the data of all points will be returned. y will contain the data of
#   point i at row index i.
# frame is the frame number of the data. for data acquired in MultiFrame
#   mode, 0 is the averaged frame and 1-n are the other frames. For user
#   defined datasets the frame number is in the range 1-n where n is the
#   number of frames in the user defined dataset. For all other data,
#   use frame number 0.
#
# returns x, the x axis values of the data
# returns y, the data. colomns correspond to the x-axis, rows to the point
#   index. for point = 0: rows for points that have no data are set to zeros.
# returns usd, a struct describing the signal
#

from win32com.client import Dispatch
import numpy as np


class Empty:
    pass


filename = r"D:\svd_to_animation\3Lines_scan_pulse_1mus_70Vpp.svd"
domainname = 'Time'
channelname = 'Vib'
signalname = 'Velocity'
displayname = 'Samples'
point = 0
frame = 0

### function [x,y,usd] = GetPointData(filename, domainname, channelname, signalname, displayname, point, frame)

file = Dispatch('PolyFile.PolyFile') 

try:
    file.Open(filename) 
    pointdomains = file.GetPointDomains() 
    pointdomain = pointdomains.Item(domainname) 
    channel = pointdomain.Channels.Item(channelname) 
    signal = channel.Signals.Item(signalname) 
    display = signal.Displays.Item(displayname) 
    #
    signalDesc = signal.Description 
    xaxis = signalDesc.XAxis 
    yaxis = signalDesc.YAxis 
    #x = xaxis.Min:(xaxis.Max - xaxis.Min)/(xaxis.MaxCount - 1):xaxis.Max 
    x = np.linspace(xaxis.Min,xaxis.Max,xaxis.MaxCount)
    
    usd = Empty()
    
    usd.Name = signalDesc.Name 
    usd.Complex = signalDesc.Complex 
    # usd.DataType = signalDesc.DataType 
    # usd.DomainType = signalDesc.DomainType 
    # usd.FunctionType = signalDesc.FunctionType 
    # usd.PowerSignal = signalDesc.PowerSignal 
    # usd.Is3D = signalDesc.ResponseDOFs.Count > 0 and 'ptcVector' in str(signalDesc.ResponseDOFs.Direction)
    
    # responseDOFs = signalDesc.ResponseDOFs 
    # if (responseDOFs.Count == 0):
    #     usd.ResponseDOFs = [] 
    # else:
    #     for i in range(1, responseDOFs.Count+1):
    #         usd.ResponseDOFs[i] = (responseDOFs.Item(i)) 
         
     
    # referenceDOFs = signalDesc.ReferenceDOFs 
    # if (referenceDOFs.Count == 0):
    #     usd.ReferenceDOFs = [] 
    # else:
    #     for i in range(1, responseDOFs.Count+1):
    #         usd.ReferenceDOFs(i) = (referenceDOFs.Item(i)) 
         
     
    # usd.DbReference = signalDesc.DbReference 
    # usd.XName = xaxis.Name 
    # usd.XUnit = xaxis.Unit 
    usd.XMin = xaxis.Min 
    usd.XMax = xaxis.Max 
    usd.XCount = xaxis.MaxCount 
    # usd.YName = yaxis.Name 
    # usd.YUnit = yaxis.Unit 
    usd.YMin = yaxis.Min 
    usd.YMax = yaxis.Max 
    
    #
    datapoints = pointdomain.datapoints 
    if (point == 0):
        # get data of all points
        y = [] 
        for i in range(1,datapoints.count):
            datapoint = datapoints.Item(i) 
            if 'ptcChannelCapsUser' in str(channel.caps):        
                ytemp = np.array([float(val) for val in datapoint.GetData(display, frame)])
                if (len(ytemp) > 0):
                    # not all points might have user defined data attached.
                    # polytec file access returns an empty array in this case.
                    if (len(y)==0):
                        y = np.zeros((datapoints.count, len(ytemp)))
                     
                    y[i-1,:] = ytemp 
                 
            else:
                try:
                    # ignore errors because of invalid data, the result row
                    # will contain zeros in this case
                    ytemp = np.array([float(val) for val in datapoint.GetData(display, frame)])
                    if len(y)==0:
                        y = np.zeros((datapoints.count, len(ytemp)))
              
                    y[i-1,:] = ytemp 
                except:
                    pass
                 
             
                #usd.YCount = y.shape[0]/usd.XCount
    else:
        datapoint = datapoints.Item(point) 
        y = np.array([float(val) for val in datapoint.GetData(display, frame)]) 
     
    # handle complex data
    if usd.Complex:# and 'ptcDisplayRealImag' in str(display.Type):
        realData = y[:,0::2]
        imagData = y[:,1::2]
        y = realData + imagData*np.complex(0,1)
     
    #
    file.Close() 
    del file
    
except:
    
    if file.IsOpen:
        file.Close() 
     
