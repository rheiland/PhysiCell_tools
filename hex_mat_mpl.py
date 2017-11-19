#
# Display scalar fields on a hexagonal mesh, using MATLAB formatted input files: 
# mesh.mat and output_*.mat
#

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import scipy
from scipy import io
import numpy as np

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(9,8))
ax0, ax1, ax2, ax3 = axes.flatten()

print("----- mesh.mat ----")
d={}
scipy.io.loadmat("mesh",d)
m=d["mesh"]
print(m.shape)
x=m[1,:]
y=m[2,:]

print("X range=",x.min(),x.max())
print("Y range=",y.min(),y.max())

"""
    fwrite( (char*) &( voxel_population_vectors[i].live_cell_counts.at(0) ) , sizeof(double) , 1 , fp );// Live tumor cells
    fwrite( (char*) &( voxel_population_vectors[i].apoptotic_cell_counts.at(0) ) , sizeof(double) , 1 , fp ); //  apoptotic tumor cells
    fwrite( (char*) &( voxel_population_vectors[i].necrotic_cell_counts[0] ) , sizeof(double) , 1 , fp );  //  necrotic tumor cells
    fwrite( (char*) &( voxel_population_vectors[i].live_cell_counts.at(1) ) , sizeof(double) , 1 , fp );  //  Vascular cells
    fwrite( (char*) &( voxel_population_vectors[i].apoptotic_cell_counts.at(1) ) , sizeof(double) , 1 , fp );  //  Vasculars - NOT BEING USED - don't visualize me unless you just need to.  I would rather have a workign script that produces a blank animation/chart over nothing.
    fwrite( (char*) &( voxel_population_vectors[i].necrotic_cell_counts[1] ) , sizeof(double) , 1 , fp );   //  Vasular field - NOT BEING USED
    fwrite( (char*) &( substrate_vectors[i].substrate_quantity.at(0) ) , sizeof(double) , 1 , fp );  //  Oxygen
    fwrite( (char*) &( substrate_vectors[i].substrate_quantity.at(1) ) , sizeof(double) , 1 , fp );  //  Anigogenic Factor
"""
print("----- voxels (output*.mat) ----")
d2 = {}
scipy.io.loadmat("output_005999",d2)
v = d2["voxels_populations"]
print(v.shape)
print("range of Live=",v[0,:].min(),v[0,:].max())
print("range of oxygen=",v[6,:].min(),v[6,:].max())
print("range of angiogenic=",v[7,:].min(),v[7,:].max())

live=v[0,:]
o2=v[6,:]
angio=v[7,:]

#-----------------------
# Options for custom colormaps: 
# https://matplotlib.org/examples/pylab_examples/custom_cmap.html
colors = [(0, 0, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)] 
cmap_name = 'my_colors'
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=4)  # N= # of discrete colors 

#------ Oxygen ---------
marker_size = 120  # area of (hexagonal) glyphs used for all scatter plots

half_dist = 400
ax0.axis([-half_dist,half_dist, -half_dist,half_dist])

# https://matplotlib.org/api/markers_api.html
voxel_plot0 = ax0.scatter(x, y, marker='h', s=marker_size, c=o2, cmap=cm)
ax0.set_aspect('equal')
ax0.set_title('Oxygen')
fig.colorbar(voxel_plot0, ax=ax0)

#------- Angiogenic factor --------
ax1.axis([-half_dist,half_dist, -half_dist,half_dist])

angio_min = angio.min()
angio_max = angio.max()
angio_del = (angio_max - angio_min)/3.0

voxel_plot1 = ax1.scatter(x, y, marker='h', s=marker_size, c=angio, cmap=cm)
ax1.set_aspect('equal')
ax1.set_title('Angio')
fig.colorbar(voxel_plot1, ax=ax1)

#------- Live cells --------
ax2.axis([-half_dist,half_dist, -half_dist,half_dist])

voxel_plot2 = ax2.scatter(x, y, marker='h', s=marker_size, c=live, cmap=cm)
ax2.set_aspect('equal')
ax2.set_title('Live')
fig.colorbar(voxel_plot2, ax=ax2)

#------- Histogram of Live cells --------
ax3.set_title('Histogram of Live')
n, bins, patches = ax3.hist(live, 10)

#-----------------
fig.tight_layout()
plt.show()
