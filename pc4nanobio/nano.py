# nanoparticles Tab

from ipywidgets import Layout, Label, Text, HBox, VBox, \
    BoundedFloatText, HTMLMath, Dropdown, Tab


class NanoTab(object):

    def __init__(self):
        tab_height = '500px'

        np_tab_layout = Layout(width='800px',  # border='2px solid black',
                               height='350px', overflow_y='scroll')
        tab_layout = Layout(width='800px',   # border='2px solid black',
                            height=tab_height, overflow_y='scroll')

        # PK
        half_conc_desc = '$T_{0.5}$'
        diffusion_coef_desc = 'Diffusion coef'
        survival_desc = 'Survival lifetime'
        binding_desc = 'ECM binding rate'
        unbinding_desc = 'ECM unbinding rate'
        sat_conc_desc = 'ECM saturation conc'
        desc_style = {'description_width': '150px'}  # vs. 'initial'

        # PD
        ec_50_desc = '$EC_{50}$'

        label_PK = Label('Pharmacokinetics:')
        pk_param_width = '270px'
        pd_param_width = '270px'
        # ------------
        np1_diff_coef = BoundedFloatText(
            min=0,
            description=diffusion_coef_desc, style=desc_style,
            disabled=False,
            layout=Layout(width=pk_param_width),  # flex_flow='row',align_items='stretch'),
        )
        np1_survival_lifetime = BoundedFloatText(
            min=0,
            description=survival_desc, style=desc_style,
            disabled=False,
            layout=Layout(width=pk_param_width),  # flex_flow='row',align_items='stretch'),
        )
        np1_binding_rate = BoundedFloatText(
            min=0,
            description=binding_desc, style=desc_style,
            disabled=False,
            layout=Layout(width=pk_param_width),
        )
        np1_unbinding_rate = BoundedFloatText(
            min=0,
            description=unbinding_desc, style=desc_style,
            layout=Layout(width=pk_param_width),
        )
        np1_saturation_conc = BoundedFloatText(
            min=0,
            description=sat_conc_desc, style=desc_style,
            layout=Layout(width=pk_param_width),
        )

        # box_layout=Layout(display='flex',flex_flow='column',align_items='stretch',border='1px solid black',width='30%')
        pk_widgets_width = '320px'
        diffusion_coef_units = HTMLMath(value=r"$\frac{\mu M^2}{min}$")

        np1_diff_coef2 = HBox([np1_diff_coef, diffusion_coef_units], layout=Layout(width=pk_widgets_width))
        survival_lifetime_units = HTMLMath(value=r"$min$")

        np1_survival_lifetime2 = HBox([np1_survival_lifetime, survival_lifetime_units], layout=Layout(width=pk_widgets_width))
        min_inv_units = HTMLMath(value=r"$\frac{1}{min}$")

        np1_binding_rate2 = HBox([np1_binding_rate, min_inv_units], layout=Layout(width=pk_widgets_width))
        np1_unbinding_rate2 = HBox([np1_unbinding_rate, min_inv_units], layout=Layout(width=pk_widgets_width))
        # np1_sat_conc2 = HBox([np1_saturation_conc,min_inv_units], layout=Layout(width=pk_widgets_width))

        np1_PK_params = VBox([label_PK, np1_diff_coef2, np1_survival_lifetime2, 
                              np1_binding_rate2, np1_unbinding_rate2, np1_saturation_conc])

        # ----------
        label_PD = Label('Pharmacodynamics:')

        constWidth = '180px'

        np1_effect_model_choice = Dropdown(
            # options=['1', '2', '3','4','5','6'],
            options=['Simple (conc)', 'Intermed (AUC)', 'Details'],
            value='Simple (conc)',
            # description='Field',
            layout=Layout(width=constWidth)
        )
        np1_EC_50 = BoundedFloatText(
            min=0,
            description=ec_50_desc, style=desc_style,
            layout=Layout(width=pd_param_width)
        )

        np1_tab = VBox([np1_PK_params, label_PD], layout=np_tab_layout)

        #------------
        np2_diff_coef = BoundedFloatText(
            min=0,
            description=diffusion_coef_desc, style=desc_style,
            layout=Layout(width=pk_param_width)  # flex_flow='row',align_items='stretch'),
        )
        np2_survival_lifetime = BoundedFloatText(
            min=0,
            description=survival_desc, style=desc_style,
            layout=Layout(width=pk_param_width)  # flex_flow='row',align_items='stretch'),
        )
        np2_binding_rate = BoundedFloatText(
            min=0,
            description=binding_desc, style=desc_style,
            layout=Layout(width=pk_param_width)
        )
        np2_unbinding_rate = BoundedFloatText(
            min=0,
            description=unbinding_desc, style=desc_style,
            layout=Layout(width=pk_param_width)
        )
        np2_saturation_conc = BoundedFloatText(
            min=0,
            description=sat_conc_desc, style=desc_style,
            layout=Layout(width=pk_param_width)
        )
        # box_layout=Layout(display='flex',flex_flow='column',align_items='stretch',border='1px solid black',width='30%')
        np2_diff_coef2 = HBox([np2_diff_coef, diffusion_coef_units], layout=Layout(width=pk_widgets_width))
        np2_survival_lifetime2 = HBox([np2_survival_lifetime, survival_lifetime_units], layout=Layout(width=pk_widgets_width))
        np2_binding_rate2 = HBox([np2_binding_rate, min_inv_units], layout=Layout(width=pk_widgets_width))
        np2_unbinding_rate2 = HBox([np2_unbinding_rate, min_inv_units], layout=Layout(width=pk_widgets_width))

        np2_PK_params = VBox([label_PK, np2_diff_coef2, np2_survival_lifetime2, np2_binding_rate2,
                              np2_unbinding_rate2, np2_saturation_conc])  # layout=box_layout)

        # ---------------
        label_PD = Label('Pharmacodynamics:')

        # ---------------
        np2_tab = VBox([np2_PK_params, label_PD], layout=np_tab_layout)

        # -------------------
        xforms_tab = Text(
            value='.',
            description='dummy:',
            layout=tab_layout,
        )

        self.tab = Tab(children=[np1_tab, np2_tab, xforms_tab])
        self.tab.set_title(0, 'Preform (spherical)')
        self.tab.set_title(1, 'Reconfig (rod)')
        self.tab.set_title(2, 'Transformations')
