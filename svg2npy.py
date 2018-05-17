#
# svg2npy.py: convert svg (asccii) output files to numpy's "npy" (binary) formatted files.
#
# Input:
#   SVG output files from PhysiCell: snapshot%08d.svg
#
# Output:
#   xyzr_*.npy - cells' centers (x,y,z) and radii (r)
#   rgb_*.npy  - associated colors (RGB, normalized [0,1])
#
# Author: Randy Heiland
#
import sys
import glob
import os
import xml.etree.ElementTree as ET
import math

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
from collections import deque


current_idx = 0
print("# args=",len(sys.argv)-1)

#for idx in range(len(sys.argv)):
use_defaults = True
show_nucleus = 0
current_idx = 0
step_value = 1
axes_min = 0.0
axes_max = 2000
#axes_max = 1000

print("current_idx=",current_idx)

def convert_svg():
  global current_idx, axes_max, rvals, markers_size
#  global vec_xyzr, vec_rgb
  fname = "snapshot%08d.svg" % current_idx
  if (os.path.isfile(fname) == False):
    print("File does not exist: ",fname)
    return

  vec_xyzr = np.empty(shape=(0,4))
  vec_rgb = np.empty(shape=(0,3))

  xlist = deque()
  ylist = deque()
  rlist = deque()
  rgb_list = deque()

#  print('\n---- ' + fname + ':')
  tree = ET.parse(fname)
  root = tree.getroot()
#  print('--- root.tag ---')
#  print(root.tag)
#  print('--- root.attrib ---')
#  print(root.attrib)


#  print('--- child.tag, child.attrib ---')
  numChildren = 0
  for child in root:
#    print(child.tag, child.attrib)
#    print("keys=",child.attrib.keys())
    # # if use_defaults and ('width' in child.attrib.keys()):
    #   axes_max = float(child.attrib['width'])
#      print("--- found width --> axes_max =", axes_max)
    # if child.text and "Current time" in child.text:
      # svals = child.text.split()
#      title_str = "(" + str(current_idx) + ") Current time: " + svals[2] + "d, " + svals[4] + "h, " + svals[7] + "m"
      # title_str = "Current time: " + svals[2] + "d, " + svals[4] + "h, " + svals[7] + "m"

#    print("width ",child.attrib['width'])
#    print('attrib=',child.attrib)
#    if (child.attrib['id'] == 'tissue'):
    if ('id' in child.attrib.keys()):
#      print('-------- found tissue!!')
      tissue_parent = child
      break

#  print('------ search tissue')
  cells_parent = None

  for child in tissue_parent:
#    print('attrib=',child.attrib)
    if (child.attrib['id'] == 'cells'):
#      print('-------- found cells, setting cells_parent')
      cells_parent = child
      break
    numChildren += 1


  num_cells = 0
#  print('------ search cells')
  for child in cells_parent:
#    print(child.tag, child.attrib)
#    print('attrib=',child.attrib)
    for circle in child:  # two circles in each child: outer + nucleus
    #  circle.attrib={'cx': '1085.59','cy': '1225.24','fill': 'rgb(159,159,96)','r': '6.67717','stroke': 'rgb(159,159,96)','stroke-width': '0.5'}
#      print('  --- cx,cy=',circle.attrib['cx'],circle.attrib['cy'])
      xval = float(circle.attrib['cx'])

      s = circle.attrib['fill']
#      print("s=",s)
#      print("type(s)=",type(s))
      if (s[0:3] == "rgb"):  # if an rgb string, e.g. "rgb(175,175,80)" 
        rgb = list(map(int, s[4:-1].split(",")))  
        rgb[:]=[x/255. for x in rgb]
      else:     # otherwise, must be a color name
        rgb_tuple = mplc.to_rgb(mplc.cnames[s])  # a tuple
        rgb = [x for x in rgb_tuple]

      # test for bogus x,y locations (rwh TODO: use max of domain?)
      too_large_val = 10000.
      if (math.fabs(xval) > too_large_val):
        print("bogus xval=",xval)
        break
      yval = float(circle.attrib['cy'])
      if (math.fabs(yval) > too_large_val):
        print("bogus xval=",xval)
        break

      rval = float(circle.attrib['r'])

      vec_xyzr = np.append(vec_xyzr, np.array([[xval,yval,0.0,rval]]), axis=0)
#      print(xval,yval)
      vec_rgb = np.append(vec_rgb, np.array([[rgb[0],rgb[1],rgb[2]]]), axis=0)
#      print('rgb=',rgb[0],rgb[1],rgb[2])

#     For .svg files with cells that *have* a nucleus, there will be a 2nd
      if (show_nucleus == 0):
        break

    num_cells += 1

#    if num_cells > 3:   # for debugging
#      print(fname,':  num_cells= ',num_cells," --- debug exit.")
#      sys.exit(1)
#      break

  print(fname,':  num_cells= ',num_cells)

  cell_file = "xyzr_%04d" % current_idx
  rgb_file = "rgb_%04d" % current_idx
  np.save(cell_file, vec_xyzr)
  np.save(rgb_file, vec_rgb)


for current_idx in range(0,505):
  convert_svg()

