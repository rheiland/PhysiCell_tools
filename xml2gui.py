import sys
import xml.etree.ElementTree as ET

#tree = ET.parse('nanobio_settings.xml')
tree = ET.parse('test1.xml')
root = tree.getroot()
fn1 = "widgets.txt"
fp1 = open(fn1,"w")
fn1b = "wtail.txt"
fp1b = open(fn1b,"w")
fn2 = "fill_gui.txt"
fp2 = open(fn2,"w")

hdr = "from ipywidgets import Layout, Label, Text, Checkbox, Button, HBox, VBox, \\ \n \
    FloatText, BoundedIntText, BoundedFloatText, HTMLMath, Dropdown \n \
\n\
class CellsTab(object): \n \
\n\
    def __init__(self): \n"
fp1.write(hdr)

prefix = ''
bspace4 = 4*' '
bspace8 = 8*' '
widget_list = []

row_counter = 0

fp2.write(bspace4 + "def fill_gui(self, xml_root):\n\n")
fp2.write(bspace8 + "uep = xml_root.find('.//cell_definition')  # find unique entry point into XML\n\n")

# TODO: somehow this jumps from apoptosis over metabolism and into middle of motility!!
# TODO: ignore "substrate" (or handle in a special manner)
# TODO: make unique names for substrate elms, e.g. self.oxygen_uptake_rate
def print_children(parent):
  global prefix, child, widget_list, row_counter
  for child in parent:
    print(prefix,child.tag)   # debug
    # if (child.tag == 'necrosis'):
    #   fpout.close()
    #   sys.exit(-1)
    prefix += '-'
#    print(len(prefix))
    if (len(prefix) <= 5): 
      if len(widget_list) > 0:
        row_counter += 1
        print(widget_list)
        print("row" + str(row_counter) + " = HBox([", end='')
        [print(elm,end=', ') for elm in widget_list]
        print("])")
#        print(str(widget_list))
        fp1b.write(bspace8 + "row" + str(row_counter) + " = HBox([" )
        [fp1b.write(elm + ", ") for elm in widget_list]
        fp1b.write("])\n")
        fp1b.flush()
      widget_list = []
    if (len(prefix) >= 4):  # only want a widget if there are "units"
#      widget_list = []
      if len(child.attrib) > 0:
        widget_desc = child.tag.replace('_',' ')
  #      if child.attrib[]
        widget_units = 'mystery_units'
        if 'units' in child.attrib.keys():
#          widget_units = child.attrib['units'] + "_units"
          widget_units = child.attrib['units']   #  {'units' : "1/min"}
        widget_name = "self." + child.tag 

	     # TODO (manually?): sometimes want: style={'description_width': 'initial'},
        if (widget_units == "dimensionless") or (widget_units == ''):
          labels_string = ""
        else:
          labels_string = "Label('" + widget_units + "')"
        widget_defn = widget_name + " = HBox([BoundedFloatText(min=0, \n \
          description='" + widget_desc + "', layout=Layout(width=constWidth), ), " + \
          labels_string + "], \n \
          layout=Layout(width=width_cell_params_units))"
#        print(bspace8,widget_defn)
#        print(widget_defn)
        fp1.write(bspace8 + widget_defn + "\n")
        fp1.flush()
        widget_list.append(widget_name)

        # in another file, generate the 'fill_gui' method contents
        fp2.write(bspace8 + "self." + child.tag + ".children[0].value = float(uep.find('.//" + child.tag + "').text)\n")
#        fp2.flush()

    print_children(child)
  prefix = prefix[1:]


print_children(root)

fp1b.flush()
fp1b.write(bspace8 + "ctab = VBox([")
for idx in range(row_counter):
  fp1b.write("row" + str(idx) + ",")
fp1b.write("])")

fp1.close()
fp1b.close()
fp2.close()
print("\n--> ",fn1,", ",fn1b,", ",fn2)
