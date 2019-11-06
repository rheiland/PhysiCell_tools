from pyMCDS import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# load cell and microenvironment data
#mcds = pyMCDS('output00000017.xml', 'Archive')
fname = 'output00000017.xml'
mcds = pyMCDS(fname)

cell_df = mcds.get_cell_df()
#xx, yy = mcds.get_2D_mesh()

# get unique cell types and radii
cell_df['radius'] = (cell_df['total_volume'].values * 3 / (4 * np.pi))**(1/3)
types = cell_df['cell_type'].unique()
colors = ['yellow', 'blue']

fig, ax = plt.subplots(figsize=(6, 6))

# Add cells layer
for i, ct in enumerate(types):
    plot_df = cell_df[cell_df['cell_type'] == ct]
    for j in plot_df.index:
        circ = Circle((plot_df.loc[j, 'position_x'], plot_df.loc[j, 'position_y']),
                       color=colors[i], radius=plot_df.loc[j, 'radius'], alpha=1.0, ec='black')
        ax.add_artist(circ)

ax.axis('equal')
ax.set_xlabel('x [micron]')
ax.set_ylabel('y [micron]')
rbox = 700
rbox = 100
plt.xlim(-rbox,rbox)
plt.ylim(-rbox,rbox)
#fig.colorbar(cs, ax=ax)
ax.set_title(fname + ':  min=' + str(mcds.get_time()) )

plt.show()

#plt.savefig('vector.png')
