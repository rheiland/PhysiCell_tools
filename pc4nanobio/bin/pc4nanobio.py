# Rf  https://www.python.org/dev/peps/pep-0008/
import ipywidgets as widgets
from hublib.ui import RunCommand
import xml.etree.ElementTree as ET  # https://docs.python.org/2/library/xml.etree.elementtree.html
import os
import glob
import shutil
from pathlib import Path
from config import ConfigTab
from cells import CellsTab
from nano import NanoTab
from svg import SVGTab
from mydata import DataTab
from substrates import SubstrateTab

#join_our_list = "(Join/ask questions at https://groups.google.com/forum/#!forum/physicell-users)\n"

constWidth = '180px'

tab_height = '500px'

tab_layout = widgets.Layout(width='800px',   # border='2px solid black',
                            height=tab_height, overflow_y='scroll',)

# create the tabs, but don't display yet
config_tab = ConfigTab()
cells = CellsTab()

tree = ET.parse('data/nanobio_settings.xml')  # this file cannot be overwritten; part of tool distro
xml_root = tree.getroot()
nanopart = NanoTab(xml_root)
svg = SVGTab()
sub = SubstrateTab()
mydata = DataTab()


def read_config_file_cb(_b):
    print("read_config_file")
    dirname = os.path.expanduser('~/.local/share/pc4nanobio')
    config_file = os.path.join(dirname, read_config_file.value)
    fill_gui_params(config_file)

def write_config_file_cb(b):
#    print('writing config', b)

    # Read in the default xml config file, just to get a valid 'root' to populate a new one
    tree = ET.parse('data/nanobio_settings.xml')  # this file cannot be overwritten; part of tool distro
    xml_root = tree.getroot()

    config_tab.fill_xml(xml_root)
    cells.fill_xml(xml_root)
    nanopart.fill_xml(xml_root)

    # TODO?: verify can write to this filename
    tree.write("data/" + write_config_file.value)
    return


def get_config_files():
    dirname = os.path.expanduser('~/.local/share/pc4nanobio')
    try:
        os.makedirs(dirname)
    except:
        pass
    return list(map(os.path.basename, glob.glob("%s/*.xml" % dirname)))

    
def default_config_file_cb(b):
#    print('WD=',os.getcwd())
#    fill_gui_params('./config/nanobio_settings.xml')  # NOTE: hard-coded for now
    fill_gui_params('./data/nanobio_settings.xml')  # NOTE: hard-coded for now


def fill_gui_params(config_file):
#    global xml_root
    
    tree = ET.parse(config_file)
    xml_root = tree.getroot()

    config_tab.fill_gui(xml_root)
    cells.fill_gui(xml_root)
    nanopart.fill_gui(xml_root)

    return


# This is used now for the RunCommand
def run_sim_func(s):
#    s.run("bin/pc-nb data/nanobio_settings.xml")  # TODO: choose: nanoHUB vs local
    new_config_file = "data/" + write_config_file.value
    if not Path(new_config_file).is_file():
      shutil.copyfile("data/nanobio_settings.xml", new_config_file)
    s.run("bin/pc-nb " + new_config_file)  
    # s.run("/Users/heiland/dev/run-nanobio/pc-nb nanobio_settings.xml")
   
        
run_button = RunCommand(start_func=run_sim_func)  # optionally: , done_func=read_data

default_config_button = widgets.Button(
    description='Reset defaults', style={'description_width': 'initial'},
    button_style='info',  # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Populate the GUI with default parameters',
)
default_config_button.on_click(default_config_file_cb)

read_config = widgets.Dropdown(
    options = get_config_files(),
    tooltip='Config File',
)
read_config_button = widgets.Button(
    description='Read config file', style={'description_width': 'initial'},
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Populate the GUI with info in your configuration file (in ~/local/share/pc4nanobio)',
    disabled=True,
)
read_config_file = widgets.Text(
    value='my_nanobio_settings.xml',
    description='',
    disabled=True,
)
read_config_button.on_click(read_config_file_cb) 
read_config_row = widgets.HBox([default_config_button, read_config_button, read_config_file])

write_config_button = widgets.Button(
    description='Write config file',
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Generate XML',
)
write_config_button.on_click(write_config_file_cb)

write_config_file = widgets.Text(
    value='my_nanobio_settings.xml',
    description='',
)
write_config_row = widgets.HBox([write_config_button, write_config_file])


#----------------------
#tabs = widgets.Tab(children=[config_tab.tab, cells.tab, nanopart.tab, svg.tab, sub.tab, mydata.tab], layout=tab_layout)  
tabs = widgets.Tab(children=[config_tab.tab, cells.tab, nanopart.tab, svg.tab, sub.tab,], layout=tab_layout)  
tab_idx = 0
tabs.set_title(tab_idx, 'Config Basics'); tab_idx += 1
tabs.set_title(tab_idx, 'Cell Properties'); tab_idx += 1
tabs.set_title(tab_idx, 'Nanoparticles'); tab_idx += 1
# tabs.set_title(tab_idx, 'XML'); tab_idx += 1
tabs.set_title(tab_idx, 'Cell Plots'); tab_idx += 1
tabs.set_title(tab_idx, 'Substrate Plots'); tab_idx += 1
#tabs.set_title(tab_idx, 'Data'); 

read_config_row = widgets.HBox([read_config_button, read_config, default_config_button])

# tab_file = open("bin/tab_helper.png", "rb")
# image = tab_file.read()
# tab_helper = widgets.Image(
#     value=image,
#     format='png',
#     width=595,
#     height=55,
# )

#gui = widgets.VBox(children=[read_config_row, tab_helper, tabs, write_config_row, run_button.w])
gui = widgets.VBox(children=[read_config_row, tabs, write_config_row, run_button.w])
default_config_file_cb(None)

