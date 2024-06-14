# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

from IPython.display import clear_output, display

import ipywidgets as widgets

from fast_pedago.utils import (
    OUTPUT_FILE_SUFFIX,
    FIGURE_HEIGHT,
)


class OutputGraphsPlotter():
    def __init__(self, working_directory_path: str, **kwargs):
        super().__init__(**kwargs)
        
        self.working_directory_path = working_directory_path


    def display_graph(self, data, plot_function) -> widgets.Output:
        # data contains a list of outputs or a single output, depending on the graph
        # If there is no data, the rest of the code will be enough to clear the screen
        if type(data) == str:
            sizing_process_to_display = [data]
        else:
            sizing_process_to_display = data
        
        path_to_output_folder = pth.join(
            self.working_directory_path, "outputs"
        )

        output_display = widgets.Output()
        with output_display:

            clear_output()
            fig = None
            
            for sizing_process_to_add in sizing_process_to_display:
                if sizing_process_to_add:
                    
                    path_to_output_file = pth.join(
                        path_to_output_folder,
                        sizing_process_to_add + OUTPUT_FILE_SUFFIX,
                    )
                                
                    # The plot function have a simplified signature if only one output can be added
                    if len(sizing_process_to_display) == 1:
                        fig = plot_function(path_to_output_file)
                    else:
                        fig = plot_function(path_to_output_file, sizing_process_to_add, fig=fig)
                
            if fig:
                fig.update_layout(height=FIGURE_HEIGHT)
                display(fig)
        
        return output_display