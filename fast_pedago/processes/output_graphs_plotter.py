# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

from typing import List

import ipywidgets as widgets
import ipyvuetify as v
from IPython.display import clear_output, display

import fastoad.api as oad

from .path_manager import PathManager
from fast_pedago.plots import simplified_payload_range_plot
from fast_pedago.objects.paths import (
    OUTPUT_FILE_SUFFIX,
    FLIGHT_DATA_FILE_SUFFIX,
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
    """
    A class that manages the plot of all the available figures.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Stores the current plot name, plot function, and data
        self.plot_name = ''
        self.plot_function = None
        self.data = []
        self.is_single_output = False
        
        self._build_layout()


    def _build_layout(self):
        """
        Builds the graph layout: the graph container and a selector specific to
        single output figures.
        """
        self.output = widgets.Output()

        # A file selection widget for graphs that can
        # only display one output.
        self.file_selector = v.Select(
            class_="pa-0 ma-0",
            label="This graph only displays one output, please choose one."
        )
        self.file_selector.on_event("click", self._update_selection_data)
        self.file_selector.on_event("change", lambda widget, event, data: self.plot_function(data))
        self.file_selector.hide()
        
        self.output_display = v.Container(
            class_="pe-10",
            children=[
                self.file_selector,
                self.output,
            ],
        )
    

    def change_graph(self, plot_name: str):
        """
        Changes the plotting function to another one, and displays a 
        file selector for when the figure only allows one aircraft,
        then plots the new figure.

        :param plot_name: the name of the new figure to plot. 
            (standard name taken from GRAPH constant)
        """
        self.plot_name = plot_name
        self.is_single_output = False
        self.file_selector.hide()
        
        if plot_name == GRAPH['General'][0]:
            self.plot_function = oad.variable_viewer
            self.file_selector.show()
            self.is_single_output = True
        elif plot_name == GRAPH['Geometry'][0]:
            self.plot_function = oad.aircraft_geometry_plot
        elif plot_name == GRAPH['Geometry'][1]:
            self.plot_function = oad.wing_geometry_plot
        elif plot_name == GRAPH['Aerodynamics'][0]:
            self.plot_function = oad.drag_polar_plot
        elif plot_name == GRAPH['Mass'][0]:
            self.plot_function = oad.mass_breakdown_bar_plot
        elif plot_name == GRAPH['Mass'][1]:
            self.plot_function = oad.mass_breakdown_sun_plot
            self.is_single_output = True
            self.file_selector.show()
        elif plot_name == GRAPH['Performances'][0]:
            self.plot_function = None
        elif plot_name == GRAPH['Performances'][1]:
            self.plot_function = simplified_payload_range_plot
        
        self.plot()


    def plot(self, data: List[str] = None):
        """
        Plots the given data on the current figure.
        
        :param data: the data to plot.
        """
        # If no data is given, use the cached one. Else use 
        # the given one and cache it.
        if data:
            self.data = data
            self.file_selector.items = data
        self._base_plot(self.data)


    def _base_plot(self, data: List[str]):
        """
        Base function to plot data. Add all aircraft to the given plot.

        :param data: all the aircraft to plot from (names of the aircraft)
        """
        # data contains a list of outputs or a single output, depending on the graph
        # If there is no data, the rest of the code will be enough to clear the screen
        if type(data) == str:
            sizing_process_to_display = [data]
        else:
            sizing_process_to_display = data

        with self.output:
            
            # Clear actual graphs :
            clear_output()
            fig = None
            if self.plot_name ==  GRAPH["Performances"][0]:
                mission_viewer = oad.MissionViewer()
            
            # Add every aircraft to the plot :
            for sizing_process_to_add in sizing_process_to_display:
                if sizing_process_to_add:
                    path_to_output_file = PathManager.path_to("output",
                        sizing_process_to_add + OUTPUT_FILE_SUFFIX,
                    )
                    path_to_flight_data_file = PathManager.path_to("output",
                        sizing_process_to_add + FLIGHT_DATA_FILE_SUFFIX,
                    )
                    
                    # Not exactly the same way to plot payload range and mission.
                    if self.plot_name == GRAPH["Performances"][1]:
                        fig = self.plot_function(
                            path_to_output_file,
                            path_to_flight_data_file,
                            sizing_process_to_add,
                            fig=fig,
                        )
                    elif self.plot_name ==  GRAPH["Performances"][0]:
                        mission_viewer.add_mission(
                            path_to_flight_data_file, sizing_process_to_add
                        )
                    
                    else:
                        # The plot function have a simplified signature if only one output can be added
                        if len(sizing_process_to_display) == 1 or self.is_single_output:
                            fig = self.plot_function(path_to_output_file)
                            # Leave the loop is the graph can only plot one
                            # output at a time. Only the first data will be
                            # plotted
                            if self.is_single_output:
                                self.file_selector.v_model = sizing_process_to_add
                                break

                        else:
                            fig = self.plot_function(path_to_output_file, sizing_process_to_add, fig=fig)

            # Display the plot:
            if fig:
                fig.update_annotations(font_size=10)
                display(fig)
            if self.plot_name ==  GRAPH["Performances"][0]:
                mission_viewer.display()


    def _update_selection_data(self, widget, event, data):
        """
        Updates the file selector with the pre-selected aircraft to choose 
        among them for single aircraft figures.
        """
        self.file_selector.items = self.data