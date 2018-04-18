# nanoparticles Tab

from ipywidgets import Layout, Label, Text, Checkbox, HBox, VBox, \
    BoundedFloatText,BoundedIntText, HTMLMath, Dropdown, Tab


class NanoSphere(object):

    def __init__(self):
        self.xml_root = None  # for debugging

        tab_height = '500px'
        width_cell_params_units = '250px'

        np_tab_layout = Layout(width='800px',  # border='2px solid black',
                               height='350px', overflow_y='scroll')
        tab_layout = Layout(width='800px',   # border='2px solid black',
                            height=tab_height, overflow_y='scroll')

        # PK
#        half_conc_desc = '$T_{0.5}$'
#        half_conc_desc = 'T_1/2'
        desc_style = {'description_width': '150px'}  # vs. 'initial'

        # PD
#        ec_50_desc = '$EC_{50}$'

        label_PK = Label('Pharmacokinetics:')
        pk_param_width = '270px'
        pd_param_width = '270px'
        constWidth = '180px'
        # ------------

        self.diffusion_coefficient = HBox([BoundedFloatText(min=0, step=0.1,
           description='diffusion coefficient', layout=Layout(width=constWidth), ), Label('µm^2/min')],
           layout=Layout(width=width_cell_params_units))
        self.survival_lifetime = HBox([BoundedFloatText(min=0, step=0.1,
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

        # box_layout=Layout(display='flex',flex_flow='column',align_items='stretch',border='1px solid black',width='30%')
        pk_widgets_width = '350px'

        self.PK_params = VBox([label_PK, 
            self.diffusion_coefficient, 
            self.survival_lifetime, 
            self.ECM_binding_rate, 
            self.ECM_unbinding_rate, 
            self.ECM_saturation_concentration, ])

        # -------------------------------------------------------
        label_PD = Label('Pharmacodynamics:')

        self.effect_model_choice = Dropdown(
            # options=['1', '2', '3','4','5','6'],
            options={'Simple (conc)' : 0, 'Intermed (AUC)' : 1, 'Details' : 2},
            value=0,
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

        self.toggle_influx = Checkbox(
            description='Active Influx',
            layout=Layout(width=constWidth),
        )
        """
        def toggle_influx_cb(b):
            if (self.toggle_influx.value):
                self.motile_bias.disabled = False
                self.speed.children[0].disabled = False
                self.persistence_time.children[0].disabled = False
            else:
                self.motile_bias.disabled = True
                self.speed.children[0].disabled = True
                self.persistence_time.children[0].disabled = True
        self.toggle_influx.observe(toggle_influx_cb)
        """
        self.relative_max_internal_concentration = HBox([BoundedFloatText(min=0, step=0.1,
           description='rel max int conc', layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units))
        self.internalization_rate = HBox([BoundedFloatText(min=0, step=0.1,
           description='intern rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units))
        self.reference_external_concentration = HBox([BoundedFloatText(min=0, step=0.1,
           description='ref ext conc', layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units))

        # -------------------------------------------------------
        label_responses = Label('Responses:')
        self.toggle_cycle= Checkbox(
            description='Cycle',
            layout=Layout(width=constWidth),
        )
        self.toggle_apoptosis = Checkbox(
            description='Apoptosis',
            layout=Layout(width=constWidth),
        )
        self.toggle_metabolism = Checkbox(
            description='Metabolism',
            layout=Layout(width=constWidth),
        )
        self.toggle_motility = Checkbox(
            description='Motility',
            layout=Layout(width=constWidth),
        )
        self.toggle_mechanics = Checkbox(
            description='Mechanics',
            layout=Layout(width=constWidth),
        )
        self.toggle_secretion = Checkbox(
            description='Secretion',
            layout=Layout(width=constWidth),
        )
        response_toggles1 = HBox([self.toggle_cycle, self.toggle_apoptosis, self.toggle_metabolism])
        response_toggles2 = HBox([self.toggle_motility, self.toggle_mechanics, self.toggle_secretion])
             



        # -------------------------------------------------------
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
        
        self.tab = VBox([self.PK_params, label_PD, self.effect_model_choice, self.EC_50, self.Hill_power,
            self.mechanistic_response_rate, self.mechanistic_deactivation_rate,
            self.toggle_influx, self.relative_max_internal_concentration, self.internalization_rate,
            self.reference_external_concentration,
            label_responses, response_toggles1,response_toggles2,
            label_cycle,row1,row2,row2b, label_necrosis,row3,row4,label_apoptosis,row5, metabolism_stuff,                          motility_stuff,                          label_mechanics, HBox([self.max_relative_adhesion_distance,self.adhesion_strength,self.repulsion_strength]),
                         label_hypoxia,row8, \
                         label_secretion,
                         HBox([self.uptake_rate[0], self.secretion_rate[0], self.saturation_density[0] ]),
                         HBox([self.uptake_rate[1], self.secretion_rate[1], self.saturation_density[1] ]),
                         HBox([self.uptake_rate[2], self.secretion_rate[2], self.saturation_density[2] ]),
                         HBox([self.uptake_rate[3], self.secretion_rate[3], self.saturation_density[3] ]),
                         HBox([self.uptake_rate[4], self.secretion_rate[4], self.saturation_density[4] ]),
                         HBox([self.uptake_rate[5], self.secretion_rate[5], self.saturation_density[5] ]),
                         ])  #,row13,row14,row15,row16])
        
        

    def fill_gui(self, xml_root):  # for Preform (spherical)

        self.xml_root = xml_root  # for debugging

#        uep = xml_root.find('.//cell_definition')  # find unique entry point into XML 
        uep = xml_root.find('.//nanoparticle')  # find unique entry point into XML 

        self.diffusion_coefficient.children[0].value = float(uep.find('.//diffusion_coefficient').text)
        self.survival_lifetime.children[0].value = float(uep.find('.//survival_lifetime').text)
        self.ECM_binding_rate.children[0].value = float(uep.find('.//ECM_binding_rate').text)
        self.ECM_unbinding_rate.children[0].value = float(uep.find('.//ECM_unbinding_rate').text)
        self.ECM_saturation_concentration.children[0].value = float(uep.find('.//ECM_saturation_concentration').text)
        self.EC_50.children[0].value = float(uep.find('.//EC_50').text)
        self.Hill_power.children[0].value = float(uep.find('.//Hill_power').text)
        self.mechanistic_response_rate.children[0].value = float(uep.find('.//mechanistic_response_rate').text)
        self.mechanistic_deactivation_rate.children[0].value = float(uep.find('.//mechanistic_deactivation_rate').text)
        self.relative_max_internal_concentration.children[0].value = float(uep.find('.//relative_max_internal_concentration').text)
        self.internalization_rate.children[0].value = float(uep.find('.//internalization_rate').text)
        self.reference_external_concentration.children[0].value = float(uep.find('.//reference_external_concentration').text)


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


class NanoRod(object):

    def __init__(self):
        self.xml_root = None

        tab_height = '500px'
        width_cell_params_units = '250px'

        np_tab_layout = Layout(width='800px',  # border='2px solid black',
                               height='350px', overflow_y='scroll')
        tab_layout = Layout(width='800px',   # border='2px solid black',
                            height=tab_height, overflow_y='scroll')

        # PK
#        half_conc_desc = '$T_{0.5}$'
#        half_conc_desc = 'T_1/2'

        # PD
#        ec_50_desc = '$EC_{50}$'

        label_PK = Label('Pharmacokinetics:')
        pk_param_width = '270px'
        pd_param_width = '270px'
        constWidth = '180px'
        # ------------

        self.diffusion_coefficient = HBox([BoundedFloatText(min=0, step=0.1,
           description='diffusion coefficient', layout=Layout(width=constWidth), ), Label('µm^2/min')],
           layout=Layout(width=width_cell_params_units))
        self.survival_lifetime = HBox([BoundedFloatText(min=0, step=0.1,
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

        # box_layout=Layout(display='flex',flex_flow='column',align_items='stretch',border='1px solid black',width='30%')
        pk_widgets_width = '350px'

        self.PK_params = VBox([label_PK, 
            self.diffusion_coefficient, 
            self.survival_lifetime, 
            self.ECM_binding_rate, 
            self.ECM_unbinding_rate, 
            self.ECM_saturation_concentration, ])

        # -------------------------------------------------------
        label_PD = Label('Pharmacodynamics:')

        self.effect_model_choice = Dropdown(
            # options=['1', '2', '3','4','5','6'],
            options={'Simple (conc)' : 0, 'Intermed (AUC)' : 1, 'Details' : 2},
            value=0,
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

        self.toggle_influx = Checkbox(
            description='Active Influx',
            layout=Layout(width=constWidth),
        )
        """
        def toggle_influx_cb(b):
            if (self.toggle_influx.value):
                self.motile_bias.disabled = False
                self.speed.children[0].disabled = False
                self.persistence_time.children[0].disabled = False
            else:
                self.motile_bias.disabled = True
                self.speed.children[0].disabled = True
                self.persistence_time.children[0].disabled = True
        self.toggle_influx.observe(toggle_influx_cb)
        """
        self.relative_max_internal_concentration = HBox([BoundedFloatText(min=0, step=0.1,
           description='rel max int conc', layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units))
        self.internalization_rate = HBox([BoundedFloatText(min=0, step=0.1,
           description='intern rate', layout=Layout(width=constWidth), ), Label('1/min')], 
           layout=Layout(width=width_cell_params_units))
        self.reference_external_concentration = HBox([BoundedFloatText(min=0, step=0.1,
           description='ref ext conc', layout=Layout(width=constWidth), ), ], 
           layout=Layout(width=width_cell_params_units))

        # -------------------------------------------------------
        label_responses = Label('Responses:')
        self.toggle_cycle= Checkbox(
            description='Cycle',
            layout=Layout(width=constWidth),
        )
        self.toggle_apoptosis = Checkbox(
            description='Apoptosis',
            layout=Layout(width=constWidth),
        )
        self.toggle_metabolism = Checkbox(
            description='Metabolism',
            layout=Layout(width=constWidth),
        )
        self.toggle_motility = Checkbox(
            description='Motility',
            layout=Layout(width=constWidth),
        )
        self.toggle_mechanics = Checkbox(
            description='Mechanics',
            layout=Layout(width=constWidth),
        )
        self.toggle_secretion = Checkbox(
            description='Secretion',
            layout=Layout(width=constWidth),
        )
        response_toggles1 = HBox([self.toggle_cycle, self.toggle_apoptosis, self.toggle_metabolism])
        response_toggles2 = HBox([self.toggle_motility, self.toggle_mechanics, self.toggle_secretion])
             



        # -------------------------------------------------------
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
        
        self.tab = VBox([self.PK_params, label_PD, self.effect_model_choice, self.EC_50, self.Hill_power,
            self.mechanistic_response_rate, self.mechanistic_deactivation_rate,
            self.toggle_influx, self.relative_max_internal_concentration, self.internalization_rate,
            self.reference_external_concentration,
            label_responses, response_toggles1,response_toggles2,
            label_cycle,row1,row2,row2b, label_necrosis,row3,row4,label_apoptosis,row5, metabolism_stuff,                          motility_stuff,                          label_mechanics, HBox([self.max_relative_adhesion_distance,self.adhesion_strength,self.repulsion_strength]),
                         label_hypoxia,row8, \
                         label_secretion,
                         HBox([self.uptake_rate[0], self.secretion_rate[0], self.saturation_density[0] ]),
                         HBox([self.uptake_rate[1], self.secretion_rate[1], self.saturation_density[1] ]),
                         HBox([self.uptake_rate[2], self.secretion_rate[2], self.saturation_density[2] ]),
                         HBox([self.uptake_rate[3], self.secretion_rate[3], self.saturation_density[3] ]),
                         HBox([self.uptake_rate[4], self.secretion_rate[4], self.saturation_density[4] ]),
                         HBox([self.uptake_rate[5], self.secretion_rate[5], self.saturation_density[5] ]),
                         ])  #,row13,row14,row15,row16])
        
        

    def fill_gui(self, xml_root):  # for Reconfig (rod)

        # find unique entry point into XML 
        uep = xml_root.find('.//nanoparticle').find('.//basic_phenotype').find('.//nanoparticle')

        self.diffusion_coefficient.children[0].value = float(uep.find('.//diffusion_coefficient').text)
        self.survival_lifetime.children[0].value = float(uep.find('.//survival_lifetime').text)
        self.ECM_binding_rate.children[0].value = float(uep.find('.//ECM_binding_rate').text)
        self.ECM_unbinding_rate.children[0].value = float(uep.find('.//ECM_unbinding_rate').text)
        self.ECM_saturation_concentration.children[0].value = float(uep.find('.//ECM_saturation_concentration').text)
        self.EC_50.children[0].value = float(uep.find('.//EC_50').text)
        self.Hill_power.children[0].value = float(uep.find('.//Hill_power').text)
        self.mechanistic_response_rate.children[0].value = float(uep.find('.//mechanistic_response_rate').text)
        self.mechanistic_deactivation_rate.children[0].value = float(uep.find('.//mechanistic_deactivation_rate').text)
        self.relative_max_internal_concentration.children[0].value = float(uep.find('.//relative_max_internal_concentration').text)
        self.internalization_rate.children[0].value = float(uep.find('.//internalization_rate').text)
        self.reference_external_concentration.children[0].value = float(uep.find('.//reference_external_concentration').text)


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


class NanoTab(object):

    def __init__(self):
        self.sphere = NanoSphere()
        self.rod = NanoRod()

        tab_height = '500px'
        tab_layout = Layout(width='800px',   # border='2px solid black',
                            height=tab_height, overflow_y='scroll')
        xforms_tab = Text(
            value='.',
            description='dummy:',
            layout=tab_layout,
        )

        self.tab = Tab(children=[self.sphere.tab, self.rod.tab, xforms_tab])
        self.tab.set_title(0, 'Preform (spherical)')
        self.tab.set_title(1, 'Reconfig (rod)')
        self.tab.set_title(2, 'Transformations')

    def fill_gui(self, xml_root):

#        uep = xml_root.find('.//cell_definition')  # find unique entry point into XML 
        self.sphere.fill_gui(xml_root)
        self.rod.fill_gui(xml_root)

