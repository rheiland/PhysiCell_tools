
import numpy as np
import scipy.io

def metric(idx):
    global current_idx

    cells_dict = {}
    iframe = 0
    fname = "output%08d_cells_physicell" % idx
    print("fname = ",fname)
    scipy.io.loadmat(fname, cells_dict)
    val = cells_dict['cells']

    num_cells = val.shape[1]
    print("num_cells =",num_cells)

    xvals = val[1,:]
    yvals = val[2,:]

    dist2 = xvals**2 + yvals**2
    dist = dist2**0.5
    print("avg dist of all cells = ",dist.sum()/len(dist))

for idx in range(0,18):
    metric(idx)