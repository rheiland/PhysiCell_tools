# substrates  Tab

import os
from ipywidgets import Layout, Text, Checkbox, HBox, VBox, FloatText, Dropdown, interactive
import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import scipy.io


class SubstrateTab(object):

    def __init__(self):
        
        # initial value
        self.field_index = 4
        # self.field_index = self.mcds_field.value + 4

        tab_height = '500px'
        constWidth = '180px'
        constWidth2 = '150px'
        tab_layout = Layout(width='800px',   # border='2px solid black',
                            height=tab_height, overflow_y='scroll')

        self.mcds_plot = interactive(self.plot_substrate, fid=(0, 200), continuous_update=False)  
        svg_plot_size = '500px'
        self.mcds_plot.layout.width = svg_plot_size
        self.mcds_plot.layout.height = svg_plot_size

        self.mcds_field = Dropdown(
            options={'oxygen': 0, 'glucose': 1, 'H+ ions': 2, 'ECM': 3, 'NP1': 4, 'NP2': 5},
            value=0,
            #     description='Field',
            layout=Layout(width=constWidth)
        )
        self.mcds_field.observe(self.mcds_field_cb)

        self.field_cmap = Text(
            value='viridis',
            description='Colormap',
            layout=Layout(width=constWidth),
        )
        self.field_cmap.observe(self.plot_substrate)

        toggle_field_cmap_fixed = Checkbox(
            description='Fix',
            layout=Layout(width=constWidth2),
        )
        field_cmap_fixed_min = FloatText(
            description='Min',
            step=0,
            disabled=True,
            layout=Layout(width=constWidth2),
        )
        field_cmap_fixed_max = FloatText(
            description='Max',
            disabled=True,
            layout=Layout(width=constWidth2),
        )

        field_cmap_row2 = HBox([self.field_cmap, toggle_field_cmap_fixed])
        field_cmap_row3 = HBox([field_cmap_fixed_min, field_cmap_fixed_max])
        # mcds_tab = widgets.VBox([mcds_dir, mcds_plot, mcds_play], layout=tab_layout)
        mcds_params = VBox([self.mcds_field, field_cmap_row2, field_cmap_row3])  # mcds_dir
        self.tab = HBox([mcds_params, self.mcds_plot], layout=tab_layout)


    def mcds_field_cb(self, b):
        #self.field_index = self.mcds_field.value
#        self.field_index = self.mcds_field.options.index(self.mcds_field.value) + 4
#        self.field_index = self.mcds_field.options[self.mcds_field.value]
        self.field_index = self.mcds_field.value + 4
#        print('field_index=',self.field_index)
        self.mcds_plot.update()

    def plot_substrate(self, fid):
        # global current_idx, axes_max, gFileId, field_index
        fname = "output%08d_microenvironment0.mat" % fid
        # fullname = output_dir_str + fname
        fullname = fname
        if not os.path.isfile(fullname):
            return

        info_dict = {}
        scipy.io.loadmat(fullname, info_dict)
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

        grid2D = M[0, :].reshape(100,100)
        xvec = grid2D[0, :]
        num_contours = 30
        my_plot = plt.contourf(xvec, xvec, M[self.field_index, :].reshape(100,100), num_contours, cmap=self.field_cmap.value)
        plt.colorbar(my_plot)
        axes_min = 0
        axes_max = 2000
        plt.xlim(axes_min, axes_max)
        plt.ylim(axes_min, axes_max)


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
