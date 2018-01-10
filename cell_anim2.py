#
# cell_anim.py - plot 2-D cells associated with PhysiCell .svg files
#
import sys
import xml.etree.ElementTree as ET
import numpy as np
import glob
import matplotlib.pyplot as plt
import math
from collections import deque


print(len(sys.argv))
if (len(sys.argv) < 3):
  usage_str = "Usage: %s start end" % (sys.argv[0])
  print(usage_str)
  print("e.g.,")
  eg_str = "%s 0 42" % (sys.argv[0])
  print(eg_str)
  sys.exit(1)
else:
   startCount = int(sys.argv[1])
   endCount = int(sys.argv[2])

d={}   # dictionary to hold all (x,y) positions of cells

""" 
--- for example ---
In [141]: d['cell1599'][0:3]
Out[141]: 
array([[ 4900.  ,  4900.  ],
       [ 4934.17,  4487.91],
       [ 4960.75,  4148.02]])
"""


fig = plt.figure(figsize=(8,8))
ax = fig.gca()
ax.set_aspect("equal")

plt.ion()

count = -1
for fname in sorted(glob.glob('snapshot*.svg')):
  xlist = deque()
  ylist = deque()
  rlist = deque()
  rgb_list = deque()
#for fname in['snapshot00000000.svg', 'snapshot00000001.svg']:
#for fname in['snapshot00000000.svg']:
#  print(fname)
  count += 1
  if count < startCount:
    continue
  if count > endCount:
    break

  print('\n---- ' + fname + ':')
  tree = ET.parse(fname)

#  print('--- root.tag, root.attrib ---')
  root = tree.getroot()
#  print('--- root.tag ---')
#  print(root.tag)
#  print('--- root.attrib ---')
#  print(root.attrib)


#  print('--- child.tag, child.attrib ---')
  numChildren = 0
  for child in root:
#    print(child.tag, child.attrib)
#    print("width ",child.attrib['width'])
#    print('attrib=',child.attrib)
#    if (child.attrib['id'] == 'tissue'):
    if ('id' in child.attrib.keys()):
#      print('-------- found tissue!!')
      tissue_parent = child
      break

#  print('------ search tissue')
  for child in tissue_parent:
#    print('attrib=',child.attrib)
    if (child.attrib['id'] == 'cells'):
#      print('-------- found cells!!')
      cells_parent = child
      break
    numChildren += 1


  num_cells = 0
#  print('------ search cells')
  for child in cells_parent:
#    print(child.tag, child.attrib)
#    print('attrib=',child.attrib)
    for circle in child:  
    # circle.attrib={'cx': '1085.59','cy': '1225.24','fill': 'rgb(159,159,96)','r': '6.67717','stroke': 'rgb(159,159,96)','stroke-width': '0.5'}
#      print('  --- cx,cy=',circle.attrib['cx'],circle.attrib['cy'])
      xval = float(circle.attrib['cx'])

      s = circle.attrib['fill']
      rgb = list(map(int, s[4:-1].split(",")))  # using Py3
      rgb[:]=[x/255. for x in rgb]
      rgb_list.append(rgb)
#      if (num_cells < 25):
#        print(s)
#        print(rgb)

      # should we test for bogus x,y locations??
      if (math.fabs(xval) > 10000.):
        print("xval=",xval)
        break
      xlist.append(xval)

      yval = float(circle.attrib['cy'])
      if (math.fabs(yval) > 10000.):
        print("xval=",xval)
        break
      ylist.append(yval)

      rval = float(circle.attrib['r'])
      rlist.append(rval)

#      if (child.attrib['id'] in d.keys()):
#        d[child.attrib['id']] = np.vstack((d[child.attrib['id']], 
#              [ float(circle.attrib['cx']), float(circle.attrib['cy']) ]))
#      else:
#        d[child.attrib['id']] = np.array( [ float(circle.attrib['cx']), float(circle.attrib['cy']) ])

      break
#    if (child.attrib['id'] == 'cells'):
#      print('-------- found cells!!')
#      tissue_child = child
    num_cells += 1
  print(fname,':  num_cells= ',num_cells)

  xvals=np.array(xlist)
  yvals=np.array(ylist)
  rvals=np.array(rlist)
  rgbs=np.array(rgb_list)
#print("xvals[0:5]=",xvals[0:5])
#print("rvals[0:5]=",rvals[0:5])
  print("rvals.min, max=",rvals.min(),rvals.max())

#ax.set_xticks([])
#ax.set_yticks([]);
#ax.set_xlim(0, 8); ax.set_ylim(0, 8)

#print 'dir(fig)=',dir(fig)
#fig.set_figwidth(8)
#fig.set_figheight(8)

  plt.scatter(xvals,yvals, s=rvals*0.9, c=rgbs)
#plt.xlim(0,2000)  # TODO - get these values from width,height in .svg at top
#plt.ylim(0,2000)
  plt.pause(1.0)

"""
for key in d.keys():
  if (len(d[key].shape) == 2):
    x = d[key][:,0]
    y = d[key][:,1]
    plt.plot(x,y)
  else:
    print(key, " has no x,y points")
#    print(" d[",key,"].shape=", d[key].shape)
#    print(" d[",key,"].size=", d[key].size)
#    print( d[key])
"""

#plt.show()
