# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO
from enum import Enum

import os.path as pth

from IPython.display import clear_output, display

import ipywidgets as widgets

import fastoad.api as oad

from fast_pedago.gui.analysis_and_plots import simplified_payload_range_plot
from fast_pedago.utils import (
    OUTPUT_FILE_SUFFIX,
    FLIGHT_DATA_FILE_SUFFIX,
    FIGURE_HEIGHT,
)


# When a new graph is added, it should be added to the dict, and then
# be plotted in the Plotter.
GRAPH = {
    'General': [
        'Variables',
    ],
    'Geometry': [
        'Aircraft',
        'Wing',
    ],
    'Aerodynamics': [
        'Drag polar',
    ],
    'Mass': [
        'Bar breakdown',
        'Sun breakdown',
    ],
    'Performances': [
        'Missions',
        'Payload-Range',
    ],
}


class OutputGraphsPlotter():
    def __init__(self, working_directory_path: str, **kwargs):
        super().__init__(**kwargs)
        
        self.working_directory_path = working_directory_path
        self.path_to_output_folder = pth.join(
            self.working_directory_path, "outputs"
        )

        self.plot_name = ''
        # Stores the function to call when plotting
        self.plot_function = None
        self.data = []
        
        self.output_display = widgets.Output()


    def change_graph(self, plot_name: str):
        self.plot_name = plot_name
        
        if plot_name == GRAPH['General'][0]:
            self.plot_function = self._variable_viewer
        elif plot_name == GRAPH['Geometry'][0]:
            self.plot_function = self._aircraft_geometry_plot
        elif plot_name == GRAPH['Geometry'][1]:
            self.plot_function = self._wing_geometry_plot
        elif plot_name == GRAPH['Aerodynamics'][0]:
            self.plot_function = self._drag_polar_plot
        elif plot_name == GRAPH['Mass'][0]:
            self.plot_function = self._mass_breakdown_bar_plot
        elif plot_name == GRAPH['Mass'][1]:
            self.plot_function = self._mass_breakdown_sun_plot
        elif plot_name == GRAPH['Performances'][0]:
            self.plot_function = self._mission_plot
        elif plot_name == GRAPH['Performances'][1]:
            self.plot_function = self._payload_range_plot
        
        self.plot()


    def plot(self, data = None):
        if data:
            self.data = data
        self.plot_function(self.data)


    def _variable_viewer(self, data):
        self._base_plot(oad.variable_viewer, data, True)

    def _aircraft_geometry_plot(self, data):
        self._base_plot(oad.aircraft_geometry_plot, data)
    
    def _wing_geometry_plot(self, data):
        self._base_plot(oad.wing_geometry_plot, data)

    def _drag_polar_plot(self, data):
        self._base_plot(oad.drag_polar_plot, data)

    def _mass_breakdown_bar_plot(self, data):
        self._base_plot(oad.mass_breakdown_bar_plot, data)

    def _mass_breakdown_sun_plot(self, data):
        self._base_plot(oad.mass_breakdown_sun_plot, data, True)

    def _mission_plot(self, data):
        self.sizing_process_to_display = data

        with self.output_display:
            clear_output()
            mission_viewer = oad.MissionViewer()

            for sizing_process_to_add in self.sizing_process_to_display:
                path_to_flight_data_file = pth.join(
                    self.path_to_output_folder,
                    sizing_process_to_add + FLIGHT_DATA_FILE_SUFFIX,
                )
                mission_viewer.add_mission(
                    path_to_flight_data_file, sizing_process_to_add
                )

            if self.sizing_process_to_display:
                mission_viewer.display()

    def _payload_range_plot(self, data):
        self.sizing_process_to_display = data
        
        with self.output_display:
            clear_output()
            fig = None

            for sizing_process_to_add in self.sizing_process_to_display:
                path_to_output_file = pth.join(
                    self.path_to_output_folder,
                    sizing_process_to_add + OUTPUT_FILE_SUFFIX,
                )
                path_to_flight_data_file = pth.join(
                    self.path_to_output_folder,
                    sizing_process_to_add + FLIGHT_DATA_FILE_SUFFIX,
                )

                fig = simplified_payload_range_plot(
                    path_to_output_file,
                    path_to_flight_data_file,
                    sizing_process_to_add,
                    fig=fig,
                )
                fig.update_layout(height=550)

            if fig:
                display(fig)


    def _base_plot(self, oad_plot, data, has_one_output_only=False) -> widgets.Output:
        # data contains a list of outputs or a single output, depending on the graph
        # If there is no data, the rest of the code will be enough to clear the screen
        if type(data) == str:
            sizing_process_to_display = [data]
        else:
            sizing_process_to_display = data

        with self.output_display:
            clear_output()
            fig = None
            
            for sizing_process_to_add in sizing_process_to_display:
                if sizing_process_to_add:
                    path_to_output_file = pth.join(
                        self.path_to_output_folder,
                        sizing_process_to_add + OUTPUT_FILE_SUFFIX,
                    )
                                
                    # The plot function have a simplified signature if only one output can be added
                    if len(sizing_process_to_display) == 1 or has_one_output_only:
                        fig = oad_plot(path_to_output_file)
                        # Leave the loop is the graph can only plot one
                        # output at a time. Only the first data will be
                        # plotted
                        if has_one_output_only:
                            break

                    else:
                        fig = oad_plot(path_to_output_file, sizing_process_to_add, fig=fig)
                
            if fig:
                fig.update_layout(height=FIGURE_HEIGHT)
                display(fig)