# plot_microenvironment.py - plot results from
#    http://www.mathcancer.org/blog/biofvm-warmup-2d-continuum-simulation-of-tumor-growth/ 
import sys
import os.path
import scipy.io
import matplotlib.pyplot as plt

""" ----  Sample use:
python plot_microenvironment.py "output_240.000000.mat" 4 "tumor cells"
python plot_microenvironment.py "output_240.000000.mat" 5 "blood vessel density"
python plot_microenvironment.py "output_240.000000.mat" 6 "growth substrate"

----------"""

print("len(sys.argv) =",len(sys.argv))
# 4=tumor cells field, 5=blood vessel density, 6=growth substrate
if (len(sys.argv) < 4):
  print("Usage:  %s <filename> <field_index> <title>" % sys.argv[0])
  sys.exit(0)
else:
  fname = sys.argv[1]
  if (os.path.exists(fname) == False):
    print("File %s does not exist" % fname)
    sys.exit(0)
  field_index = int(sys.argv[2])
  title_str = sys.argv[3]

#fname = "output_240.000000.mat"
info_dict = {}
scipy.io.loadmat(fname, info_dict)
M = info_dict['multiscale_microenvironment']
f = M[field_index,:]   # 4=tumor cells field, 5=blood vessel density, 6=growth substrate
plt.clf()
my_plot = plt.imshow(f.reshape(400,400), cmap='jet', extent=[0,20, 0,20])
plt.colorbar(my_plot)
plt.title(title_str)
plt.show()
