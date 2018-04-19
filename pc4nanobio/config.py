# Config Tab

import os
from ipywidgets import Layout, Label, Text, Checkbox, Button, HBox, VBox, \
    FloatText, BoundedIntText, BoundedFloatText, HTMLMath, Dropdown

class ConfigTab(object):

    def __init__(self):
        
#        micron_units = HTMLMath(value=r"$\mu M$")
        micron_units = Label('µm')   # use "option m" (Mac, for micro symbol)

        constWidth = '180px'
        # tab_height = '400px'
        tab_height = '500px'
        tab_layout = Layout(width='800px',   # border='2px solid black',
                            height=tab_height, overflow_y='scroll',)
        np_tab_layout = Layout(width='800px',  # border='2px solid black',
                               height='350px', overflow_y='scroll',)

        # my_domain = [0,0,-10, 2000,2000,10, 20,20,20]  # [x,y,zmin,  x,y,zmax, x,y,zdelta]
#        label_domain = Label('Domain ($\mu M$):')
        label_domain = Label('Domain (µm):')
        self.xmin = FloatText(
            # description='$X_{min}$',
            description='Xmin',
            layout=Layout(width=constWidth),
        )
        self.ymin = FloatText(
            description='Ymin',
            layout=Layout(width=constWidth),
        )
        self.zmin = FloatText(
            description='Zmin',
            layout=Layout(width=constWidth),
        )
        self.xmax = FloatText(
            description='Xmax',
            layout=Layout(width=constWidth),
        )
        self.ymax = FloatText(
            description='Ymax',
            layout=Layout(width=constWidth),
        )
        self.zmax = FloatText(
            description='Zmax',
            layout=Layout(width=constWidth),
        )
#            description='$Time_{max}$',
        self.tmax = BoundedFloatText(
            min=0.,
            max=100000000,
            description='Time',
            layout=Layout(width=constWidth),
        )
        self.xdelta = BoundedFloatText(
            min=1.,
            description='Xdelta',
            layout=Layout(width=constWidth),
        )
        self.ydelta = BoundedFloatText(
            min=1.,
            description='Ydelta',
            layout=Layout(width=constWidth),
        )
        self.zdelta = BoundedFloatText(
            min=1.,
            description='Zdelta',
            layout=Layout(width=constWidth),
        )
        """
        self.tdelta = BoundedFloatText(
            min=0.01,
            description='$Time_{delta}$',
            layout=Layout(width=constWidth),
        )
        """

        """
        self.toggle2D = Checkbox(
            description='2-D',
            layout=Layout(width=constWidth),
        )
        def toggle2D_cb(b):
            if (self.toggle2D.value):
                #zmin.disabled = zmax.disabled = zdelta.disabled = True
                zmin.disabled = True
                zmax.disabled = True
                zdelta.disabled = True
            else:
                zmin.disabled = False
                zmax.disabled = False
                zdelta.disabled = False
            
        self.toggle2D.observe(toggle2D_cb)
        """

        x_row = HBox([self.xmin, self.xmax, self.xdelta])
        y_row = HBox([self.ymin, self.ymax, self.ydelta])
        z_row = HBox([self.zmin, self.zmax, self.zdelta])
        self.tumor_radius = BoundedFloatText(
            min=1,
            max=99999,  # TODO - wth, defaults to 100?
            step=1,
            description='Tumor Radius', style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        )

        self.omp_threads = BoundedIntText(
            min=1,
            description='# threads',
            layout=Layout(width=constWidth),
        )

        # self.toggle_prng = Checkbox(
        #     description='Seed PRNG', style={'description_width': 'initial'},  # e.g. 'initial'  '120px'
        #     layout=Layout(width=constWidth),
        # )
        # self.prng_seed = BoundedIntText(
        #     min = 1,
        #     description='Seed', 
        #     disabled=True,
        #     layout=Layout(width=constWidth),
        # )
        # def toggle_prng_cb(b):
        #     if (toggle_prng.value):
        #         self.prng_seed.disabled = False
        #     else:
        #         self.prng_seed.disabled = True
            
        # self.toggle_prng.observe(toggle_prng_cb)
        #prng_row = HBox([toggle_prng, prng_seed])

        self.toggle_svg = Checkbox(
            description='SVG',
            layout=Layout(width='150px') )  # constWidth = '180px'
        # self.svg_t0 = BoundedFloatText (
        #     min=0,
        #     description='$T_0$',
        #     layout=Layout(width=constWidth),
        # )
        self.svg_interval = BoundedIntText(
            min=1,
            max=99999999,   # TODO: set max on all Bounded to avoid unwanted default
            description='interval',
            layout=Layout(width=constWidth),
        )
        def toggle_svg_cb(b):
            if (self.toggle_svg.value):
                # self.svg_t0.disabled = False #False
                self.svg_interval.disabled = False
            else:
                # self.svg_t0.disabled = True
                self.svg_interval.disabled = True
            
        self.toggle_svg.observe(toggle_svg_cb)


        self.toggle_mcds = Checkbox(
        #     value=False,
            description='Full',
            layout=Layout(width='150px'),
        )
        # self.mcds_t0 = FloatText(
        #     description='$T_0$',
        #     disabled=True,
        #     layout=Layout(width=constWidth),
        # )
        self.mcds_interval = BoundedIntText(
            min=0,
            max=99999999,
            description='interval',
#            disabled=True,
            layout=Layout(width=constWidth),
        )
        def toggle_mcds_cb(b):
            if (self.toggle_mcds.value):
                # self.mcds_t0.disabled = False #False
                self.mcds_interval.disabled = False
            else:
                # self.mcds_t0.disabled = True
                self.mcds_interval.disabled = True
            
        self.toggle_mcds.observe(toggle_mcds_cb)
       
        #svg_output_row = HBox([toggle_svg, svg_t0, svg_interval])
        #mat_output_row = HBox([toggle_mcds, mcds_t0, mcds_interval])
        svg_mat_output_row = HBox([self.toggle_svg, self.svg_interval, self.toggle_mcds, self.mcds_interval])
        #write_config_row = HBox([write_config_button, write_config_file])
        #run_sim_row = HBox([run_button, run_command_str, kill_button])
        # run_sim_row = HBox([run_button, run_command_str])
        # run_sim_row = HBox([run_button.w])  # need ".w" for the custom RunCommand widget

        label_blankline = Label('')
        tumor_radius2 = HBox([self.tumor_radius, micron_units])
        # toggle_2D_seed_row = HBox([toggle_prng, prng_seed])  # toggle2D

        label_substrate = Label('Substrate:')
        self.substrate = []
        self.diffusion_coef = []
        self.decay_rate = []

        width_cell_params_units = '250px'
        disable_substrates_flag = True
            
        self.substrate.append(  HBox([BoundedFloatText(min=0, step=0.1,
           description='o2: ', disabled=disable_substrates_flag, layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units)) )
        self.substrate.append(  HBox([BoundedFloatText(min=0, step=0.1,
           description='Glc: ', disabled=disable_substrates_flag, layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units)) )
        self.substrate.append(  HBox([BoundedFloatText(min=0, step=0.1,
           description='H+: ', disabled=disable_substrates_flag, layout=Layout(width=constWidth), ), Label('pH')], 
           layout=Layout(width=width_cell_params_units)) )
        self.substrate.append(  HBox([BoundedFloatText(min=0, step=0.1,
           description='ECM: ', disabled=disable_substrates_flag, layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units)) )
        # self.substrate.append(  HBox([BoundedFloatText(min=0, step=0.1,
        #    description='NP1: ', layout=Layout(width=constWidth), ), ], 
        #    layout=Layout(width=width_cell_params_units)) )
        # self.substrate.append(  HBox([BoundedFloatText(min=0, step=0.1,
        #    description='NP2: ', layout=Layout(width=constWidth), ), ], 
        #    layout=Layout(width=width_cell_params_units)) )

        for idx in range(4):
            self.diffusion_coef.append( HBox([BoundedFloatText(min=0, step=0.1,
               description='diffusion coef', disabled=disable_substrates_flag, layout=Layout(width=constWidth), ), Label('µm^2/min')], 
               layout=Layout(width=width_cell_params_units)) )
            self.decay_rate.append(  HBox([BoundedFloatText(min=0, step=0.1,
               description='decay rate', disabled=disable_substrates_flag, layout=Layout(width=constWidth), ), Label('1/min')], 
               layout=Layout(width=width_cell_params_units)) )


        self.tab = VBox([label_domain,x_row,y_row,z_row,  
#                         label_blankline, 
                         HBox([self.tmax, Label('min')]), self.omp_threads,  
                         tumor_radius2, svg_mat_output_row,
                         label_substrate,
                         HBox([self.substrate[0], self.diffusion_coef[0], self.decay_rate[0] ]),
                         HBox([self.substrate[1], self.diffusion_coef[1], self.decay_rate[1] ]),
                         HBox([self.substrate[2], self.diffusion_coef[2], self.decay_rate[2] ]),
                         HBox([self.substrate[3], self.diffusion_coef[3], self.decay_rate[3] ]),
                         ], layout=tab_layout)  # output_dir, toggle_2D_seed_

    # Populate the GUI widgets with values from the XML
    def fill_gui(self, xml_root):
        self.xmin.value = float(xml_root.find(".//x_min").text)
        self.xmax.value = float(xml_root.find(".//x_max").text)
        self.xdelta.value = float(xml_root.find(".//dx").text)
    
        self.ymin.value = float(xml_root.find(".//y_min").text)
        self.ymax.value = float(xml_root.find(".//y_max").text)
        self.ydelta.value = float(xml_root.find(".//dy").text)
    
        self.zmin.value = float(xml_root.find(".//z_min").text)
        self.zmax.value = float(xml_root.find(".//z_max").text)
        self.zdelta.value = float(xml_root.find(".//dz").text)
        
        self.tmax.value = float(xml_root.find(".//max_time").text)
        
        self.tumor_radius.value = float(xml_root.find(".//radius").text)
        self.omp_threads.value = int(xml_root.find(".//omp_num_threads").text)
        
        self.toggle_svg.value = bool(xml_root.find(".//SVG").find(".//enable").text)
        self.svg_interval.value = int(xml_root.find(".//SVG").find(".//interval").text)
        self.toggle_mcds.value = bool(xml_root.find(".//full_data").find(".//enable").text)
        self.mcds_interval.value = int(xml_root.find(".//full_data").find(".//interval").text)

        for el in xml_root.findall('physical_parameter_set'):  # currently 6 substrates - find all of them
            kids = el.getchildren()  # assume 3, which follow:
            self.substrate[idx].children[0].value = float(kids[0].text)
            self.diffusion_coef[idx].children[0].value = float(kids[1].text)
            self.decay_rate[idx].children[0].value = float(kids[2].text)
            idx += 1


    # Read values from the GUI widgets and generate/write a new XML
    def gui2xml(self, xml_root):
        # TODO: verify template .xml file exists!
        # tree = ET.parse('nanobio_settings.xml')
#        tree = ET.parse('nanobio_settings2.xml')
#        root = tree.getroot()

        # TODO: verify valid type (numeric) and range?
        xml_root.find(".//x_min").text = str(self.xmin.value)
        xml_root.find(".//x_max").text = str(self.xmax.value)
        xml_root.find(".//dx").text = str(self.xdelta.value)
        xml_root.find(".//y_min").text = str(self.ymin.value)
        xml_root.find(".//y_max").text = str(self.ymax.value)
        xml_root.find(".//dy").text = str(self.ydelta.value)
        xml_root.find(".//z_min").text = str(self.zmin.value)
        xml_root.find(".//z_max").text = str(self.zmax.value)
        xml_root.find(".//dz").text = str(self.zdelta.value)

        xml_root.find(".//max_time").text = str(self.tmax.value)

        xml_root.find(".//omp_num_threads").text = str(self.omp_threads.value)
        xml_root.find(".//radius").text = str(self.tumor_radius.value)

        xml_root.find(".//SVG").find(".//enable").text = str(self.toggle_svg.value)
        xml_root.find(".//SVG").find(".//interval").text = str(self.svg_interval.value)
        xml_root.find(".//full_data").find(".//enable").text = str(self.toggle_mcds.value)
        xml_root.find(".//full_data").find(".//interval").text = str(self.mcds_interval.value)


        #    user_details = ET.SubElement(root, "user_details")
        #    ET.SubElement(user_details, "PhysiCell_settings", name="version").text = "devel-version"
        #    ET.SubElement(user_details, "domain")
        #    ET.SubElement(user_details, "xmin").text = "-100"

        #    tree = ET.ElementTree(root)
        #    tree.write(write_config_file.value)
        #    tree.write("test.xml")

        # TODO: verify can write to this filename
#        tree.write(write_config_file.value)

