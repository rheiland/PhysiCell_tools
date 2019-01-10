# Given CSV parameters for PhysiCell, generate .xml configuration files.
# Write out shell commands to run simulations using the config files.
# 

import xml.etree.ElementTree as ET
from shutil import copyfile
#from subprocess import call
import subprocess 
import os
import sys

# print(len(sys.argv))
# if (len(sys.argv) < 3):
#   usage_str = "Usage: %s <pgm> <params.csv>" % (sys.argv[0])
#   print(usage_str)
# #  print("e.g.:  python params_run2.py cancer-immune-EMEWS2 params_run2.txt")
#   print("e.g.:  python params_run2.py cancer-immune-EMEWS2 ga_output_a-stripM.csv")
#   exit(1)
# else:
#    pgm = sys.argv[1]
#    params_file = sys.argv[2]

pgm = 'cancer-immune-EMEWS2'

#xml_file_in = 'config/PhysiCell_settings.xml'
xml_file_in = 'config_from_repo_rwh.xml'
output_dirs = []

# Header line (param names)
pname = 'user_parameters.immune_apoptosis_rate,user_parameters.oncoprotein_threshold,user_parameters.immune_migration_bias,user_parameters.immune_attachment_rate,user_parameters.immune_attachment_lifetime,user_parameters.immune_kill_rate,mean_tumor_count'

params_file = 'ga_output_a-stripM.csv'
count = 1
p_unique = []
with open(params_file) as f:
    for line in f:
        xml_file_out = 'nick' + str(count) + '.xml'
#        print('-->',xml_file_out)
        copyfile(xml_file_in,xml_file_out)
        tree = ET.parse(xml_file_out)
        xml_root = tree.getroot()

        dir_out = 'nick' + str(count)

#       Generate cmds to create dirs
#        print('mkdir ' + dir_out)

        xml_root.find('.//folder').text = dir_out

#        print(len(line),line)
#        print(line,end='')
        if (line[0] == '#'):
            continue

#	In this case, we don't consider the last value in the CSV as an input param
        pstring = line[:line.rfind(',')]

#	Keep track of unique params (strings)
        if pstring in p_unique:
            continue
        else:
            p_unique.append(pstring)

        pval = pstring.split(',')
#        print('pval=',pval)
#        print()

        n=0
        for key in pname.split(','):
            if ('.' in key):
                k = key.split('.')
                uep = xml_root
                for idx in range(len(k)):
                    uep = uep.find('.//' + k[idx])  # unique entry point (uep) into xml
#                    print(k[idx])
#                uep.text = val
                uep.text = pval[n]
                print(k[idx],' -->',uep.text)
                n += 1

        tree.write(xml_file_out)
        cmd =  pgm + " " +  xml_file_out 
        print(cmd)
        count += 1
#        break
