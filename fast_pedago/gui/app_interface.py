# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os
import os.path as pth
import shutil

import ipyvuetify as v

from .components import (
    Header,
    Footer,
    Drawer,
    InputsContainer,
    OutputsGraphsContainer,
    ProcessGraphContainer,
    SourceSelectionContainer,
)
from fast_pedago.processes import (
    PathManager,
    MDAMDOLauncher,
    ResidualsObjectivesPlotter,
)



DRAWER_WIDTH = "450px"
HEADER_HEIGHT = "64px" 

# As there are margins and padding in the voila template, 
# I have to adjust the padding considering both the spacings
# in the voila template and the other components sizes.
TOP_PADDING = "36px"
LEFT_PADDING = "426px"


class AppInterface(v.App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        PathManager.build_paths()
    
        self.source_data_file = PathManager.reference_aircraft
        
        self._build_layout()

        self._to_source_selection()
        
        self.inputs.set_initial_value_mda(PathManager.reference_aircraft)
        
        # Sets the residuals and objectives plotter, and the MDA/MDO launcher to run
        # MDA/MDO and plot there evolution.
        self.residuals_objectives_plotter = ResidualsObjectivesPlotter(self.process_graph)
        self.process_launcher = MDAMDOLauncher(
            PathManager.mda_configuration_file_path,
            PathManager.mdo_configuration_file_path,
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
        self.process_graph = ProcessGraphContainer(PathManager.mda_configuration_file_path)

        self.inputs.process_selection_switch.on_event("change", self._switch_process)
        self.inputs.launch_button.on_event("click", self._launch_process)
        
        # Outputs widgets
        self.output_graphs = OutputsGraphsContainer(PathManager.working_directory_path)
        
        
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
        self.process_graph.snackbar.open_or_close(None, None, None)


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

        # Remove all input files in the inputs directory
        input_file_list = os.listdir(PathManager.input_directory_path)
        for file_name in input_file_list:
            file_path = pth.join(PathManager.input_directory_path, file_name)

            # We keep the reference input_file and avoid deleting subdirectory
            if file_name != PathManager.reference_input_file_name and not pth.isdir(
                file_path
            ):
                os.remove(file_path)

        # Remove all input files in the outputs directory, we can remove all .sql because they
        # are re-generated anyway
        output_file_list = os.listdir(PathManager.output_directory_path)
        for file_name in output_file_list:
            file_path = pth.join(PathManager.output_directory_path, file_name)

            # We keep the reference input_file and avoid deleting subdirectory
            if (
                file_name != PathManager.reference_output_file_name
                and file_name != PathManager.reference_flight_data_file_name
                and not pth.isdir(file_path)
            ):
                os.remove(file_path)