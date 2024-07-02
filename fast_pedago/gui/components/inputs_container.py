# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipyvuetify as v

from fast_pedago.processes import MDAMDOLauncher
from .input_widgets import (
    Snackbar,
    SliderInput,
    RangeSliderInput,
)
from fast_pedago.utils import (
    _InputsCategory,
)


DEFAULT_PROCESS_NAME = "aircraft"

# Min and max values for sliders input values
OPT_AR_MIN = 9.0
OPT_AR_MAX = 18.0

OPT_SWEEP_W_MIN = 10.0
OPT_SWEEP_W_MAX = 45.0

OPT_WING_SPAN_MAX = 60.0


class InputsContainer(v.List):
    """
    An input container that can switch to set inputs for MDA and MDO.
    """
    def __init__(self, process_launcher: MDAMDOLauncher, **kwargs):
        """
        :param source_data_file: the path to the source file to initialize the inputs from.
        """
        super().__init__(**kwargs)
        
        self.process_launcher = process_launcher
        
        self.class_ = "pa-0"
        self.expand = True
        
        self._set_layout_mda()
        self._set_layout_mdo()
        
        self._build_layout()
        
        self.to_MDA()
    
    
    def to_MDO(self):
        """
        Changes inputs to MDO inputs
        """
        self.children = [self.inputs_header] + self.mdo_input
        self.launch_button.children =[
            v.Icon(class_="px-3", children=["fa-plane"]),
            "Launch optimization",
        ]
        self.process_name_field.label = "Opimization name"
        self.process_name_field.placeholder = "Write a name for your optimization process"


    def to_MDA(self):
        """
        Changes inputs to MDA inputs
        """
        self.children = [self.inputs_header] + self.mda_input
        self.launch_button.children =[
            v.Icon(class_="px-3", children=["fa-plane"]),
            "Launch sizing",
        ]
        self.process_name_field.label = "Sizing name"
        self.process_name_field.placeholder = "Write a name for your sizing process"


    def retrieve_mda_inputs(self):
        """
        Retrieves inputs from the MDA input widgets
        """
        self.process_launcher.set_mda_inputs(
            n_pax=self.n_pax_input.slider.v_model,
            v_app=self.v_app_input.slider.v_model,
            cruise_mach=self.cruise_mach_input.slider.v_model,
            range=self.range_input.slider.v_model,
            payload=self.payload_input.slider.v_model,
            max_payload=self.max_payload_input.slider.v_model,
            wing_aspect_ratio=self.wing_aspect_ratio_input.slider.v_model,
            bypass_ratio=self.bpr_input.slider.v_model
        )


    def retrieve_mdo_inputs(self):
        """
        Retrieves inputs from the MDO input widgets
        """
        self.process_launcher.set_mdo_inputs(
            objective=self.objective_selection.v_model,
            is_aspect_ratio_design_variable=self.ar_design_var_checkbox.v_model,
            aspect_ratio_lower_bound=self.ar_design_var_input.slider.v_model[0],
            aspect_ratio_upper_bound=self.ar_design_var_input.slider.v_model[1],
            is_wing_sweep_design_variable=self.sweep_w_design_var_checkbox.v_model,
            wing_sweep_lower_bound=self.sweep_w_design_var_input.slider.v_model[0],
            wing_sweep_upper_bound=self.sweep_w_design_var_input.slider.v_model[1],
            is_wing_span_constrained=self.wing_span_constraints_checkbox.v_model,
            wing_span_upper_bound=self.wing_span_constraint_max.slider.v_model,
        )


    def set_initial_value_mda(self, source_data_file_name: str):
        """
        Set the value of the attributes that store the variable for the MDA based on their value
        in the reference inputs.
        
        Also save the source file inputs as an object attribute that we can copy to modify inputs
        
        :param source_data_file_name: the source file to read data from
        """
        reference_inputs = self.process_launcher.get_reference_inputs(source_data_file_name)
        self.n_pax_input.slider.v_model = reference_inputs[0]
        self.v_app_input.slider.v_model = reference_inputs[1]
        self.cruise_mach_input.slider.v_model = reference_inputs[2]
        self.range_input.slider.v_model = reference_inputs[3]
        self.payload_input.slider.v_model = reference_inputs[4]
        self.max_payload_input.slider.v_model = reference_inputs[5]
        self.wing_aspect_ratio_input.slider.v_model = reference_inputs[6]
        self.bpr_input.slider.v_model = reference_inputs[7]


    def _build_layout(self):
        self.process_name = DEFAULT_PROCESS_NAME
        
        # Text box to give a name to the run
        self.process_name_field = v.TextField(
            outlined=True,
            hide_details=True,
            dense=True,
            label="Sizing name",
            placeholder="Write a name for your sizing process",
        )
        self.process_name_field.on_event("change", self._update_process_name)

        # Create a button to launch the sizing
        self.launch_button = v.Btn(
            block=True,
            color="#32cd32",
            children=[
                v.Icon(class_="px-3", children=["fa-plane"]),
                "Launch sizing"
            ],
        )
        # Create a button to trigger the MDO "mode"
        self.process_selection_switch = v.BtnToggle(
            rounded=True,
            mandatory=True,
            dense=True,
            children=[
                v.Btn(
                    v_bind='tooltip.attrs',
                    v_on='tooltip.on',
                    children=["MDA"]
                ),
                v.Btn(
                    v_bind='tooltip.attrs',
                    v_on='tooltip.on',
                    children=["MDO"])
            ],
        )


        self.inputs_header = v.ListItemGroup(
            class_="px-2",
            children=[
                v.Row(
                    align="center",
                    children=[
                        v.Col(
                            cols=4,
                            children=[
                               v.Tooltip(
                                    contained=True,
                                    v_slots=[{
                                        'name': 'activator',
                                        'variable': 'tooltip',
                                        'children': self.process_selection_switch,
                                    }],
                                    children=["Swap between analysis and optimisation mode"],
                                ), 
                            ],
                        ),
                        v.Col(
                            cols=8,
                            children=[self.launch_button],
                        ),
                    ],
                ),
                v.Row(
                    class_="px-3",
                    align="center",
                    justify="center",
                    children=[self.process_name_field],
                ),
            ],
        )

   
    def _set_layout_mdo(self):
        """
        Generates the layout for the MDO inputs
        """
        self.objective_selection = v.BtnToggle(
            v_model="toggle_exclusive",
            mandatory=True,
            children=[
                v.Btn(
                    v_bind='tooltip.attrs',
                    v_on='tooltip.on',
                    children=["Fuel sizing"],
                ),
                v.Btn(
                    v_bind='tooltip.attrs',
                    v_on='tooltip.on',
                    children=["MTOW"],
                ),
                v.Btn(
                    v_bind='tooltip.attrs',
                    v_on='tooltip.on',
                    children=["OWE"],
                ),
            ],
        )
        
        
        # Checkboxes to chose which design variable and
        # constraints to use
        self.ar_design_var_checkbox = v.Checkbox(
            class_="ms-4",
            v_model=True,
            label="Wing AR as design variable",
        )
        self.sweep_w_design_var_checkbox = v.Checkbox(
            class_="ms-4",
            v_model=False,
            label="Wing sweep as design variable",
        )
        self.wing_span_constraints_checkbox = v.Checkbox(
            input_value=False,
            label="Wing span as a constraint",
        )
        self.sweep_w_design_var_checkbox.on_event("change", self._ensure_one_design_var)
        self.ar_design_var_checkbox.on_event("change",self. _ensure_one_design_var)
        
        # Range sliders to input design variables and constraints
        self.ar_design_var_input = RangeSliderInput(
            min=5,
            max=30,
            step=1,
            range=[OPT_AR_MIN, OPT_AR_MAX],
            label="Min/Max wing AR",
            tooltip="Range of aspect ratio for the optimization [-]",
        )
        self.sweep_w_design_var_input = RangeSliderInput(
            min=5,
            max=50,
            step=1,
            range=[OPT_SWEEP_W_MIN, OPT_SWEEP_W_MAX],
            label="Sweep Range",
            tooltip="Range of wing sweep angle for the optimization [-]",
        )
        self.wing_span_constraint_max = SliderInput(
            min=20., 
            max=100., 
            step=1, 
            value=OPT_WING_SPAN_MAX,
            label="Max wing span", 
            tooltip="Maximum wing span allowed for the optimization [m]"
        )
        
        

        self.mdo_input = [
            _InputsCategory("Objective", [
                    v.Row(
                        class_="pb-4 pt-2",
                        justify="center",
                        children=[
                            v.Tooltip(
                                contained=True,
                                v_slots=[{
                                    'name': 'activator',
                                    'variable': 'tooltip',
                                    'children': self.objective_selection,
                                }],
                                children=[
                                    "Minimize fuel consumption or MTOW or OWE",
                                ],
                            ),
                        ],
                    )
            ], is_open=True),
            _InputsCategory("Design variables", [
                self.ar_design_var_checkbox,
                self.ar_design_var_input,
                self.sweep_w_design_var_checkbox,
                self.sweep_w_design_var_input,
            ]),
            _InputsCategory("Constraints", [
                self.wing_span_constraints_checkbox,
                self.wing_span_constraint_max,
            ]),    
        ]
        
    
    def _set_layout_mda(self):
        """
        Generates the layout for the MDA inputs
        """
        self.n_pax_input = SliderInput(
            min=20,
            max=400, 
            step=2,
            label="NPAX", 
            tooltip="Number of passengers"
        )
        self.v_app_input = SliderInput(
            min=45, 
            max=170, 
            step=1,
            label="Vapp", 
            tooltip="Approach speed [kts]"
        )
        self.cruise_mach_input = SliderInput(
            min=0., 
            max=1., 
            step=0.01, 
            label="Mcruise", 
            tooltip="Cruise mach"
        )
        self.range_input = SliderInput(
            min=0,
            max=10000, 
            step=100,
            label="Range", 
            tooltip="Aircraft range [NM]"
        )
        self.payload_input = SliderInput(
            min=0, 
            max=100000, 
            step=1000,
            label="Payload", 
            tooltip="Aircraft payload [kg]"
        )
        self.max_payload_input = SliderInput(
            min=0, 
            max=100000, 
            step=1000,
            label="Max Payload", 
            tooltip="Aircraft max payload [kg]"
        )
        self.wing_aspect_ratio_input = SliderInput(
            min=4, 
            max=25, 
            step=1,
            label="Wing AR", 
            tooltip="Aspect Ratio of the wing"
        )
        self.bpr_input = SliderInput(
            min=0, 
            max=25, 
            step=1, 
            label="BPR",
            tooltip="ByPass Ratio of the engine"
        )
        
        # As can be seen in the parent tab, there is an issue when cruise mach gets too high,
        # we will display a warning when that value is reached, informing students of what is
        # done behind the scene
        self.snackbar = Snackbar(
            "The sweep angle of the wing has been adjusted to avoid having compressibility "
            "drag coefficient too high"
        )
        self.cruise_mach_input.slider.on_event("change", self._mach_alert)

        self.mda_input = [
            _InputsCategory("TLARs", [
                self.n_pax_input,
                self.v_app_input,
                self.cruise_mach_input,
                self.range_input,
            ], is_open=True),
            _InputsCategory("Weight", [
                self.payload_input,
                self.max_payload_input,
            ]),
            _InputsCategory("Geometry", [
                self.wing_aspect_ratio_input,
            ]),
            _InputsCategory("Propulsion", [
                self.bpr_input,
            ]),
            self.snackbar,
        ]

    
    def _ensure_one_design_var(self, widget, event, data):
        """
        Ensures that at least one design variable is chosen
        for MDO.
        
        If the user tries to untick a checkbox, the other is ticked
        by default.

        To be called with an "on_event" ipyvuetify component method
        """
        if not data:
            if widget == self.sweep_w_design_var_checkbox:
                if not self.ar_design_var_checkbox.v_model:
                    self.ar_design_var_checkbox.v_model = True
            else:
                if not self.sweep_w_design_var_checkbox.v_model:
                    self.sweep_w_design_var_checkbox.v_model = True


    def _mach_alert(self, widget, event, data):
        # If the mach is above the value of 0.78 and the snackbar is closed, opens
        # the snackbar to alert the user
        if self.cruise_mach_input.slider.v_model > 0.78 and not self.snackbar.v_model:
            self.snackbar.open_or_close(widget, event, data)


    def _update_process_name(self, widget, event, data):
        """
        Changes process name when a new name is written
        in the input text field.

        To be used with a "on_event" of a text field ipyvuetify 
        """
        self.process_name = data


    def disable(self):
        """
        Disables all inputs components
        to let the user know he can't modify inputs.
        """
        self.process_selection_switch.children[0].disabled = True
        self.process_selection_switch.children[1].disabled = True
        self.process_name_field.readonly = True
        self.launch_button.disabled = True
        self.launch_button.color = ("#FF0000")
        
        # MDA inputs
        self.n_pax_input.disable()
        self.v_app_input.disable()
        self.cruise_mach_input.disable()
        self.range_input.disable()
        self.payload_input.disable()
        self.max_payload_input.disable()
        self.wing_aspect_ratio_input.disable()
        self.bpr_input.disable()
        
        # MDO inputs
        self.objective_selection.children[0].disabled = True
        self.objective_selection.children[1].disabled = True
        self.objective_selection.children[2].disabled = True
        self.ar_design_var_checkbox.readonly = True
        self.ar_design_var_input.disable()
        self.sweep_w_design_var_checkbox.readonly = True
        self.sweep_w_design_var_input.disable()
        self.wing_span_constraints_checkbox.readonly = True
        self.wing_span_constraint_max.disable()
    

    def enable(self):
        """
        Re-enables inputs after the end of computation.
        """
        self.process_selection_switch.children[0].disabled = False
        self.process_selection_switch.children[1].disabled = False
        self.process_name_field.readonly = False
        self.launch_button.disabled = False
        self.launch_button.color = ("#32cd32")
        
        # MDA inputs
        self.n_pax_input.enable()
        self.v_app_input.enable()
        self.cruise_mach_input.enable()
        self.range_input.enable()
        self.payload_input.enable()
        self.max_payload_input.enable()
        self.wing_aspect_ratio_input.enable()
        self.bpr_input.enable()
        
        # MDO inputs
        self.objective_selection.children[0].disabled = False
        self.objective_selection.children[1].disabled = False
        self.objective_selection.children[2].disabled = False
        self.ar_design_var_checkbox.readonly = False
        self.ar_design_var_input.enable()
        self.sweep_w_design_var_checkbox.readonly = False
        self.sweep_w_design_var_input.enable()
        self.wing_span_constraints_checkbox.readonly = False
        self.wing_span_constraint_max.enable()