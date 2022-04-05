import sys
import os
import glob
import numpy as np
from pyMCDS import pyMCDS
import matplotlib.pyplot as plt

argc = len(sys.argv)-1
print("# args=",argc)

if (argc < 3):
#  data_dir = int(sys.argv[kdx])
  print("Usage: <dir> <num_days> <ymax or -1>")
  sys.exit(-1)

#data_dir = 'output'
kdx = 1
data_dir = sys.argv[kdx]

kdx += 1
num_days = int(sys.argv[kdx])
print('# num_days = ',num_days)
kdx += 1
ymax = float(sys.argv[kdx])
print('ymax = ',ymax)

#data_dir = 'output'
kdx = 1
data_dir = sys.argv[kdx]
print('data_dir = ',data_dir)
os.chdir(data_dir)
#xml_files = glob.glob('output/output*.xml')
xml_files = glob.glob('output*.xml')
os.chdir('..')
xml_files.sort()
#print('xml_files = ',xml_files)

ds_count = len(xml_files)
print("----- ds_count = ",ds_count)
mcds = [pyMCDS(xml_files[i], data_dir) for i in range(ds_count)]  # spews lots of prints

tval = np.linspace(0, mcds[-1].get_time(), ds_count)
print('tval= ',tval)

#print(mcds[0].get_substrate_names())
# ['virion', 'assembled virion', 'interferon 1', 'pro-inflammatory cytokine', 'chemokine', 'debris', 'pro-pyroptosis cytokine', 'anti-inflammatory cytokine', 'collagen']

f = np.array([ (mcds[idx].get_concentrations('virion')).sum()  for idx in range(ds_count)] )

xvals = [*range(1,num_days+1)]
xvals = [el * 1440 for el in xvals]
xlabels = tuple(str(val) for val in range(1,num_days+1))
plt.xticks(xvals, xlabels)

if ymax > 0:
  plt.ylim([0, ymax])

plt.plot(tval,f)
plt.title(data_dir + ": virion field (sum)")
plt.xlabel("time (days)")
#plt.savefig(data_dir + '.png')
plt.show()
