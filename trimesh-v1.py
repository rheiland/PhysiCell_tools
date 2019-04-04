# plot triangular meshes & "contours" from John's .mat data
#
# $ ipython --pylab
# In [1]: %run trimesh

import scipy.io

try:
  import matplotlib
  import matplotlib.colors as mplc
except:
  print("\n---Error: cannot import matplotlib")
  print("---Try: python -m pip install matplotlib")
  print(join_our_list)
#  print("---Consider installing Anaconda's Python 3 distribution.\n")
  raise
try:
  import numpy as np  # if mpl was installed, numpy should have been too.
except:
  print("\n---Error: cannot import numpy")
  print("---Try: python -m pip install numpy\n")
  print(join_our_list)
  raise
# from collections import deque
try:
  # apparently we need mpl's Qt backend to do keypresses 
#  matplotlib.use("Qt5Agg")
#   matplotlib.use("TkAgg")
  import matplotlib.pyplot as plt
except:
  print("\n---Error: cannot use matplotlib's TkAgg backend")
  print(join_our_list)
#  print("Consider installing Anaconda's Python 3 distribution.")
  raise


info_dict = {}
#        scipy.io.loadmat(fullname, info_dict)
fname = 'ALL_testing_time_0010_space_100_sim_time_008400.mat'
scipy.io.loadmat(fname, info_dict)
m = info_dict['populations_and_locations']
xctrs = m[10,:]
yctrs = m[11,:]
zctrs = m[12,:]


#        self.fig = plt.figure(figsize=(13.2,4))  # TODO: need function of domain sizes
lfig = 5
scale_factor = 40.0
plt.figure(figsize=(lfig,lfig))

  # draw one set of triangles (pointing up/down)
#   plt.scatter(xvals,yvals, marker=(3,1,180),s=rvals*scale_radius, c=rgbs)
  # draw another set of triangles (pointing opposite dir as others)
#   plt.scatter(xvals2,yvals2, marker=(3,1,0),s=rvals2*scale_radius, c=rgbs2


# plot center points (as circles)
kmin=0;kmax=20
#plt.scatter(xctrs[kmin:kmax],yctrs[kmin:kmax], marker='o',s=3, c='black')
plt.scatter(xctrs,yctrs, marker='o',s=3, c='black')

#plt.scatter(xctrs,yctrs, marker=(3,1,180),s=2*scale_factor, c='red')
#plt.scatter(xctrs,yctrs, marker=(3,1,0),s=2*scale_factor, c='green')

"""
In [28]: yctrs[0:20]
Out[28]: 
array([-1021.13248654, -1050.        , -1021.13248654, -1050.        ,
       -1021.13248654, -1050.        , -1021.13248654, -1050.        ,
       -1021.13248654, -1050.        , -1021.13248654, -1050.        ,
       -1021.13248654,  -934.52994616,  -963.39745962,  -934.52994616,
        -963.39745962,  -934.52994616,  -963.39745962,  -934.52994616])
"""
y0 = -1050
y1 = -1021.13
ydel = 5
#ydel = 1.0
#up_down = (y1 < yctrs < y0) 
#for idx in range(2):

# Rf. numpy.any, numpy.all, numpy.where, np.take
#In [42]: np.where(yctrs < y0)
#Out[42]: (array([ 1,  3,  5,  7,  9, 11]),)


ids_up = []
ids_down = []
ydel1 = 1050-963  # 87
while y0 < (yctrs.max() + ydel):
  for idx in range(len(yctrs)):
    if yctrs[idx] > (y0-ydel) and yctrs[idx] < (y0+ydel):
        #print(idx)
        ids_up.append(idx)
#    else:
#        ids_down.append(idx)
  y0 += ydel1
#  print("y0=",y0)

y0 = 75.83
while y0 < (yctrs.max() + ydel):
  for idx in range(len(yctrs)):
    if yctrs[idx] > (y0-ydel) and yctrs[idx] < (y0+ydel):
        #print(idx)
        ids_up.append(idx)
#    else:
#        ids_down.append(idx)
  y0 += ydel1
#  print("y0=",y0)


y=[idx for idx in range(len(yctrs))]
# create numpy arrays
a=np.array(y)
b=np.array(ids_up)
ids_down = np.setdiff1d(a, b)

x_up = np.take(xctrs,ids_up)
y_up = np.take(yctrs,ids_up)

x_down = np.take(xctrs,ids_down)
y_down = np.take(yctrs,ids_down)
    
scale_factor = 40.0
scale_factor = 35.0
glyphsize = 160
glyphsize = 100
up_color = 'green'
up_color = 'tan'
down_color = 'tan'
#plt.scatter(x_up,y_up, marker=(3,1,0),s=glyphsize, c=up_color)
#plt.scatter(x_down,y_down, marker=(3,1,180),s=glyphsize, c=down_color)


live = m[0,:]
live_up = np.take(live,ids_up)
live_down = np.take(live,ids_down)
up_plot = plt.scatter(x_up,y_up, marker=(3,1,0),s=glyphsize, c=live_up)
plt.scatter(x_down,y_down, marker=(3,1,180),s=glyphsize, c=live_down)
#plt.set_aspect('equal')
plt.title("live cells")
plt.colorbar(up_plot)

plt.show()