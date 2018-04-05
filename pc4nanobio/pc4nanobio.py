import ipywidgets as widgets
from hublib.ui import RunCommand
import xml.etree.ElementTree as ET
import os
import glob
from config import ConfigTab
from cells import CellsTab
from nano import NanoTab
from svg import SVGTab
from substrates import SubTab

join_our_list = "(Join/ask questions at https://groups.google.com/forum/#!forum/physicell-users)\n"

constWidth = '180px'

tab_height = '500px'

tab_layout = widgets.Layout(width='800px',   # border='2px solid black',
                            height=tab_height, overflow_y='scroll',)

# create the tabs, but don't display yet
ctab = ConfigTab()
cells = CellsTab()
ntab = NanoTab()
svg = SVGTab()
sub = SubTab()


def read_config_file_cb(_b):
    print("read_config_file")
    dirname = os.path.expanduser('~/.local/share/pc4nanobio')
    config_file = os.path.join(dirname, read_config_file.value)
    fill_gui_params(config_file)

def write_config_file_cb(b):
    print('writing config', b)

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
        

    #    user_details = ET.SubElement(root, "user_details")
    #    ET.SubElement(user_details, "PhysiCell_settings", name="version").text = "devel-version"
    #    ET.SubElement(user_details, "domain")
    #    ET.SubElement(user_details, "xmin").text = "-100"

    #    tree = ET.ElementTree(root)
    #    tree.write(write_config_file.value)
    #    tree.write("test.xml")

    # TODO: verify can write to this filename
    tree.write(write_config_file.value)


def get_config_files():
    dirname = os.path.expanduser('~/.local/share/pc4nanobio')
    try:
        os.makedirs(dirname)
    except:
        pass
    return list(map(os.path.basename, glob.glob("%s/*.xml" % dirname)))

    
def default_config_file_cb(b):
#    print('WD=',os.getcwd())
    fill_gui_params('./config/nanobio_settings.xml')  # NOTE: hard-coded for now


def fill_gui_params(config_file):
    # FIXME:  this will need modified to use new classes
    # for example, 'xmin' is created in config.py.  Make it a class
    # variable by putting "self." before the name.  Below, it
    # will be referenced by the class instance "ctab.xmin"
    #
    # The best approach would be to add fill_gui() methods to each class
    # then the code below would be something like
    # tree = ET.parse(config_file)
    # root = tree.getroot()
    # ctab.fill_gui(root)
    # cells.fill_gui(root)
    # ...
    
    tree = ET.parse(config_file)
    root = tree.getroot()

    ctab.fill_gui(root)
#    ctab.xmin.value = float(root.find(".//x_min").text)
    
#    xmin.value = float(root.find(".//x_min").text)
#    ctab.xmax.value = float(root.find(".//x_max").text)

    
    cdp = root.find(".//cell_definition")
    #     e2 = e1.find('.//')
    cell0_max_birth_rate.children[0].value = float(cdp.find(".//max_birth_rate").text)
    cell0_o2_prolif_sat.children[0].value = float(cdp.find(".//o2_proliferation_saturation").text)
    cell0_o2_prolif_thresh.children[0].value = float(cdp.find(".//o2_proliferation_threshold").text)
    cell0_o2_ref.children[0].value = float(cdp.find(".//o2_reference").text)
    
    cell0_glucose_prolif_ref.children[0].value = float(root.find(".//glucose_proliferation_reference").text)
    cell0_glucose_prolif_sat.children[0].value = float(root.find(".//glucose_proliferation_saturation").text)
    cell0_glucose_prolif_thresh.children[0].value = float(root.find(".//glucose_proliferation_threshold").text)
    
    cell0_max_necrosis_rate.children[0].value = float(root.find(".//max_necrosis_rate").text)
    cell0_o2_necrosis_thresh.children[0].value = float(root.find(".//o2_necrosis_threshold").text)
    cell0_o2_necrosis_max.children[0].value = float(root.find(".//o2_necrosis_max").text)
    
    cell0_apoptosis_rate.children[0].value = float(cdp.find(".//apoptosis_rate").text)
    
    cell0_metab_aero.children[0].value = float(cdp.find(".//relative_aerobic_effects").text)
    cell0_metab_glyco.children[0].value = float(cdp.find(".//relative_glycolytic_effects").text)
    
    cell0_toggle_motile.value = bool(cdp.find(".//is_motile").text)
    cell0_motile_bias.value = float(cdp.find(".//bias").text)

    return


# This is used now for the RunCommand
def run_sim_func(s):
    s.run("bin/pc-nb data/nanobio_settings.xml")  # TODO: choose: nanoHUB vs local
    # s.run("/Users/heiland/dev/run-nanobio/pc-nb nanobio_settings.xml")
   
        
run_button = RunCommand(start_func=run_sim_func)  # optionally: , done_func=read_data

default_config_button = widgets.Button(
    description='Use defaults', style={'description_width': 'initial'},
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
)
read_config_file = widgets.Text(
    value='my_nanobio_settings.xml',
    description='',
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
tabs = widgets.Tab(children=[ctab.tab, cells.tab, ntab.tab, svg.tab, sub.tab], layout=tab_layout)  
tab_idx = 0
tabs.set_title(tab_idx, 'Config Basics'); tab_idx += 1
tabs.set_title(tab_idx, 'Cells'); tab_idx += 1
tabs.set_title(tab_idx, 'Nanoparticles'); tab_idx += 1
# tabs.set_title(tab_idx, 'XML'); tab_idx += 1
tabs.set_title(tab_idx, 'out:SVG'); tab_idx += 1
tabs.set_title(tab_idx, 'out:Substrates')

read_config_row = widgets.HBox([read_config_button, read_config, default_config_button])
gui = widgets.VBox(children=[read_config_row, tabs, write_config_row, run_button.w])
