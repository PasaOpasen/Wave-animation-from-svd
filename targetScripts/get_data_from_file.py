# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 14:44:07 2020

@author: qtckp
"""

from win32com.client import Dispatch
import numpy as np
#import numba

class Empty:
    pass

def XYZ(filename, point = 0):
    """
    filename is the path of the .svd file
 
    point is the (1-based) index of the point to get the coordinates from. If point is
    0 the coordiantes of all points will be returned. XYZ will contain the data of
    point i at row index i.

   returns the xyz coordinates. columns correspond to the geometry X, Y, Z
   in meter, rows to the point index.
    """
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
        
        return XYZ
    except:
        if file.IsOpen:
            file.Close() 
         
        del file
        raise Exception('Cannot in XYZ')


def get_point(filename, domainname = 'Time', channelname = 'Vib', signalname = 'Velocity', displayname= 'Samples', point=0, frame=0):
    """
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
    """
    file = Dispatch('PolyFile.PolyFile') 
    
    print(f"Load datapoints from {filename}")
    
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
            ct = datapoints.count
            for i in range(1,ct):
                datapoint = datapoints.Item(i) 
                if 'ptcChannelCapsUser' in str(channel.caps):        
                    ytemp = np.array(map(float,datapoint.GetData(display, frame)))
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
                if i%80 == 0:
                    print("---> {:.2%}".format(i/ct))
                     
                 
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
        
        return x, y, usd
    except:
        
        if file.IsOpen:
            file.Close() 
        
        raise Exception('Cannot in get_point')
    


def find_net(filename):
    
    print(f"Reading coordinates from file {filename}...")
    data = XYZ(filename)
    
    print("Solving net params...")
    xmin, xmax, ymin, ymax = data[:,0].min(), data[:,0].max(), data[:,1].min(), data[:,1].max()

    for i in range(2,data.shape[0]):
        t = data.shape[0]/i
        if t == int(t):
            if data[i-1,0] > data[i,0]:
                break
            x, y = i, int(t)
    
    print(f"Found: xcount = {x}  ycount = {y}")
    print()
    
    return np.linspace(xmin, xmax, x), np.linspace(ymin, ymax, y)
    

def get_all_data(filename):
           
    xnet, ynet = find_net(filename)
    
    time, dt, _ = get_point(filename)
    
    data = dt.T.reshape(dt.shape[1], xnet.shape[0], ynet.shape[0])
    
    return data, xnet, ynet, time
    
    

    
filename = r"D:\svd_to_animation\3Lines_scan_pulse_1mus_70Vpp.svd"   

filename = r"D:\svd_to_animation\Scan_time_CA_6mm_pulse_sw2_114kHz_BigScan.svd"

filename = r"D:\svd_to_animation\Scan_time_10-30_area_hann7_143kHz.svd"


# data = XYZ(filename)

# for i in range(1,7):
#     for j in range(1,7):
          
#         xset = set(data[:,0].round(i))
#         yset = set(data[:,1].round(j))
        
#         print(f'{i} {j}  xlen = {len(xset)}  ylen = {len(yset)}  all = {len(xset)*len(yset)} vs {data.shape[0]}')




# import pylab

# pylab.scatter(data[:,0], data[:,1])



# xmax= data[:,0].max()
# xmin = data[:,0].min()

# for i in range(2,data.shape[0]):
#     t = data.shape[0]/i
#     if t == int(t):
#         if data[i-1,0] > data[i,0]:
#             break
#         x, y = i, int(t)




#xnet, ynet = find_net(filename)

#time, dt, _ = get_point(filename)

#data = dt.T.reshape(dt.shape[1], xnet.shape[0], ynet.shape[0])





#data, x, y, t = get_all_data(filename)


#%time get_all_data(filename)
#%time numba.jit(get_all_data(filename))
#%time numba.jit(get_all_data(filename),parallel = True)








