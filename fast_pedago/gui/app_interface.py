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


# As there are margins and padding in the voila template,
# I have to adjust the padding considering both the spacings
# in the voila template and the other components sizes.
TOP_PADDING = "36px"
LEFT_PADDING = "426px"


class AppInterface(v.App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        PathManager.build_paths()

        self._build_layout()
        self._to_source_selection()

    def _to_source_selection(self):
        """
        Displays tutorial and source selection widget.
        """
        self.drawer.hide()
        self.header.open_drawer_button.hide()
        self.padding_column.hide()
        self.main_content.children = [self.source_selection]

    def _to_main(self):
        """
        Displays main window, with input drawer and tabs to change
        between residuals/objectives graph and output figures.
        """
        self.drawer.show()
        self.header.open_drawer_button.show()
        self.padding_column.show()
        self.drawer.content.children = [self.inputs]
        self.main_content.children = [self.graphs]

    def _switch_tab(self, widget, event, data):
        """
        Hides the drawer when on outputs tabs, and show it when on
        inputs tab.

        To be called with "on_event" method of a widget.
        """
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
        Builds the layout of the app: all the app components (drawer,
        input/output tabs, header, footer, tutorial).
        """
        # Source selection + home widgets
        self.source_selection = SourceSelectionContainer()
        self.source_selection.source_data_file_selector.on_event(
            "change", self._set_source_data_file
        )

        # Inputs + process graph widgets
        self.process_graph = ProcessGraphContainer()

        # Sets the residuals and objectives plotter, and the MDA/MDO launcher
        # to run MDA/MDO and plot there evolution.
        self.residuals_objectives_plotter = ResidualsObjectivesPlotter(
            self.process_graph
        )
        self.process_launcher = MDAMDOLauncher(
            self.residuals_objectives_plotter,
        )

        self.inputs = InputsContainer(self.process_launcher)

        self.inputs.process_selection_switch.on_event(
            "change",
            self._switch_process,
        )
        self.inputs.launch_button.on_event("click", self._launch_process)

        # Outputs widgets
        self.output_graphs = OutputsGraphsContainer()

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
        self.header.fast_oad_logo.on_event(
            "click", lambda *args: self._to_source_selection()
        )
        self.header.open_drawer_button.on_event(
            "click",
            self._open_or_close_drawer,
        )
        self.header.clear_all_button.button.on_event(
            "click",
            self._clear_all_files,
        )

        self.drawer = Drawer()
        self.drawer.close_drawer_button.on_event(
            "click",
            self._open_or_close_drawer,
        )

        self.to_outputs_button = v.Btn(
            color="primary",
            children=[
                "Outputs",
                v.Icon(class_="ps-2", children=["fa-angle-right"]),
            ],
        )

        self.to_inputs_button = v.Btn(
            color="primary",
            children=[
                v.Icon(class_="pe-2", children=["fa-angle-left"]),
                "Inputs",
            ],
        )

        self.navigation_buttons = v.Row(
            class_="mx-6 mt-5",
        )

        # Padding column to avoid having the main content behind
        # the drawer when expanded
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
                        no_gutters=True,
                        children=[
                            self.padding_column,
                            v.Col(
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
            Footer(),
        ]

    def _switch_process(self, widget, event, data):
        """
        Switch display between MDA and MDO depending on process selection
        button state.

        To be called with "on_event" method of a widget.
        """
        # If the button toggle is on 1, switch to MDO
        if data == 1:
            self.is_MDO = True
            self.inputs.to_MDO()
            self.process_graph.to_MDO()

        else:
            self.is_MDO = False
            self.inputs.to_MDA()
            self.process_graph.to_MDA()

    def _to_process_computation(self):
        """
        When a process is on-going, blocks the inputs and set a loading screen.
        """
        self.inputs.disable()
        self.graphs.children[0].disabled = True
        self.graphs.children[1].disabled = True

        # Show a loading widget to make it apparent that a computation is
        # underway.
        self.process_graph.set_loading("Setting up")

    def _to_process_results(self):
        """
        Re-enables input widgets after the end of a MDA/MDO process.
        """
        self.inputs.enable()
        self.graphs.children[0].disabled = False
        self.graphs.children[1].disabled = False
        if self.is_MDO:
            snackbar_to_open = self.process_graph.mdo_end_snackbar
        else:
            if self.process_launcher.get_MDA_success():
                snackbar_to_open = self.process_graph.mda_success_snackbar
            else:
                snackbar_to_open = self.process_graph.mda_failure_snackbar
        self.process_graph.open_snackbar(snackbar_to_open)

    def _launch_process(self, widget, event, data):
        """
        Retrieves the user inputs from the drawer and launch the selected
        process.

        To be called with "on_event" method of a widget.
        """
        self._to_process_computation()
        if self.is_MDO:
            self.inputs.retrieve_mdo_inputs()
        else:
            self.inputs.retrieve_mda_inputs()
        self.process_launcher.launch_processes(self.is_MDO)
        self._to_process_results()

    def _set_source_data_file(self, widget, event, data):
        """
        Sets the reference file name to use

        To be called by a widget event
        """
        self.inputs.set_initial_value_mda(data)
        self._to_main()

    def _open_or_close_drawer(self, widget, event, data):
        """
        Opens or closes the input drawer depending on its actual state.

        To be called with "on_event" method of a widget.
        """
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
        self.output_graphs.hide_graphs()

        PathManager.clear_all_files()
