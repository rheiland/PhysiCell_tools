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

show_nucleus = False  # should only need if doing "cut" slices through the cells

for idx in range(0, num_cells):
  # rf. PhysiCell User Guide for these array indices to a cell's position.
  x = val[1,idx]
  y = -val[2,idx]  # invert Y (points down)
  z = val[3,idx]

  """
  - from the User_Guide.pdf:
   false cell coloring Ki67 is recommended for the Ki67 Basic and Ki67 Advanced cycle models.
   (See Section 11.1 and Section 17.1.) Pre-mitotic Ki67+ cells are colored green (0,255,0), with a
   darker green nucleus (0,125,0). Post-mitotic Ki67+ cells are colored magenta (255,0,255), with a
   darker magenta nucleus (125,0,125). (In the Ki67 Basic model, all Ki67+ cells are green.) Ki67- cells
   are colored blue (40,200,255) with a darker blue nucleus (20,100,255).
   Apoptotic cells are colored red (255,0,0) with a darker red nucleus (125,0,0). Necrotic cells are colored
   brown (250,138,38) with a darker brown nucleus (139,69,19). All outlines are black.
  """

  # for now, rather than provide RGB colors, just provide an integer value that can be mapped to a color
  sval = 0   # default color
  if val[5,idx] == 1:  # immune cell type
    sval = 1   # lime green 
  if val[7,idx] > 100 and val[7,idx] < 104:
    sval = 2   # necrotic: brownish
  elif val[7,idx] == 100:
    sval = 3   # apoptotic: red

  total_volume = val[4,idx]
  cell_radius = (total_volume*0.2387)**0.333   # Volume = (4/3)*pi*r^3

  if (idx < max_cells):
    print(x,',',y,',',z,',',cell_radius, ',',sval)

  # fix up if ever used
  if (show_nucleus):
    nuclear_volume = val[9,idx]
    nuclear_radius = (nuclear_volume*0.2387)**0.333 
    print(x,y,z,nuclear_radius)

