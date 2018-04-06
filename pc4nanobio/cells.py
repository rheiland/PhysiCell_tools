# Cells Tab

from ipywidgets import Layout, Label, Text, Checkbox, Button, HBox, VBox, \
    FloatText, BoundedIntText, BoundedFloatText, HTMLMath, Dropdown


class CellsTab(object):

    def __init__(self):

        constWidth = '180px'
        constWidth3 = '200px'
        min_inv_units = HTMLMath(value=r"$\frac{1}{min}$")
        mmHg_units = HTMLMath(value=r"$mmHg$")

        cell_name = Text(
            value='untreated cancer',
            description='Cell line name', style={'description_width': 'initial'},
        )

        label_cycle = Label('Cycle:')   # no worky:  ,style={'font_weight': 'bold'})

        self.max_birth_rate = HBox([BoundedFloatText(
            min=0,
            # value = 0.0079,
            description='Max birth rate', style={'description_width': 'initial'},
            layout=Layout(width=constWidth3),
        ), min_inv_units], layout=Layout(width='300px'))

        width_cell_params_units = '230px'
        self.o2_prolif_sat = HBox([BoundedFloatText(
            min=0,
            description='$O_2$: Prolif sat',
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        self.o2_prolif_thresh = HBox([BoundedFloatText(
            min=0,
            description='Prolif thresh',
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        self.o2_ref = HBox([BoundedFloatText(
            min=0,
            description='Ref',
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        self.glucose_prolif_sat = HBox([BoundedFloatText(
            min=0,
            description='$Glc$: Prolif sat',
            layout=Layout(width=constWidth), style={'description_width': 'initial'},
            ), ], layout=Layout(width=width_cell_params_units))
        self.glucose_prolif_thresh = HBox([BoundedFloatText(
            min=0,
            description='Prolif thresh',
            layout=Layout(width=constWidth),
        ), ], layout=Layout(width=width_cell_params_units))
        self.glucose_prolif_ref = HBox([BoundedFloatText(
            min=0,
            description='Ref',
            layout=Layout(width=constWidth),
        ), ], layout=Layout(width=width_cell_params_units))

        # -------
        label_necrosis = Label('Necrosis:')
        self.max_necrosis_rate = HBox([BoundedFloatText(
            min=0,
            description='Max rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        self.o2_necrosis_thresh = HBox([BoundedFloatText(
            min=0,
            description='$O_2$: Thresh',
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))
        self.o2_necrosis_max = HBox([BoundedFloatText(
            min=0,
            description='Max',
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        #-------
        label_apoptosis = Label('Apoptosis:')
        self.apoptosis_rate = HBox([BoundedFloatText(
            min=0,
            description='Rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))

        # -------
        # TODO: enforce sum=1
        label_metabolism = Label('Metabolism (must sum to 1):')
        # TODO: assert these next 2 values sum to 1.0
        self.metab_aero = HBox([BoundedFloatText(
            min=0,max=1,step=0.1,
            description='Aerobic',  #style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), ], layout=Layout(width=width_cell_params_units))
        self.metab_glyco = HBox([BoundedFloatText(
            min=0,max=1,step=0.1,
            description='Glycolytic',  #style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), ], layout=Layout(width=width_cell_params_units))

        #-------
        label_motility = Label('Motility:')

        self.toggle_motile = Checkbox(
            description='Motile',
            layout=Layout(width=constWidth),
        )
        self.motile_bias = BoundedFloatText(
            min=0,
            max=1,
            step=0.1,
            description='Bias', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        )
        def toggle_motile_cb(b):
            if (self.toggle_motile.value):
                self.motile_bias.disabled = False
            else:
                self.motile_bias.disabled = True
            
        self.toggle_motile.observe(toggle_motile_cb)


        #-------
        label_mechanics = Label('Mechanics:')
        self.max_rel_adhesion_dist = HBox([BoundedFloatText(
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

        #-------
        label_hypoxia = Label('Hypoxia:')
        self.o2_hypoxic_thresh = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='$O_2$: Thresh', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), mmHg_units], layout=Layout(width=width_cell_params_units))
        self.o2_hypoxic_response = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Response', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), mmHg_units], layout=Layout(width=width_cell_params_units))
        self.o2_hypoxic_sat = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Saturation', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), mmHg_units], layout=Layout(width=width_cell_params_units))

        #-------
        label_secretion = Label('Secretion:')
        self.secretion_o2_uptake = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='$O_2$: Uptake rate', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        self.secretion_o2_secretion = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Secretion rate', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        self.secretion_o2_sat = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Saturation', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        self.secretion_glc_uptake = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='$Glc$: Uptake rate', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        self.secretion_glc_secretion = HBox([BoundedFloatText(
            min=0, 
            step=0.1,  # max=1,  
            description='Secretion rate', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        self.secretion_glc_sat = HBox([BoundedFloatText(
            min=0, 
            step=0.1,  # max=1,  
            description='Saturation', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        self.secretion_Hions_uptake = HBox([BoundedFloatText(
            min=0, 
            step=0.1,  # max=1,  
            description='$H$+: Uptake rate', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), min_inv_units], layout=Layout(width=width_cell_params_units))
        self.secretion_Hions_secretion = HBox([BoundedFloatText(
            min=0, 
            step=0.1,  # max=1,  
            description='Secretion rate', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        self.secretion_Hions_sat = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='Saturation',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        self.secretion_ECM_uptake = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='$ECM$: Uptake rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        self.secretion_ECM_secretion = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='Secretion rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        self.secretion_ECM_sat = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='Saturation',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        self.secretion_NP1_uptake = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='$NP1$: Uptake rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        self.secretion_NP1_secretion = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='Secretion rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        self.secretion_NP1_sat = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='Saturation',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        self.secretion_NP2_uptake = HBox([BoundedFloatText(
            min=0, step=0.1,   # max=1,  
            description='$NP2$: Uptake rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        self.secretion_NP2_secretion = HBox([BoundedFloatText(
            min=0, step=0.1,   # max=1,  
            description='Secretion rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        self.secretion_NP2_sat = HBox([BoundedFloatText(
            min=0, step=0.1,   # max=1,  
            description='Saturation',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        # -----------------
        # cells_max_birth_rate2 = HBox([max_birth_rate,min_inv_units], layout=Layout(width='300px'))
        # cells_o2_prolif_sat2 = HBox([o2_prolif_sat,min_inv_units])
        # cells_o2_prolif_thresh2 = HBox([o2_prolif_thresh, mmHg_units])
        cells_row1 = HBox([cell_name])
        cells_row2 = HBox([self.o2_prolif_sat, self.o2_prolif_thresh, self.o2_ref])
        cells_row3 = HBox([self.glucose_prolif_sat, self.glucose_prolif_thresh, self.glucose_prolif_ref])
        self.necrosis_row = HBox([self.o2_necrosis_thresh, self.o2_necrosis_max])
        self.tab = VBox(
            [cells_row1, 
             label_cycle, self.max_birth_rate, cells_row2, cells_row3,
             label_necrosis, self.max_necrosis_rate, self.necrosis_row,
             label_apoptosis, self.apoptosis_rate,
             label_metabolism, HBox([self.metab_aero, self.metab_glyco]),
             label_motility, HBox([self.toggle_motile, self.motile_bias]),
             label_mechanics, HBox([self.max_rel_adhesion_dist, self.adhesion_strength, self.repulsion_strength]),
             label_hypoxia, HBox([self.o2_hypoxic_thresh, self.o2_hypoxic_response, self.o2_hypoxic_sat]),
             label_secretion, HBox([self.secretion_o2_uptake, self.secretion_o2_secretion, self.secretion_o2_sat]),
             HBox([self.secretion_glc_uptake, self.secretion_glc_secretion, self.secretion_glc_sat]),
             HBox([self.secretion_Hions_uptake, self.secretion_Hions_secretion, self.secretion_Hions_sat]),
             HBox([self.secretion_ECM_uptake, self.secretion_ECM_secretion, self.secretion_ECM_sat]),
             HBox([self.secretion_NP1_uptake, self.secretion_NP1_secretion, self.secretion_NP1_sat]),
             HBox([self.secretion_NP2_uptake, self.secretion_NP1_secretion, self.secretion_NP2_sat]),
            ])

    def fill_gui(self, xml_root):
        uep = xml_root.find(".//cell_definition")  # find unique entry point into XML
    #     e2 = e1.find('.//')
        self.max_birth_rate.children[0].value = float(uep.find(".//max_birth_rate").text)
        self.o2_prolif_sat.children[0].value = float(uep.find(".//o2_proliferation_saturation").text)
        self.o2_prolif_thresh.children[0].value = float(uep.find(".//o2_proliferation_threshold").text)
        self.o2_ref.children[0].value = float(uep.find(".//o2_reference").text)
        
        self.glucose_prolif_ref.children[0].value = float(uep.find(".//glucose_proliferation_reference").text)
        self.glucose_prolif_sat.children[0].value = float(uep.find(".//glucose_proliferation_saturation").text)
        self.glucose_prolif_thresh.children[0].value = float(uep.find(".//glucose_proliferation_threshold").text)
        
        self.max_necrosis_rate.children[0].value = float(uep.find(".//max_necrosis_rate").text)
        self.o2_necrosis_thresh.children[0].value = float(uep.find(".//o2_necrosis_threshold").text)
        self.o2_necrosis_max.children[0].value = float(uep.find(".//o2_necrosis_max").text)
        
        self.apoptosis_rate.children[0].value = float(uep.find(".//apoptosis_rate").text)
        
        self.metab_aero.children[0].value = float(uep.find(".//relative_aerobic_effects").text)
        self.metab_glyco.children[0].value = float(uep.find(".//relative_glycolytic_effects").text)
        
        self.toggle_motile.value = bool(uep.find(".//is_motile").text)
        self.motile_bias.value = float(uep.find(".//bias").text)

        self.max_rel_adhesion_dist.children[0].value = float(uep.find(".//max_relative_adhesion_distance").text)
        self.adhesion_strength.children[0].value = float(uep.find(".//adhesion_strength").text)
        self.repulsion_strength.children[0].value = float(uep.find(".//repulsion_strength").text)

