import sys
import os
import glob
import numpy as np
from pyMCDS import pyMCDS
import matplotlib.pyplot as plt

argc = len(sys.argv)-1
print("# args=",argc)

if (argc < 1):
#  data_dir = int(sys.argv[kdx])
  print("Usage: provide output subdir")
  sys.exit(-1)


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

#print(mcds[0].get_substrate_names())
# ['virion', 'assembled virion', 'interferon 1', 'pro-inflammatory cytokine', 'chemokine', 'debris', 'pro-pyroptosis cytokine', 'anti-inflammatory cytokine', 'collagen']

for idx in range(ds_count):
  # print(np.isnan([ (mcds[idx].get_concentrations('virion')).sum()  for idx in range(ds_count)] )
  if True in np.isnan([ (mcds[idx].get_concentrations('virion')) ]):
    print("------- found NaN in file # ",idx)
