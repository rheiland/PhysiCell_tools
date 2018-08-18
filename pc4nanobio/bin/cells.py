# Cells Tab

from ipywidgets import Layout, Label, Text, Checkbox, Button, RadioButtons, Box, HBox, VBox, \
  FloatText, BoundedIntText, BoundedFloatText, HTMLMath, Dropdown 
 
class CellsTab(object): 
 
    def __init__(self): 
        constWidth = '180px'
        #width_cell_params_units = '240px'
        width_cell_params_units = '270px'
        
        self.cell_name = Text(
            value='untreated cancer',
            disabled = False,
            description='Cell line name', style={'description_width': 'initial'},
        )

        #-------------------------------
        label_cycle = Label('Cycle:')
        self.max_birth_rate = HBox([BoundedFloatText(min=0, step=0.0001,
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
        self.max_necrosis_rate = HBox([BoundedFloatText(min=0, step=0.001,
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
        self.apoptosis_rate = HBox([BoundedFloatText(min=0, step=0.00001,
           description='rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units))

        #-------------------------------
        # TODO: enforce sum=1
        label_metabolism = Label('Metabolism (must sum to 1):')
        # TODO: assert these next 2 values sum to 1.0
        self.relative_aerobic_effects = HBox([BoundedFloatText(min=0,max=1,step=0.1, disabled=True,
            description='Aerobic',  #style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), ], layout=Layout(width=width_cell_params_units))
        self.relative_glycolytic_effects = HBox([BoundedFloatText(min=0,max=1,step=0.1, disabled=True,
            description='Glycolytic',  #style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), ], layout=Layout(width=width_cell_params_units))
        

        #-------------------------------
        label_motility = Label('Motility:')
        self.is_motile = Checkbox(
            description='motile', disabled=False,
            layout=Layout(width=constWidth),
        )
        self.bias = HBox([BoundedFloatText(max=1, step=0.01,
            description='bias', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), ], layout=Layout(width=width_cell_params_units))
#        speed_units = HTMLMath(value=r"$\frac{\mu M^2}{min}$")
        speed_units = Label('micron/min')   # use "option m" (Mac, for micro symbol)
        self.speed = HBox([BoundedFloatText(min=0, step=0.1,
           description='speed', layout=Layout(width=constWidth), ), speed_units], 
           layout=Layout(width=width_cell_params_units))
        self.persistence_time = HBox([BoundedFloatText(min=0, step=0.1,
           description='persistence time', layout=Layout(width=constWidth), ), Label('min')], 
           layout=Layout(width=width_cell_params_units))

        # constWidt = '180px'
        self.gradient_substrate_index = BoundedIntText(
            min=0,  value=0, disabled = False, 
            description='substrate index', style={'description_width': 'initial'},
            layout=Layout(width='160px'),
            )
        self.negative_taxis = RadioButtons(
            options={"grad" : 0, "-grad" : 1},   # {u"\u2207" : 0, "-" +  u"\u2207" : 1},
            value=0,
            disabled=True,
            description='',
        )
        
            
        self.is_motile.observe(self.is_motile_cb)
        

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
        self.uptake_rate.append(  HBox([BoundedFloatText(min=0, step=0.01,
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


        row_secretion = []
        for idx in range(2):
          row_secretion.append( HBox([self.uptake_rate[idx], self.secretion_rate[idx], self.saturation_density[idx] ]) )

        # row12 = HBox([self.uptake_rate[1], self.secretion_rate[1], self.saturation_density[1] ])
        # row13 = HBox([self.uptake_rate3, self.secretion_rate3, self.saturation_density3 ])
        # row14 = HBox([self.uptake_rate4, self.secretion_rate4, self.saturation_density4 ])
        # row15 = HBox([self.uptake_rate5, self.secretion_rate5, self.saturation_density5 ])
        # row16 = HBox([self.uptake_rate6, self.secretion_rate6, self.saturation_density6 ])
        
        box_layout = Layout(border='1px solid')
        cycle_box = VBox([label_cycle,row1,row2,row2b], layout=box_layout)
        necrosis_box = VBox([label_necrosis,row3,row4], layout=box_layout)
        apoptosis_box = VBox([label_apoptosis,HBox([self.apoptosis_rate ])], layout=box_layout)
        metabolism_box = VBox([label_metabolism,HBox([self.relative_aerobic_effects,self.relative_glycolytic_effects])], layout=box_layout)
        motility_box = VBox([ HBox([label_motility, self.is_motile, self.gradient_substrate_index, self.negative_taxis,]),
            HBox([ self.bias, self.speed, self.persistence_time]), ], layout=box_layout)
        mechanics_box = VBox([label_mechanics, 
          HBox([self.max_relative_adhesion_distance,self.adhesion_strength,self.repulsion_strength]) ], layout=box_layout)
        hypoxia_box = VBox([label_hypoxia, 
          HBox([self.o2_hypoxic_threshold, self.o2_hypoxic_response, self.o2_hypoxic_saturation ]) ], layout=box_layout)
        secretion_box = VBox([label_secretion,
          HBox([self.uptake_rate[0], self.secretion_rate[0], self.saturation_density[0] ]),
          HBox([self.uptake_rate[1], self.secretion_rate[1], self.saturation_density[1] ]),
          HBox([self.uptake_rate[2], self.secretion_rate[2], self.saturation_density[2] ]),
          HBox([self.uptake_rate[3], self.secretion_rate[3], self.saturation_density[3] ]),
          HBox([self.uptake_rate[4], self.secretion_rate[4], self.saturation_density[4] ]),
          HBox([self.uptake_rate[5], self.secretion_rate[5], self.saturation_density[5] ]) ],
          layout=box_layout)

        self.tab = VBox([self.cell_name, cycle_box, necrosis_box, apoptosis_box,
          metabolism_box, motility_box, mechanics_box, hypoxia_box,
          secretion_box,
          ])  #,row13,row14,row15,row16])
        
    def is_motile_cb(self, b):
        if (self.is_motile.value):
            self.bias.children[0].disabled = False
            self.speed.children[0].disabled = False
            self.persistence_time.children[0].disabled = False
            self.negative_taxis.disabled = False
        else:
            self.bias.children[0].disabled = True
            self.speed.children[0].disabled = True
            self.persistence_time.children[0].disabled = True
            self.negative_taxis.disabled = True
        
    def fill_gui(self, xml_root):

        uep = xml_root.find('.//cell_definition')  # find unique entry point into XML 

        self.cell_name.value = uep.attrib['name']
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

        # metabolism
        self.relative_aerobic_effects.children[0].value = float(uep.find('.//relative_aerobic_effects').text)
        self.relative_glycolytic_effects.children[0].value = float(uep.find('.//relative_glycolytic_effects').text)

        # motility
        self.is_motile.value = False
        if ( (uep.find('.//is_motile').text).lower()  == 'true'):
          self.is_motile.value = True
        self.is_motile_cb(None)
        self.gradient_substrate_index.value = int(uep.find('.//gradient_substrate_index').text)
        self.bias.children[0].value = float(uep.find('.//bias').text)
#        self.negative_taxis.value = bool(uep.find('.//negative_taxis').text)
        self.negative_taxis.value = 0
        if ( (uep.find('.//negative_taxis').text).lower() == "true"):
          self.negative_taxis.value = 1
        self.speed.children[0].value = float(uep.find('.//speed').text)
        self.persistence_time.children[0].value = float(uep.find('.//persistence_time').text)

        # mechanics
        self.max_relative_adhesion_distance.children[0].value = float(uep.find('.//max_relative_adhesion_distance').text)
        self.adhesion_strength.children[0].value = float(uep.find('.//adhesion_strength').text)
        self.repulsion_strength.children[0].value = float(uep.find('.//repulsion_strength').text)

        # hypoxia
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

    # Read values from the GUI widgets and generate/write a new XML
    def fill_xml(self, xml_root):
        # TODO: verify template .xml file exists!
        # tree = ET.parse('nanobio_settings.xml')
#        tree = ET.parse('nanobio_settings2.xml')
#        root = tree.getroot()

        uep = xml_root.find('.//cell_definition')  # find unique entry point into XML 

        uep.attrib['name'] = self.cell_name.value 
        # TODO: verify valid type (numeric) and range?
        uep.find(".//max_birth_rate").text = str(self.max_birth_rate.children[0].value)
        uep.find('.//o2_proliferation_saturation').text = str(self.o2_proliferation_saturation.children[0].value)
        uep.find('.//o2_proliferation_threshold').text = str(self.o2_proliferation_threshold.children[0].value)
        uep.find('.//o2_reference').text = str(self.o2_reference.children[0].value)
        uep.find('.//glucose_proliferation_reference').text = str(self.glucose_proliferation_reference.children[0].value)
        uep.find('.//glucose_proliferation_saturation').text = str(self.glucose_proliferation_saturation.children[0].value)
        uep.find('.//glucose_proliferation_threshold').text = str(self.glucose_proliferation_threshold.children[0].value)
        uep.find('.//max_necrosis_rate').text = str(self.max_necrosis_rate.children[0].value)
        uep.find('.//o2_necrosis_threshold').text = str(self.o2_necrosis_threshold.children[0].value)
        uep.find('.//o2_necrosis_max').text = str(self.o2_necrosis_max.children[0].value)
        uep.find('.//apoptosis_rate').text = str(self.apoptosis_rate.children[0].value)

        # motility
        uep.find('.//is_motile').text = "false"
        if (self.is_motile.value):
          uep.find('.//is_motile').text = "true"
        uep.find('.//gradient_substrate_index').text = str(self.gradient_substrate_index.value)
        uep.find('.//bias').text = str(self.bias.children[0].value)
        # uep.find('.//negative_taxis').text = bool(self.negative_taxis.value)
        uep.find('.//negative_taxis').text = 'false'
        if (self.negative_taxis.value > 0):
            uep.find('.//negative_taxis').text = 'true'
        uep.find('.//speed').text = str(self.speed.children[0].value)
        uep.find('.//persistence_time').text = str(self.persistence_time.children[0].value)

        # mechanics
        uep.find('.//max_relative_adhesion_distance').text = str(self.max_relative_adhesion_distance.children[0].value)
        uep.find('.//adhesion_strength').text = str(self.adhesion_strength.children[0].value)
        uep.find('.//repulsion_strength').text = str(self.repulsion_strength.children[0].value)

        # hypoxia
        uep.find('.//o2_hypoxic_threshold').text = str(self.o2_hypoxic_threshold.children[0].value)
        uep.find('.//o2_hypoxic_response').text = str(self.o2_hypoxic_response.children[0].value)
        uep.find('.//o2_hypoxic_saturation').text = str(self.o2_hypoxic_saturation.children[0].value)

        sep = uep.find('.//secretion')  # secretion entry point
        idx = 0
        for el in sep.findall('substrate'):  # currently 6 substrates - find all of them
            kids = el.getchildren()  # assume 3, which follow:
            kids[0].text = str(self.uptake_rate[idx].children[0].value)
            kids[1].text = str(self.secretion_rate[idx].children[0].value)
            kids[2].text = str(self.saturation_density[idx].children[0].value)
            idx += 1

