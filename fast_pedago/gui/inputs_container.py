# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import copy

import numpy as np

import ipyvuetify as v

import openmdao.api as om
import fastoad.api as oad

from fast_pedago import source_data_files
from fast_pedago.gui.sliders import (
    SliderInput,
    RangeSliderInput,
)
from fast_pedago.utils import (
    _TooltipButton,
    _InputsCategory,
)


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
    def __init__(self, **kwargs):
        """
        :param source_data_file: the path to the source file to initialize the inputs from.
        """
        super().__init__(**kwargs)
        
        
        self.class_ = "pa-0"
        self.expand = True
        
        self._set_layout_mda()
        self._set_layout_mdo()
        
        self.to_MDA()
    
    
    def to_MDO(self):
        """
        Changes inputs to MDO inputs
        """
        self.children = self.mdo_input
    
    def to_MDA(self):
        """
        Changes inputs to MDA inputs
        """
        self.children = self.mda_input
        

    def retrieve_mda_inputs(self):
        """
        Retrieves inputs from the MDA input widgets
        
        :return: an oad DataFile containing the source file inputs merged
        with the user inputs
        """
        # Create the input file with the current value
        new_inputs = copy.deepcopy(self.reference_inputs)

        # No need to provide list or numpy array for scalar values.
        new_inputs["data:TLAR:NPAX"].value = self.n_pax_input.value

        new_inputs[
            "data:TLAR:approach_speed"
        ].value = self.v_app_input.value
        new_inputs["data:TLAR:approach_speed"].units = "kn"  # Unit from the widget

        # If the Mach get too high and because we originally didn't plan on changing sweep,
        # the compressibility drag might get too high causing the code to not converge ! We
        # will thus adapt the sweep based on the mach number with a message to let the
        # student know about it. We'll keep the product M_cr * cos(phi_25) constant at the
        # value obtain with M_cr = 0.78 and phi_25 = 24.54 deg
        if self.cruise_mach_input.value > 0.78:
            cos_phi_25 = (
                0.78
                / self.cruise_mach_input.value
                * np.cos(np.deg2rad(24.54))
            )
            phi_25 = np.arccos(cos_phi_25)
            new_inputs["data:geometry:wing:sweep_25"].value = phi_25
            new_inputs["data:geometry:wing:sweep_25"].units = "rad"

        new_inputs[
            "data:TLAR:cruise_mach"
        ].value = self.cruise_mach_input.value

        new_inputs["data:TLAR:range"].value = self.range_input.value
        new_inputs["data:TLAR:range"].units = "NM"  # Unit from the widget

        new_inputs[
            "data:weight:aircraft:payload"
        ].value = self.payload_input.value
        new_inputs["data:weight:aircraft:payload"].units = "kg"  # Unit from the widget

        new_inputs[
            "data:weight:aircraft:max_payload"
        ].value = self.max_payload_input.value
        new_inputs[
            "data:weight:aircraft:max_payload"
        ].units = "kg"  # Unit from the widget

        new_inputs[
            "data:geometry:wing:aspect_ratio"
        ].value = self.wing_aspect_ratio_input.value

        new_inputs[
            "data:propulsion:rubber_engine:bypass_ratio"
        ].value = self.bpr_input.value
        
        return new_inputs


    def retrieve_mdo_inputs(self, configurator: oad.FASTOADProblemConfigurator):
        """
        Retrieves inputs from the MDO input widgets
        
        :param configurator: the configurator from which the problem is created

        :return: a FastOADProblem configured with the user inputs merged with
        the source file inputs.
        """
        # Get the problem, no need to write inputs. The fact that the reference was created
        # based on the same configuration we will always use should ensure the completion of
        # the input file
        problem = configurator.get_problem(read_inputs=True)

        if self.ar_design_var_checkbox.v_model:

            problem.model.add_design_var(
                name="data:geometry:wing:aspect_ratio",
                lower=self.ar_design_var_input.range[0],
                upper=self.ar_design_var_input.range[1],
            )

        if self.sweep_w_design_var_checkbox.v_model:

            problem.model.add_design_var(
                name="data:geometry:wing:sweep_25",
                units="deg",
                lower=self.sweep_w_design_var_input.range[0],
                upper=self.sweep_w_design_var_input.range[1],
            )
        
        # The objective is found using the v-model of the button group
        # 0: fuel sizing, 1: MTOW, 2: OWE
        if self.objective_selection.v_model==0:
            problem.model.add_objective(
                name="data:mission:sizing:block_fuel",
                units="kg",
                scaler=1e-4,
            )
        elif self.objective_selection.v_model == 1:
            problem.model.add_objective(
                name="data:weight:aircraft:MTOW", units="kg", scaler=1e-4
            )
        else:
            # Selected objective is the OWE
            problem.model.add_objective(
                name="data:weight:aircraft:OWE", units="kg", scaler=1e-4
            )

        if self.wing_span_constraints_checkbox.v_model:
            problem.model.add_constraint(
                name="data:geometry:wing:span",
                units="m",
                lower=0.0,
                upper=self.wing_span_constraint_max.value
            )
        
        return problem

    def set_initial_value_mda(self, source_data_file_name):
        """
        Set the value of the attributes that store the variable for the MDA based on their value
        in the reference inputs.
        
        Also save the source file inputs as an object attribute that we can copy to modify inputs
        
        :param source_data_file_name: the source file to read data from
        """
        # Read the source data file
        source_data_file_path = pth.join(
            pth.dirname(source_data_files.__file__),
            source_data_file_name.replace(" ", "_") + "_source_data_file.xml"
        )
        self.reference_inputs = oad.DataFile(source_data_file_path)
        
        # No need to convert to alternate units
        self.n_pax_input.value = self.reference_inputs["data:TLAR:NPAX"].value[0]
        # Convert in kts in case it was not
        self.v_app_input.value = om.convert_units(
            self.reference_inputs["data:TLAR:approach_speed"].value[0],
            self.reference_inputs["data:TLAR:approach_speed"].units,
            "kn",
        )
        self.cruise_mach_input.value = self.reference_inputs["data:TLAR:cruise_mach"].value[0]
        # Convert in nm in case it was not, etc, etc, ...
        self.range_input.value = om.convert_units(
            self.reference_inputs["data:TLAR:range"].value[0],
            self.reference_inputs["data:TLAR:range"].units,
            "NM",
        )
        self.payload_input.value = om.convert_units(
            self.reference_inputs["data:weight:aircraft:payload"].value[0],
            self.reference_inputs["data:weight:aircraft:payload"].units,
            "kg",
        )
        self.max_payload_input.value = om.convert_units(
            self.reference_inputs["data:weight:aircraft:max_payload"].value[0],
            self.reference_inputs["data:weight:aircraft:max_payload"].units,
            "kg",
        )
        self.wing_aspect_ratio_input.value = self.reference_inputs[
            "data:geometry:wing:aspect_ratio"
        ].value[0]
        self.bpr_input.value = self.reference_inputs[
            "data:propulsion:rubber_engine:bypass_ratio"
        ].value[0]

   
    def _set_layout_mdo(self):
        """
        Generates the layout for the MDO inputs
        """
        self.objective_selection = v.BtnToggle(
            v_model="toggle_exclusive",
            mandatory=True,
            children=[
                _TooltipButton("Fuel sizing", tooltip="Minimize the aircraft fuel consumption on the design mission"),
                _TooltipButton("MTOW", tooltip="Minimize the aircraft MTOW"),
                _TooltipButton("OWE", tooltip="Minimize the aircraft OWE"),
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
            v_model=True,
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
            label="Min/Max AR_w",
            tooltip="Range of aspect ratio for the optimisation [-]",
        )
        self.sweep_w_design_var_input = RangeSliderInput(
            min=5,
            max=50,
            step=1,
            range=[OPT_SWEEP_W_MIN, OPT_SWEEP_W_MAX],
            label="Sweep Range",
            tooltip="range of wing sweep angle for the optimisation [-]",
        )
        self.wing_span_constraint_max = SliderInput(
            min=20., 
            max=100., 
            step=0.01, 
            value=OPT_WING_SPAN_MAX,
            label="Max b_w", 
            tooltip="Maximum wing span allowed for the optimisation [m]"
        )
        
        

        self.mdo_input = [
            _InputsCategory("Objective", [
                    v.Row(
                        class_="pb-4 pt-2",
                        justify="center",
                        children=[
                            self.objective_selection
                        ],
                    )
            ]),
            _InputsCategory("Design variables", [
                self.ar_design_var_checkbox,
                self.ar_design_var_input,
                self.sweep_w_design_var_checkbox,
                self.sweep_w_design_var_input,
            ]),
            _InputsCategory("Constraints", [
                self.wing_span_constraint_max,
            ]),    
        ]
        
    
    def _set_layout_mda(self):
        """
        Generates the layout for the MDA inputs
        """
        self.n_pax_input = SliderInput(
            min=19,
            max=500, 
            step=1,
            label="N_PAX", 
            tooltip="Number of passengers"
        )
        self.v_app_input = SliderInput(
            min=45., 
            max=200., 
            step=0.1,
            label="V_app", 
            tooltip="Approach speed [kts]"
        )
        self.cruise_mach_input = SliderInput(
            min=0., 
            max=1., 
            step=0.01, 
            label="M_cruise", 
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
            step=10,
            label="Payload", 
            tooltip="Aircraft payload [kg]"
        )
        self.max_payload_input = SliderInput(
            min=0, 
            max=100000, 
            step=10,
            label="Max Payload", 
            tooltip="Aircraft max payload [kg]"
        )
        self.wing_aspect_ratio_input = SliderInput(
            min=4., 
            max=25., 
            step=0.1,
            label="AR_w", 
            tooltip="Aspect Ratio of the wing"
        )
        self.bpr_input = SliderInput(
            min=0, 
            max=25., 
            step=0.1, 
            label="BPR",
            tooltip="ByPass Ratio of the engine"
        )

        self.mda_input = [
            _InputsCategory("TLARs", [
                self.n_pax_input,
                self.v_app_input,
                self.cruise_mach_input,
                self.range_input,
            ]),
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



""" 
        #############################################################
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
        

        ############################################################################################
        # We also create a bow specific for launching an MDO which will only consists of selecting
        # the objectives and the bounds for the design variables
        # Input box
        
        


        ##########################################################################################
    
"""