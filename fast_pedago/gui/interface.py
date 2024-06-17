# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os
import os.path as pth
import shutil

import ipyvuetify as v

import fastoad.api as oad

from fast_pedago import (
    configuration,
    source_data_files,
)
from fast_pedago.processes import (
    MDAMDOLauncher,
    ResidualsObjectivesPlotter,
)
from . import (
    Header,
    Footer,
    InputsContainer,
    OutputsSelectionContainer,
    ProcessGraphContainer,
)


DRAWER_WIDTH = "450px"
HEADER_HEIGHT = "64px" 

# As there are margins and padding in the voila template, 
# I have to adjust the padding considering both the spacings
# in the voila template and the other components sizes.
TOP_PADDING = "36px"
LEFT_PADDING = "426px"


DEFAULT_SOURCE_DATA_FILE = "reference aircraft"


class Interface(v.App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        self.source_data_file = DEFAULT_SOURCE_DATA_FILE
        
        self._configure_paths()
        self._build_inputs_layout()
        self._build_outputs_layout()
        self._build_layout()
        
        self._to_inputs()
        
        self.inputs.set_initial_value_mda("reference aircraft")
        self.process_graph.generate_n2_xdsm(self.mda_configuration_file_path)
        
        # Sets the residuals and objectives plotter, and the MDA/MDO launcher to run
        # MDA/MDO and plot there evolution.
        self.residuals_objectives_plotter = ResidualsObjectivesPlotter(self.process_graph)
        self.process_launcher = MDAMDOLauncher(
            self.mda_configuration_file_path,
            self.mda_configuration_file_path,
            self.inputs,
            self.residuals_objectives_plotter,
        )


    def _to_inputs(self):
        self.drawer_content.children = [self.inputs]
        self.main_content.children = [self.process_graph]
        self.navigation_buttons.children = [self.to_outputs_button]
        self.navigation_buttons.justify = "end"
    
    
    def _to_outputs(self):
        self.drawer_content.children = [self.outputs]
        self.main_content.children = [self.process_graph]
        self.navigation_buttons.children = [self.to_inputs_button]
        self.navigation_buttons.justify = "start"


    def _build_inputs_layout(self):
        self.inputs = InputsContainer()
        self.process_graph = ProcessGraphContainer()
        
        # Buttons actions are defined outside of inputs to put all the non-graphical
        # code in the same place.
        self.inputs.process_selection_switch.on_event("change", self._switch_process)
        self.inputs.launch_button.on_event("click", self._launch_process)


    def _build_outputs_layout(self):
        self.outputs = OutputsSelectionContainer(self.working_directory_path)
        self.output_graphs = ...


    def _build_layout(self):
        """
        Builds the layout of the app.
        """ 
        # The content attributes will be used to change the components
        # displayed depending on the phase of the app : inputs, outputs, 
        # source file selection.
        self.drawer_content = v.Container(
            class_="pa-0",
        )
        
        self.main_content = v.Container(
            class_="pt-0",
            fluid=True,
            fill_height=True,
        )
        
        # Some of the components are made to hide when on small screens
        # This is to adjust the layout since the navigation drawer hides
        # on small screens.
        header = Header()
        header.open_drawer_button.on_event("click.stop", self._open_close_drawer)
        
        close_drawer_button = v.Btn(
            class_="me-5 hidden-lg-and-up",
            icon=True,
            children=[
                v.Icon(children=["fa-times"]),
            ],
        )
        close_drawer_button.on_event("click", self._open_close_drawer)
        
        self.drawer = v.NavigationDrawer(
            app=True,
            clipped=True,
            width=DRAWER_WIDTH,
            v_model=True,
            children=[
                v.Container(
                    style_="padding: " + HEADER_HEIGHT + " 0 0 0;",
                    class_="hidden-md-and-down",
                ),
                v.Row(
                    justify="end",
                    children=[
                        close_drawer_button,
                    ],
                ),
                self.drawer_content,
            ],
        )
        
        self.to_outputs_button = v.Btn(
            color="primary",
            children=[
                "Outputs",
                v.Icon(
                    class_="ps-2",
                    children=["fa-angle-right"]
                ),
            ],
        )
        
        self.to_inputs_button = v.Btn(
            color="primary",
            children=[
                v.Icon(
                    class_="pe-2",
                    children=["fa-angle-left"]
                ),
                "Inputs",
            ],
        )

        self.navigation_buttons = v.Row(
            class_="mx-6 mt-5",
        )
        # As I don't want _to_inputs and _to_outputs to be called only by widgets
        # events, I have to put them in a lambda function here since the on_event
        # requires args widget, event and data.
        self.to_inputs_button.on_event("click", lambda *args: self._to_inputs())
        self.to_outputs_button.on_event("click", lambda *args : self._to_outputs())

        self.children = [
            header,
            self.drawer,
            # Main content : to display graphs
            v.Html(
                tag="main",
                class_="v-main",
                children=[
                    v.Row(
                    style_="padding: " + TOP_PADDING + " 0 0 0;",
                    ),
                    v.Row(
                        children=[
                            v.Col(
                                cols="1",
                                style_="padding: 100px 0 0 " + LEFT_PADDING + ";",
                                class_="hidden-md-and-down",
                            ),
                            v.Col(
                                class_="pa-0",
                                children=[
                                    self.navigation_buttons,
                                    v.Row(
                                        children=[
                                            self.main_content,
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            Footer()
        ]


    def _configure_paths(self):
        # The configuration file path, source file path and input file path will be shared by
        # children tab, so we will define them there and pass them on. The file for the
        # sensitivity analysis is specific. Consequently, we won't generate it from
        # fast-oad_cs25. Additionally, to make it simpler to handle relative path from the
        # configuration file, instead of using this one directly we will make a copy of it in a
        # data directory of the active directory.

        self.working_directory_path = pth.join(os.getcwd(), "workdir")
        self.data_directory_path = pth.join(os.getcwd(), "data")

        # Create an attribute to store the converged sizing processes, it will be updated each
        # time we exit the launch tab.
        self.available_sizing_process = []

        if not pth.exists(self.working_directory_path):
            os.mkdir(self.working_directory_path)

        if not pth.exists(self.data_directory_path):
            os.mkdir(self.data_directory_path)

        # Please note here that I'm using a different configuration file from the original one
        # because I wanted to use the one from fast-oad_cs25 and change some paths
        self.mda_configuration_file_path = pth.join(
            self.data_directory_path, "oad_sizing_sensitivity_analysis.yml"
        )
        self.mdo_configuration_file_path = pth.join(
            self.data_directory_path, "oad_optim_sensitivity_analysis.yml"
        )

        self.reference_input_file_path = pth.join(
            self.working_directory_path,
            pth.join("inputs", "reference_aircraft_input_file.xml"),
        )

        # Avoid operation if we don't have to
        if not pth.exists(self.mda_configuration_file_path):
            shutil.copy(
                pth.join(
                    pth.dirname(configuration.__file__),
                    "oad_sizing_sensitivity_analysis.yml",
                ),
                self.mda_configuration_file_path,
            )

        if not pth.exists(self.mdo_configuration_file_path):
            shutil.copy(
                pth.join(
                    pth.dirname(configuration.__file__),
                    "oad_optim_sensitivity_analysis.yml",
                ),
                self.mdo_configuration_file_path,
            )

        # Technically, we could simply copy the reference file because I already did the input
        # generation but to be more generic we will do it like this which will make it longer on
        # the first execution.
        if not pth.exists(self.reference_input_file_path):
            oad.generate_inputs(
                configuration_file_path=self.mda_configuration_file_path,
                source_data_path=pth.join(
                    pth.dirname(source_data_files.__file__),
                    "reference_aircraft_source_data_file.xml",
                ),
            )
    

    def _open_close_drawer(self, widget, event, data):
            self.drawer.v_model = not self.drawer.v_model


    def _switch_process(self, widget, event, data):

        # If the button toggle is on 1, switch to MDO
        if data==1:
            self.is_MDO = True
            self.inputs.to_MDO()
            self.process_graph.to_MDO()

        else:
            self.is_MDO = False
            self.inputs.to_MDA()
            self.process_graph.to_MDA()


    def _to_process_computation(self):
        """
        When a process is on-going, disables all inputs components
        to let the user know he can't modify inputs.
        """
        self.inputs.launch_button.color = (
            "#FF0000"
        )
        
        # Show a loading widget to make it apparent that a computation is
        # underway.
        self.process_graph.set_loading("Setting up")


    def _to_process_results(self):
        """
        Re-enables input widgets after the end of a MDA/MDO process
        """
        self.inputs.launch_button.color = (
            "#32cd32"
        )


    def _launch_process(self, widget, event, data):
        self._to_process_computation()
        self.process_launcher.launch_processes(self.is_MDO)
        self._to_process_results()