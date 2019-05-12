import sys,pathlib
import xml.etree.ElementTree as ET
import math
import scipy.io
import matplotlib
#import matplotlib.pyplot as plt  # NB! do this AFTER the TkAgg line below!
#import matplotlib.colors as mplc
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
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

if (len(sys.argv) < 3):
  current_idx = 0
  field_idx = 4
  fix_cmap = 0
  print("Usage: %s start_idx field_idx fix_cmap(0/1) vmin vmax" % sys.argv[0])
  print("e.g. %s start_idx field_idx fix_cmap(0/1) vmin vmax\n" % sys.argv[0])
else:
  kdx = 1
  current_idx = int(sys.argv[kdx]); kdx += 1
  field_idx = int(sys.argv[kdx]); kdx += 1
  fix_cmap = int(sys.argv[kdx]); kdx += 1
  vmin = float(sys.argv[kdx]); kdx += 1
  vmax = float(sys.argv[kdx]); kdx += 1

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
print("numx, numy = ",numx,numy)


fig = plt.figure(figsize=(7,5.8))
#ax = fig.gca()

time_delay = 0.1
count = -1

cbar = None

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
#    print(title_str)

    fname = "output%08d_microenvironment0.mat" % current_idx
    output_dir_str = '.'
    fullname = output_dir_str + "/" + fname
    if not pathlib.Path(fullname).is_file():
        print("file not found",fullname)
        return

    info_dict = {}
    scipy.io.loadmat(fullname, info_dict)
    M = info_dict['multiscale_microenvironment']
#    print('plot_substrate: field_idx=',field_idx)
    f = M[field_idx,:]   # 
    
    #N = int(math.sqrt(len(M[0,:])))
    #grid2D = M[0,:].reshape(N,N)
    xgrid = M[0, :].reshape(numy, numx)
    ygrid = M[1, :].reshape(numy, numx)

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
      my_plot = plt.contourf(xgrid, ygrid, M[field_idx, :].reshape(numy, numx), levels=levels, extend='both', cmap=cmap)
    else:
      # my_plot = plt.contourf(xvec,xvec,M[field_idx,:].reshape(N,N), cmap=cmap)
      my_plot = plt.contourf(xgrid, ygrid, M[field_idx, :].reshape(numy, numx), cmap=cmap)

    if cbar == None:
#      cbar = plt.colorbar(my_plot, boundaries=np.arange(vmin, vmax, 1.0))
      cbar = plt.colorbar(my_plot)
    else:
      cbar = plt.colorbar(my_plot, cax=cbar.ax)

#    plt.axis('equal')
    plt.title(title_str)

#    plt.show()

    png_file = "aaa%08d.png" % current_idx
    fig.savefig(png_file)
    plt.pause(time_delay)


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
  elif event.key == 'right':  # right arrow key
#        print('go forwards')
#        fig.canvas.draw()
    current_idx += step_value
    plot_substrate()
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
  else:
    print('press', event.key)

plot_substrate()
print("\nNOTE: click in plot window to give it focus before using keys.")

fig.canvas.mpl_connect('key_press_event', press)
#plot_substrate(frame_idx)
plt.show()

