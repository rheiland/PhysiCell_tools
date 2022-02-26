import sys
import os
import glob
import numpy as np
from pyMCDS_cells import pyMCDS_cells
import matplotlib.pyplot as plt

argc = len(sys.argv)-1
print("# args=",argc)

#data_dir = 'output'
if (argc < 3):
#  data_dir = int(sys.argv[kdx])
  print("Usage: <output dir> <num_days> <ymax>")
  sys.exit(-1)

kdx = 1
data_dir = sys.argv[kdx]
print('# data_dir = ',data_dir)

kdx += 1
num_days = int(sys.argv[kdx])
print('# num_days = ',num_days)
kdx += 1
ymax = float(sys.argv[kdx])
print('ymax = ',ymax)

os.chdir(data_dir)
xml_files = glob.glob('output*.xml')
os.chdir('..')
xml_files.sort()
#print('xml_files = ',xml_files)

ds_count = len(xml_files)
print("# ----- ds_count = ",ds_count)
mcds = [pyMCDS_cells(xml_files[i], data_dir) for i in range(ds_count)]

tval = np.linspace(0, mcds[-1].get_time(), ds_count)
print('type(tval)= ',type(tval))
print('tval= ',repr(tval))

# y_load = np.array( [np.floor(mcds[idx].data['discrete_cells']['assembled_virion']).sum()  for idx in range(ds_count)] ).astype(int)
# print(y_load)

# # mac,neut,cd8,DC,cd4,Fib
yval4 = np.array( [(np.count_nonzero((mcds[idx].data['discrete_cells']['cell_type'] == 4) & (mcds[idx].data['discrete_cells']['cycle_model'] < 100.) == True)) for idx in range(ds_count)] )
print('macs=',repr(yval4))

# count Neuts
yval5 = np.array( [(np.count_nonzero((mcds[idx].data['discrete_cells']['cell_type'] == 5) & (mcds[idx].data['discrete_cells']['cycle_model'] < 100.) == True)) for idx in range(ds_count)] )
print('neuts=',repr(yval5))

# count CD8
yval6 = np.array( [(np.count_nonzero((mcds[idx].data['discrete_cells']['cell_type'] == 3) & (mcds[idx].data['discrete_cells']['cycle_model'] < 100.) == True)) for idx in range(ds_count)] )
print('cd8=',repr(yval6))

# count DC
yval7 = np.array( [(np.count_nonzero((mcds[idx].data['discrete_cells']['cell_type'] == 6) & (mcds[idx].data['discrete_cells']['cycle_model'] < 100.) == True)) for idx in range(ds_count)] )
print('DC=',repr(yval7))

# count CD4
yval8 = np.array( [(np.count_nonzero((mcds[idx].data['discrete_cells']['cell_type'] == 7) & (mcds[idx].data['discrete_cells']['cycle_model'] < 100.) == True)) for idx in range(ds_count)] )
print('cd4=',repr(yval8))

# count Fibroblasts
yval9 = np.array( [(np.count_nonzero((mcds[idx].data['discrete_cells']['cell_type'] == 8) & (mcds[idx].data['discrete_cells']['cycle_model'] < 100.) == True)) for idx in range(ds_count)] )
print('fib=',repr(yval9))

plt.plot(tval, yval4, label='Mac', linewidth=1, color='lime')
plt.plot(tval, yval5, linestyle='dashed', label='Neut', linewidth=1, color='cyan')
plt.plot(tval, yval6, label='CD8', linewidth=1, color='red')
plt.plot(tval, yval7, linestyle='dashed', label='DC', linewidth=1, color='fuchsia')
plt.plot(tval, yval8, label='CD4', linewidth=1, color='orange')
plt.plot(tval, yval9, linestyle='dashed',  label='Fib', linewidth=1, color='orange')

#plt.legend(loc='center left', prop={'size': 15})
plt.legend(loc='upper left', prop={'size': 10})
#plt.legend(loc='upper right', prop={'size': 10})

# plt.xticks([1440,2*1440, 3*1440, 4*1440, 5*1440, 6*1440, 7*1440, 8*1440, 9*1440, 10*1440], ('1', '2','3','4','5','6','7','8','9','10'))
ndays = 30
ndays = 15
ndays = 12
ndays = num_days
xvals = [*range(1,ndays+1)]
xvals = [el * 1440 for el in xvals]
xlabels = tuple(str(val) for val in range(1,ndays+1))
plt.xticks(xvals, xlabels)
plt.ylim([0, ymax])
#plt.xticks([1440,2*1440, 3*1440, 4*1440, 5*1440, 6*1440, 7*1440, 8*1440, 9*1440, 10*1440, 11*1440, 12*1440, 13*1440, 14*1440, 15*1440], ('1', '2','3','4','5','6','7','8','9','10','11','12','13','14','15'))

# plt.xticks([1440,2*1440, 3*1440, 4*1440, 5*1440, 6*1440, 7*1440, 8*1440,9*1440,10*1440,11*1440,12*1440,13*1440,14*1440,15*1440,16*1440,17*1440,18*1440,19*1440,20*1440,21*1440], ('1', '2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21'))

plt.xlabel('Time (days)')
plt.ylabel('Number of cells')

plt.title(data_dir + ": immune cell counts")
outfile = data_dir + '_immune.png'
plt.savefig(outfile)
#plt.show()
