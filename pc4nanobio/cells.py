# Cells Tab

from ipywidgets import Layout, Label, Text, Checkbox, Button, HBox, VBox,      FloatText, BoundedIntText, BoundedFloatText, HTMLMath, Dropdown 
 
class CellsTab(object): 
 
    def __init__(self): 
        constWidth = '180px'
        width_cell_params_units = '240px'
        
        cell_name = Text(
            value='untreated cancer',
            description='Cell line name', style={'description_width': 'initial'},
        )

        #-------------------------------
        label_cycle = Label('Cycle:')
        self.max_birth_rate = HBox([BoundedFloatText(min=0, step=0.1,
           description='max birth rate', style={'description_width': 'initial'}, layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units))
        self.o2_proliferation_saturation = HBox([BoundedFloatText(min=0, step=0.1,
           description='o2: prolif sat', layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units))
        self.o2_proliferation_threshold = HBox([BoundedFloatText(min=0, step=0.1,
           description='prolif thresh', layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units))
        self.o2_reference = HBox([BoundedFloatText(min=0, step=0.1,
           description='ref', layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units))
        self.glucose_proliferation_reference = HBox([BoundedFloatText(min=0, step=0.1,
           description='Glc: prolif ref', layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units))
        self.glucose_proliferation_saturation = HBox([BoundedFloatText(min=0, step=0.1,
           description='prolif sat', layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units))
        self.glucose_proliferation_threshold = HBox([BoundedFloatText(min=0, step=0.1,
           description='prolif thresh', layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units))
        
        #-------------------------------
        label_necrosis = Label('Necrosis:')
        self.max_necrosis_rate = HBox([BoundedFloatText(min=0, step=0.1,
           description='max rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units))
        self.o2_necrosis_threshold = HBox([BoundedFloatText(min=0, step=0.1,
           description='o2: thresh', layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units))
        self.o2_necrosis_max = HBox([BoundedFloatText(min=0, step=0.1,
           description='max', layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units))
        
        #-------------------------------
        label_apoptosis = Label('Apoptosis:')
        self.apoptosis_rate = HBox([BoundedFloatText(min=0, step=0.1,
           description='rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units))

        #-------------------------------
        # TODO: enforce sum=1
        label_metabolism = Label('Metabolism (must sum to 1):')
        # TODO: assert these next 2 values sum to 1.0
        self.metab_aero = HBox([BoundedFloatText(min=0,max=1,step=0.1,
            description='Aerobic',  #style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), ], layout=Layout(width=width_cell_params_units))
        self.metab_glyco = HBox([BoundedFloatText(min=0,max=1,step=0.1,
            description='Glycolytic',  #style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), ], layout=Layout(width=width_cell_params_units))
        
        metabolism_stuff = VBox([label_metabolism, HBox([self.metab_aero,self.metab_glyco])])

        #-------------------------------
        label_motility = Label('Motility:')
        self.toggle_motile = Checkbox(
            description='Motile',
            layout=Layout(width=constWidth),
        )
        self.motile_bias = HBox([BoundedFloatText(max=1, step=0.1,
            description='bias', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), ], layout=Layout(width=width_cell_params_units))
#        speed_units = HTMLMath(value=r"$\frac{\mu M^2}{min}$")
        speed_units = Label('µm/min')   # use "option m" (Mac, for micro symbol)
        self.speed = HBox([BoundedFloatText(min=0, step=0.1,
           description='speed', layout=Layout(width=constWidth), ), speed_units], 
           layout=Layout(width=width_cell_params_units))
        self.persistence_time = HBox([BoundedFloatText(min=0, step=0.1,
           description='persistence time', layout=Layout(width=constWidth), ), Label('min')], 
           layout=Layout(width=width_cell_params_units))
        
        def toggle_motile_cb(b):
            if (self.toggle_motile.value):
                self.motile_bias.disabled = False
                self.speed.children[0].disabled = False
                self.persistence_time.children[0].disabled = False
            else:
                self.motile_bias.disabled = True
                self.speed.children[0].disabled = True
                self.persistence_time.children[0].disabled = True
            
        self.toggle_motile.observe(toggle_motile_cb)
        
#         motility_stuff = VBox([label_motility, HBox([self.toggle_motile, self.motile_bias, self.speed, self.persistence_time])])
        motility_stuff = VBox([HBox([label_motility,self.toggle_motile]), HBox([ self.motile_bias, self.speed, self.persistence_time])])

        #-------------------------------
        label_mechanics = Label('Mechanics:')
        self.max_relative_adhesion_distance = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Max adhesion distance', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), ], layout=Layout(width=width_cell_params_units))
        self.adhesion_strength = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Adhesion strength', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), ], layout=Layout(width=width_cell_params_units))
        self.repulsion_strength = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Repulsion strength', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), ], layout=Layout(width=width_cell_params_units))
        
        #-------------------------------
        label_hypoxia = Label('Hypoxia:')
        self.o2_hypoxic_threshold = HBox([BoundedFloatText(min=0, step=0.1,
           description='o2: threshold', layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units))
        self.o2_hypoxic_response = HBox([BoundedFloatText(min=0, step=0.1,
           description='response', layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units))
        self.o2_hypoxic_saturation = HBox([BoundedFloatText(min=0, step=0.1,
           description='saturation', layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units))
        
        #-------------------------------
        label_secretion = Label('Secretion:')
        self.uptake_rate = []
        self.secretion_rate = []
        self.saturation_density = []

        self.uptake_rate.append(  HBox([BoundedFloatText(min=0, step=0.1,
           description='o2: uptake rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units)) )
        self.uptake_rate.append(  HBox([BoundedFloatText(min=0, step=0.1,
           description='Glc: uptake rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units)) )
        self.uptake_rate.append(  HBox([BoundedFloatText(min=0, step=0.1,
           description='H+: uptake rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units)) )
        self.uptake_rate.append(  HBox([BoundedFloatText(min=0, step=0.1,
           description='ECM: uptake rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units)) )
        self.uptake_rate.append(  HBox([BoundedFloatText(min=0, step=0.1,
           description='NP1: uptake rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units)) )
        self.uptake_rate.append(  HBox([BoundedFloatText(min=0, step=0.1,
           description='NP2: uptake rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units)) )


        for idx in range(6):
            self.secretion_rate.append( HBox([BoundedFloatText(min=0, step=0.1,
               description='secretion rate', layout=Layout(width=constWidth), ), Label('1/min')], 
               layout=Layout(width=width_cell_params_units)) )
            self.saturation_density.append(  HBox([BoundedFloatText(min=0, step=0.1,
               description='saturation', layout=Layout(width=constWidth), ), ], 
               layout=Layout(width=width_cell_params_units)) )


        row1 = HBox([self.max_birth_rate ])
        row2 = HBox([self.o2_proliferation_saturation, self.o2_proliferation_threshold, self.o2_reference])
        row2b = HBox([self.glucose_proliferation_reference, self.glucose_proliferation_saturation, self.glucose_proliferation_threshold ])
        row3 = HBox([self.max_necrosis_rate ])
        row4 = HBox([self.o2_necrosis_threshold, self.o2_necrosis_max ])
        row5 = HBox([self.apoptosis_rate ])

        row8 = HBox([self.o2_hypoxic_threshold, self.o2_hypoxic_response, self.o2_hypoxic_saturation ])

        row_secretion = []
        for idx in range(2):
          row_secretion.append( HBox([self.uptake_rate[idx], self.secretion_rate[idx], self.saturation_density[idx] ]) )

        # row12 = HBox([self.uptake_rate[1], self.secretion_rate[1], self.saturation_density[1] ])
        # row13 = HBox([self.uptake_rate3, self.secretion_rate3, self.saturation_density3 ])
        # row14 = HBox([self.uptake_rate4, self.secretion_rate4, self.saturation_density4 ])
        # row15 = HBox([self.uptake_rate5, self.secretion_rate5, self.saturation_density5 ])
        # row16 = HBox([self.uptake_rate6, self.secretion_rate6, self.saturation_density6 ])
        
        self.tab = VBox([cell_name, label_cycle,row1,row2,row2b, label_necrosis,row3,row4,                          label_apoptosis,row5,                          metabolism_stuff,                          motility_stuff,                          label_mechanics, HBox([self.max_relative_adhesion_distance,self.adhesion_strength,self.repulsion_strength]),
                         label_hypoxia,row8, \
                         label_secretion,
                         HBox([self.uptake_rate[0], self.secretion_rate[0], self.saturation_density[0] ]),
                         HBox([self.uptake_rate[1], self.secretion_rate[1], self.saturation_density[1] ]),
                         HBox([self.uptake_rate[2], self.secretion_rate[2], self.saturation_density[2] ]),
                         HBox([self.uptake_rate[3], self.secretion_rate[3], self.saturation_density[3] ]),
                         HBox([self.uptake_rate[4], self.secretion_rate[4], self.saturation_density[4] ]),
                         HBox([self.uptake_rate[5], self.secretion_rate[5], self.saturation_density[5] ]),
                         ])  #,row13,row14,row15,row16])
        
        
    def fill_gui(self, xml_root):

        uep = xml_root.find('.//cell_definition')  # find unique entry point into XML 

        self.max_birth_rate.children[0].value = float(uep.find('.//max_birth_rate').text)
        self.o2_proliferation_saturation.children[0].value = float(uep.find('.//o2_proliferation_saturation').text)
        self.o2_proliferation_threshold.children[0].value = float(uep.find('.//o2_proliferation_threshold').text)  
        self.o2_reference.children[0].value = float(uep.find('.//o2_reference').text)
        self.glucose_proliferation_reference.children[0].value = float(uep.find('.//glucose_proliferation_reference').text)
        self.glucose_proliferation_saturation.children[0].value = float(uep.find('.//glucose_proliferation_saturation').text)
        self.glucose_proliferation_threshold.children[0].value = float(uep.find('.//glucose_proliferation_threshold').text)
        self.max_necrosis_rate.children[0].value = float(uep.find('.//max_necrosis_rate').text)
        self.o2_necrosis_threshold.children[0].value = float(uep.find('.//o2_necrosis_threshold').text)
        self.o2_necrosis_max.children[0].value = float(uep.find('.//o2_necrosis_max').text)
        self.apoptosis_rate.children[0].value = float(uep.find('.//apoptosis_rate').text)
        self.speed.children[0].value = float(uep.find('.//speed').text)
        self.persistence_time.children[0].value = float(uep.find('.//persistence_time').text)
        self.o2_hypoxic_threshold.children[0].value = float(uep.find('.//o2_hypoxic_threshold').text)
        self.o2_hypoxic_response.children[0].value = float(uep.find('.//o2_hypoxic_response').text)
        self.o2_hypoxic_saturation.children[0].value = float(uep.find('.//o2_hypoxic_saturation').text)

        # wow, this actually works :-)
        sep = uep.find('.//secretion')  # secretion entry point
        idx = 0
        for el in sep.findall('substrate'):  # currently 6 substrates - find all of them
            kids = el.getchildren()  # assume 3, which follow:
            self.uptake_rate[idx].children[0].value = float(kids[0].text)
            self.secretion_rate[idx].children[0].value = float(kids[1].text)
            self.saturation_density[idx].children[0].value = float(kids[2].text)
            idx += 1
#            if idx == 2:
#                break

