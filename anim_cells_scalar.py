# Examples (run from directory containing the .mat files):
#  python anim_cells_scalar.py 0 5 700 1300 
#
__author__ = "Randy Heiland"

import sys
import glob
import os
import xml.etree.ElementTree as ET
import math
from pathlib import Path
join_our_list = "(Join/ask questions at https://groups.google.com/forum/#!forum/physicell-users)\n"
try:
  import matplotlib
  from matplotlib import gridspec
  import matplotlib.colors as mplc
  from matplotlib.patches import Circle, Ellipse, Rectangle
  from matplotlib.collections import PatchCollection
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
try:
  # apparently we need mpl's Qt backend to do keypresses 
#  matplotlib.use("Qt5Agg")
  matplotlib.use("TkAgg")
  import matplotlib.pyplot as plt
except:
  print("\n---Error: cannot use matplotlib's TkAgg backend")
  print(join_our_list)
#  print("Consider installing Anaconda's Python 3 distribution.")
  raise

# from pyMCDS_cells import pyMCDS_cells 
from pyMCDS import pyMCDS

current_idx = 0
print("# args=",len(sys.argv)-1)

#for idx in range(len(sys.argv)):
use_defaults = True
show_nucleus = 0
current_idx = 0
axes_min = 0.0
axes_max = 1000  


if (len(sys.argv) == 5):
  use_defaults = False
  kdx = 1
  show_nucleus = int(sys.argv[kdx])
  kdx += 1
  current_idx = int(sys.argv[kdx])
  kdx += 1
  axes_min = float(sys.argv[kdx])
  kdx += 1
  axes_max = float(sys.argv[kdx])
elif (len(sys.argv) != 1):
  print("Please provide either no args or 4 args:")
  usage_str = "show_nucleus start_index axes_min axes_max"
  print(usage_str)
  print("e.g.,")
  eg_str = "%s 0 0 0 2000" % (sys.argv[0])
  print(eg_str)
  sys.exit(1)

#"""
print("show_nucleus=",show_nucleus)
print("current_idx=",current_idx)
print("axes_min=",axes_min)
print("axes_max=",axes_max)
#"""

"""
if (len(sys.argv) > 1):
   current_idx = int(sys.argv[1])
if (len(sys.argv) > 2):
   axes_min = float(sys.argv[2])
   axes_max = float(sys.argv[3])

if (len(sys.argv) > 4):
  usage_str = "[<start_index> [<axes_min axes_max>]]"
  print(usage_str)
  print("e.g.,")
  eg_str = "%s 1 10 700 1300" % (sys.argv[0])
  print(eg_str)
  sys.exit(1)
"""

print("current_idx=",current_idx)

#d={}   # dictionary to hold all (x,y) positions of cells

""" 
--- for example ---
In [141]: d['cell1599'][0:3]
Out[141]: 
array([[ 4900.  ,  4900.  ],
       [ 4934.17,  4487.91],
       [ 4960.75,  4148.02]])
"""

fig = plt.figure(figsize=(7,7))
gs = gridspec.GridSpec(2,2, height_ratios=[20,1], width_ratios=[20,1]) # top row is [plot, substrate colorbar]; bottom row is [cells colorbar, nothing]
# ax0 = fig.gca()
ax0 = fig.add_subplot(gs[0,0], adjustable='box')
#ax.set_aspect("equal")

cax1 = None
cax2 = None


#plt.ion()

time_delay = 0.1

count = -1
#while True:

#-----------------------------------------------------
def circles(x, y, s, c='b', vmin=None, vmax=None, **kwargs):
    # global ax0   # rwh - doesn't matter!
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
        c = c.values
        c = np.broadcast_to(c, zipped.shape).ravel()
        collection.set_array(c)
        collection.set_clim(vmin, vmax)

    # ax0 = plt.gca()   # rwh - NO, bad news (cells disappear)!
    ax0.add_collection(collection)
    ax0.autoscale_view()
    plt.draw_if_interactive()
    # if c is not None:
    #     plt.sci(collection)
    return collection

#-----------------------------------------------------
def plot_cell_scalar():
    global current_idx, axes_max,cax2,ax0

    frame = current_idx 

    xml_file_root = "output%08d.xml" % frame
    # print("plot_cell_scalar():  current_idx= ",current_idx)
    print("plot_cell_scalar():  xml_file_root = ",xml_file_root)
    xml_file = os.path.join('.', xml_file_root)

    # cell_scalar_humanreadable_name = self.cell_scalar_combobox.currentText()
    # if cell_scalar_humanreadable_name in self.cell_scalar_human2mcds_dict.keys():
    #     cell_scalar_mcds_name = self.cell_scalar_human2mcds_dict[cell_scalar_humanreadable_name]
    # else:
    #     cell_scalar_mcds_name = cell_scalar_humanreadable_name
    # cbar_name = self.cell_scalar_cbar_combobox.currentText()

    cbar_name = 'viridis'

    if not Path(xml_file).is_file():
        print("ERROR: file not found",xml_file)
        return

    # mcds = pyMCDS(xml_file_root, '.', microenv=False, graph=False, verbose=False)
    mcds = pyMCDS(xml_file_root, microenv=False, graph=False, verbose=False)
    total_min = mcds.get_time()  # warning: can return float that's epsilon from integer value
    # Get the cell data
    try:
        df_all_cells = mcds.get_cell_df()
    except:
        print("vis_tab.py: plot_cell_scalar(): error performing mcds.get_cell_df()")
        return

    # if self.celltype_filter:
    #     df_cells = df_all_cells.loc[ df_all_cells['cell_type'].isin(self.celltype_filter) ]
    # else:
    #     df_cells = df_all_cells
    df_cells = df_all_cells   # leak?

    try:
        # cell_scalar = df_cells[cell_scalar_mcds_name]
        cell_scalar = df_cells["pressure"]
    except:
        print("vis_tab.py: plot_cell_scalar(): error performing df_cells[cell_scalar_mcds_name]")
        return
            
    # if self.fix_cells_cmap_flag:
    #     vmin = self.cells_cmin_value
    #     vmax = self.cells_cmax_value
    # else:
    vmin = cell_scalar.min()
    vmax = cell_scalar.max()
        
    num_cells = len(cell_scalar)
    print("  num_cells = ",num_cells)
    # fix_cmap = 0
    print(f'   cell_scalar.min(), max() = {vmin}, {vmax}')
    cell_vol = df_cells['total_volume']
    # print(f'   cell_vol.min(), max() = {cell_vol.min()}, {cell_vol.max()}')

    four_thirds_pi =  4.188790204786391
    cell_radii = np.divide(cell_vol, four_thirds_pi)
    cell_radii = np.power(cell_radii, 0.333333333333333333333333333333333333333)

    xvals = df_cells['position_x']
    yvals = df_cells['position_y']

        # else: 
        #     self.cell_scalar_cbar_combobox.setEnabled(True)
        #     self.discrete_variable = None   # memory leak??
        #     self.discrete_variable_observed = set()
            
    mins = round(total_min)  # hack, assume we want integer mins
    hrs = int(mins/60)
    days = int(hrs/24)
    # print(f"mins={mins}, hrs={hrs}, days={days}")
    title_str = '%d days, %d hrs, %d mins' % (days, hrs-days*24, mins-hrs*60)
    title_str = '%f mins' % (total_min)  # rwh: custom
    title_str += " (" + str(num_cells) + " agents)"

    axes_min = mcds.get_mesh()[0][0][0][0]
    axes_max = mcds.get_mesh()[0][0][-1][0]

    cell_fill = True
    cell_edge = False
    cell_edge = True

    # plt.cla()   # rwh - custom, needed here
    ax0.cla()   # rwh - custom, needed here
    if (cell_fill):
        if (cell_edge):
            try:
                # cell_plot = circles(xvals,yvals, s=cell_radii, c=cell_scalar, edgecolor='black', linewidth=1, cmap=cbar_name, vmin=vmin, vmax=vmax)
                cell_plot = circles(xvals,yvals, s=cell_radii, c=cell_scalar, edgecolor='black', linewidth=1,  vmin=vmin, vmax=vmax)
            except (ValueError):
                print("\n------ ERROR: Exception from circles with edges\n")
                pass
        else:
            cell_plot = circles(xvals,yvals, s=cell_radii, c=cell_scalar, cmap=cbar_name, vmin=vmin, vmax=vmax)

    else:  # semi-trransparent cell, but with (thicker) edge  (TODO: how to make totally transparent?)
        if (cell_edge):
            cell_plot = circles(xvals,yvals, s=cell_radii, c=cell_scalar, edgecolor='black', linewidth=1, cmap=cbar_name, vmin=vmin, vmax=vmax, alpha=0.5)
        else:
            cell_plot = circles(xvals,yvals, s=cell_radii, c=cell_scalar, cmap=cbar_name, vmin=vmin, vmax=vmax, alpha=0.5)


    # print("------- plot_cell_scalar() -------------")
    num_axes =  len(fig.axes)
    # print("# axes = ",num_axes)
    # if num_axes > 1: 
    # if self.axis_id_cellscalar:
            
    # If it's not there, we create it
    if cax2 is None:
        cax2 = fig.add_subplot(gs[1,0])
        # ax2_divider = make_axes_locatable(self.ax0)
        # self.cax2 = ax2_divider.append_axes("bottom", size="4%", pad="8%")
    cbar2 = fig.colorbar(cell_plot, ticks=None, cax=cax2, orientation="horizontal")
    cbar2.ax.tick_params(labelsize=9)
    # cbar2.ax.set_xlabel(cell_scalar_humanreadable_name, fontsize=9)
    cbar2.ax.set_xlabel("pressure", fontsize=9)

    ax0.set_title(title_str, fontsize=9)

    plot_xmin=plot_ymin= -500
    plot_xmax=plot_ymax= 500
    ax0.set_xlim(plot_xmin, plot_xmax)
    ax0.set_ylim(plot_ymin, plot_ymax)

    ax0.set_aspect('equal')

    plt.pause(0.001)  # rwh - yipeee, this causes a redraw!!

step_value = 1
def press(event):
  global current_idx, step_value, ax0
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
    plot_cell_scalar()
  elif event.key == 'right':  # right arrow key
#        print('go forwards')
#        fig.canvas.draw()
    current_idx += step_value
    # ax0.cla()
    plot_cell_scalar()
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
    plot_cell_scalar()
  else:
    print('press', event.key)


#for current_idx in range(40):
#  fname = "snapshot%08d.svg" % current_idx
plot_cell_scalar()
print("\nNOTE: click in plot window to give it focus before using keys.")

fig.canvas.mpl_connect('key_press_event', press)

# keep last plot displayed
#plt.ioff()
plt.show()
