# plot triangular meshes & "contours" from John's .mat data
#
# $ ipython --pylab
# In [1]: %run trimesh

import sys
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

#glyphsize = 10

print(len(sys.argv))
if (len(sys.argv) < 2):
  print("Usage: " + sys.argv[0] + " [glyphsize]")
  print("e.g.  glyphsize=10")
  sys.exit(0)
else:
  glyphsize = int(sys.argv[1])

print("glyphsize=",glyphsize)

info_dict = {}
#        scipy.io.loadmat(fullname, info_dict)
fname = 'ALL_testing_time_0010_space_025_sim_time_008400.mat'
fname = 'ALL_testing_time_0010_space_100_sim_time_008400.mat'
fname = 'diffusion_circle_time_0001_space_100_sim_time_000100.mat'
scipy.io.loadmat(fname, info_dict)
m = info_dict['populations_and_locations']
xctrs = m[10,:]
yctrs = m[11,:]
zctrs = m[12,:]


#        self.fig = plt.figure(figsize=(13.2,4))  # TODO: need function of domain sizes
lfig = 5
lfig = 9
lfig = 8
scale_factor = 40.0
#plt.figure(figsize=(lfig,lfig))
#fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(14,6))
#fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(lfig,lfig))
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(2*lfig,lfig))
#ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7 = axes.flatten()
#ax0, ax1, ax2, ax3 = axes.flatten()
ax0, ax1 = axes.flatten()
#ax0 = axes.flatten()

  # draw one set of triangles (pointing up/down)
#   plt.scatter(xvals,yvals, marker=(3,1,180),s=rvals*scale_radius, c=rgbs)
  # draw another set of triangles (pointing opposite dir as others)
#   plt.scatter(xvals2,yvals2, marker=(3,1,0),s=rvals2*scale_radius, c=rgbs2


# plot center points (as circles)
kmin=0;kmax=20
#plt.scatter(xctrs[kmin:kmax],yctrs[kmin:kmax], marker='o',s=3, c='black')
#ax0.scatter(xctrs,yctrs, marker='o',s=1, c='black')

#plt.scatter(xctrs,yctrs, marker=(3,1,180),s=2*scale_factor, c='red')
#plt.scatter(xctrs,yctrs, marker=(3,1,0),s=2*scale_factor, c='green')

"""
# fname = 'ALL_testing_time_0010_space_100_sim_time_008400.mat'
In [28]: yctrs[0:20]
Out[28]: 
array([-1021.13248654, -1050.        , -1021.13248654, -1050.        ,
       -1021.13248654, -1050.        , -1021.13248654, -1050.        ,
       -1021.13248654, -1050.        , -1021.13248654, -1050.        ,
       -1021.13248654,  -934.52994616,  -963.39745962,  -934.52994616,
        -963.39745962,  -934.52994616,  -963.39745962,  -934.52994616])
"""
y00 = -1050
y1 = -1021.13
  
"""
# higher res
# fname = 'ALL_testing_time_0010_space_025_sim_time_008400.mat'
In [122]: yctrs[0:30]
Out[122]: 
array([-1021.13248654, -1006.69872981, -1028.34936491, -1028.34936491,
       -1050.        , -1064.43375673, -1042.78312164, -1042.78312164,
       -1006.69872981, -1021.13248654,  -999.48185145,  -999.48185145,
       -1006.69872981, -1021.13248654,  -999.48185145,  -999.48185145,
       -1050.        , -1064.43375673, -1042.78312164, -1042.78312164,
       -1021.13248654, -1006.69872981, -1028.34936491, -1028.34936491,
       -1064.43375673, -1050.        , -1071.65063509, -1071.65063509,
       -1064.43375673, -1050.        ])

In [125]: yctrs.min(),yctrs.max()
Out[125]: (-1071.650635094611, 1078.9791176367453)

2nd row of "up" is y=-1050   # --> diff=21.6
"""

yints = yctrs.astype(int)
#yi = yints.astype(int)
yrows = np.sort(np.unique(yints))
print("len(yrows)=",len(yrows))  # 200


y00 = -1071.65
y1 = -1064.4

ydel_uprows = 21.6

ydelta = 5
#ydel = 1.0
#up_down = (y1 < yctrs < y0) 
#for idx in range(2):

# Rf. numpy.any, numpy.all, numpy.where, np.take
#In [42]: np.where(yctrs < y0)
#Out[42]: (array([ 1,  3,  5,  7,  9, 11]),)


ids_total = []
ids_up = []
ids_down = []
ydel1 = 1050-963  # 87
ydel1 = y1-y00
print("ydel1=",ydel1)
ydel1 -= 1
print("ydel1=",ydel1)
y0 = y00
#while y0 < (yctrs.max() + ydel):
#while y0 < (0.0 + ydel):
y_upper = y00 + 3*ydelta
y_upper = y00 + 12*ydelta
y_upper = -990
y_upper = 0.0
#while y0 < y_upper:   # --> len(ids_up) = 74

# Alternating y-values in yrows will be with "up" tris
for kdx in range(0,len(yrows), 2):
  y0 = yrows[kdx]
  for idx in range(len(yctrs)):
#    if yctrs[idx] < y_upper:
#        ids_total.append(idx)
    if yctrs[idx] > (y0-ydelta) and yctrs[idx] < (y0+ydelta):
#        print(idx,yctrs[idx])
        ids_up.append(idx)
        #print(idx,yctrs[idx]," is up")

y=[idx for idx in range(len(yctrs))]
# create numpy arrays
a = np.array(y)
#a = np.array(ids_total)
b = np.array(ids_up)
ids_down = np.setdiff1d(a, b)   # get "down" tris' indices in yctrs
print("len(ids_up),len(ids_down): ",len(ids_up),len(ids_down))

x_up = np.take(xctrs,ids_up)
y_up = np.take(yctrs,ids_up)

x_down = np.take(xctrs,ids_down)
y_down = np.take(yctrs,ids_down)
    
scale_factor = 40.0
scale_factor = 35.0
up_color = 'tan'
up_color = 'green'
down_color = 'tan'
#plt.scatter(x_up,y_up, marker=(3,1,0),s=glyphsize, c=up_color)
#plt.scatter(x_down,y_down, marker=(3,1,180),s=glyphsize, c=down_color)

field_idx = 0  # live cells
field_idx = 6  # o2 c
field = m[field_idx,:]  
field_up = np.take(field,ids_up)
field_down = np.take(field,ids_down)
up_plot = ax0.scatter(x_up,y_up, marker=(3,1,0),s=glyphsize, c=field_up)

ax0.scatter(x_down,y_down, marker=(3,1,180),s=glyphsize, c=field_down)
#plt.set_aspect('equal')
ax0.set_aspect('equal')
ax0.set_title("oxygen, t=0")
#fig.colorbar(up_plot, ax=ax0)

# other plots
ax1.set_aspect('equal')
ax1.set_title("oxygen, t=1")
#fig.colorbar(up_plot, ax=ax1)

#ax2.set_aspect('equal')
#ax2.set_title("oxygen, t=2")
#fig.colorbar(up_plot, ax=ax2)

#ax3.set_aspect('equal')
#ax3.set_title("oxygen, t=3")
#fig.colorbar(up_plot, ax=ax3)

plt.show()