# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import webbrowser

import ipywidgets as widgets

import plotly.graph_objects as go

import openmdao.api as om
import fastoad.api as oad

from fast_pedago.utils.functions import _image_from_path  # noqa

OUTPUT_FILE_SUFFIX = "_output_file.xml"
FLIGHT_DATA_FILE_SUFFIX = "_flight_points.csv"


class ImpactVariableInputLaunchTab(widgets.HBox):
    def __init__(
        self, configuration_file_path: str, reference_input_file_path: str, **kwargs
    ):

        super().__init__(**kwargs)

        self.reference_input_file_path = reference_input_file_path
        self.configuration_file_path = configuration_file_path

        # Read the reference input file path so that we can give first accurate first value. Also
        # save it as an object attribute that we can copy to modify inputs
        self.reference_inputs = oad.DataFile(self.reference_input_file_path)

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

        # Define attribute to store variable value and give them an initial value corresponding
        # to the reference inputs. Also, those are gonna be attribute of the parent HBox so that the
        # children can exchange those information
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
        self.input_box_widget = widgets.VBox()

        self.input_widget_layout = widgets.Layout(
            width="95%",
            height="50px",
            justify_content="space-between",
            align_items="center",
        )

        # Create the widgets to change the value of the parameters in the sensitivity analysis,
        # which entails: create the widget, create the function to update the input and on_click
        # that function
        self.n_pax_input_widget = widgets.BoundedFloatText(
            min=19.0,
            max=500.0,
            step=1.0,
            value=self.n_pax,
            description="N_PAX",
            description_tooltip="Number of Passengers",
            layout=self.input_widget_layout,
        )

        def update_n_pax(change):
            self.n_pax = change["new"]

        self.n_pax_input_widget.observe(update_n_pax, names="value")

        self.v_app_input_widget = widgets.BoundedFloatText(
            min=45.0,
            max=200.0,
            step=0.1,
            value=self.v_app,
            description="V_app",
            description_tooltip="Approach speed [kts]",
            layout=self.input_widget_layout,
        )

        def update_v_app(change):
            self.v_app = change["new"]

        self.v_app_input_widget.observe(update_v_app, names="value")

        self.cruise_mach_input_widget = widgets.BoundedFloatText(
            min=0.0,
            max=1.0,
            step=0.01,
            value=self.cruise_mach,
            description="M_cruise",
            description_tooltip="Cruise mach",
            layout=self.input_widget_layout,
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

        self.range_input_widget = widgets.BoundedFloatText(
            min=0.0,
            max=10000.0,
            step=100.0,
            value=self.range,
            description="Range",
            description_tooltip="Aircraft range [nm]",
            layout=self.input_widget_layout,
        )

        def update_range(change):
            self.range = change["new"]

        self.range_input_widget.observe(update_range, names="value")

        self.payload_input_widget = widgets.BoundedFloatText(
            min=0.0,
            max=100000.0,
            step=10.0,
            value=self.payload,
            description="Payload",
            description_tooltip="Aircraft payload [kg]",
            layout=self.input_widget_layout,
        )

        def update_payload(change):
            self.payload = change["new"]

        self.payload_input_widget.observe(update_payload, names="value")

        self.max_payload_input_widget = widgets.BoundedFloatText(
            min=0.0,
            max=100000.0,
            step=10.0,
            value=self.max_payload,
            description="Max Payload",
            description_tooltip="Aircraft max payload [kg]",
            layout=self.input_widget_layout,
        )

        def update_max_payload(change):
            self.max_payload = change["new"]

        self.max_payload_input_widget.observe(update_max_payload, names="value")

        self.wing_aspect_ratio_input_widget = widgets.BoundedFloatText(
            min=4.0,
            max=25.0,
            step=0.1,
            value=self.wing_aspect_ratio,
            description="AR_w",
            description_tooltip="Aspect Ratio of the wing",
            layout=self.input_widget_layout,
        )

        def update_wing_aspect_ratio(change):
            self.wing_aspect_ratio = change["new"]

        self.wing_aspect_ratio_input_widget.observe(
            update_wing_aspect_ratio, names="value"
        )

        self.bpr_input_widget = widgets.BoundedFloatText(
            min=0.0,
            max=25.0,
            step=0.1,
            value=self.bpr,
            description="BPR",
            description_tooltip="ByPass Ratio of the engine",
            layout=self.input_widget_layout,
        )

        def update_bpr(change):
            self.bpr = change["new"]

        self.bpr_input_widget.observe(update_bpr, names="value")
        self.text_box_layout = widgets.Layout(align_items="center")

        self.text_box_TLAR = widgets.VBox()
        self.text_box_TLAR.children = [widgets.HTML(value="<u>TLARs</u>")]
        self.text_box_TLAR.layout = self.text_box_layout

        self.text_box_weight = widgets.VBox()
        self.text_box_weight.children = [widgets.HTML(value="<u>Weight</u>")]
        self.text_box_weight.layout = self.text_box_layout

        self.text_box_geometry = widgets.VBox()
        self.text_box_geometry.children = [widgets.HTML(value="<u>Geometry</u>")]
        self.text_box_geometry.layout = self.text_box_layout

        self.text_box_propulsion = widgets.VBox()
        self.text_box_propulsion.children = [widgets.HTML(value="<u>Propulsion</u>")]
        self.text_box_propulsion.layout = self.text_box_layout

        self.input_box_widget.children = [
            self.text_box_TLAR,
            self.n_pax_input_widget,
            self.v_app_input_widget,
            self.cruise_mach_input_box,
            self.range_input_widget,
            self.text_box_weight,
            self.payload_input_widget,
            self.max_payload_input_widget,
            self.text_box_geometry,
            self.wing_aspect_ratio_input_widget,
            self.text_box_propulsion,
            self.bpr_input_widget,
        ]
        self.input_box_widget.layout = widgets.Layout(
            width="33%",
            justify_content="flex-start",
            border="2px solid black",
        )

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

        self.text_box_objectives = widgets.VBox()
        self.text_box_objectives.children = [widgets.HTML(value="<u>Objective</u>")]
        self.text_box_objectives.layout = self.text_box_layout

        self.objective_selection_widget = widgets.ToggleButtons(
            options=["Fuel sizing", "MTOW"],
            disabled=False,
            tooltips=[
                "Minimize the aircraft fuel consumption on the design mission",
                "Minimize the aircraft MTOW",
            ],
            style=widgets.ToggleButtonsStyle(button_width="160px"),
        )
        self.objective_selection_widget.layout = widgets.Layout(
            width="95%", height="50px", justify_content="center"
        )

        self.text_box_design_var = widgets.VBox()
        self.text_box_design_var.children = [
            widgets.HTML(value="<u>Design variables</u>")
        ]
        self.text_box_design_var.layout = self.text_box_layout

        self.ar_design_var_checkbox = widgets.Checkbox(
            value=True,
            description="Wing AR as design variable",
            disabled=False,
            indent=False,
            style={"description_width": "initial"},
        )
        self.ar_design_var_checkbox.layout = widgets.Layout(
            width="95%",
            height="50px",
            align_items="center",
        )

        self.ar_design_var_min_widget = widgets.BoundedFloatText(
            min=5.0,
            max=30.0,
            step=0.1,
            value=self.opt_ar_min,
            description="Min AR_w",
            description_tooltip="Minimum aspect ratio for the optimisation [-]",
            layout=self.input_widget_layout,
        )

        def update_ar_min(change):

            if change["new"] > self.opt_ar_max:
                self.ar_design_var_min_widget.value = self.opt_ar_max
            else:
                self.opt_ar_min = change["new"]

        self.ar_design_var_min_widget.observe(update_ar_min, names="value")

        self.ar_design_var_max_widget = widgets.BoundedFloatText(
            min=5.0,
            max=30.0,
            step=0.1,
            value=self.opt_ar_max,
            description="Max AR_w",
            description_tooltip="Maximum aspect ratio for the optimisation [-]",
            layout=self.input_widget_layout,
        )

        def update_ar_max(change):

            if change["new"] < self.opt_ar_min:
                self.ar_design_var_max_widget.value = self.opt_ar_min
            else:
                self.opt_ar_max = change["new"]

        self.ar_design_var_max_widget.observe(update_ar_max, names="value")

        self.sweep_w_design_var_checkbox = widgets.Checkbox(
            value=False,
            description="Wing sweep as design variable",
            disabled=False,
            indent=False,
            style={"description_width": "initial"},
        )
        self.sweep_w_design_var_checkbox.layout = widgets.Layout(
            width="95%",
            height="50px",
            align_items="center",
        )

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

        self.sweep_w_design_var_min_widget = widgets.BoundedFloatText(
            min=5.0,
            max=50.0,
            step=0.01,
            value=self.opt_sweep_w_min,
            description="Min Sweep",
            description_tooltip="Minimum wing sweep angle for the optimisation [-]",
            layout=self.input_widget_layout,
        )

        def update_sweep_w_min(change):

            if change["new"] > self.opt_sweep_w_max:
                self.sweep_w_design_var_min_widget.value = self.opt_sweep_w_max
            else:
                self.opt_sweep_w_min = change["new"]

        self.sweep_w_design_var_min_widget.observe(update_sweep_w_min, names="value")

        self.sweep_w_design_var_max_widget = widgets.BoundedFloatText(
            min=5.0,
            max=50.0,
            step=0.01,
            value=self.opt_sweep_w_max,
            description="Max Sweep",
            description_tooltip="Maximum wing sweep angle for the optimisation [-]",
            layout=self.input_widget_layout,
        )

        def update_sweep_w_max(change):
            if change["new"] < self.opt_sweep_w_min:
                self.sweep_w_design_var_max_widget.value = self.opt_sweep_w_min
            else:
                self.opt_sweep_w_max = change["new"]

        self.sweep_w_design_var_max_widget.observe(update_sweep_w_max, names="value")

        self.text_box_constraints = widgets.VBox()
        self.text_box_constraints.children = [widgets.HTML(value="<u>Constraints</u>")]
        self.text_box_constraints.layout = self.text_box_layout

        self.wing_span_constraints_checkbox = widgets.Checkbox(
            value=False,
            description="Wing span as a constraint",
            disabled=False,
            indent=False,
            style={"description_width": "initial"},
        )
        self.wing_span_constraints_checkbox.layout = widgets.Layout(
            width="95%",
            height="50px",
            align_items="center",
        )

        self.wing_span_constraint_max_widget = widgets.BoundedFloatText(
            min=20.0,
            max=100.0,
            step=0.01,
            value=self.opt_wing_span_max,
            description="Max b_w",
            description_tooltip="Maximum wing span allowed for the optimisation [m]",
            layout=self.input_widget_layout,
        )

        def update_wing_span_max(change):
            self.opt_wing_span_max = change["new"]

        self.wing_span_constraint_max_widget.observe(
            update_wing_span_max, names="value"
        )

        self.mdo_input_box_widget.children = [
            self.text_box_objectives,
            self.objective_selection_widget,
            self.text_box_design_var,
            self.ar_design_var_checkbox,
            self.ar_design_var_min_widget,
            self.ar_design_var_max_widget,
            self.sweep_w_design_var_checkbox,
            self.sweep_w_design_var_min_widget,
            self.sweep_w_design_var_max_widget,
            self.text_box_constraints,
            self.wing_span_constraints_checkbox,
            self.wing_span_constraint_max_widget,
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
            title_text="Relative value of residuals", type="log", range=[-10.0, 1.0]
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
                "Displays a graph of the evolution of residulas with the number of iterations",
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
            self.input_box_widget,
            self.launch_box_and_visualization_widget,
        ]

        def update_input_box(event):

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
