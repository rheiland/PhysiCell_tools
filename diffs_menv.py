import sys
import os
import pathlib
import math
import scipy.io
import numpy as np
# current_idx = 0

# "virion","assembled virion","interferon 1","pro-inflammatory cytokine","chemokine","debris"
print ('len(sys.argv) = ',len(sys.argv))
if (len(sys.argv) < 4):
  current_idx = 0
  # field_index = 4
  print("Usage: dir1 dir2 index")
  sys.exit(1)
else:
  kdx = 1
  dir1 = sys.argv[kdx]
  kdx += 1
  dir2 = sys.argv[kdx]
  kdx += 1
  current_idx = int(sys.argv[kdx])
  kdx += 1
  # field_index = int(sys.argv[kdx])

#print('frame, field = ',current_idx, field_index)

#dir1 = 'out9a'
#dir2 = 'out9b'
fname = "output%08d_microenvironment0.mat" % current_idx
fname1 = os.path.join(dir1,fname)
fname2 = os.path.join(dir2,fname)
if not pathlib.Path(fname1).is_file():
    print("file not found: ",fname1)
if not pathlib.Path(fname2).is_file():
    print("file not found: ",fname2)

dict1 = {}
dict2 = {}
scipy.io.loadmat(fname1, dict1)
M1 = dict1['multiscale_microenvironment']   # M.shape=(10,1600); type(M)=numpy.ndarray
scipy.io.loadmat(fname2, dict2)
M2 = dict2['multiscale_microenvironment']   # M.shape=(10,1600); type(M)=numpy.ndarray

# print(" menv equal = ",np.array_equal(M1,M2))

# "virion","assembled virion","interferon 1","pro-inflammatory cytokine","chemokine","debris"
print("virion, assembled virion, interferon 1, pro-inflammatory cytokine, chemokine, debris")
for isub in range(4,10):
  f1 = M1[isub,:] 
  f2 = M2[isub,:] 
  print(isub,') min,max:', f1.min(),f1.max())
  print('    min,max:', f2.min(),f2.max())
  if np.array_equal(f1,f2):
    print("    True")
  else:
    print(" >>> FALSE <<<")