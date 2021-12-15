#
# M1P~/git/tumor3D_ML/output$ python plot_substrate3D_slice.py 16 4
#
# Dependencies include matplotlib and numpy. We recommend installing the Anaconda Python3 distribution.
#
# Author: Randy Heiland (except for the circles() function)
#
#
__author__ = "Randy Heiland"

import sys,pathlib
import xml.etree.ElementTree as ET
import math
import scipy.io
import matplotlib
import numpy as np
from numpy.random import randn
import matplotlib.pyplot as plt


if (len(sys.argv) < 3):
  frame_idx = 0
  field_index = 4
else:
  kdx = 1
  frame_idx = int(sys.argv[kdx])
  kdx += 1
  field_index = int(sys.argv[kdx])

print('frame, field = ',frame_idx, field_index)

fig = plt.figure(figsize=(7,5.8))
#ax = fig.gca()

time_delay = 0.1
count = -1

cbar = None

#def plot_substrate(FileId):
def plot_substrate():
    global frame_idx, axes_max, cbar

    # select whichever substrate index you want, e.g., for one model:
    # 4=tumor cells field, 5=blood vessel density, 6=growth substrate
#    field_index = 4  
#    field_index = 5  

    xml_file = "output%08d.xml" % frame_idx
    print("xml_file = ",xml_file)
    tree = ET.parse(xml_file)
    root = tree.getroot()
#    print('time=' + root.find(".//current_time").text)
    mins = float(root.find(".//current_time").text)
    hrs = mins/60.
    days = hrs/24.
    title_str = '%d days, %d hrs, %d mins' % (int(days),(hrs%24), mins - (hrs*60))

    xml_file = "output%08d.xml" % frame_idx
    tree = ET.parse(xml_file)
    root = tree.getroot()
    print('time=' + root.find(".//current_time").text)

#     print('debug> plot_substrate: idx=',FileId)
#    fname = "output%08d_microenvironment0.mat" % FileId
    fname = "output%08d_microenvironment0.mat" % frame_idx
    output_dir_str = '.'
    fullname = output_dir_str + "/" + fname
    if not pathlib.Path(fullname).is_file():
        print("file not found",fullname)
        return

    info_dict = {}
    scipy.io.loadmat(fullname, info_dict)
    M = info_dict['multiscale_microenvironment']
#     global_field_index = int(mcds_field.value)
    print('plot_substrate: field_index=',field_index)
    f = M[field_index,:]   # 
    #plt.clf()
    #my_plot = plt.imshow(f.reshape(400,400), cmap='jet', extent=[0,20, 0,20])
    
#    fig = plt.figure(figsize=(7,7))
#    fig = plt.figure(figsize=(7,5.8))

    # N = int(math.sqrt(len(M[0,:])))
    N = 50
    grid2D = M[0,:].reshape(N,N,N)
    xvec = grid2D[0,0,:]
    #xvec.size
    #xvec.shape
    num_contours = 30
    num_contours = 10
#    my_plot = plt.contourf(xvec,xvec,M[field_index,:].reshape(100,100), num_contours, cmap='viridis') #'viridis'
    substrate = M[field_index,:].reshape(N,N,N)
    # my_plot = plt.contourf(xvec,xvec,M[field_index,:].reshape(N,N), num_contours, cmap='viridis') #'viridis'
    my_plot = plt.contourf(xvec,xvec, substrate[:,:,25], num_contours, cmap='viridis') #'viridis'
#    cbar.remove()
    if cbar == None:
      cbar = plt.colorbar(my_plot)
    else:
      cbar = plt.colorbar(my_plot, cax=cbar.ax)
    axes_min = 0
    axes_min = -2000
    axes_max = 2000
#    plt.xlim(axes_min,axes_max)
#    plt.ylim(axes_min,axes_max)
    # plt.title(fname)
    plt.title(title_str)
#     ax.set_title(fname)
#    plt.axis('equal')

#    plt.show()

plot_substrate()
plt.show()

