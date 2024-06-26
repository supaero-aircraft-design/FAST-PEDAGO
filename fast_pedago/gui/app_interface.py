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
    Drawer,
    InputsContainer,
    OutputsGraphsContainer,
    ProcessGraphContainer,
    SourceSelectionContainer,
)


DRAWER_WIDTH = "450px"
HEADER_HEIGHT = "64px" 

# As there are margins and padding in the voila template, 
# I have to adjust the padding considering both the spacings
# in the voila template and the other components sizes.
TOP_PADDING = "36px"
LEFT_PADDING = "426px"


DEFAULT_SOURCE_DATA_FILE = "reference aircraft"


class AppInterface(v.App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        self.source_data_file = DEFAULT_SOURCE_DATA_FILE
        
        self._configure_paths()
        self._build_layout()
        
        self._to_source_selection()
        
        self.inputs.set_initial_value_mda("reference aircraft")
        
        # Sets the residuals and objectives plotter, and the MDA/MDO launcher to run
        # MDA/MDO and plot there evolution.
        self.residuals_objectives_plotter = ResidualsObjectivesPlotter(self.process_graph)
        self.process_launcher = MDAMDOLauncher(
            self.mda_configuration_file_path,
            self.mdo_configuration_file_path,
            self.inputs,
            self.residuals_objectives_plotter,
        )


    def _to_source_selection(self):
        self.drawer.hide()
        self.header.open_drawer_button.hide()
        self.padding_column.hide()
        self.main_content.children = [self.source_selection]


    def _to_main(self):
        self.drawer.show()
        self.header.open_drawer_button.show()
        self.padding_column.show()
        self.drawer.content.children = [self.inputs]
        self.main_content.children = [self.graphs]


    def _switch_tab(self, widget, event, data):
        if data == 1:
            self.drawer.hide()
            self.header.open_drawer_button.hide()
            self.padding_column.hide()
        else:
            self.drawer.show()
            self.header.open_drawer_button.show()
            self.padding_column.show()


    def _build_layout(self):
        """
        Builds the layout of the app.
        """ 
        # Source selection + home widgets
        self.source_selection = SourceSelectionContainer()
        self.source_selection.source_data_file_selector.on_event("change", self._set_source_data_file)
        
        # Inputs + process graph widgets
        self.inputs = InputsContainer()
        self.process_graph = ProcessGraphContainer(self.mda_configuration_file_path)

        self.inputs.process_selection_switch.on_event("change", self._switch_process)
        self.inputs.launch_button.on_event("click", self._launch_process)
        
        # Outputs widgets
        self.output_graphs = OutputsGraphsContainer(self.working_directory_path)
        
        
        self.main_content = v.Container(
            class_="pt-0",
            fluid=True,
            fill_height=True,
        )
        
        self.graphs = v.Tabs(
            centered=True,
            grow=True,
            hide_slider=True,
            children=[
                v.Tab(children=["Inputs"]),
                v.Tab(children=["Outputs"]),
                v.TabItem(
                    children=[
                        v.Divider(),
                        self.process_graph,
                    ],
                ),
                v.TabItem(
                    children=[
                        v.Divider(),
                        self.output_graphs,
                    ],
                ),
            ],
        )
        self.graphs.on_event("change", self._switch_tab)
        
        self.header = Header()
        self.header.fast_oad_top_layer_logo.on_event("click", lambda *args : self._to_source_selection())
        self.header.open_drawer_button.on_event("click", self._open_or_close_drawer)
        self.header.clear_all_button.button.on_event("click", self._clear_all_files)
        
        self.drawer = Drawer()
        self.drawer.close_drawer_button.on_event("click", self._open_or_close_drawer)
        
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
        
        # Padding column to avoid having the main content behind the drawer when expanded
        self.padding_column = v.Col(
            cols="1",
            style_="padding: 100px 0 0 " + LEFT_PADDING + ";",
            class_="hidden-md-and-down",
        )

        self.children = [
            self.header,
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
                            self.padding_column,
                            v.Col(
                                class_="pa-0",
                                children=[
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
        When a process is on-going.
        """
        self.inputs.disable()
        self.graphs.children[0].disabled = True
        self.graphs.children[1].disabled = True
        
        # Show a loading widget to make it apparent that a computation is
        # underway.
        self.process_graph.set_loading("Setting up")


    def _to_process_results(self):
        """
        Re-enables input widgets after the end of a MDA/MDO process
        """
        self.inputs.enable()
        self.graphs.children[0].disabled = False
        self.graphs.children[1].disabled = False


    def _launch_process(self, widget, event, data):
        self._to_process_computation()
        self.process_launcher.launch_processes(self.is_MDO)
        self._to_process_results()


    def _set_source_data_file(self, widget, event, data):
        """
        Sets the reference file name to use
        
        To be called by a widget event
        """
        self.source_data_files = data
        self.inputs.set_initial_value_mda(data)
        self._to_main()
    
    
    def _open_or_close_drawer(self, widget, event, data):
        self.drawer.v_model = not self.drawer.v_model
    
    
    def _clear_all_files(self, widget, event, data):
        """
        Clear all files contained in "workdir", in subdirectories "inputs"
        and "outputs", that are not the files of the reference aircraft.
        Also makes the user come back to source selection.

        The subdirectories of workdir are not deleted in the process.
        """
        # Gets back to source file selection
        self._to_source_selection()
        # Clears the output selection
        self.output_graphs.output_selection.v_model = []

        working_directory_path = pth.join(os.getcwd(), "workdir")
        input_directory_path = pth.join(working_directory_path, "inputs")
        output_directory_path = pth.join(working_directory_path, "outputs")

        # Remove all input files in the inputs directory
        input_file_list = os.listdir(input_directory_path)
        for file_name in input_file_list:
            file_path = pth.join(input_directory_path, file_name)

            # We keep the reference input_file and avoid deleting subdirectory
            if file_name != "reference_aircraft_input_file.xml" and not pth.isdir(
                file_path
            ):
                os.remove(file_path)

        # Remove all input files in the outputs directory, we can remove all .sql because they
        # are re-generated anyway
        output_file_list = os.listdir(output_directory_path)
        for file_name in output_file_list:
            file_path = pth.join(output_directory_path, file_name)

            # We keep the reference input_file and avoid deleting subdirectory
            if (
                file_name != "reference_aircraft_output_file.xml"
                and file_name != "reference_aircraft_flight_points.csv"
                and not pth.isdir(file_path)
            ):
                os.remove(file_path)