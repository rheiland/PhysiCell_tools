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

        cell0_max_birth_rate = HBox([BoundedFloatText(
            min=0,
            # value = 0.0079,
            description='Max birth rate', style={'description_width': 'initial'},
            layout=Layout(width=constWidth3),
        ), min_inv_units], layout=Layout(width='300px'))

        width_cell_params_units = '230px'
        cell0_o2_prolif_sat = HBox([BoundedFloatText(
            min=0,
            description='$O_2$: Prolif sat',
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        cell0_o2_prolif_thresh = HBox([BoundedFloatText(
            min=0,
            description='Prolif thresh',
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        cell0_o2_ref = HBox([BoundedFloatText(
            min=0,
            description='Ref',
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        cell0_glucose_prolif_sat = HBox([BoundedFloatText(
            min=0,
            description='$Glc$: Prolif sat',
            layout=Layout(width=constWidth), style={'description_width': 'initial'},
            ), ], layout=Layout(width=width_cell_params_units))
        cell0_glucose_prolif_thresh = HBox([BoundedFloatText(
            min=0,
            description='Prolif thresh',
            layout=Layout(width=constWidth),
        ), ], layout=Layout(width=width_cell_params_units))
        cell0_glucose_prolif_ref = HBox([BoundedFloatText(
            min=0,
            description='Ref',
            layout=Layout(width=constWidth),
        ), ], layout=Layout(width=width_cell_params_units))

        # -------
        label_necrosis = Label('Necrosis:')
        cell0_max_necrosis_rate = HBox([BoundedFloatText(
            min=0,
            description='Max rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        cell0_o2_necrosis_thresh = HBox([BoundedFloatText(
            min=0,
            description='$O_2$: Thresh',
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))
        cell0_o2_necrosis_max = HBox([BoundedFloatText(
            min=0,
            description='Max',
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        #-------
        label_apoptosis = Label('Apoptosis:')
        cell0_apoptosis_rate = HBox([BoundedFloatText(
            min=0,
            description='Rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))

        # -------
        # TODO: enforce sum=1
        label_metabolism = Label('Metabolism (must sum to 1):')
        # TODO: assert these next 2 values sum to 1.0
        cell0_metab_aero = HBox([BoundedFloatText(
            min=0,max=1,step=0.1,
            description='Aerobic',  #style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), ], layout=Layout(width=width_cell_params_units))
        cell0_metab_glyco = HBox([BoundedFloatText(
            min=0,max=1,step=0.1,
            description='Glycolytic',  #style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), ], layout=Layout(width=width_cell_params_units))

        #-------
        label_motility = Label('Motility:')

        cell0_toggle_motile = Checkbox(
            description='Motile',
            layout=Layout(width=constWidth),
        )
        cell0_motile_bias = BoundedFloatText(
            min=0,
            max=1,
            step=0.1,
            description='Bias', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        )
        def cell0_toggle_motile_cb(b):
            if (cell0_toggle_motile.value):
                cell0_motile_bias.disabled = False
            else:
                cell0_motile_bias.disabled = True
            
        cell0_toggle_motile.observe(cell0_toggle_motile_cb)


        #-------
        label_mechanics = Label('Mechanics:')
        cell0_max_rel_adhesion_dist = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Max adhesion distance', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), ], layout=Layout(width=width_cell_params_units))
        cell0_adhesion_strength = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Adhesion strength', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), ], layout=Layout(width=width_cell_params_units))
        cell0_repulsion_strength = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Repulsion strength', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), ], layout=Layout(width=width_cell_params_units))

        #-------
        label_hypoxia = Label('Hypoxia:')
        cell0_o2_hypoxic_thresh = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='$O_2$: Thresh', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), mmHg_units], layout=Layout(width=width_cell_params_units))
        cell0_o2_hypoxic_response = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Response', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), mmHg_units], layout=Layout(width=width_cell_params_units))
        cell0_o2_hypoxic_sat = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Saturation', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), mmHg_units], layout=Layout(width=width_cell_params_units))

        #-------
        label_secretion = Label('Secretion:')
        cell0_secretion_o2_uptake = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='$O_2$: Uptake rate', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        cell0_secretion_o2_secretion = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Secretion rate', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        cell0_secretion_o2_sat = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='Saturation', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        cell0_secretion_glc_uptake = HBox([BoundedFloatText(
            min=0, step=0.1, #max=1,  
            description='$Glc$: Uptake rate', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        cell0_secretion_glc_secretion = HBox([BoundedFloatText(
            min=0, 
            step=0.1,  # max=1,  
            description='Secretion rate', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        cell0_secretion_glc_sat = HBox([BoundedFloatText(
            min=0, 
            step=0.1,  # max=1,  
            description='Saturation', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        cell0_secretion_Hions_uptake = HBox([BoundedFloatText(
            min=0, 
            step=0.1,  # max=1,  
            description='$H$+: Uptake rate', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
            ), min_inv_units], layout=Layout(width=width_cell_params_units))
        cell0_secretion_Hions_secretion = HBox([BoundedFloatText(
            min=0, 
            step=0.1,  # max=1,  
            description='Secretion rate', # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        cell0_secretion_Hions_sat = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='Saturation',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        cell0_secretion_ECM_uptake = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='$ECM$: Uptake rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        cell0_secretion_ECM_secretion = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='Secretion rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        cell0_secretion_ECM_sat = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='Saturation',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        cell0_secretion_NP1_uptake = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='$NP1$: Uptake rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        cell0_secretion_NP1_secretion = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='Secretion rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        cell0_secretion_NP1_sat = HBox([BoundedFloatText(
            min=0, step=0.1,  # max=1,  
            description='Saturation',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        cell0_secretion_NP2_uptake = HBox([BoundedFloatText(
            min=0, step=0.1,   # max=1,  
            description='$NP2$: Uptake rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        cell0_secretion_NP2_secretion = HBox([BoundedFloatText(
            min=0, step=0.1,   # max=1,  
            description='Secretion rate',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), min_inv_units], layout=Layout(width=width_cell_params_units))
        cell0_secretion_NP2_sat = HBox([BoundedFloatText(
            min=0, step=0.1,   # max=1,  
            description='Saturation',  # style={'description_width': 'initial'},
            layout=Layout(width=constWidth),
        ), mmHg_units], layout=Layout(width=width_cell_params_units))

        # -----------------
        # cells_max_birth_rate2 = HBox([max_birth_rate,min_inv_units], layout=Layout(width='300px'))
        # cells_o2_prolif_sat2 = HBox([o2_prolif_sat,min_inv_units])
        # cells_o2_prolif_thresh2 = HBox([o2_prolif_thresh, mmHg_units])
        cells_row1 = HBox([cell_name])
        cells_row2 = HBox([cell0_o2_prolif_sat, cell0_o2_prolif_thresh, cell0_o2_ref])
        cells_row3 = HBox([cell0_glucose_prolif_sat, cell0_glucose_prolif_thresh, cell0_glucose_prolif_ref])
        cell0_necrosis_row = HBox([cell0_o2_necrosis_thresh, cell0_o2_necrosis_max])
        self.tab = VBox(
            [cells_row1, 
             label_cycle, cell0_max_birth_rate, cells_row2, cells_row3,
             label_necrosis, cell0_max_necrosis_rate, cell0_necrosis_row,
             label_apoptosis, cell0_apoptosis_rate,
             label_metabolism, HBox([cell0_metab_aero, cell0_metab_glyco]),
             label_motility, HBox([cell0_toggle_motile, cell0_motile_bias]),
             label_mechanics, HBox([cell0_max_rel_adhesion_dist, cell0_adhesion_strength, cell0_repulsion_strength]),
             label_hypoxia, HBox([cell0_o2_hypoxic_thresh, cell0_o2_hypoxic_response, cell0_o2_hypoxic_sat]),
             label_secretion, HBox([cell0_secretion_o2_uptake, cell0_secretion_o2_secretion, cell0_secretion_o2_sat]),
             HBox([cell0_secretion_glc_uptake, cell0_secretion_glc_secretion, cell0_secretion_glc_sat]),
             HBox([cell0_secretion_Hions_uptake, cell0_secretion_Hions_secretion, cell0_secretion_Hions_sat]),
             HBox([cell0_secretion_ECM_uptake, cell0_secretion_ECM_secretion, cell0_secretion_ECM_sat]),
             HBox([cell0_secretion_NP1_uptake, cell0_secretion_NP1_secretion, cell0_secretion_NP1_sat]),
             HBox([cell0_secretion_NP2_uptake, cell0_secretion_NP1_secretion, cell0_secretion_NP2_sat]),
            ])
