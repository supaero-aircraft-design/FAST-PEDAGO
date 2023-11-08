# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

from IPython.display import clear_output

import ipywidgets as widgets

import fastoad.api as oad

from fast_pedago.tabs.impact_variable_inputs_tab import OUTPUT_FILE_SUFFIX
from fast_pedago.dropdowns import get_select_single_sizing_process_dropdown


class ImpactVariableOutputTab(widgets.VBox):
    def __init__(self, working_directory_path: str, **kwargs):

        super().__init__(**kwargs)

        self.working_directory_path = working_directory_path

        # Initialize it with fake values that we will overwrite as we scan through available
        # processes in the launch tab
        self.output_file_selection_widget = get_select_single_sizing_process_dropdown()

        self.output_display = widgets.Output()

        def display_outputs(change):

            with self.output_display:

                clear_output()

                # Only display if something other than None is selected
                if change["new"] != "None":

                    path_to_output_folder = pth.join(
                        self.working_directory_path, "outputs"
                    )
                    path_to_output_file = pth.join(
                        path_to_output_folder, change["new"] + OUTPUT_FILE_SUFFIX
                    )
                    oad.variable_viewer(path_to_output_file)

        self.output_file_selection_widget.observe(display_outputs, names="value")

        self.children = [self.output_file_selection_widget, self.output_display]
