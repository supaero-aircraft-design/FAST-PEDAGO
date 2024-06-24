# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

from typing import Tuple

import numpy as np
import pandas as pd

import scipy.constants as sc

import plotly
import plotly.graph_objects as go

from fastoad.io import VariableIO

import os.path as pth

from IPython.display import clear_output, display

import ipywidgets as widgets
import ipyvuetify as v

import fastoad.api as oad

from fast_pedago.utils import (
    OUTPUT_FILE_SUFFIX,
    FLIGHT_DATA_FILE_SUFFIX,
)

FIGURE_HEIGHT = 450
COLORS = plotly.colors.qualitative.Plotly


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
            class_="pa-0",
            children=[
                self.file_selector,
                self.output,
            ],
        )

    def change_graph(self, plot_name: str):
        self.plot_name = plot_name
        self.file_selector.hide()
        
        if plot_name == GRAPH['General'][0]:
            self.plot_function = self._variable_viewer
            self.file_selector.show()
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
            self.file_selector.show()
        elif plot_name == GRAPH['Performances'][0]:
            self.plot_function = self._mission_plot
        elif plot_name == GRAPH['Performances'][1]:
            self.plot_function = self._payload_range_plot
        
        self.plot()


    def plot(self, data = None):
        if data:
            self.data = data
            self.file_selector.items = data
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

        with self.output:
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
        
        with self.output:
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

                fig = self._simplified_payload_range_plot(
                    path_to_output_file,
                    path_to_flight_data_file,
                    sizing_process_to_add,
                    fig=fig,
                )
                fig.update_layout(height=FIGURE_HEIGHT, title_font_size=10)

            if fig:
                display(fig)


    def _base_plot(self, oad_plot, data, is_single_output=False) -> widgets.Output:
        # data contains a list of outputs or a single output, depending on the graph
        # If there is no data, the rest of the code will be enough to clear the screen
        if type(data) == str:
            sizing_process_to_display = [data]
        else:
            sizing_process_to_display = data

        with self.output:
            clear_output()
            fig = None
            
            for sizing_process_to_add in sizing_process_to_display:
                if sizing_process_to_add:
                    path_to_output_file = pth.join(
                        self.path_to_output_folder,
                        sizing_process_to_add + OUTPUT_FILE_SUFFIX,
                    )
                                
                    # The plot function have a simplified signature if only one output can be added
                    if len(sizing_process_to_display) == 1 or is_single_output:
                        fig = oad_plot(path_to_output_file)
                        # Leave the loop is the graph can only plot one
                        # output at a time. Only the first data will be
                        # plotted
                        if is_single_output:
                            self.file_selector.v_model = sizing_process_to_add
                            break

                    else:
                        fig = oad_plot(path_to_output_file, sizing_process_to_add, fig=fig)
                
            if fig:
                fig.update_layout(height=FIGURE_HEIGHT, title_font_size=10)
                display(fig)


    # pylint: disable-msg=too-many-locals
    def _simplified_payload_range_plot(self,
        aircraft_file_path: str,
        flight_data_file_path: str,
        name=None,
        fig=None,
        *,
        file_formatter=None
    ) -> go.FigureWidget:
        """
        Returns a figure plot of the payload range diagram of the aircraft. Relies on Breguet's range
        equation.
        Different designs can be superposed by providing an existing fig.
        Each design can be provided a name.

        :param aircraft_file_path: path of the aircraft data file
        :param flight_data_file_path: path of flight data file
        :param name: name to give to the trace added to the figure
        :param fig: existing figure to which add the plot
        :param file_formatter: the formatter that defines the format of data file. If not provided,
                            default format will be assumed.
        :return: wing plot figure
        """

        variables = VariableIO(aircraft_file_path, file_formatter).read()

        mtow = variables["data:weight:aircraft:MTOW"].value[0]
        owe = variables["data:weight:aircraft:OWE"].value[0]
        mfw = variables["data:weight:aircraft:MFW"].value[0]
        max_payload = variables["data:weight:aircraft:max_payload"].value[0]

        # When running an MD0, since we are using breguet we don't have access to
        # "data:mission:sizing:reserve:fuel" hence why we approximate it like that
        reserve = (
            variables["data:mission:sizing:needed_block_fuel"].value[0]
            - variables["data:mission:sizing:main_route:fuel"].value[0]
        )

        nominal_range = variables["data:TLAR:range"].value[0]
        nominal_payload = variables["data:weight:aircraft:payload"].value[0]

        if fig is None:
            fig = go.Figure()
            color_counter = 0
        else:
            color_counter = len(fig.data)

        trace_colour = COLORS[color_counter % len(COLORS)]

        mean_tas, mean_sfc, mean_l_over_d = self._extract_value_from_flight_data_file(
            flight_data_file_path=flight_data_file_path
        )

        takeoff_mass_array = np.array([mtow, mtow, owe + mfw])
        payload_array = np.array([max_payload, mtow - owe - mfw, 0.0])
        landing_mass_array = payload_array + owe + reserve

        # Initial solve only for points B, D, E
        range_array = (
            mean_tas
            * mean_l_over_d
            / (mean_sfc * sc.g)
            * np.log(takeoff_mass_array / landing_mass_array)
            / 1852.0
        )

        # Readjust so that the design point end up on the [B, D] segment. First find the linear
        # function that represent the [B, D] segment under the form y = a * x + b.

        coeff_a = (payload_array[0] - payload_array[1]) / (range_array[0] - range_array[1])
        coeff_b = payload_array[0] - coeff_a * range_array[0]

        # ow we readjust the range so that that function match the design point
        k_ra = (nominal_payload - coeff_b) / (coeff_a * nominal_range)

        payload_array_for_display = np.concatenate((np.array([max_payload]), payload_array))
        range_array_for_display = np.concatenate((np.zeros(1), range_array)) / k_ra

        scatter_external_bound = go.Scatter(
            x=range_array_for_display,
            y=payload_array_for_display,
            mode="lines",
            name=name,
            legendgroup=name,
            legendgrouptitle_text=name,
            line=dict(color=trace_colour),
        )
        scatter_nominal_mission = go.Scatter(
            x=[nominal_range],
            y=[nominal_payload],
            mode="markers",
            name=name + "-Design range",
            legendgroup=name,
            line=dict(color=trace_colour),
        )

        fig.add_trace(scatter_external_bound)
        fig.add_trace(scatter_nominal_mission)
        fig = go.FigureWidget(fig)
        fig.update_layout(
            height=FIGURE_HEIGHT,
            title_text="Payload-Range diagram",
            title_x=0.5,
            xaxis_title="Range [Nm]",
            yaxis_title="Payload [Kg]",
        )

        return fig


    def _extract_value_from_flight_data_file(self,
        flight_data_file_path: str,
    ) -> Tuple[float, float, float]:
        """
        Extract from the flight data point file the average value during cruise to compute Breguet's
        range equation.

        :param flight_data_file_path: path of flight data file
        :return: the average speed, sfc and lift-to-drag ratio during cruise
        """

        flight_data = pd.read_csv(flight_data_file_path, index_col=0)
        cruise_flight_data = flight_data.loc[
            flight_data["name"] == "sizing:main_route:cruise"
        ]

        mean_sfc = float(np.mean(cruise_flight_data["sfc [kg/N/s]"].to_numpy()))
        mean_l_over_d = float(
            np.mean(
                cruise_flight_data["CL [-]"].to_numpy()
                / cruise_flight_data["CD [-]"].to_numpy()
            )
        )
        # Actually constant over the flight
        mean_tas = float(cruise_flight_data["true_airspeed [m/s]"].to_numpy()[0])

        return mean_tas, mean_sfc, mean_l_over_d


    def _update_selection_data(self, widget, event, data):
        self.file_selector.items = self.data