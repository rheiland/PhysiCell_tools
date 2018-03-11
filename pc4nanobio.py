# %load pc4nanobio.py
import ipywidgets as widgets
from ipywidgets import Layout, Button, Box
#from ipywidgets import interact, interactive
from subprocess import Popen, PIPE, STDOUT
#from hublib.cmd import runCommand
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import sys, os, glob, random, math
import numpy as np
from collections import deque

join_our_list = "(Join/ask questions at https://groups.google.com/forum/#!forum/physicell-users)\n"

get_ipython().run_line_magic('matplotlib', 'inline')

constWidth = '175px'
xmin = widgets.FloatText(
    value= -500.,
    description='$X_{min}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

ymin = widgets.FloatText(
    value= -500.,
    description='$Y_{min}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

zmin = widgets.FloatText(
    value= -500.,
    description='$Z_{min}$',
    disabled= True,
    layout = Layout(width = constWidth),
)
    
xmax = widgets.FloatText(
    value= 500.,
    description='$X_{max}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

ymax = widgets.FloatText(
    value= 500.,
    description='$Y_{max}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

zmax = widgets.FloatText(
    value= 500,
    description='$Z_{max}$',
    disabled=True,
    layout = Layout(width = constWidth),
)

tmax = widgets.BoundedFloatText(
    min = 0.,
    max = 100000000,
    value= 10000.,
    description='$Time_{max}$',
    disabled=False,
    layout = Layout(width = constWidth),
)
    
xdelta = widgets.BoundedFloatText(
    min = 1.,
    value= 20.,
    description='$X_{delta}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

ydelta = widgets.BoundedFloatText(
    min = 1.,
    value= 20.,
    description='$Y_{delta}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

zdelta = widgets.BoundedFloatText(
    min = 1.,
    value= 20.,
    description='$Z_{delta}$',
    disabled=True,
    layout = Layout(width = constWidth),
)
    
tdelta = widgets.BoundedFloatText(
    min = 0.01,
    value= 10.,
    description='$Time_{delta}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

toggle2D = widgets.Checkbox(
    value=True,
    description='2-D',
    disabled=False
)
def toggle2D_cb(b):
    #print(type(b))
    #print(b['new'])
    if (b['new']):
        #zmin.disabled = zmax.disabled = zdelta.disabled = True
        zmin.disabled = True
        zmax.disabled = True
    else:
        zmin.disabled = False
        zmax.disabled = False
    
toggle2D.observe(toggle2D_cb)

x_row = widgets.HBox([xmin,xmax,xdelta])
y_row = widgets.HBox([ymin,ymax,ydelta])
z_row = widgets.HBox([zmin,zmax,zdelta])
box_layout = Layout(display='flex',
                    flex_flow='column',
                    align_items='stretch',
                    border='solid',
                    width='90%')
#z_row = Box(children=items, layout=box_layout)
#z_row = Box([toggle2D,zmin,zmax,zdelta], layout=box_layout)
#domain_range = Box([x_row,y_row,z_row], layout=box_layout)


omp_threads = widgets.BoundedIntText(
    value=8,
    min=1,
    step=1,
    description='# threads',
    disabled=False,
)
prng_toggle = widgets.Checkbox(
    value=False,
    description='Seed PRNG',
    disabled=False,
    layout = Layout(width = constWidth),
)
prng_seed = widgets.BoundedIntText(
    min = 1,
    value=13,
    description='Seed value',
    disabled=False,
    layout = Layout(width = constWidth),
)
prng_row = widgets.HBox([prng_toggle, prng_seed])

#----- Output ------
output_dir_str = 'output'  # match the "value" of the widget below
output_dir = widgets.Text(
    value='output',
    description='Output Dir:',
)
def config_output_dir_cb(w):
    global output_dir_str
    output_dir_str = w.value
    print(output_dir_str)
    
output_dir.on_submit(config_output_dir_cb)

svg_toggle = widgets.Checkbox(
    value=True,
    description='SVG',
    disabled=False,
    layout = Layout(width = constWidth),
)
svg_t0 = widgets.BoundedFloatText (
    min=0,
    value=0.0,
    description='$T_0$',
    disabled=False,
    layout = Layout(width = constWidth),
)
svg_num_delT = widgets.BoundedIntText(
    min=1,
    value=5,
    description='Every $N^{th}$ time step',
    disabled=False,
    layout = Layout(width = constWidth),
)

mcds_toggle = widgets.Checkbox(
    value=False,
    description='MCDS',
    disabled=False,
    layout = Layout(width = constWidth),
)
mcds_t0 = widgets.FloatText(
    value=0.0,
    description='$T_0$',
    disabled=True,
    layout = Layout(width = constWidth),
)
mcds_num_delT = widgets.BoundedIntText(
    min=0,
    value=5,
    description='Every $N^{th}$ time step',
    disabled=True,
    layout = Layout(width = constWidth),
)

#----------------------------
def read_config_file_cb(b):
#    global pc4nanobio_config_xml
    tree = ET.parse(read_config_file.value)
    root = tree.getroot()
    xmin.value = float(root.find(".//xmin").text)
    xmax.value = float(root.find(".//xmax").text)
    xdelta.value = float(root.find(".//dx").text)
    
    ymin.value = float(root.find(".//ymin").text)
    ymax.value = float(root.find(".//ymax").text)
    ydelta.value = float(root.find(".//dy").text)
    
    zmin.value = float(root.find(".//zmin").text)
    zmax.value = float(root.find(".//zmax").text)
    zdelta.value = float(root.find(".//dz").text)
    
    tmax.value = float(root.find(".//max_time").text)
    
    omp_threads.value = int(root.find(".//omp_num_threads").text)
    
    output_dir.value = (root.find(".//folder").text)
    
    return

read_config_button = Button(
    description='Read config file',
    disabled=False,
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Read XML',
)
read_config_file = widgets.Text(
    value='nanobio_settings.xml',
    description='',
    disabled=False,
)
read_config_button.on_click(read_config_file_cb)

#----------------------------
def write_config_file_cb(b):
    print('writing config')

    # TODO: verify template .xml file exists!
    tree = ET.parse('nanobio_template.xml')
    root = tree.getroot()
    
    # TODO: verify valid type (numeric) and range?
    root.find(".//xmin").text = str(xmin.value)
    root.find(".//xmax").text = str(xmax.value)
    root.find(".//dx").text = str(xdelta.value)
    
    root.find(".//ymin").text = str(ymin.value)
    root.find(".//ymax").text = str(ymax.value)
    root.find(".//zmin").text = str(zmin.value)
    root.find(".//zmax").text = str(zmax.value)
    
    root.find(".//max_time").text = str(tmax.value)
    
    root.find(".//omp_num_threads").text = str(omp_threads.value)
    
    root.find(".//folder").text = str(output_dir.value)
    
    
#    user_details = ET.SubElement(root, "user_details")
#    ET.SubElement(user_details, "PhysiCell_settings", name="version").text = "devel-version"
#    ET.SubElement(user_details, "domain")
#    ET.SubElement(user_details, "xmin").text = "-100"

#    tree = ET.ElementTree(root)
#    tree.write(write_config_file.value)
#    tree.write("test.xml")

    # TODO: verify can write to this filename
    tree.write(write_config_file.value)
    
write_config_button = Button(
    description='Write config file',
    disabled=False,
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Generate XML',
)
write_config_button.on_click(write_config_file_cb)

write_config_file = widgets.Text(
    value='nano2.xml',
    description='',
    disabled=False
)

#----------------------------
run_output = widgets.Output(layout=widgets.Layout(width='900px', height='100px', border='solid'))
run_output

def run_cb(b):
    global my_proc
    print('run sim...')
    with run_output:
        args = ['/Users/heiland/git/PhysiCell-nanobio-com-fork/trunk/src/PhysiCell-nanobio','nanobio_settings.xml']
        my_proc = Popen(args, stdout=PIPE, stderr=STDOUT)
        #runCommand('/Users/heiland/git/PhysiCell-nanobio-com-fork/trunk/src/PhysiCell-nanobio nanobio_settings.xml')
        
        # This should be safe because we're not piping stdin to the process.
    # It gets tricky if we are, because the process can be waiting for input while we're waiting for output.
    while True:
        # Wait for some output, read it and print it.
        with run_output:
            my_output = my_proc.stdout.read1(1024).decode('utf-8')
            print(my_output, end='')

        # Has the subprocess finished yet?
        if my_proc.poll() is not None:
            break

    if my_proc.returncode != 0:
        print("Exited with error code:", my_proc.returncode)
    
    
run_button = Button(
    description='Run',
    disabled=False,
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Run simulation',
)
run_button.on_click(run_cb)

run_command = widgets.Text(
    value='PhysiCell-nanobio nanobio_settings.xml',
    description='',
    disabled=False,
)

def kill_cb(b):
    global my_proc
    print('kill sim...')
    my_proc.terminate()
    
kill_button = Button(
    description='Kill',
    disabled=False,
    button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Kill simulation',
)
kill_button.on_click(kill_cb)

read_config_row = widgets.HBox([read_config_button, read_config_file])
svg_output_row = widgets.HBox([svg_toggle, svg_t0, svg_num_delT])
mat_output_row = widgets.HBox([mcds_toggle, mcds_t0, mcds_num_delT])
write_config_row = widgets.HBox([write_config_button, write_config_file])
run_sim_row = widgets.HBox([run_button, run_command, kill_button])
config_tab = widgets.VBox([read_config_row, toggle2D, x_row,y_row,z_row,  tmax, omp_threads, prng_row,  
                           output_dir,svg_output_row,mat_output_row, write_config_row, run_sim_row, run_output])


#----------------------------------------------

#current_idx = 0

#for idx in range(len(sys.argv)):
use_defaults = True
show_nucleus = 0
current_idx = 0
axes_min = 0.0
axes_max = 2000
axes_max = 1000
scale_radius = 1.0

svg_dir_str = '.'

def plot_svg(SVG):
  global current_idx, axes_max
  global svg_dir_str
#  dir = svg_dir.value
  fname = svg_dir_str + "/snapshot%08d.svg" % SVG

  if (os.path.isfile(fname) == False):
    print("File does not exist: ",fname)
    return

  xlist = deque()
  ylist = deque()
  rlist = deque()
  rgb_list = deque()

#  print('\n---- ' + fname + ':')
  tree = ET.parse(fname)
  root = tree.getroot()
#  print('--- root.tag ---')
#  print(root.tag)
#  print('--- root.attrib ---')
#  print(root.attrib)


#  print('--- child.tag, child.attrib ---')
  numChildren = 0
  for child in root:
#    print(child.tag, child.attrib)
#    print("keys=",child.attrib.keys())
    if use_defaults and ('width' in child.attrib.keys()):
      axes_max = float(child.attrib['width'])
#      print("--- found width --> axes_max =", axes_max)
    if child.text and "Current time" in child.text:
      svals = child.text.split()
      #title_str = "(" + str(current_idx) + ") Current time: " + svals[2] + "d, " + svals[4] + "h, " + svals[7] + "m"
      title_str = "Current time: " + svals[2] + "d, " + svals[4] + "h, " + svals[7] + "m"

#    print("width ",child.attrib['width'])
#    print('attrib=',child.attrib)
#    if (child.attrib['id'] == 'tissue'):
    if ('id' in child.attrib.keys()):
#      print('-------- found tissue!!')
      tissue_parent = child
      break

#  print('------ search tissue')
  cells_parent = None

  for child in tissue_parent:
#    print('attrib=',child.attrib)
    if (child.attrib['id'] == 'cells'):
#      print('-------- found cells, setting cells_parent')
      cells_parent = child
      break
    numChildren += 1


  num_cells = 0
#  print('------ search cells')
  for child in cells_parent:
#    print(child.tag, child.attrib)
#    print('attrib=',child.attrib)
    for circle in child:  # two circles in each child: outer + nucleus
    #  circle.attrib={'cx': '1085.59','cy': '1225.24','fill': 'rgb(159,159,96)','r': '6.67717','stroke': 'rgb(159,159,96)','stroke-width': '0.5'}
#      print('  --- cx,cy=',circle.attrib['cx'],circle.attrib['cy'])
      xval = float(circle.attrib['cx'])

      s = circle.attrib['fill']
#      print("s=",s)
#      print("type(s)=",type(s))
      if (s[0:3] == "rgb"):  # if an rgb string, e.g. "rgb(175,175,80)" 
        rgb = list(map(int, s[4:-1].split(",")))  
        rgb[:]=[x/255. for x in rgb]
      else:     # otherwise, must be a color name
        rgb_tuple = mplc.to_rgb(mplc.cnames[s])  # a tuple
        rgb = [x for x in rgb_tuple]

      # test for bogus x,y locations (rwh TODO: use max of domain?)
      too_large_val = 10000.
      if (math.fabs(xval) > too_large_val):
        print("bogus xval=",xval)
        break
      yval = float(circle.attrib['cy'])
      if (math.fabs(yval) > too_large_val):
        print("bogus xval=",xval)
        break

      rval = float(circle.attrib['r'])
#      if (rgb[0] > rgb[1]):
#        print(num_cells,rgb, rval)
      xlist.append(xval)
      ylist.append(yval)
      rlist.append(rval)
      rgb_list.append(rgb)

#     For .svg files with cells that *have* a nucleus, there will be a 2nd
      if (show_nucleus == 0):
        break

    num_cells += 1

#    if num_cells > 3:   # for debugging
#      print(fname,':  num_cells= ',num_cells," --- debug exit.")
#      sys.exit(1)
#      break

  #print(fname,':  num_cells= ',num_cells)

  xvals = np.array(xlist)
  yvals = np.array(ylist)
  rvals = np.array(rlist)
  rgbs =  np.array(rgb_list)
#print("xvals[0:5]=",xvals[0:5])
#print("rvals[0:5]=",rvals[0:5])
#  print("rvals.min, max=",rvals.min(),rvals.max())

  plt.cla()
  title_str += " (" + str(num_cells) + " agents)"
  plt.title(title_str)
  plt.xlim(axes_min,axes_max)
  plt.ylim(axes_min,axes_max)
  plt.scatter(xvals,yvals, s=rvals*scale_radius, c=rgbs)
#plt.xlim(0,2000)  # TODO - get these values from width,height in .svg at top
#plt.ylim(0,2000)
#  plt.pause(time_delay)
  plt.axis('equal')


# keep last plot displayed
#plt.ioff()
#plt.show()

def svg_dir_cb(w):
    global svg_dir_str
    svg_dir_str = w.value
    print(svg_dir_str)
    
svg_dir = widgets.Text(
    value='.',
    description='Directory:',
)
#svg_dir.observe(svg_dir_cb)
svg_dir.on_submit(svg_dir_cb)

svg_plot = widgets.interactive(plot_svg, SVG=(0, 480), continuous_update=False)
output = svg_plot.children[-1]
output.layout.height = '300px'
svg_plot

svg_play = widgets.Play(
#     interval=10,
    value=50,
    min=0,
    max=100,
    step=1,
    description="Press play",
    disabled=False,
)
svg_slider = widgets.IntSlider()
widgets.jslink((svg_play, 'value'), (svg_slider, 'value'))
widgets.HBox([svg_play, svg_slider])

svg_tab = widgets.VBox([svg_dir, svg_plot, svg_play])
#---------------------

dummy_tab_stuff = widgets.Text(
    value='.',
    description='dummy:',
)
tabs = widgets.Tab(children=[config_tab, dummy_tab_stuff,dummy_tab_stuff, svg_tab])
tab_idx = 0
tabs.set_title(tab_idx, 'Config Basics | Run'); tab_idx += 1
tabs.set_title(tab_idx, 'Cells'); tab_idx += 1
tabs.set_title(tab_idx, 'PK/PD'); tab_idx += 1
tabs.set_title(tab_idx, 'SVG Plots')
widgets.VBox(children=[tabs])

