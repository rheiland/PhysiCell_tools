# substrates  Tab

import os, math
from ipywidgets import Layout, Text, Checkbox, Button, BoundedIntText, HBox, VBox, Box, FloatText, Dropdown, interactive
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.colors as mplc
import scipy.io
import xml.etree.ElementTree as ET  # https://docs.python.org/2/library/xml.etree.elementtree.html


class SubstrateTab(object):

    def __init__(self):
        
        self.output_dir = '.'

        # initial value
        self.field_index = 4
        # self.field_index = self.mcds_field.value + 4

        tab_height = '500px'
        constWidth = '180px'
        constWidth2 = '150px'
        tab_layout = Layout(width='900px',   # border='2px solid black',
                            height=tab_height, ) #overflow_y='scroll')

        max_frames = 253   # first time + 30240 / 120
        self.mcds_plot = interactive(self.plot_substrate, frame=(0, max_frames), continuous_update=False)  
        svg_plot_size = '700px'
        self.mcds_plot.layout.width = svg_plot_size
        self.mcds_plot.layout.height = svg_plot_size

        self.max_frames = BoundedIntText(
            min=0, max=99999, value=max_frames,
            description='Max frames',
            layout=Layout(width='160px'),
        )
        self.max_frames.observe(self.update_max_frames)

        self.field_min_max = {'oxygen': [0., 38.], 'glucose': [0.8, 1.], 'H+ ions': [0., 1.], 
                                'ECM': [0., 1.], 'NP1': [0., 1.], 'NP2': [0., 0.1]}
        # hacky I know, but make a dict that's got (key,value) reversed from the dict in the Dropdown below
        self.field_dict = {0:'oxygen', 1:'glucose', 2:'H+ ions', 3:'ECM', 4:'NP1', 5:'NP2'}
        self.mcds_field = Dropdown(
            options={'oxygen': 0, 'glucose': 1, 'H+ ions': 2, 'ECM': 3, 'NP1': 4, 'NP2': 5},
            value=0,
            #     description='Field',
            layout=Layout(width=constWidth)
        )
#        self.mcds_field.observe(self.mcds_field_cb)
        self.mcds_field.observe(self.mcds_field_changed_cb)

        # self.field_cmap = Text(
        #     value='viridis',
        #     description='Colormap',
        #     disabled=True,
        #     layout=Layout(width=constWidth),
        # )
        self.field_cmap = Dropdown(
            options=['viridis', 'jet', 'YlOrRd'],
            value='viridis',
            #     description='Field',
            layout=Layout(width=constWidth)
        )
        #self.field_cmap.observe(self.plot_substrate)
#        self.field_cmap.observe(self.plot_substrate)
        self.field_cmap.observe(self.mcds_field_cb)

        self.cmap_fixed = Checkbox(
            description='Fix',
            disabled=False,
            layout=Layout(width=constWidth2),
        )

        self.save_min_max= Button(
            description='Save', #style={'description_width': 'initial'},
            button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Save min/max for this substrate',
            disabled=True,
            layout=Layout(width='90px')
        )

        def save_min_max_cb(b):
#            field_name = self.mcds_field.options[]
#            field_name = next(key for key, value in self.mcds_field.options.items() if value == self.mcds_field.value)
            field_name = self.field_dict[self.mcds_field.value]
#            print(field_name)
#            self.field_min_max = {'oxygen': [0., 30.], 'glucose': [0., 1.], 'H+ ions': [0., 1.], 'ECM': [0., 1.], 'NP1': [0., 1.], 'NP2': [0., 1.]}
            self.field_min_max[field_name][0] = self.cmap_min.value
            self.field_min_max[field_name][1] = self.cmap_max.value
#            print(self.field_min_max)

        self.save_min_max.on_click(save_min_max_cb)

        self.cmap_min = FloatText(
            description='Min',
            value=0,
            step = 0.1,
            disabled=True,
            #layout=Layout(width=constWidth2),
        )
        self.cmap_min.observe(self.mcds_field_cb)

        self.cmap_max = FloatText(
            description='Max',
            value=38,
            step = 0.1,
            disabled=True,
            #layout=Layout(width=constWidth2),
        )
        self.cmap_max.observe(self.mcds_field_cb)

        def cmap_fixed_cb(b):
            if (self.cmap_fixed.value):
                self.cmap_min.disabled = False
                self.cmap_max.disabled = False
                self.save_min_max.disabled = False
            else:
                self.cmap_min.disabled = True
                self.cmap_max.disabled = True
                self.save_min_max.disabled = True
#            self.mcds_field_cb()

        self.cmap_fixed.observe(cmap_fixed_cb)

        field_cmap_row2 = HBox([self.field_cmap, self.cmap_fixed])

#        field_cmap_row3 = HBox([self.save_min_max, self.cmap_min, self.cmap_max])
        items_auto = [
            self.save_min_max, #layout=Layout(flex='3 1 auto', width='auto'),
            self.cmap_min, 
            self.cmap_max,  
         ]
        box_layout = Layout(display='flex',
                    flex_flow='row',
                    align_items='stretch',
                    width='80%')
        field_cmap_row3 = Box(children=items_auto, layout=box_layout)

#        field_cmap_row3 = Box([self.save_min_max, self.cmap_min, self.cmap_max])

        # mcds_tab = widgets.VBox([mcds_dir, mcds_plot, mcds_play], layout=tab_layout)
        mcds_params = VBox([self.mcds_field, field_cmap_row2, field_cmap_row3, self.max_frames])  # mcds_dir
#        mcds_params = VBox([self.mcds_field, field_cmap_row2, field_cmap_row3,])  # mcds_dir

        self.tab = HBox([mcds_params, self.mcds_plot], layout=tab_layout)
#        self.tab = HBox([mcds_params, self.mcds_plot])

    def update_max_frames(self,_b):
        self.mcds_plot.children[0].max = self.max_frames.value

    def mcds_field_changed_cb(self, b):
        self.field_index = self.mcds_field.value + 4

        field_name = self.field_dict[self.mcds_field.value]
#        print('mcds_field_cb: '+field_name)
        self.cmap_min.value = self.field_min_max[field_name][0]
        self.cmap_max.value = self.field_min_max[field_name][1]
        self.mcds_plot.update()

    def mcds_field_cb(self, b):
        #self.field_index = self.mcds_field.value
#        self.field_index = self.mcds_field.options.index(self.mcds_field.value) + 4
#        self.field_index = self.mcds_field.options[self.mcds_field.value]
        self.field_index = self.mcds_field.value + 4

        # field_name = self.mcds_field.options[self.mcds_field.value]
        # self.cmap_min.value = self.field_min_max[field_name][0]  # oxygen, etc
        # self.cmap_max.value = self.field_min_max[field_name][1]  # oxygen, etc

#        self.field_index = self.mcds_field.value + 4

#        print('field_index=',self.field_index)
        self.mcds_plot.update()

    def plot_substrate(self, frame):
        # global current_idx, axes_max, gFileId, field_index
        fname = "output%08d_microenvironment0.mat" % frame
        xml_fname = "output%08d.xml" % frame
        # fullname = output_dir_str + fname

#        fullname = fname
        full_fname = os.path.join(self.output_dir, fname)
        full_xml_fname = os.path.join(self.output_dir, xml_fname)
#        self.output_dir = '.'

#        if not os.path.isfile(fullname):
        if not os.path.isfile(full_fname):
#            print("File does not exist: ", full_fname)
            print("No: ", full_fname)
            return

#        tree = ET.parse(xml_fname)
        tree = ET.parse(full_xml_fname)
        xml_root = tree.getroot()
        mins= round(int(float(xml_root.find(".//current_time").text)))  # TODO: check units = mins
        hrs = mins/60.
        days = hrs/24.
        title_str = '%dd, %dh, %dm' % (int(days),(hrs%24), mins - (hrs*60))


        info_dict = {}
#        scipy.io.loadmat(fullname, info_dict)
        scipy.io.loadmat(full_fname, info_dict)
        M = info_dict['multiscale_microenvironment']
        #     global_field_index = int(mcds_field.value)
        #     print('plot_substrate: field_index =',field_index)
        f = M[self.field_index, :]   # 4=tumor cells field, 5=blood vessel density, 6=growth substrate
        # plt.clf()
        # my_plot = plt.imshow(f.reshape(400,400), cmap='jet', extent=[0,20, 0,20])
    
        fig = plt.figure(figsize=(7.2,6))  # this strange figsize results in a ~square contour plot
        #     fig.set_tight_layout(True)
        #     ax = plt.axes([0, 0.05, 0.9, 0.9 ]) #left, bottom, width, height
        #     ax = plt.axes([0, 0.0, 1, 1 ])
        #     cmap = plt.cm.viridis # Blues, YlOrBr, ...
        #     im = ax.imshow(f.reshape(100,100), interpolation='nearest', cmap=cmap, extent=[0,20, 0,20])
        #     ax.grid(False)

        N = int(math.sqrt(len(M[0,:])))
        grid2D = M[0, :].reshape(N,N)
        xvec = grid2D[0, :]

        num_contours = 15
#        levels = MaxNLocator(nbins=10).tick_values(vmin, vmax)
        levels = MaxNLocator(nbins=num_contours).tick_values(self.cmap_min.value, self.cmap_max.value)
        if (self.cmap_fixed.value):
            my_plot = plt.contourf(xvec, xvec, M[self.field_index, :].reshape(N,N), levels=levels, extend='both', cmap=self.field_cmap.value)
        else:    
#        my_plot = plt.contourf(xvec, xvec, M[self.field_index, :].reshape(N,N), num_contours, cmap=self.field_cmap.value)
            my_plot = plt.contourf(xvec, xvec, M[self.field_index, :].reshape(N,N), num_contours, cmap=self.field_cmap.value)

        plt.title(title_str)
        plt.colorbar(my_plot)
        axes_min = 0
        axes_max = 2000
        # plt.xlim(axes_min, axes_max)
        # plt.ylim(axes_min, axes_max)


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

