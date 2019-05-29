"""
read_cell_info.py - read a "output*_cells_physicell.mat" file and print cells' info

"""
import scipy.io

cells_dict = {}
iframe = 3696
fname = "output%08d_cells_physicell" % iframe

#print("fname = ",fname)
scipy.io.loadmat(fname, cells_dict)
#val = cells_dict['basic_agents']
val = cells_dict['cells']


# Read cell centers
num_cells = val.shape[1]
print("num_cells =",num_cells)
max_cells = num_cells 
max_cells = 40 

for idx in range(0, num_cells):
  # rf. PhysiCell User Guide for these array indices to a cell's position.
  x = val[1,idx]
  y = -val[2,idx]  # invert Y (points down)
  z = val[3,idx]

  sval = 0   # immune cells are black??
  if val[5,idx] == 1:  # immune cell type
    sval = 1   # lime green 
  if val[7,idx] > 100 and val[7,idx] < 104:
    sval = 2   # necrotic: brownish
  elif val[7,idx] == 100:
    sval = 3   # apoptotic: red

  radius = (val[4,idx]*0.2387)**0.333 

  if (idx < max_cells):
    print(x,y,z,radius)

