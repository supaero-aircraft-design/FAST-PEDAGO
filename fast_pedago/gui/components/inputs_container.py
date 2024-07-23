import ipyvuetify as v

from .input_widgets import (
    Snackbar,
    SliderInput,
    RangeSliderInput,
)
from fast_pedago.processes import ProcessLauncher
from fast_pedago.utils import PathManager


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

    def __init__(self, process_launcher: ProcessLauncher, **kwargs):
        """
        :param source_data_file: the path to the source file to initialize *
            the inputs from.
        """
        super().__init__(**kwargs)

        self.process_launcher = process_launcher

        self._build_layout()
        self.to_MDA()

    def to_MDO(self):
        """
        Changes layout to MDO inputs
        """
        self.children = [self.inputs_header] + self._mdo_input
        self.launch_button.children = [
            v.Icon(class_="px-3", children=["fa-plane"]),
            "Launch optimization",
        ]
        self.process_name_field.label = "Optimization name"
        self.process_name_field.placeholder = (
            "Write a name for your optimization process"
        )

    def to_MDA(self):
        """
        Changes layout to MDA inputs
        """
        self.children = [self.inputs_header] + self._mda_input
        self.launch_button.children = [
            v.Icon(class_="px-3", children=["fa-plane"]),
            "Launch sizing",
        ]
        self.process_name_field.label = "Sizing name"
        self.process_name_field.placeholder = "Write a name for your sizing process"

    def _build_layout(self):
        """
        Builds the main layout of the inputs container, with a text field,
        launch button, and button to switch from MDA to MDO.
        """
        self.class_ = "pa-0"
        self.expand = True

        self._build_layout_mda()
        self._build_layout_mdo()

        # This reference file should always be there and is always taken as
        # reference
        self.source_data_file_selector = v.Select(
            hide_details=True,
            label="Select a reference aircraft",
            items=PathManager.list_available_reference_file(),
            v_model=PathManager.reference_aircraft,
        )
        self.set_initial_value_mda(PathManager.reference_aircraft)

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
                v.Icon(
                    class_="px-3",
                    children=["fa-plane"],
                ),
                "Launch sizing",
            ],
        )

        # Create a button to trigger the MDO "mode"
        self.process_selection_switch = v.BtnToggle(
            rounded=True,
            mandatory=True,
            dense=True,
            color="primary",
            children=[
                v.Btn(
                    v_bind="tooltip.attrs",
                    v_on="tooltip.on",
                    children=["MDA"],
                ),
                v.Btn(
                    v_bind="tooltip.attrs",
                    v_on="tooltip.on",
                    children=["MDO"],
                ),
            ],
        )
        process_selection_switch_wrapper = v.Tooltip(
            contained=True,
            v_slots=[
                {
                    "name": "activator",
                    "variable": "tooltip",
                    "children": self.process_selection_switch,
                }
            ],
            children=["Swap between analysis and optimization mode"],
        )

        self.inputs_header = v.ListItemGroup(
            class_="px-2 pt-1",
            children=[
                v.Row(
                    class_="px-3",
                    align="center",
                    children=[
                        self.source_data_file_selector,
                    ],
                ),
                v.Row(
                    align="center",
                    children=[
                        v.Col(
                            cols=4,
                            children=[
                                process_selection_switch_wrapper,
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
                v.Divider(class_="mt-3"),
            ],
        )

    def _build_layout_mdo(self):
        """
        Generates the layout for the MDO inputs.
        """
        self._objective_selection = v.BtnToggle(
            v_model="toggle_exclusive",
            mandatory=True,
            children=[
                v.Btn(
                    v_bind="tooltip.attrs",
                    v_on="tooltip.on",
                    children=["Fuel sizing"],
                ),
                v.Btn(
                    v_bind="tooltip.attrs",
                    v_on="tooltip.on",
                    children=["MTOW"],
                ),
                v.Btn(
                    v_bind="tooltip.attrs",
                    v_on="tooltip.on",
                    children=["OWE"],
                ),
            ],
        )

        # Range sliders to input design variables and constraints
        self._ar_design_var_input = RangeSliderInput(
            min=5,
            max=30,
            step=1,
            range=[OPT_AR_MIN, OPT_AR_MAX],
            label="Min/Max wing AR",
            tooltip="Range of aspect ratio for the optimization [-]",
            with_checkbox=True,
        )
        self._sweep_w_design_var_input = RangeSliderInput(
            min=5,
            max=50,
            step=1,
            range=[OPT_SWEEP_W_MIN, OPT_SWEEP_W_MAX],
            label="Sweep Range",
            tooltip="Range of wing sweep angle for the optimization [-]",
            with_checkbox=True,
        )
        self._wing_span_constraint_input = SliderInput(
            min=20.0,
            max=100.0,
            step=1,
            value=OPT_WING_SPAN_MAX,
            label="Max wing span",
            tooltip="Maximum wing span allowed for the optimization [m]",
            with_checkbox=True,
        )

        self._sweep_w_design_var_input.checkbox.on_event(
            "change", self._ensure_one_design_var
        )
        self._ar_design_var_input.checkbox.on_event(
            "change", self._ensure_one_design_var
        )

        self._mdo_input = [
            _InputsCategory(
                "Objective",
                [
                    v.Row(
                        class_="pb-4 pt-2",
                        justify="center",
                        children=[
                            v.Tooltip(
                                contained=True,
                                v_slots=[
                                    {
                                        "name": "activator",
                                        "variable": "tooltip",
                                        "children": self._objective_selection,
                                    }
                                ],
                                children=[
                                    "Minimize fuel consumption or MTOW or OWE",
                                ],
                            ),
                        ],
                    )
                ],
                is_open=True,
            ),
            _InputsCategory(
                "Design variables",
                [
                    self._ar_design_var_input,
                    self._sweep_w_design_var_input,
                ],
            ),
            _InputsCategory(
                "Constraints",
                [
                    self._wing_span_constraint_input,
                ],
            ),
        ]

    def _build_layout_mda(self):
        """
        Generates the layout for the MDA inputs.
        """
        self._n_pax_input = SliderInput(
            min=20,
            max=400,
            step=1,
            label="NPAX",
            tooltip="Number of passengers",
        )
        self._v_app_input = SliderInput(
            min=45,
            max=170,
            step=0.1,
            label="Vapp",
            tooltip="Approach speed [kts]",
        )
        self._cruise_mach_input = SliderInput(
            min=0.0,
            max=1.0,
            step=0.01,
            label="Mcruise",
            tooltip="Cruise mach",
        )
        self._range_input = SliderInput(
            min=0,
            max=10000,
            step=10,
            label="Range",
            tooltip="Aircraft range [NM]",
        )
        self._payload_input = SliderInput(
            min=0,
            max=100000,
            step=10,
            label="Payload",
            tooltip="Aircraft payload [kg]",
        )
        self._max_payload_input = SliderInput(
            min=0,
            max=100000,
            step=10,
            label="Max Payload",
            tooltip="Aircraft max payload [kg]",
        )
        self._wing_aspect_ratio_input = SliderInput(
            min=4,
            max=25,
            step=0.1,
            label="Wing AR",
            tooltip="Aspect Ratio of the wing",
        )
        self._bpr_input = SliderInput(
            min=2,
            max=15,
            step=0.1,
            label="BPR",
            tooltip="ByPass Ratio of the engine",
        )

        # As can be seen in the parent tab, there is an issue when cruise mach
        # gets too high, we will display a warning when that value is reached,
        # informing students of what is done behind the scene.
        self._snackbar = Snackbar(
            "The sweep angle of the wing has been adjusted to avoid having "
            "compressibility drag coefficient too high"
        )
        self._cruise_mach_input.slider.on_event("change", self._mach_alert)

        self._mda_input = [
            _InputsCategory(
                "TLARs",
                [
                    self._n_pax_input,
                    self._v_app_input,
                    self._cruise_mach_input,
                    self._range_input,
                ],
                is_open=True,
            ),
            _InputsCategory(
                "Weight",
                [
                    self._payload_input,
                    self._max_payload_input,
                ],
            ),
            _InputsCategory(
                "Geometry",
                [
                    self._wing_aspect_ratio_input,
                ],
            ),
            _InputsCategory(
                "Propulsion",
                [
                    self._bpr_input,
                ],
            ),
            self._snackbar,
        ]

    def _ensure_one_design_var(self, widget, event, data):
        """
        Ensures that at least one design variable is chosen
        for MDO.

        If the user tries to un-tick a checkbox, the other is ticked
        by default.

        To be called with an "on_event" ipyvuetify component method
        """
        if data:
            if widget == self._sweep_w_design_var_input.checkbox:
                if self._ar_design_var_input.checkbox.v_model:
                    self._ar_design_var_input.checkbox.v_model = False

            elif widget == self._ar_design_var_input.checkbox:
                if self._sweep_w_design_var_input.checkbox.v_model:
                    self._sweep_w_design_var_input.checkbox.v_model = False

    def _mach_alert(self, widget, event, data):
        """
        Opens the snackbar to alert the user if the mach is above the value
        of 0.78 and the snackbar is closedK

        To be called with "on_event" method of a widget.
        """
        if self._cruise_mach_input.slider.v_model > 0.78:
            if not self._snackbar.v_model:
                self._snackbar.display(widget, event, data)

    def _update_process_name(self, widget, event, data):
        """
        Changes process name when a new name is written
        in the input text field.

        To be used with a "on_event" of a text field ipyvuetify
        """
        self.process_launcher.set_aircraft_name(data)

    def disable(self):
        """
        Disables all inputs components
        to let the user know he can't modify inputs.
        """
        self.source_data_file_selector.disabled = True
        self.process_selection_switch.children[0].disabled = True
        self.process_selection_switch.children[1].disabled = True
        self.process_name_field.readonly = True
        self.launch_button.disabled = True
        self.launch_button.color = "#FF0000"

        # MDA inputs
        self._n_pax_input.disable()
        self._v_app_input.disable()
        self._cruise_mach_input.disable()
        self._range_input.disable()
        self._payload_input.disable()
        self._max_payload_input.disable()
        self._wing_aspect_ratio_input.disable()
        self._bpr_input.disable()

        # MDO inputs
        self._objective_selection.children[0].disabled = True
        self._objective_selection.children[1].disabled = True
        self._objective_selection.children[2].disabled = True
        self._ar_design_var_input.disable()
        self._sweep_w_design_var_input.disable()
        self._wing_span_constraint_input.disable()

    def enable(self):
        """
        Re-enables inputs after the end of computation.
        """
        self.source_data_file_selector.disabled = False
        self.process_selection_switch.children[0].disabled = False
        self.process_selection_switch.children[1].disabled = False
        self.process_name_field.readonly = False
        self.launch_button.disabled = False
        self.launch_button.color = "#32cd32"

        # MDA inputs
        self._n_pax_input.enable()
        self._v_app_input.enable()
        self._cruise_mach_input.enable()
        self._range_input.enable()
        self._payload_input.enable()
        self._max_payload_input.enable()
        self._wing_aspect_ratio_input.enable()
        self._bpr_input.enable()

        # MDO inputs
        self._objective_selection.children[0].disabled = False
        self._objective_selection.children[1].disabled = False
        self._objective_selection.children[2].disabled = False
        self._ar_design_var_input.enable()
        self._sweep_w_design_var_input.enable()
        self._wing_span_constraint_input.enable()

    def retrieve_mda_inputs(self):
        """
        Retrieves inputs from the MDA input widgets and configure the
        process launcher with it.
        """
        self.process_launcher.set_mda_inputs(
            n_pax=self._n_pax_input.slider.v_model,
            v_app=self._v_app_input.slider.v_model,
            cruise_mach=self._cruise_mach_input.slider.v_model,
            range=self._range_input.slider.v_model,
            payload=self._payload_input.slider.v_model,
            max_payload=self._max_payload_input.slider.v_model,
            wing_aspect_ratio=self._wing_aspect_ratio_input.slider.v_model,
            bypass_ratio=self._bpr_input.slider.v_model,
        )

    def retrieve_mdo_inputs(self):
        """
        Retrieves inputs from the MDO input widgets and configure the
        process launcher with it.
        """
        self.process_launcher.set_mdo_inputs(
            self._objective_selection.v_model,
            not self._ar_design_var_input.checkbox.v_model,
            self._ar_design_var_input.slider.v_model[0],
            self._ar_design_var_input.slider.v_model[1],
            not self._sweep_w_design_var_input.checkbox.v_model,
            self._sweep_w_design_var_input.slider.v_model[0],
            self._sweep_w_design_var_input.slider.v_model[1],
            not self._wing_span_constraint_input.checkbox.v_model,
            self._wing_span_constraint_input.slider.v_model,
        )

    def set_initial_value_mda(self, source_data_file_name: str):
        """
        Set the value of the attributes that store the variable for the MDA
        based on their value in the reference inputs.

        Also save the source file inputs as an object attribute that we can
        copy to modify inputs.

        :param source_data_file_name: the source file to read data from
        """
        reference_inputs = self.process_launcher.get_reference_inputs(
            source_data_file_name
        )
        self._n_pax_input.slider.v_model = reference_inputs[0]
        self._v_app_input.slider.v_model = reference_inputs[1]
        self._cruise_mach_input.slider.v_model = reference_inputs[2]
        self._range_input.slider.v_model = reference_inputs[3]
        self._payload_input.slider.v_model = reference_inputs[4]
        self._max_payload_input.slider.v_model = reference_inputs[5]
        self._wing_aspect_ratio_input.slider.v_model = reference_inputs[6]
        self._bpr_input.slider.v_model = reference_inputs[7]


class _InputsCategory(v.ListGroup):
    """
    Internal class to factorize layout of an input category
    such as weight inputs, geometry inputs, TLARs, etc.

    It displays the name of the category as a title and
    the input widgets under it.
    """

    def __init__(
        self,
        name: str,
        inputs: v.VuetifyWidget = [],
        is_open: bool = False,
        **kwargs,
    ):
        """
        :param name: the name of the category
        :param inputs: a list of input widgets
        :param is_open: True if the group is initially open
        """
        super().__init__(**kwargs)

        self.value = is_open
        self.v_slots = [
            {
                "name": "activator",
                "children": [
                    v.ListItemTitle(
                        children=[
                            name,
                        ],
                    ),
                ],
            }
        ]
        self.children = [v.ListItem(children=[input]) for input in inputs]
