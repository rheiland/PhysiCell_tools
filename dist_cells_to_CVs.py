import scipy.io
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.colors as mplc

cells_dict = {} # cells info
scipy.io.loadmat("output00000000_cells",cells_dict)
cells_dict.keys()
v=cells_dict['basic_agents'];
x= v[1,:]
y= v[2,:]

cv_dict = {}  # central vein positions
scipy.io.loadmat("../paper/more_matlab/central_vein_pos.mat",cv_dict)
pos = cv_dict['central_vein_pos'];
#pos[:,0].min()
#pos[:,0].max()

dmin = np.ones(5570)*1.e10

# 5570 cells
num_cv = 11
for idx in range(num_cv): # for each central vein
  xdel = x - pos[idx,0]
  ydel = y - pos[idx,1]
  d = np.sqrt(xdel*xdel + ydel*ydel)
  ids = np.where(d<dmin)
  dmin[ids] = d[ids]

plt.scatter(x,y, c=dmin)
plt.show()

# write out .mat file
scipy.io.savemat('dmin.mat', {'dist_min':dmin})

"""
ddict = {}
dist_colors = scipy.io.loadmat("dmin.mat", ddict)
ddict['dist_min']
"""

#plt.show()

