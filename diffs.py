# Use ImageMagick's "convert" to convert .svg files to some other format, e.g. jpg or png

import sys
import os

print(len(sys.argv))
if (len(sys.argv) < 5):
  usage_str = "Usage: %s dir1 dir2 start_idx stop_idx" % (sys.argv[0])
  print(usage_str)
  exit(1)
else:
  dir1 = sys.argv[1]
  dir2 = sys.argv[2]
  start_idx = int(sys.argv[3])
  stop_idx = int(sys.argv[4])

for idx in range(start_idx,stop_idx+1):
  fname = "snapshot%08d.svg" % idx
  cmd = "diff " + dir1 + "/" + fname + " " + dir2 + "/" + fname 
  print(cmd)
  os.system(cmd)
