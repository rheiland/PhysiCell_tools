import sys
import xml.etree.ElementTree as ET

#tree = ET.parse('nanobio_settings.xml')
tree = ET.parse('test1.xml')
root = tree.getroot()
fp1 = open("gui.dot","w")


def print_children(parent, recursive):
  global prefix, child, widget_list, row_counter
#  if not recursive:
#    print(parent.tag, end= ' -- ')
  if len(parent.getchildren()) == 0:
#    print(parent.tag, end= ' -- ')
    return
  for child in parent:
    print(parent.tag + " -- " + child.tag)

  for child in parent:
    if recursive:
      print_children(child, recursive)
  print()

recurse_flag = True
#print_children(root,recurse_flag)
print('-----------------------------\n')
uep = root.find(".//basic_phenotype")
print_children(uep,recurse_flag)
uep = root.find(".//cycle")
#print_children(uep,recurse_flag)
#fp1.close()
