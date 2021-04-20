"""
  step_substrate_nogrid_steep.py - step through 2D cell plots on top of substrate plots, with the grid

"""
import sys,pathlib
import xml.etree.ElementTree as ET
import os
import math
import matplotlib.colors as mplc
from collections import deque
import scipy.io
import matplotlib
#import matplotlib.pyplot as plt  # NB! do this AFTER the TkAgg line below!
#import matplotlib.colors as mplc
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Ellipse, Rectangle
from matplotlib.collections import PatchCollection
import numpy as np
from numpy.random import randn


try:
  # apparently we need mpl's Qt backend to do keypresses 
#  matplotlib.use("Qt5Agg")
  matplotlib.use("TkAgg")
  import matplotlib.pyplot as plt
except:
  print("\n---Error: cannot use matplotlib's TkAgg backend")
#  print("Consider installing Anaconda's Python 3 distribution.")
  raise

current_idx = 0

# if (len(sys.argv) < 3):
#   current_idx = 0
#   field_idx = 4
#   fix_cmap = 0
#   print("Usage: %s start_idx field_idx fix_cmap(0/1) vmin vmax" % sys.argv[0])
#   print("e.g. %s start_idx field_idx fix_cmap(0/1) vmin vmax\n" % sys.argv[0])
# else:
#   kdx = 1
#   current_idx = int(sys.argv[kdx]); kdx += 1
#   field_idx = int(sys.argv[kdx]); kdx += 1
#   fix_cmap = int(sys.argv[kdx]); kdx += 1
#   vmin = float(sys.argv[kdx]); kdx += 1
#   vmax = float(sys.argv[kdx]); kdx += 1


current_idx = 0
print("# args=",len(sys.argv)-1)

#for idx in range(len(sys.argv)):
use_defaults = True
current_idx = 0
xmin = 0.0
xmax = 1000  # but overridden by "width" attribute in .svg

vmin = 0.0
vmax = 1050
fix_cmap = 0

time_delay = 0.1

if (len(sys.argv) == 7):
  use_defaults = False
  kdx = 1
  current_idx = int(sys.argv[kdx])
  kdx += 1
  xmin = float(sys.argv[kdx])
  kdx += 1
  xmax = float(sys.argv[kdx])
  kdx += 1
  ymin = float(sys.argv[kdx])
  kdx += 1
  ymax = float(sys.argv[kdx])
  # kdx += 1
  # scale_radius = float(sys.argv[kdx])
  kdx += 1
  field_idx = int(sys.argv[kdx])
else:
  print("Usage:")
  # usage_str = "show_nucleus start_index svg_xmin svg_xmax svg_ymin svg_ymax xmin xmax ymin ymax scale_radius field_idx"
  usage_str = "start_index xmin xmax ymin ymax field_idx"
  print(usage_str)
  print("e.g.,")
  eg_str = "%s 0 -100 100 -100 100 0" % (sys.argv[0])
  print(eg_str)
  sys.exit(1)

#field_idx = 0
field_idx += 4

print('current_idx, field_idx = ',current_idx, field_idx)

# figure out the domain sizes (might not be square)
ifname = "initial.xml"
tree = ET.parse(ifname)
xml_root = tree.getroot()
xcoord_vals = xml_root.find(".//x_coordinates").text.split()
ycoord_vals = xml_root.find(".//y_coordinates").text.split()
xmin = float(xcoord_vals[0])
xmax = float(xcoord_vals[-1])   # should be 999.0
ymin = float(ycoord_vals[0])
ymax = float(ycoord_vals[-1])   # should be 999.0

# numx = int((xmax - xmin) / xdel)  # need to also round maybe?
# numy = int((ymax - ymin) / ydel)
numx = len(xcoord_vals)
numy = len(ycoord_vals)
print("numx, numy = ",numx,numy)  # e.g., 75 75


fig = plt.figure(figsize=(7,5.8))
#ax = fig.gca()

count = -1

cbar = None

#-----------------------------------------------------
def circles(x, y, s, c='b', vmin=None, vmax=None, **kwargs):
    """
    See https://gist.github.com/syrte/592a062c562cd2a98a83 

    Make a scatter plot of circles. 
    Similar to plt.scatter, but the size of circles are in data scale.
    Parameters
    ----------
    x, y : scalar or array_like, shape (n, )
        Input data
    s : scalar or array_like, shape (n, ) 
        Radius of circles.
    c : color or sequence of color, optional, default : 'b'
        `c` can be a single color format string, or a sequence of color
        specifications of length `N`, or a sequence of `N` numbers to be
        mapped to colors using the `cmap` and `norm` specified via kwargs.
        Note that `c` should not be a single numeric RGB or RGBA sequence 
        because that is indistinguishable from an array of values
        to be colormapped. (If you insist, use `color` instead.)  
        `c` can be a 2-D array in which the rows are RGB or RGBA, however. 
    vmin, vmax : scalar, optional, default: None
        `vmin` and `vmax` are used in conjunction with `norm` to normalize
        luminance data.  If either are `None`, the min and max of the
        color array is used.
    kwargs : `~matplotlib.collections.Collection` properties
        Eg. alpha, edgecolor(ec), facecolor(fc), linewidth(lw), linestyle(ls), 
        norm, cmap, transform, etc.
    Returns
    -------
    paths : `~matplotlib.collections.PathCollection`
    Examples
    --------
    a = np.arange(11)
    circles(a, a, s=a*0.2, c=a, alpha=0.5, ec='none')
    plt.colorbar()
    License
    --------
    This code is under [The BSD 3-Clause License]
    (http://opensource.org/licenses/BSD-3-Clause)
    """

    if np.isscalar(c):
        kwargs.setdefault('color', c)
        c = None

    if 'fc' in kwargs:
        kwargs.setdefault('facecolor', kwargs.pop('fc'))
    if 'ec' in kwargs:
        kwargs.setdefault('edgecolor', kwargs.pop('ec'))
    if 'ls' in kwargs:
        kwargs.setdefault('linestyle', kwargs.pop('ls'))
    if 'lw' in kwargs:
        kwargs.setdefault('linewidth', kwargs.pop('lw'))
    # You can set `facecolor` with an array for each patch,
    # while you can only set `facecolors` with a value for all.

    zipped = np.broadcast(x, y, s)
    patches = [Circle((x_, y_), s_)
               for x_, y_, s_ in zipped]
    collection = PatchCollection(patches, **kwargs)
    if c is not None:
        c = np.broadcast_to(c, zipped.shape).ravel()
        collection.set_array(c)
        collection.set_clim(vmin, vmax)

    ax = plt.gca()
    ax.add_collection(collection)
    ax.autoscale_view()
    plt.draw_if_interactive()
    if c is not None:
        plt.sci(collection)
    return collection

#-----------------------------------------------------
def plot_substrate():
    global current_idx, axes_max, cbar

    # select whichever substrate index you want, e.g., for one model:
    # 4=tumor cells field, 5=blood vessel density, 6=growth substrate

    xml_file = "output%08d.xml" % current_idx
    tree = ET.parse(xml_file)
    root = tree.getroot()
#    print('time=' + root.find(".//current_time").text)
    mins = float(root.find(".//current_time").text)
    hrs = mins/60.
    days = hrs/24.
    title_str = '%d days, %d hrs, %d mins' % (int(days),(hrs%24), mins - (hrs*60))
    print(title_str)

    fname = "output%08d_microenvironment0.mat" % current_idx
    output_dir_str = '.'
    fullname = output_dir_str + "/" + fname
    if not pathlib.Path(fullname).is_file():
        print("file not found",fullname)
        return

    info_dict = {}
    scipy.io.loadmat(fullname, info_dict)
    M = info_dict['multiscale_microenvironment']
    print('plot_substrate: field_idx=',field_idx)
    f = M[field_idx,:]   # 

    print("M.shape = ",M.shape)  # e.g.,  (6, 421875)  (where 421875=75*75*75)
    # numx = int(M.shape[1] ** (1./3) + 1)
    # numy = numx
    print("numx, numy = ",numx, numy )
    nxny = numx * numy
    idx_plane = 37
    idx0 = idx_plane * nxny
    idx1 = idx0 + nxny
    xgrid = M[0, idx0:idx1].reshape(numy, numx)
    ygrid = M[1, idx0:idx1].reshape(numy, numx)
    
    #N = int(math.sqrt(len(M[0,:])))
    #grid2D = M[0,:].reshape(N,N)
    # xgrid = M[0, :].reshape(numy, numx)
    # ygrid = M[1, :].reshape(numy, numx)
    # print("M.shape = ",M.shape)  # e.g.,  (6, 421875)  (where 421875=75*75*75)
    # xgrid = M[0, :].reshape(numy, numx)
    # ygrid = M[1, :].reshape(numy, numx)

#    xvec = grid2D[0,:]
    #xvec.size
    #xvec.shape
    num_contours = 30
    num_contours = 10
#    vmin = 30.
#    vmax = 38.

    levels = MaxNLocator(nbins=30).tick_values(vmin, vmax)
#    cmap = plt.get_cmap('PiYG')
    cmap = plt.get_cmap('viridis')
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

#    my_plot = plt.contourf(xvec,xvec,M[field_idx,:].reshape(N,N), num_contours, cmap='viridis') #'viridis'
    if fix_cmap > 0:
      # my_plot = plt.contourf(xvec,xvec,M[field_idx,:].reshape(N,N), levels=levels, cmap=cmap)
      my_plot = plt.contourf(xgrid, ygrid, M[field_idx, idx0:idx1].reshape(numy, numx, ), levels=levels, extend='both', cmap=cmap)
    else:
      # my_plot = plt.contourf(xvec,xvec,M[field_idx,:].reshape(N,N), cmap=cmap)
      my_plot = plt.contourf(xgrid, ygrid, M[field_idx, idx0:idx1].reshape(numy, numx), cmap=cmap)

    if cbar == None:  # if we always do this, it creates an additional colorbar!
#      cbar = plt.colorbar(my_plot, boundaries=np.arange(vmin, vmax, 1.0))
      cbar = plt.colorbar(my_plot)
    else:
      cbar.ax.clear()
      cbar = plt.colorbar(my_plot, cax=cbar.ax)

#    plt.axis('equal')
    plt.title(title_str)

#    plt.show()
    plt.draw_if_interactive()

    png_file = "aaa%08d.png" % current_idx
    fig.savefig(png_file)
    plt.pause(time_delay)

#------------------------------
step_value = 1
def press(event):
  global current_idx, step_value
#    print('press', event.key)
  sys.stdout.flush()
  if event.key == 'escape':
    sys.exit(1)
  elif event.key == 'h':  # help
    print('esc: quit')
    print('right arrow: increment by step_value')
    print('left arrow:  decrement by step_value')
    print('up arrow:   increment step_value by 1')
    print('down arrow: decrement step_value by 1')
    print('0: reset to 0th frame')
    print('h: help')
  elif event.key == 'left':  # left arrow key
#    print('go backwards')
#    fig.canvas.draw()
    current_idx -= step_value
    if (current_idx < 0):
      current_idx = 0
    plot_substrate()
#    plot_svg()
  elif event.key == 'right':  # right arrow key
#        print('go forwards')
#        fig.canvas.draw()
    current_idx += step_value
    plot_substrate()
#    plot_svg()
  elif event.key == 'up':  # up arrow key
    step_value += 1
    print('step_value=',step_value)
  elif event.key == 'down':  # down arrow key
    step_value -= 1
    if (step_value <= 0):
      step_value = 1
    print('step_value=',step_value)
  elif event.key == '0':  # reset to 0th frame/file
    current_idx = 0
    plot_substrate()
#    plot_svg()
  else:
    print('press', event.key)

#------------------------------
plot_substrate()
#plot_svg()
print("\nNOTE: click in plot window to give it focus before using keys.")

fig.canvas.mpl_connect('key_press_event', press)
#plot_substrate(frame_idx)
plt.show()

