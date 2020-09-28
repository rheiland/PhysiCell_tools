from pyMCDS_cells import pyMCDS_cells
import numpy as np
import os
import glob
import matplotlib.pyplot as plt

# os.chdir('data')
xml_files = glob.glob('output*.xml')
xml_files.sort()

n = len(xml_files)
t= np.zeros(n)
num_epi = np.zeros(n)
idx = 0
for f in xml_files:
#    mcds = pyMCDS_cells(f,'data')
    mcds = pyMCDS_cells(f,'.')
    cycle = mcds.data['discrete_cells']['cycle_model']
    cycle = cycle.astype(int)
    cell_type = mcds.data['discrete_cells']['cell_type']
#    macrophage = np.where(cell_type == 4.0)
#    epi = np.where(cell_type == 1.0)  # all epi
    epi = np.where((cell_type == 1.0) & ( cycle < 100 ))  # non-dead epi
    t[idx] = mcds.get_time()
    num_epi[idx] = len(epi[0])
    idx += 1

plt.plot(t,num_epi,'-o',)
plt.show()