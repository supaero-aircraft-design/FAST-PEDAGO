# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

from IPython.display import clear_output, display

import ipywidgets as widgets
import ipyvuetify as v

from fast_pedago.utils import (
    OUTPUT_FILE_SUFFIX,
    FLIGHT_DATA_FILE_SUFFIX,
)
from fast_pedago.gui.dropdowns import SelectOutput
from fast_pedago.gui.buttons import MultipleProcessSelectionInfoButton
from fast_pedago.gui.analysis_and_plots import simplified_payload_range_plot

from fast_pedago.gui.tabs import BaseTab

class ImpactVariablePayloadRangeTab(BaseTab):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sizing_process_to_display = []

        # Initialize it with fake values that we will overwrite as we scan through available
        # processes in the launch tab
        self.output_file_selection_widget = SelectOutput()
        self.info_button = MultipleProcessSelectionInfoButton()

        self.selection_and_info_box = v.Row(
            children=[
                v.Col(
                    cols=11,
                    children=[
                        self.output_file_selection_widget,
                    ],
                ),
                v.Col(
                    children=[
                        self.info_button, 
                    ],
                ),
            ],
        )

        self.output_display = widgets.Output()

        self.output_file_selection_widget.on_event(
            "change",
            self.display_payload_range_graph,
        )

        self.children = [
            self.selection_and_info_box, 
            self.output_display,
        ]
        
    
    # As this graph use a custom function, I did not manage to factorize 
    # the function in the base tab class
    def display_payload_range_graph(self, widget, event, data):

        # First check if there are any sizing process to add to the display of if we need to
        # clear them
        if data == "None":
            self.sizing_process_to_display = []

        elif data not in self.sizing_process_to_display:
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
                path_to_flight_data_file = pth.join(
                    path_to_output_folder,
                    sizing_process_to_add + FLIGHT_DATA_FILE_SUFFIX,
                )

                fig = simplified_payload_range_plot(
                    path_to_output_file,
                    path_to_flight_data_file,
                    sizing_process_to_add,
                    fig=fig,
                )
                fig.update_layout(height=550)

            if self.sizing_process_to_display:

                display(fig)