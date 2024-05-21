# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

from IPython.display import clear_output, display

import ipywidgets as widgets

import fastoad.api as oad

from fast_pedago.gui.tabs.impact_variable_inputs_tab import OUTPUT_FILE_SUFFIX
from fast_pedago.gui.dropdowns import get_select_multiple_sizing_process_dropdown
from fast_pedago.gui.buttons import get_multiple_process_selection_info_button


class ImpactVariableMassBarBreakdownTab(widgets.VBox):
    def __init__(self, working_directory_path: str, **kwargs):

        super().__init__(**kwargs)

        self.working_directory_path = working_directory_path
        self.sizing_process_to_display = []

        # Initialize it with fake values that we will overwrite as we scan through available
        # processes in the launch tab
        self.output_file_selection_widget = (
            get_select_multiple_sizing_process_dropdown()
        )
        self.info_button = get_multiple_process_selection_info_button()

        self.selection_and_info_box = widgets.HBox()
        self.selection_and_info_box.children = [
            self.output_file_selection_widget,
            self.info_button,
        ]

        self.selection_and_info_box.layout = widgets.Layout(
            width="98%",
            height="6%",
            justify_content="space-between",
            align_items="flex-start",
        )

        self.output_display = widgets.Output()

        def display_graph(change):

            # First check if there are any sizing process to add to the display of if we need to
            # clear them
            if change["new"] == "None":
                self.sizing_process_to_display = []

            elif change["new"] not in self.sizing_process_to_display:
                self.sizing_process_to_display.append(change["new"])

            with self.output_display:

                clear_output()

                fig = None

                for sizing_process_to_add in self.sizing_process_to_display:

                    path_to_output_folder = pth.join(
                        self.working_directory_path, "outputs"
                    )
                    path_to_output_file = pth.join(
                        path_to_output_folder,
                        sizing_process_to_add + OUTPUT_FILE_SUFFIX,
                    )

                    fig = oad.mass_breakdown_bar_plot(
                        path_to_output_file, sizing_process_to_add, fig=fig
                    )
                    fig.update_layout(height=550)

                if self.sizing_process_to_display:

                    display(fig)

        self.output_file_selection_widget.observe(display_graph, names="value")

        self.children = [self.selection_and_info_box, self.output_display]
