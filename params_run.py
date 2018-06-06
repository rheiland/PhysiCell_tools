#
# 

import xml.etree.ElementTree as ET
from shutil import copyfile
#from subprocess import call
import subprocess 
import os
import sys

#print(len(sys.argv))
if (len(sys.argv) < 2):
  usage_str = "Usage: %s <params.txt>" % (sys.argv[0])
  print(usage_str)
#  print("e.g.,")
#  eg_str = "%s 0 1000 10 20 jpg" % (sys.argv[0])
#  print(eg_str)
  exit(1)
else:
#   start_idx = int(sys.argv[1])
#   stop_idx = int(sys.argv[2])
   params_file = sys.argv[1]


xml_file_in = 'config/PhysiCell_settings.xml'
xml_file_out = 'config/tmp.xml'
copyfile(xml_file_in,xml_file_out)
tree = ET.parse(xml_file_out)
xml_root = tree.getroot()
#d = {}
first_time = True
output_dirs = []
#with open("param_runs.txt") as f:
with open(params_file) as f:
    for line in f:
        print(len(line),line)
        if (line[0] == '#'):
            continue
        (key, val) = line.split()
        if (key == 'folder'):
            if first_time:  # we've read the 1st 'folder'
                first_time = False
            else:  # we've read  additional 'folder's
#                first_time = True
                # write the config file to the previous folder (output) dir and start a simulation
                print('---write (previous) config file and start its sim')
                tree.write(xml_file_out)
#                subprocess.call(["clones2", xml_file_out]) # maybe Popen instead of call (for background)
                cmd = "clones2 " +  xml_file_out + " &"
                os.system(cmd)

            xml_file_out = val + '/config.xml'  # copy config file into the output dir
            output_dirs.append(val)
        if ('.' in key):
            k = key.split('.')
            uep = xml_root
            for idx in range(len(k)):
                uep = uep.find('.//' + k[idx])  # unique entry point (uep) into xml
#                print(k[idx])
            uep.text = val
#    	d[key] = val
        else:
            if (key == 'folder' and not os.path.exists(val)):
                print('creating ' + val)
                os.makedirs(val)

            xml_root.find('.//' + key).text = val

tree.write(xml_file_out)

cwd = os.getcwd()
#call(cwd + '/clones2 ' + cwd + '/config/tmp.xml')
#subprocess.call(["clones2", "config/tmp.xml"])
#subprocess.call(["clones2", xml_file_out])

cmd = "clones2 " +  xml_file_out + " &"
os.system(cmd)

print(output_dirs)

# python svg2other.py 0 120 1 25 jpg
# mencoder "mf://snapshot*.jpg" -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=10000:mbd=2:trell -mf fps=10:type=jpg -nosound -o foo.avi
# convert foo.avi tiny_tumor_defaults.mp4
