# nanoparticles Tab

from ipywidgets import Layout, Label, Text, Checkbox, RadioButtons, HBox, VBox, \
    BoundedFloatText,BoundedIntText, HTMLMath, Dropdown, Tab


class NanoParticle(object):

    def __init__(self, border_color, xml_uep):  # uep = unique entry point
#        self.xml_root = None  # for debugging

        self.xml_uep = xml_uep

        tab_height = '500px'
        width_cell_params_units = '270px'

        np_tab_layout = Layout(width='800px',  # border='2px solid black',
                               height='350px', overflow_y='scroll')
        tab_layout = Layout(width='800px',   # border='2px solid black',
                            height=tab_height, overflow_y='scroll')

        # PK
#        half_conc_desc = '$T_{0.5}$'
        desc_style = {'description_width': '150px'}  # vs. 'initial'
#        ec_50_desc = '$EC_{50}$'
        label_PK = Label('Pharmacokinetics:')
        pk_param_width = '270px'
        pd_param_width = '270px'
        constWidth = '180px'

        # box_layout=Layout(display='flex',flex_flow='column',align_items='stretch',border='1px solid black',width='30%')
        box_layout = Layout(border='1px solid ' + border_color)
        # ------------

        disabled_flag = False

        self.diffusion_coefficient = HBox([BoundedFloatText(min=0, step=0.1,
           description='diffusion coefficient', layout=Layout(width=constWidth), ), Label('micron^2/min')],
           layout=Layout(width=width_cell_params_units))   # option-m  µm
        self.survival_lifetime = HBox([BoundedFloatText(min=0, max=1.e6, step=0.1,
           description='survival lifetime', layout=Layout(width=constWidth), ), Label('min')],
           layout=Layout(width=width_cell_params_units))
        self.ECM_binding_rate = HBox([BoundedFloatText(min=0, step=0.1,
           description='ECM binding rate', layout=Layout(width=constWidth), ), Label('1/min')],
           layout=Layout(width=width_cell_params_units))
        self.ECM_unbinding_rate = HBox([BoundedFloatText(min=0, step=0.1,
           description='ECM unbinding rate', layout=Layout(width=constWidth), ), Label('1/min')],
           layout=Layout(width=width_cell_params_units))
        self.ECM_saturation_concentration = HBox([BoundedFloatText(min=0, step=0.1,
           description='ECM saturation concentration', layout=Layout(width=constWidth), ), ],
           layout=Layout(width=width_cell_params_units))

        pk_widgets_width = '350px'


        self.PK_params = VBox([label_PK, 
            self.diffusion_coefficient, 
            self.survival_lifetime, 
#            self.ECM_binding_rate, 
#            self.ECM_unbinding_rate, 
#            self.ECM_saturation_concentration, 
        ], layout=box_layout)

        # --------------------------------------------
        label_PD = Label('Pharmacodynamics:')

        self.effect_model_choice = Dropdown(
            # options=['1', '2', '3','4','5','6'],
            options={'Simple (conc)' : 0, 'Intermed (AUC)' : 1, 'Details (act/deact)' : 2},
            value=0,
            disabled = True,
            # description='Field',
            layout=Layout(width=constWidth)
        )
        self.EC_50 = HBox([BoundedFloatText(min=0, step=0.1,
            description='EC_50', layout=Layout(width=constWidth), ), ], 
            layout=Layout(width=width_cell_params_units))
        self.Hill_power = HBox([BoundedIntText(min=0, step=0.1,
            description='Hill power', layout=Layout(width=constWidth), ), ], 
            layout=Layout(width=width_cell_params_units))
        self.mechanistic_response_rate = HBox([BoundedFloatText(min=0, step=0.1,
           description='mech resp rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units))
        self.mechanistic_deactivation_rate = HBox([BoundedFloatText(min=0, step=0.1,
           description='mech deact rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units))

        #-------------------------------
        self.enable_active_influx = Checkbox(
            description='Active Influx',
            layout=Layout(width=constWidth),
        )
        self.enable_active_influx.observe(self.enable_active_influx_cb)

        self.relative_max_internal_concentration = HBox([BoundedFloatText(min=0, step=0.1,
           description='rel max int conc', layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units))
        self.internalization_rate = HBox([BoundedFloatText(min=0, step=0.1,
           description='intern rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units))
        self.reference_external_concentration = HBox([BoundedFloatText(min=0, step=0.1,
           description='ref ext conc', layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units))

        #-------------------------------
#        label_cycle = Label('Cycle:')
        self.cycle_response = Checkbox(
            description='Cycle', disabled=False,
            layout=Layout(width=constWidth),
        )
        self.cycle_response.observe(self.cycle_response_cb)

        self.max_birth_rate = HBox([BoundedFloatText(min=0, step=0.0001, disabled=disabled_flag,
           description='max birth rate', style={'description_width': 'initial'}, layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units))
        self.o2_proliferation_saturation = HBox([BoundedFloatText(min=0, step=0.1, disabled=disabled_flag,
           description='o2: prolif sat', layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units))
        self.o2_proliferation_threshold = HBox([BoundedFloatText(min=0, step=0.1, disabled=disabled_flag,
           description='prolif thresh', layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units))
        self.o2_reference = HBox([BoundedFloatText(min=0, step=0.1, disabled=disabled_flag,
           description='ref', layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units))
        self.glucose_proliferation_reference = HBox([BoundedFloatText(min=0, step=0.1, disabled=disabled_flag,
           description='Glc: prolif ref', layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units))
        self.glucose_proliferation_saturation = HBox([BoundedFloatText(min=0, step=0.1, disabled=disabled_flag,
           description='prolif sat', layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units))
        self.glucose_proliferation_threshold = HBox([BoundedFloatText(min=0, step=0.1, disabled=disabled_flag,
           description='prolif thresh', layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units))
        
        #-------------------------------
        self.necrosis_response= Label('Necrosis:')
        # self.necrosis_response= Checkbox(
        #     description='Necrosis',disabled=disabled_flag,
        #     layout=Layout(width=constWidth),   # ='180px'
        # )
        # self.necrosis_response.observe(self.necrosis_response_cb)

        self.max_necrosis_rate = HBox([BoundedFloatText(min=0, step=0.001, disabled=disabled_flag,
           description='max rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units))
        self.o2_necrosis_threshold = HBox([BoundedFloatText(min=0, step=0.1,disabled=disabled_flag,
           description='o2: thresh', layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units))
        self.o2_necrosis_max = HBox([BoundedFloatText(min=0, step=0.1,disabled=disabled_flag,
           description='max', layout=Layout(width=constWidth), ), Label('mmHg')], 
           layout=Layout(width=width_cell_params_units))
        
        #-------------------------------
        self.apoptosis_response = Checkbox(
            description='Apoptosis',disabled=disabled_flag,
            layout=Layout(width=constWidth),
        )
        self.apoptosis_response.observe(self.apoptosis_response_cb)

        self.apoptosis_rate = HBox([BoundedFloatText(min=0, step=0.001, disabled=disabled_flag,
           description='rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units))

        #-------------------------------
        # TODO: enforce sum=1
#        label_metabolism = Label('Metabolism (must sum to 1):')
        self.metabolism_response = Checkbox(
            description='Metabolism', disabled=True,
            layout=Layout(width=constWidth),
        )
        self.metabolism_response.observe(self.metabolism_response_cb)

        # TODO: assert these next 2 values sum to 1.0
        self.metab_aero = HBox([BoundedFloatText(min=0,max=1,step=0.1,
            description='Aerobic', disabled=True, #style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), ], layout=Layout(width=width_cell_params_units))
        self.metab_glyco = HBox([BoundedFloatText(min=0,max=1,step=0.1,
            description='Glycolytic', disabled=True, #style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), ], layout=Layout(width=width_cell_params_units))
        
#        metabolism_stuff = VBox([label_metabolism, HBox([self.metab_aero,self.metab_glyco])])

        #-------------------------------
#        label_motility = Label('Motility:')
        self.motility_response = Checkbox(
            description='Motility', disabled=True, 
            layout=Layout(width='200px'),
        )
        self.motility_response.observe(self.motility_response_cb)

        self.is_motile = Checkbox(
            description='motile', disabled=True, 
            layout=Layout(width='200px'),
        )
        self.is_motile.observe(self.is_motile_cb)

        self.bias = HBox([BoundedFloatText(max=1, step=0.01,
            description='bias', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), ], layout=Layout(width=width_cell_params_units))

#        speed_units = HTMLMath(value=r"$\frac{\mu M^2}{min}$")
        speed_units = Label('micron/min')   # use "option m" µ (Mac, for micro symbol)
        self.speed = HBox([BoundedFloatText(min=0, step=0.1,
           description='speed', layout=Layout(width=constWidth), ), speed_units], 
           layout=Layout(width='290px'))  # width_cell_params_units = '270px'
        self.persistence_time = HBox([BoundedFloatText(min=0, step=0.1,
           description='persistence time', layout=Layout(width=constWidth), ), Label('min')], 
           layout=Layout(width=width_cell_params_units))

#        taxis_gradient = u"\u2207"
        self.gradient_substrate_index = BoundedIntText(
            min=0, 
            description='substrate index',  style={'description_width': 'initial'},
            layout=Layout(width='200px'),
            )
        self.negative_taxis = RadioButtons(
#            options={u"\u2207" : 0, "-" +  u"\u2207" : 1},
            options={"grad" : 0, "-grad" : 1},   # {u"\u2207" : 0, "-" +  u"\u2207" : 1},
            value=0,
            description='',
            disabled=False
        )
        
        #-------------------------------
        self.mechanics_response = Checkbox(
            description='Mechanics',disabled=disabled_flag,
            layout=Layout(width=constWidth),
        )
        self.mechanics_response.observe(self.mechanics_response_cb)

        self.max_relative_adhesion_distance = HBox([BoundedFloatText(
            min=0, step=0.1, disabled=disabled_flag,
            description='Max adhesion distance', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), ], layout=Layout(width=width_cell_params_units))
        self.adhesion_strength = HBox([BoundedFloatText(
            min=0, step=0.1, disabled=disabled_flag,
            description='Adhesion strength', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), ], layout=Layout(width=width_cell_params_units))
        self.repulsion_strength = HBox([BoundedFloatText(
            min=0, step=0.1, disabled=disabled_flag,
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
        self.secretion_response = Checkbox(
            description='Secretion', disabled=disabled_flag,
            layout=Layout(width=constWidth),
        )
        self.secretion_response.observe(self.secretion_response_cb)

        self.uptake_rate = []
        self.secretion_rate = []
        self.saturation_density = []

        self.uptake_rate.append(  HBox([BoundedFloatText(min=0, step=0.1, disabled=disabled_flag,
           description='o2: uptake rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units)) )
        self.uptake_rate.append(  HBox([BoundedFloatText(min=0, step=0.001,disabled=disabled_flag,
           description='Glc: uptake rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units)) )
        self.uptake_rate.append(  HBox([BoundedFloatText(min=0, step=0.1,disabled=disabled_flag,
           description='H+: uptake rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units)) )
        self.uptake_rate.append(  HBox([BoundedFloatText(min=0, step=0.1,disabled=disabled_flag,
           description='ECM: uptake rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units)) )
        self.uptake_rate.append(  HBox([BoundedFloatText(min=0, step=0.1,disabled=disabled_flag,
           description='NP1: uptake rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units)) )
        self.uptake_rate.append(  HBox([BoundedFloatText(min=0, step=0.1,disabled=disabled_flag,
           description='NP2: uptake rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units)) )

        for idx in range(6):
            self.secretion_rate.append( HBox([BoundedFloatText(min=0, step=0.1,disabled=disabled_flag,
               description='secretion rate', layout=Layout(width=constWidth), ), Label('1/min')], 
               layout=Layout(width=width_cell_params_units)) )
            self.saturation_density.append(  HBox([BoundedFloatText(min=0, step=0.1,disabled=disabled_flag,
               description='saturation', layout=Layout(width=constWidth), ), ], 
               layout=Layout(width=width_cell_params_units)) )

        row_secretion = []
        for idx in range(2):
          row_secretion.append( HBox([self.uptake_rate[idx], self.secretion_rate[idx], self.saturation_density[idx] ]) )

        
        #----------------------------------------------------------
        pd_box = VBox([label_PD, self.effect_model_choice, self.EC_50, self.Hill_power,
            self.mechanistic_response_rate, self.mechanistic_deactivation_rate,], layout=box_layout)
        influx_box = VBox([self.enable_active_influx,
            self.relative_max_internal_concentration, self.internalization_rate, 
            self.reference_external_concentration,], layout=box_layout)
        cycle_box = VBox([self.cycle_response,
            self.max_birth_rate,
            HBox([self.o2_proliferation_saturation, self.o2_proliferation_threshold, self.o2_reference]),
            HBox([self.glucose_proliferation_reference, self.glucose_proliferation_saturation, self.glucose_proliferation_threshold ]),
            ], layout=box_layout)
        necrosis_box = VBox([self.necrosis_response,
            self.max_necrosis_rate, self.o2_necrosis_threshold, self.o2_necrosis_max
            ], layout=box_layout)
        apoptosis_box = VBox([self.apoptosis_response,
            HBox([self.apoptosis_rate ]), 
            ], layout=box_layout)
        metabolism_box = VBox([self.metabolism_response,
            HBox([self.metab_aero,self.metab_glyco]),
            ], layout=box_layout)
        motility_box = VBox([ HBox([self.motility_response, self.is_motile, self.gradient_substrate_index, self.negative_taxis]),
            HBox([ self.bias, self.speed, self.persistence_time]),
            ], layout=box_layout)
        mechanics_box = VBox([self.mechanics_response,
            HBox([self.max_relative_adhesion_distance,self.adhesion_strength,self.repulsion_strength]),
            ], layout=box_layout)
        hypoxia_box = VBox([label_hypoxia,
            HBox([self.o2_hypoxic_threshold, self.o2_hypoxic_response, self.o2_hypoxic_saturation ]),
            ], layout=box_layout)
        secretion_box = VBox([self.secretion_response,
            HBox([self.uptake_rate[0], self.secretion_rate[0], self.saturation_density[0] ]),
            HBox([self.uptake_rate[1], self.secretion_rate[1], self.saturation_density[1] ]),
            HBox([self.uptake_rate[2], self.secretion_rate[2], self.saturation_density[2] ]),
            HBox([self.uptake_rate[3], self.secretion_rate[3], self.saturation_density[3] ]),
            HBox([self.uptake_rate[4], self.secretion_rate[4], self.saturation_density[4] ]),
            HBox([self.uptake_rate[5], self.secretion_rate[5], self.saturation_density[5] ]) ], layout=box_layout)


        #----------- returns our tab contents at last ---------------
        self.tab = VBox([self.PK_params, 
            pd_box, influx_box, cycle_box, necrosis_box,
            apoptosis_box, metabolism_box, motility_box, mechanics_box, hypoxia_box,
            secretion_box
            ])  
        
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

    def enable_active_influx_cb(self, b):
        if (self.enable_active_influx.value):
            self.relative_max_internal_concentration.children[0].disabled = False
            self.internalization_rate.children[0].disabled = False
            self.reference_external_concentration.children[0].disabled = False
        else:
            self.relative_max_internal_concentration.children[0].disabled = True
            self.internalization_rate.children[0].disabled = True
            self.reference_external_concentration.children[0].disabled = True

    def cycle_response_cb(self, b):
        disabled_flag = True
        if (self.cycle_response.value):
            disabled_flag = False
        self.max_birth_rate.children[0].disabled = disabled_flag
        self.o2_proliferation_saturation.children[0].disabled = disabled_flag
        self.o2_proliferation_threshold.children[0].disabled = disabled_flag
        self.o2_reference.children[0].disabled = disabled_flag
        self.glucose_proliferation_reference.children[0].disabled = disabled_flag
        self.glucose_proliferation_saturation.children[0].disabled = disabled_flag
        self.glucose_proliferation_threshold.children[0].disabled = disabled_flag

    def apoptosis_response_cb(self, b):
        disabled_flag = True
        if (self.apoptosis_response.value):
            disabled_flag = False
        self.apoptosis_rate.children[0].disabled = disabled_flag

    def metabolism_response_cb(self, b):
        disabled_flag = True
        if (self.metabolism_response.value):
            disabled_flag = False

    def motility_response_cb(self, b):
        disabled_flag = True
        if (self.motility_response.value):
            disabled_flag = False
        self.is_motile.disabled = disabled_flag
        self.bias.children[0].disabled = disabled_flag
        self.gradient_substrate_index.disabled = disabled_flag
        self.negative_taxis.disabled = disabled_flag
        self.speed.children[0].disabled = disabled_flag
        self.persistence_time.children[0].disabled = disabled_flag
            
    def mechanics_response_cb(self, b):
        disabled_flag = True
        if (self.mechanics_response.value):
            disabled_flag = False
        self.max_relative_adhesion_distance.children[0].disabled = disabled_flag
        self.adhesion_strength.children[0].value = disabled_flag
        self.repulsion_strength.children[0].value = disabled_flag

    def secretion_response_cb(self, b):
        disabled_flag = True
        if (self.secretion_response.value):
            disabled_flag = False
        for idx in range(6):
            self.uptake_rate[idx].children[0].disabled = disabled_flag
            self.secretion_rate[idx].children[0].disabled = disabled_flag
            self.saturation_density[idx].children[0].disabled = disabled_flag

    #----------------------------------------
    def fill_gui(self):  # for NanoParticles - both Preform (spherical) and (rod)
#        self.xml_root = xml_root  # for debugging
#        uep = xml_root.find('.//nanoparticle')  # find unique entry point into XML 
        uep = self.xml_uep

        # PK
        self.diffusion_coefficient.children[0].value = float(uep.find('.//diffusion_coefficient').text)
        self.survival_lifetime.children[0].value = float(uep.find('.//survival_lifetime').text)

        # PD
        self.ECM_binding_rate.children[0].value = float(uep.find('.//ECM_binding_rate').text)
        self.ECM_unbinding_rate.children[0].value = float(uep.find('.//ECM_unbinding_rate').text)
        self.ECM_saturation_concentration.children[0].value = float(uep.find('.//ECM_saturation_concentration').text)
        self.EC_50.children[0].value = float(uep.find('.//EC_50').text)
        self.Hill_power.children[0].value = float(uep.find('.//Hill_power').text)
        self.mechanistic_response_rate.children[0].value = float(uep.find('.//mechanistic_response_rate').text)
        self.mechanistic_deactivation_rate.children[0].value = float(uep.find('.//mechanistic_deactivation_rate').text)

        # active influx
        self.enable_active_influx.value = False
        if ( (uep.find('.//enable_active_influx').text).lower()  == 'true'):
          self.enable_active_influx.value = True
        self.enable_active_influx_cb(None)
        self.relative_max_internal_concentration.children[0].value = float(uep.find('.//relative_max_internal_concentration').text)
        self.internalization_rate.children[0].value = float(uep.find('.//internalization_rate').text)
        self.reference_external_concentration.children[0].value = float(uep.find('.//reference_external_concentration').text)

        # cycle
        self.cycle_response.value = False
        if ( (uep.find('.//cycle').text).lower()  == 'true'):
          self.cycle_response.value = True
        self.cycle_response_cb(None)
        self.max_birth_rate.children[0].value = float(uep.find('.//max_birth_rate').text)
        self.o2_proliferation_saturation.children[0].value = float(uep.find('.//o2_proliferation_saturation').text)
        self.o2_proliferation_threshold.children[0].value = float(uep.find('.//o2_proliferation_threshold').text)  
        self.o2_reference.children[0].value = float(uep.find('.//o2_reference').text)
        self.glucose_proliferation_reference.children[0].value = float(uep.find('.//glucose_proliferation_reference').text)
        self.glucose_proliferation_saturation.children[0].value = float(uep.find('.//glucose_proliferation_saturation').text)
        self.glucose_proliferation_threshold.children[0].value = float(uep.find('.//glucose_proliferation_threshold').text)

        # necrosis
        self.max_necrosis_rate.children[0].value = float(uep.find('.//max_necrosis_rate').text)
        self.o2_necrosis_threshold.children[0].value = float(uep.find('.//o2_necrosis_threshold').text)
        self.o2_necrosis_max.children[0].value = float(uep.find('.//o2_necrosis_max').text)

        # apoptosis
        self.apoptosis_response.value = False
        if ( (uep.find('.//apoptosis').text).lower()  == 'true'):
          self.apoptosis_response.value = True
        self.apoptosis_response_cb(None)
        self.apoptosis_rate.children[0].value = float(uep.find('.//apoptosis_rate').text)

        # metabolism
        self.metabolism_response.value = False
        if ( (uep.find('.//metabolism').text).lower()  == 'true'):
          self.metabolism_response.value = True
        self.metabolism_response_cb(None)

        # motility
        self.motility_response.value = False
        if ( (uep.find('.//motility').text).lower()  == 'true'):
          self.motility_response.value = True
        self.motility_response_cb(None)

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
        self.mechanics_response.value = False
        if ( (uep.find('.//mechanics').text).lower()  == 'true'):
          self.mechanics_response.value = True
        self.mechanics_response_cb(None)
        self.max_relative_adhesion_distance.children[0].value = float(uep.find('.//max_relative_adhesion_distance').text)
        self.adhesion_strength.children[0].value = float(uep.find('.//adhesion_strength').text)
        self.repulsion_strength.children[0].value = float(uep.find('.//repulsion_strength').text)

        # hypoxia
        self.o2_hypoxic_threshold.children[0].value = float(uep.find('.//o2_hypoxic_threshold').text)
        self.o2_hypoxic_response.children[0].value = float(uep.find('.//o2_hypoxic_response').text)
        self.o2_hypoxic_saturation.children[0].value = float(uep.find('.//o2_hypoxic_saturation').text)

        # secretion
        self.secretion_response.value = False
        if ( (uep.find('.//secretion').text).lower()  == 'true'):
          self.secretion_response.value = True
        self.secretion_response_cb(None)
        sep = uep.find('.//basic_phenotype').find('.//secretion')  # secretion entry point (beware of same in previous "enabled_responses")
        idx = 0
        for el in sep.findall('substrate'):  # currently 6 substrates - find all of them
            kids = el.getchildren()  # assume 3, which follow:
            self.uptake_rate[idx].children[0].value = float(kids[0].text)
            self.secretion_rate[idx].children[0].value = float(kids[1].text)
            self.saturation_density[idx].children[0].value = float(kids[2].text)
            idx += 1
#            if idx == 2:
#                break

    def fill_xml(self, uep):  # for NanoParticles - both Preform (spherical) and (rod)
#        uep = xml_root.find('.//nanoparticle')  # find unique entry point into XML
#        uep = self.xml_uep

        # PK
        uep.find('.//diffusion_coefficient').text = str(self.diffusion_coefficient.children[0].value)
        uep.find('.//survival_lifetime').text = str(self.survival_lifetime.children[0].value)
        uep.find('.//ECM_binding_rate').text = str(self.ECM_binding_rate.children[0].value)
        uep.find('.//ECM_unbinding_rate').text = str(self.ECM_unbinding_rate.children[0].value)
        uep.find('.//ECM_saturation_concentration').text = str(self.ECM_saturation_concentration.children[0].value)

        # PD
        uep.find('.//EC_50').text = str(self.EC_50.children[0].value)
        uep.find('.//Hill_power').text = str(self.Hill_power.children[0].value)
        uep.find('.//mechanistic_response_rate').text = str(self.mechanistic_response_rate.children[0].value)
        uep.find('.//mechanistic_deactivation_rate').text = str(self.mechanistic_deactivation_rate.children[0].value)
        uep.find('.//enable_active_influx').text = "false"
        # active influx
        if (self.enable_active_influx.value):
          uep.find('.//enable_active_influx').text = "true"
        uep.find('.//relative_max_internal_concentration').text = str(self.relative_max_internal_concentration.children[0].value)
        uep.find('.//internalization_rate').text = str(self.internalization_rate.children[0].value)
        uep.find('.//reference_external_concentration').text = str(self.reference_external_concentration.children[0].value)

        # cycle
        uep.find('.//cycle').text = "false"
        if (self.cycle_response.value):
          uep.find('.//cycle').text = "true"
        uep.find('.//max_birth_rate').text = str(self.max_birth_rate.children[0].value)
        uep.find('.//o2_proliferation_saturation').text = str(self.o2_proliferation_saturation.children[0].value)
        uep.find('.//o2_proliferation_threshold').text = str(self.o2_proliferation_threshold.children[0].value)
        uep.find('.//o2_reference').text = str(self.o2_reference.children[0].value)
        uep.find('.//glucose_proliferation_reference').text = str(self.glucose_proliferation_reference.children[0].value)
        uep.find('.//glucose_proliferation_saturation').text = str(self.glucose_proliferation_saturation.children[0].value)
        uep.find('.//glucose_proliferation_threshold').text = str(self.glucose_proliferation_threshold.children[0].value)

        # necrosis
        uep.find('.//max_necrosis_rate').text = str(self.max_necrosis_rate.children[0].value)
        uep.find('.//o2_necrosis_threshold').text = str(self.o2_necrosis_threshold.children[0].value)
        uep.find('.//o2_necrosis_max').text = str(self.o2_necrosis_max.children[0].value)

        # apoptosis
        uep.find('.//apoptosis').text = "false"
        if (self.apoptosis_response.value):
          uep.find('.//apoptosis').text = "true"
        uep.find('.//apoptosis_rate').text = str(self.apoptosis_rate.children[0].value)

        # metabolism

        # motility
        uep.find('.//motility').text = "false"
        if (self.motility_response.value):
          uep.find('.//motility').text = "true"
        uep.find('.//is_motile').text = "false"
        if (self.is_motile.value):
          uep.find('.//is_motile').text = "true"
        uep.find('.//bias').text = str(self.bias.children[0].value)
        uep.find('.//negative_taxis').text = 'false'
        if (self.negative_taxis.value > 0):
            uep.find('.//negative_taxis').text = 'true'
        uep.find('.//speed').text = str(self.speed.children[0].value)
        uep.find('.//persistence_time').text = str(self.persistence_time.children[0].value)

        # mechanics
        uep.find('.//mechanics').text = "false"
        if (self.mechanics_response.value):
          uep.find('.//mechanics').text = "true"

        # hypoxia
        uep.find('.//o2_hypoxic_threshold').text = str(self.o2_hypoxic_threshold.children[0].value)
        uep.find('.//o2_hypoxic_response').text = str(self.o2_hypoxic_response.children[0].value)
        uep.find('.//o2_hypoxic_saturation').text = str(self.o2_hypoxic_saturation.children[0].value)

        # secretion
        uep.find('.//secretion').text = "false"
        if (self.secretion_response.value):
          uep.find('.//secretion').text = "true"

        sep = uep.find('.//basic_phenotype').find('.//secretion')  # secretion entry point (beware of same in previous "enabled_responses")
        idx = 0
        for el in sep.findall('substrate'):  # currently 6 substrates - find all of them
            kids = el.getchildren()  # assume 3, which follow:
            kids[0].text = str(self.uptake_rate[idx].children[0].value)
            kids[1].text = str(self.secretion_rate[idx].children[0].value)
            kids[2].text = str(self.saturation_density[idx].children[0].value)
            idx += 1


#============================
class NanoSphere(NanoParticle):

    def __init__(self, xml_root):
        uep = xml_root.find('.//nanoparticle')  # find unique entry point into XML for (1st) nanoparticle
        super().__init__('red',uep)

    def fill_xml(self, xml_root):
        uep = xml_root.find('.//nanoparticle')  # find unique entry point into XML for (1st) nanoparticle
        super().fill_xml(uep)

#============================
class NanoRod(NanoParticle):

    def __init__(self, xml_root):
        for np in xml_root.iter('nanoparticle'):  # hacky: iterate thru all (2) NPs to land on last/2nd
            uep = np
        super().__init__('black',uep)

    def fill_xml(self, xml_root):
        for np in xml_root.iter('nanoparticle'):  # hacky: iterate thru all (2) NPs to land on last/2nd
            uep = np
        super().fill_xml(uep)

#============================
class NanoTransform(object):

    def __init__(self):
        tab_height = '500px'
        width_cell_params_units = '250px'

        np_tab_layout = Layout(width='800px',  # border='2px solid black',
                               height='350px', overflow_y='scroll')
        tab_layout = Layout(width='800px',   # border='2px solid black',
                            height=tab_height, overflow_y='scroll')

        constWidth = '180px'

        self.start_NP_ID = []
        self.end_NP_ID = []
        start_end_NP_ID = []
        self.start_substrate_ID = []
        self.end_substrate_ID = []
        start_end_substrate_ID = []
        self.condition_substrate_ID = []
        self.condition1 = []
        self.rate1 = []
        self.condition2 = []
        self.rate2 = []

        label_xform1 = Label('Transform #1:')

        disabled_flag = True

        for idx in range(2):
            self.start_NP_ID.append( BoundedIntText(min=0, disabled=disabled_flag,
                description='NP ID', layout=Layout(width=constWidth), ) )
            self.end_NP_ID.append( BoundedIntText(min=0, disabled=disabled_flag,
                layout=Layout(width='90px'), ) )
            start_end_NP_ID.append( HBox([self.start_NP_ID[idx], Label('-->'),self.end_NP_ID[idx]]) )

            self.start_substrate_ID.append( BoundedIntText(min=0, disabled=disabled_flag,
                description='substrate ID', layout=Layout(width=constWidth), ) )
            self.end_substrate_ID.append( BoundedIntText(min=0, disabled=disabled_flag,
                layout=Layout(width='90px'), ) )
            start_end_substrate_ID.append( HBox([self.start_substrate_ID[idx], Label('-->'),self.end_substrate_ID[idx]]) )

            self.condition_substrate_ID.append( BoundedIntText(min=0, disabled=disabled_flag,
                description='cond substrate ID', layout=Layout(width=constWidth), ) )
            self.condition1.append( BoundedFloatText(min=0, disabled=disabled_flag,
                description='condition1', layout=Layout(width=constWidth), ) )
            self.rate1.append( HBox([BoundedFloatText(min=0, step=0.1,disabled=disabled_flag,
                description='rate1', layout=Layout(width=constWidth), ), Label('1/min')],
                layout=Layout(width=width_cell_params_units)) )

            self.condition2.append( BoundedFloatText(min=0, disabled=disabled_flag,
                description='condition2', layout=Layout(width=constWidth), ) )
            self.rate2.append( HBox([BoundedFloatText(min=0, step=0.1, disabled=disabled_flag,
                description='rate2', layout=Layout(width=constWidth), ), Label('1/min')],
                layout=Layout(width=width_cell_params_units)) )

        #-------------------
        label_xform2 = Label('Transform #2:')

        #-------------------
#        self.tab = VBox([label_xform1, start_end_NP_ID, start_end_substrate_ID,
#            self.condition_substrate_ID, self.condition1,self.rate1,  self.condition2,self.rate2])
        self.tab = VBox([label_xform1, start_end_NP_ID[0], start_end_substrate_ID[0],
            self.condition_substrate_ID[0], self.condition1[0],self.rate1[0],  
            self.condition2[0],self.rate2[0],
            label_xform2, start_end_NP_ID[1], start_end_substrate_ID[1],
            self.condition_substrate_ID[1], self.condition1[1],self.rate1[1],  
            self.condition2[1],self.rate2[1]] )

    def fill_gui(self, xml_root):  # for Transformations

        uep = xml_root.find('.//transformations')  # find unique entry point into XML 
        idx = 0
        for el in uep.findall('transformation'):  # currently 2 
            kids = el.getchildren()  # assume 3, which follow:
            self.start_NP_ID[idx].value = int(kids[0].text)
            self.end_NP_ID[idx].value = int(kids[1].text)
            self.start_substrate_ID[idx].value = int(kids[2].text)
            self.end_substrate_ID[idx].value = int(kids[3].text)
            self.condition_substrate_ID[idx].value = int(kids[4].text)
            self.condition1[idx].value = float(kids[5].text)
            self.rate1[idx].children[0].value = float(kids[6].text)  # need 'children' if a HBox
            self.condition2[idx].value = float(kids[7].text)
            self.rate2[idx].children[0].value = float(kids[8].text)
            idx += 1


#============================
class NanoTab(object):

    def __init__(self, xml_root):

#        uep = xml_root.find('.//nanoparticle')  # find unique entry point into XML for (1st) nanoparticle
#        self.sphere = NanoParticle('red', uep)
        self.sphere = NanoSphere(xml_root)

#        for np in xml_root.iter('nanoparticle'):  # hacky: iterate thru all (2) NPs to land on last/2nd
#            uep = np
#        self.rod = NanoParticle('black', uep)
        self.rod = NanoRod(xml_root)

        self.xform = NanoTransform()

        tab_height = '500px'
        tab_layout = Layout(width='800px',   # border='2px solid black',
                            height=tab_height, overflow_y='scroll')

        self.tab = Tab(children=[self.sphere.tab, self.rod.tab, self.xform.tab])
        self.tab.set_title(0, 'Preform (spherical)')
        self.tab.set_title(1, 'Reconfig (rod)')
        self.tab.set_title(2, 'Transformations')

    def fill_gui(self, xml_root):
#        uep = xml_root.find('.//cell_definition')  # find unique entry point into XML 
        self.sphere.fill_gui()
        self.rod.fill_gui()
        self.xform.fill_gui(xml_root)

    def fill_xml(self, xml_root):
        self.sphere.fill_xml(xml_root)
        self.rod.fill_xml(xml_root)
#        self.xform.fill_gui(xml_root)

