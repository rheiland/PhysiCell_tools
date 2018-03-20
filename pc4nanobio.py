
# coding: utf-8

# In[120]:


# %load pc4nanobio.py


# In[53]:


# %load pc4nanobio.py
import ipywidgets as widgets
from ipywidgets import Layout, Button, Box
#from ipywidgets import interact, interactive
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
tab_height = '600px'
tab_height = '500px'
tab_layout = widgets.Layout(border='2px solid black', width='900px', height=tab_height)
#tab_layout.height = '500px'

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
box_layout = Layout(display='flex',
                    flex_flow='column',
                    align_items='stretch',
                    border='solid',
                    width='90%')
#z_row = Box(children=items, layout=box_layout)
#z_row = Box([toggle2D,zmin,zmax,zdelta], layout=box_layout)
#domain_range = Box([x_row,y_row,z_row], layout=box_layout)

tumor_radius = widgets.BoundedFloatText(
    value=100,
    min=1,
    max=99999,  # TODO - wth
    step=1,
    description='Tumor Radius',
    disabled=False,
    layout = Layout(width = constWidth),

)

omp_threads = widgets.BoundedIntText(
    value=8,
    min=1,
    step=1,
    description='# threads',
    disabled=False,
    layout = Layout(width = constWidth),

)

toggle_prng = widgets.Checkbox(
    value=False,
    description='Seed PRNG',
    disabled=False,
    layout = Layout(width = constWidth),
    #layout = Layout(width = '190px'),
)
prng_seed = widgets.BoundedIntText(
    min = 1,
    value = 13,
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
    value='output',
    description='Output Dir:',
)
def config_output_dir_cb(w):
    global output_dir_str
    output_dir_str = w.value
    print(output_dir_str)
    
output_dir.on_submit(config_output_dir_cb)

toggle_svg = widgets.Checkbox(
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
svg_interval = widgets.BoundedIntText(
    min=1,
    max=99999999,
    value=5,
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
    value=False,
    description='Full',
    disabled=False,
    layout = Layout(width = constWidth),
)
mcds_t0 = widgets.FloatText(
    value=0.0,
    description='$T_0$',
    disabled=True,
    layout = Layout(width = constWidth),
)
mcds_interval = widgets.BoundedIntText(
    min=0,
    max=99999999,
    value=5,
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
    
    output_dir.value = (root.find(".//folder").text)
    svg_interval.value = int(root.find(".//interval").text)
    mcds_interval.value = int(root.find(".//interval").text)
    
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
config_tab = widgets.VBox([read_config_row, toggle_2D_seed_row, x_row,y_row,z_row,  tmax, omp_threads,  
                           tumor_radius, output_dir,svg_mat_output_row], layout=tab_layout)


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

def plot_microenv(FileId):
    global current_idx, axes_max
    global svg_dir_str
    #  dir = svg_dir.value
#     print('debug> plot_microenv: idx=',FileId)
    fname = svg_dir_str + "/output00000000_microenvironment0.mat"  # % idx
    fname = svg_dir_str + "/output%08d_microenvironment0.mat" % FileId

    info_dict = {}
    scipy.io.loadmat(fname, info_dict)
    M = info_dict['multiscale_microenvironment']
    field_index = 0
    f = M[field_index,:]   # 4=tumor cells field, 5=blood vessel density, 6=growth substrate
    #plt.clf()
    #my_plot = plt.imshow(f.reshape(400,400), cmap='jet', extent=[0,20, 0,20])
    
    fig = plt.figure(figsize=(6,6))
#     fig.set_tight_layout(True)
    ax = plt.axes([0, 0.05, 0.9, 0.9 ]) #left, bottom, width, height
    cmap = plt.cm.Blues   # 'jet'
    cmap = plt.cm.YlOrBr
    im = ax.imshow(f.reshape(100,100), interpolation='nearest', cmap=cmap, extent=[0,20, 0,20])
    ax.grid(False)
    ax.set_title('Oxygen')
    cax = plt.axes([0.95, 0.05, 0.05,0.9 ])
    plt.colorbar(mappable=im, cax=cax)
    
    
#     my_plot = plt.imshow(f.reshape(100,100), cmap='jet', extent=[0,20, 0,20])
#     plt.colorbar(my_plot)
#     plt.title("Oxygen")
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
    description='Directory:',
)
#svg_dir.observe(svg_dir_cb)
svg_dir.on_submit(svg_dir_cb)

#rwh - is this where I change size of render window?? (apparently not)
svg_plot = widgets.interactive(plot_svg, SVG=(0, 100), continuous_update=False)
# output = svg_plot.children[-1]
# output.layout.height = '300px'
# output = svg_plot.children[1]
svg_plot_size = '500px'
svg_plot.layout.width = svg_plot_size
svg_plot.layout.height = svg_plot_size
#svg_plot

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
    description='Name:',
)
max_birth_rate = widgets.BoundedFloatText (
    min=0,
    value=0.0072,
    description='max birth rate',
    disabled=False,
    layout = Layout(width = constWidth),
)

o2_prolif_sat = widgets.BoundedFloatText (
    min=0,
    value=38,
    description='$O_2$: prolif sat',
    disabled=False,
    layout = Layout(width = constWidth),
)
o2_prolif_thresh = widgets.BoundedFloatText (
    min=0,
    value=5,
    description='prolif thresh',
    disabled=False,
    layout = Layout(width = constWidth),
)

glucose_prolif_ref = widgets.BoundedFloatText (
    min=0,
    value=1,
    description='$G$: prolif ref',
    disabled=False,
    layout = Layout(width = constWidth),
)
glucose_prolif_sat = widgets.BoundedFloatText (
    min=0,
    value=1,
    description='prolif sat',
    disabled=False,
    layout = Layout(width = constWidth),
)
glucose_prolif_thresh = widgets.BoundedFloatText (
    min=0,
    value=0,
    description='prolif thresh',
    disabled=False,
    layout = Layout(width = constWidth),
)

cells_row1 = widgets.HBox([cell_name, max_birth_rate])
cells_row2 = widgets.HBox([o2_prolif_sat, o2_prolif_thresh])
cells_row3 = widgets.HBox([glucose_prolif_ref, glucose_prolif_sat, glucose_prolif_thresh])
cells_tab = widgets.VBox([cells_row1, cells_row2, cells_row3], layout=tab_layout)


#=========
np_half_conc = widgets.BoundedFloatText (
    min=0,
    value=1,
    description='$T_{0.5}$',
    disabled=False,
    tooltip='this is a tooltip',
    layout = Layout(width = constWidth),
)
np_mean_survival_time = widgets.BoundedFloatText (
    min=0,
    value=0,
    description='mean surv time',
    disabled=False,
    layout = Layout(width = constWidth),
)
np_diff_coef = widgets.BoundedFloatText (
    min=0,
    value=0,
    description='diffusion coef',
    disabled=False,
    layout = Layout(width = constWidth),
)
np_ratio = widgets.BoundedFloatText (
    min=0,
    value=0,
    description='R',
    disabled=False,
    layout = Layout(width = constWidth),
)
nparticles_tab = widgets.VBox([np_half_conc, np_mean_survival_time, np_diff_coef, np_ratio], layout=tab_layout)

#-------------------
pkpd_tab = widgets.Text(
    value='.',
    description='dummy:',
    layout=tab_layout,
)

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
    description='Directory:',
)
mcds_dir.on_submit(mcds_dir_cb)

#mcds_plot = widgets.interactive(plot_mcds, MCDS=(0, 500), continuous_update=False)
mcds_plot = widgets.interactive(plot_microenv, FileId=(0, 10), continuous_update=False)
# mcds_output = mcds_plot.children[-1]
mcds_plot.layout.width = svg_plot_size
mcds_output.layout.height = svg_plot_size
#mcds_plot

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

# mcds_tab = widgets.VBox([mcds_dir, mcds_plot, mcds_play], layout=tab_layout)
mcds_tab = widgets.HBox([mcds_dir, mcds_plot], layout=tab_layout)

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
tabs = widgets.Tab(children=[config_tab, cells_tab, nparticles_tab, pkpd_tab, xml_tab, svg_tab, mcds_tab])
tab_idx = 0
tabs.set_title(tab_idx, 'Config Basics'); tab_idx += 1
tabs.set_title(tab_idx, 'Cells'); tab_idx += 1
tabs.set_title(tab_idx, 'Nanoparticles'); tab_idx += 1   # nanoparticles, r'\(\eta)'
tabs.set_title(tab_idx, 'PK/PD'); tab_idx += 1
tabs.set_title(tab_idx, 'XML'); tab_idx += 1
tabs.set_title(tab_idx, 'SVG output'); tab_idx += 1
tabs.set_title(tab_idx, 'Full output')

# run_sim = widgets.VBox([write_config_row, run_sim_row, run_output])
run_sim = widgets.VBox([write_config_row, run_button.w])

widgets.VBox(children=[tabs,run_sim])




# In[5]:


pwd


# In[8]:


type(svg_plot)


# In[17]:


len(svg_plot.children)


# In[33]:


svg_plot.children[1].layout = Layout(width='500px',height='900px')


# In[30]:


svg_plot.children[0].layout = Layout(height='130px')


# In[94]:


dir(svg_plot)


# In[68]:


type(runCommand)

