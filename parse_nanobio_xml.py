import xml.etree.ElementTree as ET

tree = ET.parse('nanobio_settings.xml')
root = tree.getroot()

prefix = ''
def print_children(parent):
  global prefix
  for child in parent:
    print(prefix,child.tag)
    prefix += '-'
    print_children(child)
  prefix = prefix[1:]

print_children(root)
