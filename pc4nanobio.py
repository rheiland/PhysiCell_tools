
# coding: utf-8

# In[74]:


# %load pc4nanobio.py

# %load pc4nanobio.py
import ipywidgets as widgets
from ipywidgets import Layout, Button, Box
#from ipywidgets import interact, interactiveel
from subprocess import Popen, PIPE, STDOUT
from hublib.cmd import runCommand
from hublib.ui import RunCommand
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import scipy.io
import sys, os, glob, random, math
import numpy as np
from collections import deque

join_our_list = "(Join/ask questions at https://groups.google.com/forum/#!forum/physicell-users)\n"

get_ipython().run_line_magic('matplotlib', 'inline')

constWidth = '175px'
constWidth = '160px'
tab_height = '400px'
tab_height = '500px'
tab_layout = widgets.Layout( width='800px',   # border='2px solid black',
                            height=tab_height, overflow_y='scroll',)
np_tab_layout = widgets.Layout( width='800px',  # border='2px solid black',
                               height='350px', overflow_y='scroll',)
#tab_layout.height = '500px'

# my_domain = [0,0,-10, 2000,2000,10, 20,20,20]  # [x,y,zmin,  x,y,zmax, x,y,zdelta]
label_domain = widgets.Label('Domain (microns)')
xmin = widgets.FloatText(
    description='$X_{min}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

ymin = widgets.FloatText(
    description='$Y_{min}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

zmin = widgets.FloatText(
    description='$Z_{min}$',
    disabled= True,
    layout = Layout(width = constWidth),
)
    
xmax = widgets.FloatText(
    description='$X_{max}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

ymax = widgets.FloatText(
    description='$Y_{max}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

zmax = widgets.FloatText(
    description='$Z_{max}$',
    disabled=True,
    layout = Layout(width = constWidth),
)

tmax = widgets.BoundedFloatText(
    min = 0.,
    max = 100000000,
    description='$Time_{max}$',
    disabled=False,
    layout = Layout(width = constWidth),
)
    
xdelta = widgets.BoundedFloatText(
    min = 1.,
    description='$X_{delta}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

ydelta = widgets.BoundedFloatText(
    min = 1.,
    description='$Y_{delta}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

zdelta = widgets.BoundedFloatText(
    min = 1.,
    description='$Z_{delta}$',
    disabled=True,
    layout = Layout(width = constWidth),
)
    
tdelta = widgets.BoundedFloatText(
    min = 0.01,
    description='$Time_{delta}$',
    disabled=False,
    layout = Layout(width = constWidth),
)

toggle2D = widgets.Checkbox(
    description='2-D',
    disabled=False,
    layout = Layout(width = constWidth),
)
def toggle2D_cb(b):
    if (toggle2D.value):
        #zmin.disabled = zmax.disabled = zdelta.disabled = True
        zmin.disabled = True
        zmax.disabled = True
        zdelta.disabled = True
    else:
        zmin.disabled = False
        zmax.disabled = False
        zdelta.disabled = False
    
toggle2D.observe(toggle2D_cb)

x_row = widgets.HBox([xmin,xmax,xdelta])
y_row = widgets.HBox([ymin,ymax,ydelta])
z_row = widgets.HBox([zmin,zmax,zdelta])
# box_layout = Layout(display='flex',
#                     flex_flow='column',
#                     align_items='stretch',
#                     border='1px solid black',
#                     width='90%')
#z_row = Box(children=items, layout=box_layout)
#z_row = Box([toggle2D,zmin,zmax,zdelta], layout=box_layout)
#domain_range = Box([x_row,y_row,z_row], layout=box_layout)

tumor_radius = widgets.BoundedFloatText(
    min=1,
    max=99999,  # TODO - wth
    step=1,
    description='Tumor Radius', style={'description_width': 'initial'},
    disabled=False,
    layout = Layout(width = constWidth),
)

omp_threads = widgets.BoundedIntText(
    min=1,
    step=1,
    description='# threads',
    disabled=False,
    layout = Layout(width = constWidth),
)

toggle_prng = widgets.Checkbox(
    description='Seed PRNG', style={'description_width': 'initial'},  # e.g. 'initial'  '120px'
    disabled=False,
    layout = Layout(width = constWidth),
)
prng_seed = widgets.BoundedIntText(
    min = 1,
    description='Seed', 
    disabled=True,
    layout = Layout(width = constWidth),
)
def toggle_prng_cb(b):
    if (toggle_prng.value):
        prng_seed.disabled = False
    else:
        prng_seed.disabled = True
    
toggle_prng.observe(toggle_prng_cb)

#prng_row = widgets.HBox([toggle_prng, prng_seed])

#----- Output ------
output_dir_str = 'output'  # match the "value" of the widget below
output_dir = widgets.Text(
#     value='output',
    description='Output Dir',
)
def config_output_dir_cb(w):
    global output_dir_str
    output_dir_str = w.value
    print(output_dir_str)
    
output_dir.on_submit(config_output_dir_cb)

toggle_svg = widgets.Checkbox(
    description='SVG',
    disabled=False,
    layout = Layout(width = constWidth),
)
svg_t0 = widgets.BoundedFloatText (
    min=0,
    description='$T_0$',
    disabled=False,
    layout = Layout(width = constWidth),
)
svg_interval = widgets.BoundedIntText(
    min=1,
    max=99999999,
    description='interval',
    disabled=False,
    layout = Layout(width = constWidth),
)
def toggle_svg_cb(b):
    if (toggle_svg.value):
        svg_t0.disabled = False #False
        svg_interval.disabled = False
    else:
        svg_t0.disabled = True
        svg_interval.disabled = True
    
toggle_svg.observe(toggle_svg_cb)


toggle_mcds = widgets.Checkbox(
#     value=False,
    description='Full',
    disabled=False,
    layout = Layout(width = constWidth),
)
mcds_t0 = widgets.FloatText(
    description='$T_0$',
    disabled=True,
    layout = Layout(width = constWidth),
)
mcds_interval = widgets.BoundedIntText(
    min=0,
    max=99999999,
    description='interval',
    disabled=True,
    layout = Layout(width = constWidth),
)
def toggle_mcds_cb(b):
    if (toggle_mcds.value):
        mcds_t0.disabled = False #False
        mcds_interval.disabled = False
    else:
        mcds_t0.disabled = True
        mcds_interval.disabled = True
    
toggle_mcds.observe(toggle_mcds_cb)

#----------------------------
# NOTE: any time the elm names change in the XML, need to change here!!!
def read_config_file_cb(b):
#    global pc4nanobio_config_xml
    tree = ET.parse(read_config_file.value)
    root = tree.getroot()
    xmin.value = float(root.find(".//x_min").text)
    xmax.value = float(root.find(".//x_max").text)
    xdelta.value = float(root.find(".//dx").text)
    
    ymin.value = float(root.find(".//y_min").text)
    ymax.value = float(root.find(".//y_max").text)
    ydelta.value = float(root.find(".//dy").text)
    
    zmin.value = float(root.find(".//z_min").text)
    zmax.value = float(root.find(".//z_max").text)
    zdelta.value = float(root.find(".//dz").text)
    
    tmax.value = float(root.find(".//max_time").text)
    
    tumor_radius.value = float(root.find(".//radius").text)
    omp_threads.value = int(root.find(".//omp_num_threads").text)
    
#     output_dir.value = (root.find(".//folder").text)
    svg_interval.value = int(root.find(".//SVG").find(".//interval").text)
    mcds_interval.value = int(root.find(".//full_data").find(".//interval").text)
    
    max_birth_rate.value = float(root.find(".//max_birth_rate").text)
    o2_prolif_sat.value = float(root.find(".//o2_proliferation_saturation").text)
    o2_prolif_thresh.value = float(root.find(".//o2_proliferation_threshold").text)
#     o2_ref.value = float(root.find(".//o2_reference").text)
    glucose_prolif_ref.value = float(root.find(".//glucose_proliferation_reference").text)
    glucose_prolif_sat.value = float(root.find(".//glucose_proliferation_saturation").text)
    glucose_prolif_thresh.value = float(root.find(".//glucose_proliferation_threshold").text)
    
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
    root.find(".//x_min").text = str(xmin.value)
    root.find(".//x_max").text = str(xmax.value)
    root.find(".//dx").text = str(xdelta.value)
    root.find(".//y_min").text = str(ymin.value)
    root.find(".//y_max").text = str(ymax.value)
    root.find(".//dy").text = str(ydelta.value)
    root.find(".//z_min").text = str(zmin.value)
    root.find(".//z_max").text = str(zmax.value)
    root.find(".//dz").text = str(zdelta.value)
    
    root.find(".//max_time").text = str(tmax.value)
    
    root.find(".//radius").text = str(tumor_radius.value)
    root.find(".//omp_num_threads").text = str(omp_threads.value)
    
#     root.find(".//folder").text = str(output_dir.value)
    
    
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
#run_output

run_command_str = widgets.Text(
    value='pc-nb nanobio_settings.xml',
    description='',
    disabled=False,
)

def run_sim(s):
    s.run("/Users/heiland/dev/run-nanobio/pc-nb nanobio_settings.xml")
    
def run_cb(b):
    global my_proc
    print('running: ', run_command_str.value)
    with run_output:
#         print(type(run_button))
#         print(dir(run_button))
#         args = ['/Users/heiland/git/PhysiCell-nanobio-com-fork/trunk/src/PhysiCell-nanobio','nanobio_settings.xml']
        args = ['/Users/heiland/dev/run-nanobio/pc-nb','nanobio_settings.xml']
        #my_proc = Popen(args, stdout=PIPE, stderr=STDOUT)
        #runCommand('/Users/heiland/git/PhysiCell-nanobio-com-fork/trunk/src/PhysiCell-nanobio nanobio_settings.xml')
        sys.path.insert(0, os.path.abspath('..'))
#         runCommand('/Users/heiland/dev/run-nanobio/pc-nb nanobio_settings.xml')
        runCommand('pc-nb nanobio_settings.xml')
        
    # NOTE: using the following approach will block us from other processes, e.g. visualizing results or executing a cmd in another cell
    # This should be safe because we're not piping stdin to the process.
    # It gets tricky if we are, because the process can be waiting for input while we're waiting for output.
#     while True:
#         # Wait for some output, read it and print it.
#         with run_output:
#             my_output = my_proc.stdout.read1(1024).decode('utf-8')
#             print(my_output, end='')

#         # Has the subprocess finished yet?
#         if my_proc.poll() is not None:
#             break

    if my_proc.returncode != 0:
        print("Exited with error code:", my_proc.returncode)

        
run_button = RunCommand(start_func=run_sim)  # optionally: , done_func=read_data

# run_button = Button(
#     description='Run',
#     disabled=False,
#     button_style='success', # 'success', 'info', 'warning', 'danger' or ''
#     tooltip='Run simulation',
# )
# run_button.on_click(run_cb)

# def kill_cb(b):
#     global my_proc
#     print('kill sim...')
#     my_proc.terminate()
    
# kill_button = Button(
#     description='Kill',
#     disabled=False,
#     button_style='danger', # 'success', 'info', 'warning', 'danger' or ''
#     tooltip='Kill simulation',
# )
# kill_button.on_click(kill_cb)

read_config_row = widgets.HBox([read_config_button, read_config_file])
#svg_output_row = widgets.HBox([toggle_svg, svg_t0, svg_interval])
#mat_output_row = widgets.HBox([toggle_mcds, mcds_t0, mcds_interval])
svg_mat_output_row = widgets.HBox([toggle_svg,svg_interval, toggle_mcds,mcds_interval])
write_config_row = widgets.HBox([write_config_button, write_config_file])
#run_sim_row = widgets.HBox([run_button, run_command_str, kill_button])
# run_sim_row = widgets.HBox([run_button, run_command_str])
# run_sim_row = widgets.HBox([run_button.w])  # need ".w" for the custom RunCommand widget

toggle_2D_seed_row = widgets.HBox([toggle2D, toggle_prng, prng_seed])
config_tab = widgets.VBox([read_config_row, toggle_2D_seed_row, label_domain,x_row,y_row,z_row,  tmax, omp_threads,  
                           tumor_radius,svg_mat_output_row], layout=tab_layout)  # output_dir


#----------------------------------------------

#current_idx = 0

#for idx in range(len(sys.argv)):
use_defaults = True
show_nucleus = 0
current_idx = 0
axes_min = 0.0
axes_max = 2000
#axes_max = 1000
scale_radius = 1.0

svg_dir_str = output_dir_str
mcds_dir_str = output_dir_str

field_index = 4
def plot_substrate(FileId):
    global current_idx, axes_max, gFileId, field_index
    global svg_dir_str
    #  dir = svg_dir.value
#     print('debug> plot_substrate: idx=',FileId)
    gFileId = FileId
    fname = "output%08d_microenvironment0.mat" % FileId
    fullname = svg_dir_str + "/" + fname

    info_dict = {}
    scipy.io.loadmat(fullname, info_dict)
    M = info_dict['multiscale_microenvironment']
#     global_field_index = int(mcds_field.value)
#     print('plot_substrate: field_index =',field_index)
    f = M[field_index,:]   # 4=tumor cells field, 5=blood vessel density, 6=growth substrate
    #plt.clf()
    #my_plot = plt.imshow(f.reshape(400,400), cmap='jet', extent=[0,20, 0,20])
    
    fig = plt.figure(figsize=(7.2,6))  # this strange figsize results in a ~square contour plot
#     fig.set_tight_layout(True)
#     ax = plt.axes([0, 0.05, 0.9, 0.9 ]) #left, bottom, width, height
#     ax = plt.axes([0, 0.0, 1, 1 ])
#     cmap = plt.cm.viridis # Blues, YlOrBr, ...
#     im = ax.imshow(f.reshape(100,100), interpolation='nearest', cmap=cmap, extent=[0,20, 0,20])
#     ax.grid(False)

    grid2D = M[0,:].reshape(100,100)
    xvec = grid2D[0,:]
    #xvec.size
    #xvec.shape
    num_contours = 30
    my_plot = plt.contourf(xvec,xvec,M[field_index,:].reshape(100,100), num_contours, cmap=field_cmap.value) #'viridis'
    plt.colorbar(my_plot)
    axes_min = 0
    axes_max = 2000
    plt.xlim(axes_min,axes_max)
    plt.ylim(axes_min,axes_max)
#     plt.title(fname)
#     ax.set_title(fname)
#     plt.axis('equal')
    #plt.show()


get_ipython().run_line_magic('matplotlib', 'inline')
def plot_svg(SVG):
  global current_idx, axes_max
  global svg_dir_str
#  dir = svg_dir.value
#   print('plot_svg: SVG=',SVG)
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
#       print("debug> found width --> axes_max =", axes_max)
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

#rwh - is this where I change size of render window?? (YES - yipeee!)
#   plt.figure(figsize=(6, 6))
#   plt.cla()
  title_str += " (" + str(num_cells) + " agents)"
#   plt.title(title_str)
#   plt.xlim(axes_min,axes_max)
#   plt.ylim(axes_min,axes_max)
#   plt.scatter(xvals,yvals, s=rvals*scale_radius, c=rgbs)
    
  fig = plt.figure(figsize=(6,6))
  ax = plt.axes([0, 0.05, 0.9, 0.9 ]) #left, bottom, width, height

#   im = ax.imshow(f.reshape(100,100), interpolation='nearest', cmap=cmap, extent=[0,20, 0,20])
#   ax.xlim(axes_min,axes_max)
#   ax.ylim(axes_min,axes_max)
  ax.scatter(xvals,yvals, s=rvals*scale_radius, c=rgbs)
  plt.xlim(axes_min,axes_max)
  plt.ylim(axes_min,axes_max)
#   ax.grid(False)
  ax.set_title(title_str)
    
#plt.xlim(0,2000)  # TODO - get these values from width,height in .svg at top
#plt.ylim(0,2000)
#  plt.pause(time_delay)
#   plt.axis('equal')   # doing this will cause the axes to scale dynamically, probably unwanted


# keep last plot displayed
#plt.ioff()
#   plt.show()

def svg_dir_cb(w):
    global svg_dir_str
    svg_dir_str = w.value
    print(svg_dir_str)
    
svg_dir = widgets.Text(
    value=svg_dir_str,
    description='Directory',
)
#svg_dir.observe(svg_dir_cb)
svg_dir.on_submit(svg_dir_cb)

#rwh - is this where I change size of render window?? (apparently not)
svg_plot = widgets.interactive(plot_svg, SVG=(0, 500), continuous_update=False)
# output = svg_plot.children[-1]
# output.layout.height = '300px'
# output = svg_plot.children[1]
svg_plot_size = '500px'
svg_plot.layout.width = svg_plot_size
svg_plot.layout.height = svg_plot_size

# video-style widget - perhaps for future use
# svg_play = widgets.Play(
#     interval=1,
#     value=50,
#     min=0,
#     max=100,
#     step=1,
#     description="Press play",
#     disabled=False,
# )
# def svg_slider_change(change):
#     print('svg_slider_change: type(change)=',type(change),change.new)
#     plot_svg(change.new)
    
#svg_play
# svg_slider = widgets.IntSlider()
# svg_slider.observe(svg_slider_change, names='value')

# widgets.jslink((svg_play, 'value'), (svg_slider,'value')) #  (svg_slider, 'value'), (plot_svg, 'value'))

# svg_slider = widgets.IntSlider()
# widgets.jslink((play, 'value'), (slider, 'value'))
# widgets.HBox([svg_play, svg_slider])

# Using the following generates a new mpl plot; it doesn't use the existing plot!
#svg_anim = widgets.HBox([svg_play, svg_slider])

#svg_tab = widgets.VBox([svg_dir, svg_plot, svg_anim], layout=tab_layout)
svg_tab = widgets.HBox([svg_dir, svg_plot], layout=tab_layout)

#svg_tab = widgets.VBox([svg_dir, svg_anim], layout=tab_layout)
#---------------------

cell_name = widgets.Text(
    value='untreated cancer',
    description='Name',
)
label_cycle = widgets.Label('Cycle:')
max_birth_rate = widgets.BoundedFloatText (
    min=0,
    description='Max birth rate', style={'description_width': 'initial'},
    disabled=False,
    layout = Layout(width = constWidth),
)
o2_prolif_sat = widgets.BoundedFloatText (
    min=0,
    description='$O_2$: Prolif sat',
    disabled=False,
    layout = Layout(width = constWidth),
)
o2_prolif_thresh = widgets.BoundedFloatText (
    min=0,
    description='Prolif thresh',
    disabled=False,
    layout = Layout(width = constWidth),
)
o2_prolif_ref = widgets.BoundedFloatText (
    min=0,
    description='Ref',
    disabled=False,
    layout = Layout(width = constWidth),
)

glucose_prolif_sat = widgets.BoundedFloatText (
    min=0,
    description='$G$: Prolif sat',
    disabled=False,
    layout = Layout(width = constWidth),
)
glucose_prolif_thresh = widgets.BoundedFloatText (
    min=0,
    description='Prolif thresh',
    disabled=False,
    layout = Layout(width = constWidth),
)
glucose_prolif_ref = widgets.BoundedFloatText (
    min=0,
    description='Ref',
    disabled=False,
    layout = Layout(width = constWidth),
)
#----
label_necrosis = widgets.Label('Necrosis:')
label_apoptosis = widgets.Label('Apoptosis:')
label_metabolism = widgets.Label('Metabolism:')
label_motility = widgets.Label('Motility:')
label_mechanics = widgets.Label('Mechanics:')
label_hypoxia = widgets.Label('Hypoxia:')
label_secretion = widgets.Label('Secretion:')



cells_row1 = widgets.HBox([cell_name])
cells_row2 = widgets.HBox([o2_prolif_sat, o2_prolif_thresh, o2_prolif_ref])
cells_row3 = widgets.HBox([glucose_prolif_sat, glucose_prolif_thresh, glucose_prolif_ref])
cells_tab = widgets.VBox([cells_row1,label_cycle,max_birth_rate,cells_row2, cells_row3,
                label_necrosis,max_birth_rate,cells_row2, cells_row3,
                label_apoptosis,label_metabolism,label_motility,
                label_mechanics,label_hypoxia,label_secretion]) #, layout=tab_layout)

#=========
half_conc_desc = '$T_{0.5}$'
diffusion_coef_desc = 'Diffusion coef'
survival_desc = 'Survival lifetime'
binding_desc = 'ECM binding rate'
unbinding_desc = 'ECM unbinding rate'
sat_conc_desc = 'ECM saturation conc'
desc_style = {'description_width': '150px'}  # vs. 'initial'

label_PK = widgets.Label('Pharmacokinetics:')
pk_param_width = '270px'
diffusion_coef_units = widgets.HTMLMath(value=r"$\frac{\mu M^2}{min}$")
survival_lifetime_units = widgets.HTMLMath(value=r"$min$")
min_inv_units = widgets.HTMLMath(value=r"$\frac{1}{min}$")

#------------
np1_diff_coef = widgets.BoundedFloatText (
    min=0,
    description= diffusion_coef_desc, style=desc_style,
    disabled=False,
    layout = Layout(width = pk_param_width),  #flex_flow='row',align_items='stretch'),
)
np1_survival_lifetime = widgets.BoundedFloatText (
    min=0,
    description= survival_desc, style=desc_style,
    disabled=False,
    layout = Layout(width = pk_param_width),  #flex_flow='row',align_items='stretch'),
)
np1_binding_rate = widgets.BoundedFloatText (
    min=0,
    description= binding_desc, style=desc_style,
    disabled=False,
    layout = Layout(width = pk_param_width),
)
np1_unbinding_rate = widgets.BoundedFloatText (
    min=0,
    description= unbinding_desc, style=desc_style,
    disabled=False,
    layout = Layout(width = pk_param_width),
)
np1_saturation_conc = widgets.BoundedFloatText (
    min=0,
    description= sat_conc_desc, style=desc_style,
    disabled=False,
    layout = Layout(width = pk_param_width),
)
#box_layout = Layout(display='flex',flex_flow='column',align_items='stretch',border='1px solid black',width='30%')
pk_widgets_width = '320px'
np1_diff_coef2 = widgets.HBox([np1_diff_coef,diffusion_coef_units], layout=Layout(width=pk_widgets_width),)
np1_survival_lifetime2 = widgets.HBox([np1_survival_lifetime,survival_lifetime_units], layout=Layout(width=pk_widgets_width),)
np1_binding_rate2 = widgets.HBox([np1_binding_rate,min_inv_units], layout=Layout(width=pk_widgets_width),)
np1_unbinding_rate2 = widgets.HBox([np1_unbinding_rate,min_inv_units], layout=Layout(width=pk_widgets_width),)
#np1_sat_conc2 = widgets.HBox([np1_saturation_conc,min_inv_units], layout=Layout(width=pk_widgets_width),)

np1_PK_params = widgets.VBox([label_PK,np1_diff_coef2,np1_survival_lifetime2,np1_binding_rate2,np1_unbinding_rate2,np1_saturation_conc]) #, layout=box_layout)

label_PD = widgets.Label('Pharmacodynamics:')

np1_tab = widgets.VBox([np1_PK_params, label_PD], layout=np_tab_layout)


#------------
#------------
np2_diff_coef = widgets.BoundedFloatText (
    min=0,
    description= diffusion_coef_desc, style=desc_style,
    disabled=False,
    layout = Layout(width = pk_param_width),  #flex_flow='row',align_items='stretch'),
)
np2_survival_lifetime = widgets.BoundedFloatText (
    min=0,
    description= survival_desc, style=desc_style,
    disabled=False,
    layout = Layout(width = pk_param_width),  #flex_flow='row',align_items='stretch'),
)
np2_binding_rate = widgets.BoundedFloatText (
    min=0,
    description= binding_desc, style=desc_style,
    disabled=False,
    layout = Layout(width = pk_param_width),
)
np2_unbinding_rate = widgets.BoundedFloatText (
    min=0,
    description= unbinding_desc, style=desc_style,
    disabled=False,
    layout = Layout(width = pk_param_width),
)
np2_saturation_conc = widgets.BoundedFloatText (
    min=0,
    description= sat_conc_desc, style=desc_style,
    disabled=False,
    layout = Layout(width = pk_param_width),
)
#box_layout = Layout(display='flex',flex_flow='column',align_items='stretch',border='1px solid black',width='30%')
np2_diff_coef2 = widgets.HBox([np2_diff_coef,diffusion_coef_units], layout=Layout(width=pk_widgets_width),)
np2_survival_lifetime2 = widgets.HBox([np2_survival_lifetime,survival_lifetime_units], layout=Layout(width=pk_widgets_width),)
np2_binding_rate2 = widgets.HBox([np2_binding_rate,min_inv_units], layout=Layout(width=pk_widgets_width),)
np2_unbinding_rate2 = widgets.HBox([np2_unbinding_rate,min_inv_units], layout=Layout(width=pk_widgets_width),)

np2_PK_params = widgets.VBox([label_PK,np2_diff_coef2,np2_survival_lifetime2,np2_binding_rate2,
                              np2_unbinding_rate2,np2_saturation_conc]) #, layout=box_layout)

label_PD = widgets.Label('Pharmacodynamics:')


np2_tab = widgets.VBox([np2_PK_params, label_PD], layout=np_tab_layout)

#-------------------
xforms_tab = widgets.Text(
    value='.',
    description='dummy:',
    layout=tab_layout,
)
np_tab = widgets.Tab(children=[np1_tab, np2_tab, xforms_tab])
np_tab.set_title(0, 'Preform (spherical)')
np_tab.set_title(1, 'Reconfig (rod)')
np_tab.set_title(2, 'Transformations')



#--------------------

def plot_mcds(MCDS):
    global current_idx, axes_max
    global mcds_dir_str
    fname = mcds_dir_str + "/output%08d.mat" % MCDS
    return

def mcds_dir_cb(w):
    global mcds_dir_str
    mcds_dir_str = w.value
    print(mcds_dir_str)
    
mcds_dir = widgets.Text(
    value=mcds_dir_str,
    description='Directory',
)
mcds_dir.on_submit(mcds_dir_cb)

#mcds_plot = widgets.interactive(plot_mcds, MCDS=(0, 500), continuous_update=False)
mcds_plot = widgets.interactive(plot_substrate, FileId=(0, 100), continuous_update=False)
mcds_plot.layout.width = svg_plot_size
mcds_plot.layout.height = svg_plot_size

# mcds_play = widgets.Play(
# #     interval=10,
#     value=50,
#     min=0,
#     max=100,
#     step=1,
#     description="Press play",
#     disabled=False,
# )
# #mcds_slider = widgets.IntSlider()

# widgets.jslink((mcds_play, 'value'), (mcds_slider, 'value'))
# widgets.HBox([mcds_play, mcds_slider])

mcds_field = widgets.Dropdown(
    options=['1', '2', '3','4','5','6'],
    value='1',
    description='Field',
    disabled=False,
    layout = Layout(width = constWidth),
)
def mcds_field_cb(b):
    global field_index
    field_index = int(mcds_field.value) + 3  # match actual (0-offset) field in data
#     print(gFileId)
#     plot_substrate(gFileId)  # argh, this will create a *new* plot
    
mcds_field.observe(mcds_field_cb)

field_cmap = widgets.Text(
    value='viridis',
    description='Colormap',
    layout = Layout(width = constWidth),
)
toggle_field_cmap_fixed = widgets.Checkbox(
    disabled=False,
    description='Fix',
    layout = Layout(width = constWidth2),
)
field_cmap_fixed_min = widgets.FloatText (
    description='Min',
    step=0,
    disabled=True,
    layout = Layout(width = constWidth2),
)
field_cmap_fixed_max = widgets.FloatText (
    description='Max',
    disabled=True,
    layout = Layout(width = constWidth2),
)

field_cmap_row2 = widgets.HBox([field_cmap, toggle_field_cmap_fixed])
field_cmap_row3 = widgets.HBox([field_cmap_fixed_min,field_cmap_fixed_max])
# mcds_tab = widgets.VBox([mcds_dir, mcds_plot, mcds_play], layout=tab_layout)
mcds_params = widgets.VBox([mcds_dir, mcds_field, field_cmap_row2,field_cmap_row3])
mcds_tab = widgets.HBox([mcds_params, mcds_plot], layout=tab_layout)

#----------------------
xml_editor = widgets.Textarea(
    description="",
    disabled=False,
    layout = widgets.Layout(border='1px solid black', width='900px', height='500px'), #tab_layout,  #Layout(min_width = '900px', min_height='300px'),
)
#xml_editor.value = "Mary had a lamb, yada yada...\nfleece was white yada..."
with open('nanobio_settings.xml') as xml_filep:
    xml_editor.value = xml_filep.read()
xml_filep.closed

write_xml_button = Button(
    description='Save XML config file',
    disabled=False,
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Write XML',
)

#write_xml_button.on_click(read_config_file_cb)
xml_tab = widgets.VBox([xml_editor,write_xml_button], layout=tab_layout)

#----------------------
tabs = widgets.Tab(children=[config_tab, cells_tab, np_tab, svg_tab, mcds_tab])  # xml_tab
tab_idx = 0
tabs.set_title(tab_idx, 'Config Basics'); tab_idx += 1
tabs.set_title(tab_idx, 'Cells'); tab_idx += 1
tabs.set_title(tab_idx, 'Nanoparticles'); tab_idx += 1
# tabs.set_title(tab_idx, 'XML'); tab_idx += 1
tabs.set_title(tab_idx, 'SVG'); tab_idx += 1
tabs.set_title(tab_idx, 'Substrates')

# run_sim = widgets.VBox([write_config_row, run_sim_row, run_output])
run_sim = widgets.VBox([write_config_row, run_button.w])

widgets.VBox(children=[tabs,run_sim], layout=tab_layout)


