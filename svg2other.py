# Use ImageMagick's "convert" to convert .svg files to some other format, e.g. jpg or png

import sys
import os

print(len(sys.argv))
if (len(sys.argv) < 6):
  usage_str = "Usage: %s start_idx stop_idx step resize_pct jpg|png" % (sys.argv[0])
  print(usage_str)
  print("e.g.,")
  eg_str = "%s 0 1000 10 20 jpg" % (sys.argv[0])
  print(eg_str)
  exit(1)
else:
   start_idx = int(sys.argv[1])
   stop_idx = int(sys.argv[2])
   step = int(sys.argv[3])
   resize_pct = sys.argv[4]
   new_format = sys.argv[5]

for idx in range(start_idx,stop_idx+1,step):
  fname = "snapshot%08d" % idx
  cmd = "convert " + fname + ".svg -resize " + resize_pct + "% " + fname + "." + new_format
  print(cmd)
  os.system(cmd)
