from pyMCDS import pyMCDS
import matplotlib.pyplot as plt
#from matplotlib.patches import Circle, Ellipse, Rectangle
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import matplotlib.colors as mplc
import numpy as np
import os
# import zipfile
# import glob
# import platform


axes_min = -500.0
axes_max = 500.   # TODO: get from input file

    #-----------------------------------------------------
def circles(x, y, s, c='b', vmin=None, vmax=None, **kwargs):

# See https://gist.github.com/syrte/592a062c562cd2a98a83 

# Make a scatter plot of circles. 
# Similar to plt.scatter, but the size of circles are in data scale.
# Parameters
# ----------
# x, y : scalar or array_like, shape (n, )
#     Input data
# s : scalar or array_like, shape (n, ) 
#     Radius of circles.
# c : color or sequence of color, optional, default : 'b'
#     `c` can be a single color format string, or a sequence of color
#     specifications of length `N`, or a sequence of `N` numbers to be
#     mapped to colors using the `cmap` and `norm` specified via kwargs.
#     Note that `c` should not be a single numeric RGB or RGBA sequence 
#     because that is indistinguishable from an array of values
#     to be colormapped. (If you insist, use `color` instead.)  
#     `c` can be a 2-D array in which the rows are RGB or RGBA, however. 
# vmin, vmax : scalar, optional, default: None
#     `vmin` and `vmax` are used in conjunction with `norm` to normalize
#     luminance data.  If either are `None`, the min and max of the
#     color array is used.
# kwargs : `~matplotlib.collections.Collection` properties
#     Eg. alpha, edgecolor(ec), facecolor(fc), linewidth(lw), linestyle(ls), 
#     norm, cmap, transform, etc.
# Returns
# -------
# paths : `~matplotlib.collections.PathCollection`
# Examples
# --------
# a = np.arange(11)
# circles(a, a, s=a*0.2, c=a, alpha=0.5, ec='none')
# plt.colorbar()
# License
# --------
# This code is under [The BSD 3-Clause License]
# (http://opensource.org/licenses/BSD-3-Clause)

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
    # plt.draw_if_interactive()
    if c is not None:
        plt.sci(collection)
    # return collection

#-------------------------
def plot_cells(frame):
# global current_idx, axes_max
    global current_frame
    current_frame = frame
    fname = "output%08d.xml" % frame
    #        full_fname = os.path.join(self.output_dir, fname)
    # with debug_view:
        # print("plot_cells:", full_fname) 
    # print("-- plot_cells:", full_fname) 
    if not os.path.isfile(fname):
        print("Once output files are generated, click the slider.")   
        return

    #mcds = pyMCDS(fname, self.output_dir)
    mcds = pyMCDS(fname)
    # print(mcds.get_time())

    cell_ids = mcds.data['discrete_cells']['ID']
    #        print(cell_ids.shape)
    #        print(cell_ids[:4])

    #cell_vec = np.zeros((cell_ids.shape, 3))
    num_cells = cell_ids.shape[0]
    cell_vec = np.zeros((cell_ids.shape[0], 3))
    vec_list = ['position_x', 'position_y', 'position_z']
    for i, lab in enumerate(vec_list):
        cell_vec[:, i] = mcds.data['discrete_cells'][lab]
    xvals = cell_vec[:, 0]
    yvals = cell_vec[:, 1]
    print('x range: ',xvals.min(), xvals.max())
    print('y range: ',yvals.min(), yvals.max())

    title_str = str(mcds.get_time()) + " min (" + str(num_cells) + " agents)"
    cell_vols = mcds.data['discrete_cells']['total_volume']
    cell_radii = (cell_vols* 0.75 / 3.14159)**0.3333
    circles(xvals,yvals, s=cell_radii, fc='none')

    plt.xlim(axes_min, axes_max)
    plt.ylim(axes_min, axes_max)
    plt.title(title_str)
    plt.axes().set_aspect('equal')
    plt.show()

plot_cells(14)
