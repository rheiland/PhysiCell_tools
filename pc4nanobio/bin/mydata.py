# Config Tab

import os
from ipywidgets import Layout, Label, Button, HBox, VBox

class DataTab(object):

    def __init__(self):
        
        constWidth = '180px'
        # tab_height = '400px'
        tab_height = '500px'
        tab_layout = Layout(width='800px',   # border='2px solid black',
                            height=tab_height, overflow_y='scroll',)
        data_tab_layout = Layout(width='800px',  # border='2px solid black',
                               height='350px', overflow_y='scroll',)

        download_button = Button(
            description='Download data', style={'description_width': 'initial'},
            button_style='info', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Download all output data',
            disabled=True,
        )
#        download_button.on_click(self.download_cb) 

        self.tab = VBox([download_button, Label('coming...')], layout=tab_layout)  

    def download_cb(self, _b):
        print("downloading data (not really)")
#        dirname = os.path.expanduser('~/.local/share/pc4nanobio')
#        config_file = os.path.join(dirname, read_config_file.value)
#        fill_gui_params(config_file)