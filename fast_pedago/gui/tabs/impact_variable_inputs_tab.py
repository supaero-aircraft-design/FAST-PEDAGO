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
            cols=12,
            md=4,
        )
        
        ########################################
        #TODO
        # Implement tooltip
        class SliderInput(v.VuetifyTemplate):
            min = traitlets.Float(default_value=0).tag(sync=True)
            max = traitlets.Float(default_value=100).tag(sync=True)
            step = traitlets.Float(default_value=10).tag(sync=True)
            label = traitlets.Unicode(default_value=None, allow_none=True).tag(sync=True)
            tooltip = traitlets.Unicode(default_value=None, allow_none=True).tag(sync=True)
            value = traitlets.Unicode(default_value=None, allow_none=True).tag(sync=True)
            @traitlets.default('template')
            def _template(self):
                return f'''
                <template>
                    <v-slider
                        v-model="value"
                        class="align-center"
                        label={self.label}
                        :max="max"
                        :min="min"
                        :step="step"
                        hide-details
                    >
                        <template v-slot:append>
                            <v-text-field
                                v-model="value"
                                class="mt-0 pt-0"
                                variant="outlined"
                                density="compact"
                                hide-details
                                single-line
                                type="number"
                                style="width: 60px"
                            >
                            </v-text-field>
                        </template>
                    </v-slider>
                </template>
                ''' + '''
                <script>
                    export default {
                        methods: {
                            decrement () {
                                this.value--
                            },
                            increment () {
                                this.value++
                            },
                        },
                    }
                </script>
                '''

        self.n_pax_input = SliderInput(min=19,max=500, step=1, label="N_PAX", tooltip="Number of passengers")
        self.v_app_input = SliderInput(min=45., max=200., step=0.1, label="V_app", tooltip="Approach speed [kts]")
        self.cruise_mach_input = SliderInput(min=0., max=1., step=0.01, label="M_cruise", tooltip="Cruise mach")
        self.range_input = SliderInput(min=0, max=10000, step=100, label="Range", tooltip="Aircraft range [NM]")
        self.payload_input = SliderInput(min=0, max=100000, step=10, label="Payload", tooltip="Aircraft payload [kg]")
        self.max_payload_input = SliderInput(min=0, max=100000, step=10, label="Max Payload", tooltip="Aircraft max payload [kg]")
        self.wing_aspect_ratio_input = SliderInput(min=4., max=25., step=0.1, label="AR_w", tooltip="Aspect Ratio of the wing")
        self.bpr_input = SliderInput(min=0, max=25., step=0.1, label="BPR", tooltip="ByPass Ratio of the engine")



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
        class Inputs(v.Card):
            def __init__(self, name, inputs=[], **kwargs):
                super().__init__(**kwargs)
                
                self.children=[
                    v.CardTitle(
                        children=[name]
                    ),
                ] + inputs
            
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
            self.TLAR_inputs,
            self.weight_inputs,
            self.geometry_inputs,
            self.propulsion_inputs,
        ]

        ############################################################################################
        # We also create a bow specific for launching an MDO which will only consists of selecting
        # the objectives and the bounds for the design variables
        # Input box
        self.mdo_input_box_widget = widgets.VBox()
        self.mdo_input_box_widget.layout = widgets.Layout(
            width="33%",
            align_items="center",
            border="2px solid black",
        )
        
        # FIXME 
        # Tooltip doesn't work
        class SelectionButton(v.Btn):
            def __init__(self, name, tooltip, **kwargs):
                super().__init__(**kwargs)

                self.children=[
                    name,
                    v.Tooltip(
                        activator="parent",
                        location="top",
                        children=tooltip,
                    ),
                ]
        

        self.objective_selection = v.BtnToggle(
            v_model="toggle_exclusive",
            children=[
                SelectionButton("Fuel sizing", tooltip="Minimize the aircraft fuel consumption on the design mission"), 
                SelectionButton("MTOW", tooltip="Minimize the aircraft MTOW"),
                SelectionButton("OWE", tooltip="Minimize the aircraft OWE"),
            ],
        )
        
        self.objectives_inputs = Inputs("Objective", [self.objective_selection])


        self.ar_design_var_checkbox = v.Checkbox(
            input_value=True,
            label="Wing AR as design variable",
        )
        
        self.ar_design_var_slider = v.RangeSlider(
            min=5.0,
            max=30.0,
            step=0.1,
            thumb_label="always",
            label="Min/Max AR_w",
            tooltip="Range of aspect ratio for the optimisation [-]",
        )

        self.sweep_w_design_var_checkbox = v.Checkbox(
            input_value=True,
            label="Wing sweep as design variable",
        )

        # TODO
        # Implement following functions with new widgets
        
        def ensure_one_design_var_sweep_w(change):
            # If we un-tick the bow and the other box is un-ticked, we force the other box to be
            # ticked
            if not change["new"] and not self.ar_design_var_checkbox.value:
                self.ar_design_var_checkbox.value = True

        self.sweep_w_design_var_checkbox.observe(
            ensure_one_design_var_sweep_w, names="value"
        )

        def ensure_one_design_var_ar_w(change):
            # If we un-tick the bow and the other box is un-ticked, we force the other box to be
            # ticked
            if not change["new"] and not self.sweep_w_design_var_checkbox.value:
                self.sweep_w_design_var_checkbox.value = True

        self.ar_design_var_checkbox.observe(ensure_one_design_var_ar_w, names="value")


        self.sweep_w_design_var_slider = v.RangeSlider(
            min=5.0,
            max=50.0,
            step=0.01,
            thumb_label="always",
            label="Sweep Range",
            tooltip="range of wing sweep angle for the optimisation [-]",
        )
        
        self.design_var_inputs = Inputs("Design variables", [
            self.ar_design_var_checkbox,
            self.ar_design_var_slider,
            self.sweep_w_design_var_checkbox,
            self.sweep_w_design_var_slider,
        ])


        self.wing_span_constraints_checkbox = v.Checkbox(
            input_value=False,
            label="Wing span as a constraint",
        )

        self.wing_span_constraint_max = SliderInput(
            min=20., 
            max=100., 
            step=0.01, 
            label="Max b_w", 
            tooltip="Maximum wing span allowed for the optimisation [m]"
        )

        self.constraints_inputs = Inputs("Constraints", [
            self.wing_span_constraint_max,
        ])
        

        self.mdo_input_box_widget.children = [
            self.objectives_inputs,
            self.design_var_inputs,
            self.constraints_inputs,
        ]

        ############################################################################################
        # Residuals visualization box
        self.graph_visualization_box = widgets.VBox(
            layout=widgets.Layout(
                height="550px", justify_content="center", align_items="center"
            )
        )

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
        self.graph_visualization_box.children = [self.residuals_visualization_widget]

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
            self.n2_image_path, height="", width="95%"
        )

        ############################################################################################
        self.xdsm_visualization_widget = _image_from_path(
            self.xdsm_image_path, height="", width="95%"
        )

        ############################################################################################
        # Launch box

        self.launch_box_and_visualization_widget = widgets.VBox()

        self.launch_box = widgets.HBox()

        # Text box to give a name to the run
        self.process_name_widget = widgets.Text(
            description="Sizing name",
            placeholder="Write a name for your sizing process",
            tooltip="Name of the sizing process",
        )
        self.process_name_widget.layout = widgets.Layout(
            width="50%",
            height="auto",
            justify_content="space-between",
            align_items="flex-start",
        )

        def update_sizing_process_name(change):
            self.sizing_process_name = change["new"]

        self.process_name_widget.observe(update_sizing_process_name, names="value")

        # Create a button to launch the sizing
        self.launch_button_widget = widgets.Button(description="Launch sizing process")
        self.launch_button_widget.icon = "fa-plane"
        self.launch_button_widget.layout = widgets.Layout(width="31%", height="auto")
        self.launch_button_widget.style.button_color = "GreenYellow"

        # Create a button to trigger the MDO "mode"
        self.mdo_selection_widget = widgets.ToggleButton(
            value=False,
            description="MDO",
            icon="check",
            tooltip="Check that box to swap in optimization mode",
        )
        self.mdo_selection_widget.layout = widgets.Layout(
            width="10%",
            height="auto",
        )

        # Add a filler box to force the buttons on the bottom and so that the picture appear clearly
        self.filler_box = widgets.Box(
            layout=widgets.Layout(
                width="3%",
                height="auto",
            ),
        )

        self.launch_box.children = [
            self.filler_box,
            self.process_name_widget,
            self.launch_button_widget,
            self.filler_box,
            self.mdo_selection_widget,
        ]

        self.launch_box.layout = widgets.Layout(
            width="100%",
            height="50px",
            justify_content="center",
            align_items="center",
        )

        self.display_selection_widget = widgets.ToggleButtons(
            options=["Residuals", "N2", "N2 (browser)", "XDSM", "XDSM (browser)"],
            disabled=False,
            button_style="",  # 'success', 'info', 'warning', 'danger' or ''
            tooltips=[
                "Displays a graph of the evolution of residuals with the number of iterations",
                "Displays the N2 diagram of the sizing process",
                "Displays the N2 diagram of the sizing process in a new browser tab",
                "Displays the XDSM diagram of the sizing process",
                "Displays the XDSM diagram of the sizing process in a new browser tab",
            ],
            style={"button_width": "120px"},
        )

        self.display_selection_widget.layout = widgets.Layout(
            width="98%",
            height="50px",
            justify_content="center",
            align_items="center",
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

        self.launch_box_and_visualization_widget.layout = widgets.Layout(
            width="66%",
            justify_content="flex-start",
            border="2px solid black",
        )

        self.children = [
            self.input_box,
            self.launch_box_and_visualization_widget,
        ]

        def update_input_box(event):

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
            if event["new"]:
                self.children = [
                    self.mdo_input_box_widget,
                    self.launch_box_and_visualization_widget,
                ]
                self.launch_button_widget.description = "Launch optimization process"

            else:
                self.children = [
                    self.input_box_widget,
                    self.launch_box_and_visualization_widget,
                ]
                self.launch_button_widget.description = "Launch sizing process"

        self.mdo_selection_widget.observe(update_input_box, names="value")

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
