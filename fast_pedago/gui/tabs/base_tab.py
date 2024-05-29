# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

from IPython.display import clear_output, display

import ipywidgets as widgets
import ipyvuetify as v

import fastoad.api as oad

from fast_pedago.utils import OUTPUT_FILE_SUFFIX

class BaseTab(v.TabItem):
    def __init__(
        self, 
        configuration_file_path: str=None, 
        reference_input_file_path: str=None,
        working_directory_path: str=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        
        self.reference_input_file_path = reference_input_file_path
        self.configuration_file_path = configuration_file_path
        self.working_directory_path = working_directory_path
        
        self.debug = v.Html(tag="div", children=["test"])
        
        
        # This widget is unused in a non-output tab
        self.output_display = widgets.Output()

    def print_debug(self, widget, event, data):
            self.debug.children = str(data)

    def display_graph(self, widget, data, plot_function):

            self.print_debug(None, None, widget.is_single_output)

            # First check if there are any sizing process to add to the display of if we need to
            # clear them
            if data == "None":
                self.sizing_process_to_display = []

            # Output will be added only if it is not already in the process to display
            # and if the chart is for a single output, check if there is already a current
            # output
            elif data not in self.sizing_process_to_display:
                if (not widget.is_single_output or
                    widget.is_single_output and not self.sizing_process_to_display):
                    self.sizing_process_to_display.append(data)

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

                    fig = plot_function(
                        path_to_output_file, sizing_process_to_add, fig=fig
                    )
                    fig.update_layout(height=550)

                if self.sizing_process_to_display:

                    display(fig)