# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import webbrowser

import ipywidgets as widgets
import ipyvuetify as v
import traitlets

import plotly.graph_objects as go

import openmdao.api as om
import fastoad.api as oad

from fast_pedago.utils.functions import _image_from_path  # noqa

from fast_pedago.gui.tabs import BaseTab

from fast_pedago.gui.sliders import (
    SliderInput,
    RangeSliderInput,
)

OUTPUT_FILE_SUFFIX = "_output_file.xml"
FLIGHT_DATA_FILE_SUFFIX = "_flight_points.csv"


class ImpactVariableInputLaunchTab(BaseTab):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Generate the N2 diagram and the XDSM. We will locate them near the configuration file
        # as in this case there are more data than actual results. Also, since the take a lot of
        # time to generate, before actually generating them, we check if they exist
        configuration_file_name = pth.basename(self.configuration_file_path)
        self.n2_image_path = self.configuration_file_path.replace(
            configuration_file_name, "n2.png"
        )
        self.n2_file_path = self.configuration_file_path.replace(
            configuration_file_name, "n2.html"
        )
        self.xdsm_image_path = self.configuration_file_path.replace(
            configuration_file_name, "xdsm.png"
        )
        self.xdsm_file_path = self.configuration_file_path.replace(
            configuration_file_name, "xdsm.html"
        )

        # Read the reference input file path so that we can give first accurate first value. Also
        # save it as an object attribute that we can copy to modify inputs
        self.reference_inputs = oad.DataFile(self.reference_input_file_path)

        # Define attribute to store variable value. Also, those are gonna be attribute of the
        # parent HBox so that the children can exchange those information.
        # No need to convert to alternate units
        self.n_pax = None
        self.v_app = None
        self.cruise_mach = None
        self.range = None
        self.payload = None
        self.max_payload = None
        self.wing_aspect_ratio = None
        self.bpr = None

        # Could be done much more cleanly with a setter of the reference file attribute !
        self.set_initial_value_mda()

        self.sizing_process_name = "reference_aircraft"

        self.opt_ar_min = 9.0
        self.opt_ar_max = 18.0

        self.opt_sweep_w_min = 10.0
        self.opt_sweep_w_max = 45.0

        self.opt_wing_span_max = 60.0

        # Have to put every widget and sub widget in the same class unfortunately or else the widget
        # from the input bow won't modify the launch box :/

        ############################################################################################
        # Input box
        self.input_box = v.Col(
            cols=3,
        )
        
        ########################################
        
        self.n_pax_input = SliderInput(min=19,max=500, step=1, value=self.n_pax, label="N_PAX", tooltip="Number of passengers")
        self.v_app_input = SliderInput(min=45., max=200., step=0.1, value=self.v_app, label="V_app", tooltip="Approach speed [kts]")
        self.cruise_mach_input = SliderInput(min=0., max=1., step=0.01, value=self.cruise_mach, label="M_cruise", tooltip="Cruise mach")
        self.range_input = SliderInput(min=0, max=10000, step=100, value=self.range, label="Range", tooltip="Aircraft range [NM]")
        self.payload_input = SliderInput(min=0, max=100000, step=10, value=self.payload, label="Payload", tooltip="Aircraft payload [kg]")
        self.max_payload_input = SliderInput(min=0, max=100000, step=10, value=self.max_payload, label="Max Payload", tooltip="Aircraft max payload [kg]")
        self.wing_aspect_ratio_input = SliderInput(min=4., max=25., step=0.1, value=self.wing_aspect_ratio, label="AR_w", tooltip="Aspect Ratio of the wing")
        self.bpr_input = SliderInput(min=0, max=25., step=0.1, label="BPR", value=self.bpr, tooltip="ByPass Ratio of the engine")


        ########################################

        # Create the widgets to change the value of the parameters in the sensitivity analysis,
        # which entails: create the widget, create the function to update the input and on_click
        # that function

        self.cruise_mach_input_widget = widgets.BoundedFloatText(
            min=0.0,
            max=1.0,
            step=0.01,
            value=self.cruise_mach,
            description="M_cruise",
            description_tooltip="Cruise mach",
        )
        
        self.cruise_mach_input_box = widgets.HBox()
        self.cruise_mach_input_box.children = [self.cruise_mach_input_widget]
        self.cruise_mach_input_box.layout = widgets.Layout(
            width="100%",
            height="54px",
            align_items="center",
        )

        # As can be seen in the parent tab, there is an issue when cruise mach gets too high,
        # we will display a warning when that value is reached, informing students of what is
        # done behind the scene
        self.cruise_mach_warning_button = widgets.Button(
            description="",
            icon="fa-info-circle",
            button_style="warning",
            tooltip="The sweep angle of the wing has been adjusted to avoid having compressibility "
            "drag coefficient too high ",
        )
        self.cruise_mach_warning_button.layout = widgets.Layout(
            height="28px", width="36px"
        )

        self.cruise_mach_filler_box = widgets.Box(
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                align_items="center",
                width="17px",
                height="28px",
            ),
        )

        def update_cruise_mach(change):
            self.cruise_mach = change["new"]

            if self.cruise_mach > 0.78:

                self.cruise_mach_input_box.children = [
                    self.cruise_mach_input_widget,
                    self.cruise_mach_warning_button,
                    self.cruise_mach_filler_box,
                ]

            else:

                self.cruise_mach_input_box.children = [
                    self.cruise_mach_input_widget,
                ]

        self.cruise_mach_input_widget.observe(update_cruise_mach, names="value")

        ###########################
        class Inputs(v.Container):
            def __init__(self, name, inputs=[], **kwargs):
                super().__init__(**kwargs)
                
                self.class_="ps-6 pb-0 pt-2" 
                
                self.children=[
                    v.Row(
                        children=[
                            v.Html(
                                tag="div",
                                style_="font-weight: bold;",
                                children=[name],
                            ),
                        ],
                    ),
                    v.Row(
                        children=inputs,
                    ),
                    v.Divider(
                        class_="pb-2 mt-1",
                    ),
                ]
            
        self.TLAR_inputs = Inputs("TLARs", [
            self.n_pax_input,
            self.v_app_input,
            self.cruise_mach_input,
            self.range_input,
        ])
        self.weight_inputs = Inputs("Weight", [
            self.payload_input,
            self.max_payload_input,
        ])
        self.geometry_inputs = Inputs("Geometry", [
            self.wing_aspect_ratio_input,
        ])
        self.propulsion_inputs = Inputs("Propulsion", [
            self.bpr_input,
        ])

        self.input_box.children = [
            v.Card(
                children=[
                    self.TLAR_inputs,
                    self.weight_inputs,
                    self.geometry_inputs,
                    self.propulsion_inputs,
                ],
            ),
        ]

        ############################################################################################
        # We also create a bow specific for launching an MDO which will only consists of selecting
        # the objectives and the bounds for the design variables
        # Input box
        self.mdo_input_box_widget = v.Col(
            cols=3,
        )
        
        # FIXME 
        # Tooltip doesn't work
        class SelectionButton(v.Btn):
            def __init__(self, name, tooltip, **kwargs):
                super().__init__(**kwargs)

                self.children = [
                    name,
                    v.Tooltip(
                        activator="parent",
                        location="top",
                        children=tooltip,
                    ),
                ]
        
        self.debug = v.Html(tag="div", children=["test"])
        def print_debug(widget, event, data):
            self.debug.children = str(widget.v_model)
        
        self.objective_selection = v.BtnToggle(
            v_model="toggle_exclusive",
            mandatory=True,
            children=[
                SelectionButton("Fuel sizing", tooltip="Minimize the aircraft fuel consumption on the design mission"),
                SelectionButton("MTOW", tooltip="Minimize the aircraft MTOW"),
                SelectionButton("OWE", tooltip="Minimize the aircraft OWE"),
            ],
        ) 
        
        self.objective_selection.on_event("change", print_debug)
        
        self.objectives_inputs = Inputs("Objective", [
            v.Row(
                class_="pb-4 pt-2",
                justify="center",
                children=[
                    self.objective_selection
                ],
            )
        ])


        self.ar_design_var_checkbox = v.Checkbox(
            class_="ms-4",
            v_model=True,
            label="Wing AR as design variable",
        )
        
        self.ar_design_var_input = RangeSliderInput(
            min=5,
            max=30,
            step=1,
            range=[self.opt_ar_min, self.opt_ar_max],
            label="Min/Max AR_w",
            tooltip="Range of aspect ratio for the optimisation [-]",
        )

        self.sweep_w_design_var_checkbox = v.Checkbox(
            class_="ms-4",
            v_model=True,
            label="Wing sweep as design variable",
        )

        # TODO
        # Implement following functions with new widgets
        
        def ensure_one_design_var(widget, event, data):
            # If we un-tick the bow and the other box is un-ticked, we force the other box to be
            # ticked
            if not data:
                if widget == self.sweep_w_design_var_checkbox:
                    if not self.ar_design_var_checkbox.v_model:
                        self.ar_design_var_checkbox.v_model = True
                else:
                    if not self.sweep_w_design_var_checkbox.v_model:
                        self.sweep_w_design_var_checkbox.v_model = True

        self.sweep_w_design_var_checkbox.on_event("change", ensure_one_design_var)
        self.ar_design_var_checkbox.on_event("change", ensure_one_design_var)


        self.sweep_w_design_var_input = RangeSliderInput(
            min=5,
            max=50,
            step=1,
            range=[self.opt_sweep_w_min, self.opt_sweep_w_max],
            label="Sweep Range",
            tooltip="range of wing sweep angle for the optimisation [-]",
        )
        
        self.design_var_inputs = Inputs("Design variables", [
            self.ar_design_var_checkbox,
            self.ar_design_var_input,
            self.sweep_w_design_var_checkbox,
            self.sweep_w_design_var_input,
        ])


        self.wing_span_constraints_checkbox = v.Checkbox(
            input_value=False,
            label="Wing span as a constraint",
        )

        self.wing_span_constraint_max = SliderInput(
            min=20., 
            max=100., 
            step=0.01, 
            value=self.opt_wing_span_max,
            label="Max b_w", 
            tooltip="Maximum wing span allowed for the optimisation [m]"
        )

        self.constraints_inputs = Inputs("Constraints", [
            self.wing_span_constraint_max,
        ])
        

        self.mdo_input_box_widget.children = [
            v.Card(
                children=[
                    self.debug,
                    self.objectives_inputs,
                    self.design_var_inputs,
                    self.constraints_inputs,    
                ],
            ),
        ]

        ############################################################################################

        # This value for the height will only work for that particular definition of the back
        # image. Which means it is not generic enough. If no height is specified however the
        # widget will be too big for its container which is not very pretty.
        residuals_visualization_layout = go.Layout(height=550)

        base_scatter = go.Scatter(x=[], y=[], name="Relative error")
        residuals_norm_scatter = go.Scatter(x=[], y=[], mode="lines", name="Threshold")

        self.residuals_visualization_figure = go.Figure(
            data=[base_scatter, residuals_norm_scatter],
            layout=residuals_visualization_layout,
        )
        self.residuals_visualization_figure.update_yaxes(
            title_text="Relative value of residuals", type="log", range=[-7.0, 1.0]
        )
        self.residuals_visualization_figure.update_xaxes(
            title_text="Number of iterations"
        )
        self.residuals_visualization_figure.update_layout(
            title_text="Evolution of the residuals", title_x=0.5
        )

        self.residuals_visualization_widget = go.FigureWidget(
            self.residuals_visualization_figure
        )
        
        # Residuals visualization box
        self.graph_visualization_box = v.Row(
            justify="center",
            children=[
                self.residuals_visualization_widget,
            ],
        )

        objective_scatter = go.Scatter(x=[], y=[], name="Objective")
        optimized_value_scatter = go.Scatter(
            x=[], y=[], mode="lines", name="Optimized value"
        )

        self.objectives_visualization_figure = go.Figure(
            data=[objective_scatter, optimized_value_scatter],
            layout=residuals_visualization_layout,
        )
        self.objectives_visualization_figure.update_yaxes(
            title_text="Objective value",
        )
        self.objectives_visualization_figure.update_xaxes(
            title_text="Number of function calls"
        )
        self.objectives_visualization_figure.update_layout(
            title_text="Evolution of the objective", title_x=0.5
        )

        self.objectives_visualization_widget = go.FigureWidget(
            self.objectives_visualization_figure
        )

        ############################################################################################
        self.n2_visualization_widget = _image_from_path(
            self.n2_image_path, height="100vh", width="100"
        )

        ############################################################################################
        self.xdsm_visualization_widget = _image_from_path(
            self.xdsm_image_path, height="100vh", width="100"
        )

        ############################################################################################
        # Launch box

        self.launch_box_and_visualization_widget = v.Col()

        # Text box to give a name to the run
        self.process_name_widget = v.TextField(
            outlined=True,
            hide_details=True,
            label="Sizing name",
            placeholder="Write a name for your sizing process",
        )

        def update_sizing_process_name(widget, event, data):
            self.sizing_process_name = data

        self.process_name_widget.on_event("change", update_sizing_process_name)

        # Create a button to launch the sizing
        self.launch_button_widget = v.Btn(
            block=True,
            color="#32cd32",
            width="31%",
            children=[
                v.Icon(class_="px-3", children=["fa-plane"]),
                "Launch sizing process"
            ],
        )

        # Create a button to trigger the MDO "mode"
        self.mdo_selection_widget = v.Switch(
            v_model=False,
            class_="mt-0 pt-2",
            label="MDO",
            tooltip="Check that box to swap in optimization mode",
        )

        self.launch_box = v.Container(
            fluid=True,
            class_="pe-7",
            children=[
                v.Row(children=[self.process_name_widget]),
                v.Row(
                    children=[
                        v.Col(children=[self.mdo_selection_widget]),
                        v.Col(class_="px-0", cols=10, children=[self.launch_button_widget]),
                    ],
                ),
            ],
        )
        
        self.display_selection_widget = v.Row(
            class_="pb-4 pt-2",
            justify="center",
            children=[
                v.BtnToggle(
                    v_model="toggle_one",
                    mandatory=True,
                    children=[
                        SelectionButton("Residuals", tooltip="Displays a graph of the evolution of residuals with the number of iterations"), 
                        SelectionButton("N2", tooltip="Displays the N2 diagram of the sizing process"),
                        SelectionButton("N2 (browser)", tooltip="Displays the N2 diagram of the sizing process in a new browser tab"),
                        SelectionButton("XDSM", tooltip="Displays the XDSM diagram of the sizing process"),
                        SelectionButton("XDSM (browser)", tooltip="Displays the XDSM diagram of the sizing process in a new browser tab"),
                    ],
                ),
            ],
        )


        def display_graph(change):

            if change["new"] == "Residuals":

                # It looks like the fact that we switch back and forth between image
                # automatically resizes this FigureWidget so we'll ensure that the layout remains
                # consistent. Additionally, we have to resize before displaying or else,
                # for some reasons, the figure is suddenly too big every other time ...
                self.residuals_visualization_widget.update_layout(
                    dict(height=550, autosize=None)
                )
                self.graph_visualization_box.children = [
                    self.residuals_visualization_widget
                ]

            elif change["new"] == "N2":

                self.graph_visualization_box.children = [self.n2_visualization_widget]

            elif change["new"] == "N2 (browser)":

                webbrowser.open_new_tab(self.n2_file_path)

            elif change["new"] == "XDSM":

                self.graph_visualization_box.children = [self.xdsm_visualization_widget]

            else:

                webbrowser.open_new_tab(self.xdsm_file_path)

        self.display_selection_widget.observe(display_graph, names="value")

        self.launch_box_and_visualization_widget.children = [
            self.launch_box,
            self.graph_visualization_box,
            self.display_selection_widget,
        ]

        self.children = [
            v.Row(
                children=[
                    self.input_box,
                    self.launch_box_and_visualization_widget,
                ]
            )
        ]

        def update_input_box(widget, event, data):

            # For some reason checking the box resizes the residuals graph, this should prevent
            # it Additionally, we have to resize before displaying or else, for some reasons,
            # the figure is suddenly too big every other time ...
            self.residuals_visualization_widget.update_layout(
                dict(height=550, autosize=None)
            )
            self.objectives_visualization_widget.update_layout(
                dict(height=550, autosize=None)
            )

            current_children = self.graph_visualization_box.children[0]
            self.graph_visualization_box.children = [current_children]

            # We are in MDO mode
            if data:
                # Unfortunately the getter of the "children" attribute returns 
                # a copy of the children list, so a new one has to be given
                self.children[0].children = [
                    self.mdo_input_box_widget, 
                    self.launch_box_and_visualization_widget
                ]
                self.launch_button_widget.children =[
                    v.Icon(class_="px-3", children=["fa-plane"]),
                    "Launch optimization process",
                ]
                self.process_name_widget.label = "Opimization name"
                self.process_name_widget.placeholder = "Write a name for your optimization process"

            else:
                self.children[0].children = [
                    self.input_box, 
                    self.launch_box_and_visualization_widget
                ]
                self.launch_button_widget.children =[
                    v.Icon(class_="px-3", children=["fa-plane"]),
                    "Launch sizing process",
                ]
                self.process_name_widget.label = "Sizing name"
                self.process_name_widget.placeholder = "Write a name for your sizing process"

        self.mdo_selection_widget.on_event("change", update_input_box)

    def set_initial_value_mda(self):
        """
        Set the value of the attributes that store the variable for the MDA based on their value
        in the reference inputs.
        """

        # Should also recreate the widget so that they appear with the proper initial value ?

        # No need to convert to alternate units
        self.n_pax = self.reference_inputs["data:TLAR:NPAX"].value[0]
        # Convert in kts in case it was not
        self.v_app = om.convert_units(
            self.reference_inputs["data:TLAR:approach_speed"].value[0],
            self.reference_inputs["data:TLAR:approach_speed"].units,
            "kn",
        )
        self.cruise_mach = self.reference_inputs["data:TLAR:cruise_mach"].value[0]
        # Convert in nm in case it was not, etc, etc, ...
        self.range = om.convert_units(
            self.reference_inputs["data:TLAR:range"].value[0],
            self.reference_inputs["data:TLAR:range"].units,
            "NM",
        )
        self.payload = om.convert_units(
            self.reference_inputs["data:weight:aircraft:payload"].value[0],
            self.reference_inputs["data:weight:aircraft:payload"].units,
            "kg",
        )
        self.max_payload = om.convert_units(
            self.reference_inputs["data:weight:aircraft:max_payload"].value[0],
            self.reference_inputs["data:weight:aircraft:max_payload"].units,
            "kg",
        )
        self.wing_aspect_ratio = self.reference_inputs[
            "data:geometry:wing:aspect_ratio"
        ].value[0]
        self.bpr = self.reference_inputs[
            "data:propulsion:rubber_engine:bypass_ratio"
        ].value[0]
