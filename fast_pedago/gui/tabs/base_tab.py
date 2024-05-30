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
        
        # This widget is unused in a non-output tab
        self.output_display = widgets.Output()

    def display_graph(self, data, plot_function):
        # data contains a list of outputs or a single output, depending on the graph
        # If there is no data, the rest of the code will be enough to clear the screen
        if type(data) == str:
            self.sizing_process_to_display = [data]
        else:
            self.sizing_process_to_display = data
        
        path_to_output_folder = pth.join(
            self.working_directory_path, "outputs"
        )

        with self.output_display:

            clear_output()
            fig = None
            
            for sizing_process_to_add in self.sizing_process_to_display:
                if sizing_process_to_add:
                    
                    path_to_output_file = pth.join(
                        path_to_output_folder,
                        sizing_process_to_add + OUTPUT_FILE_SUFFIX,
                    )
                                
                    # The plot function have a simplified signature if only one output can be added
                    if len(self.sizing_process_to_display) == 1:
                        fig = plot_function(path_to_output_file)
                    else:
                        fig = plot_function(path_to_output_file, sizing_process_to_add, fig=fig)
                
            if fig:
                fig.update_layout(height=550)
                display(fig)