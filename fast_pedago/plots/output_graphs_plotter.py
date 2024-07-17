from typing import List, Union
from typing import Callable

import plotly.graph_objects as go

import ipywidgets as widgets
import ipyvuetify as v
from IPython.display import clear_output, display

from fast_pedago.plots import (
    simplified_payload_range_plot,
    stability_diagram_plot,
    aircraft_top_view_plot,
    aircraft_front_view_plot,
    aircraft_side_view_plot,
    flaps_and_slats_plot,
    wing_plot,
    variable_viewer,
    mass_breakdown_bar_plot,
    mass_breakdown_sun_plot,
    drag_polar_plot,
    wing_geometry_plot,
    aircraft_geometry_plot,
    polar_with_L_R_ratio_plot,
    static_margin_plot,
    BetterMissionViewer,
)

from fast_pedago.utils import (
    PathManager,
    OUTPUT_FILE_SUFFIX,
    FLIGHT_DATA_FILE_SUFFIX,
)


# When a new graph is added, it should be added to the dict, and then
# be plotted in the Plotter.
# To add a graph, add its plotting function, and 'True' if the graph is
# made to plot only one aircraft, False either.
# If the plotting function has a particularity such as a different signature
# (simplified_payload_range) or a particular way to be plotted (mission),
# modify the _base_plot function to add the cases.
GRAPH = {
    "General": {
        "Variables": [
            variable_viewer,
            True,
        ],
    },
    "Geometry": {
        "Aircraft": [
            aircraft_geometry_plot,
            False,
        ],
        "Wing": [
            wing_geometry_plot,
            False,
        ],
        "Front view": [
            aircraft_front_view_plot,
            False,
        ],
        "Side view": [
            aircraft_side_view_plot,
            False,
        ],
        "Top view": [
            aircraft_top_view_plot,
            False,
        ],
        "Flaps and slats": [
            flaps_and_slats_plot,
            False,
        ],
        "Detailed wing": [
            wing_plot,
            True,
        ],
    },
    "Aerodynamics": {
        "Stability diagram": [
            stability_diagram_plot,
            True,
        ],
        "Static margin": [
            static_margin_plot,
            False,
        ],
        "Drag polar": [
            drag_polar_plot,
            False,
        ],
        "Polar with max L/R": [
            polar_with_L_R_ratio_plot,
            False,
        ],
    },
    "Mass": {
        "Bar breakdown": [
            mass_breakdown_bar_plot,
            False,
        ],
        "Sun breakdown": [
            mass_breakdown_sun_plot,
            True,
        ],
    },
    "Performances": {
        "Mission": [
            None,
            False,
        ],
        "Payload-Range": [
            simplified_payload_range_plot,
            False,
        ],
    },
}


class OutputGraphsPlotter:
    """
    A class that manages the plot of all the available figures.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Stores the current plot name, plot function, and data
        self.plot_category = ""
        self.plot_name = ""
        self.plot_function: Callable = None
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
            label="This graph only displays one output, please choose one.",
        )
        self.file_selector.on_event("click", self._update_selection_data)
        self.file_selector.on_event(
            "change", lambda widget, event, data: self._base_plot(data)
        )
        self.file_selector.hide()

        self.output_display = v.Container(
            class_="pa-2",
            fluid=True,
            children=[
                self.file_selector,
                self.output,
            ],
        )

    def change_graph(self, plot_category: str, plot_name: str):
        """
        Changes the plotting function to another one, and displays a
        file selector for when the figure only allows one aircraft,
        then plots the new figure.

        :param plot_name: the name of the new figure to plot.
            (standard name taken from GRAPH constant)
        """
        if plot_category in list(GRAPH):
            if plot_name in list(GRAPH[plot_category]):
                self.plot_category = plot_category
                self.plot_name = plot_name
                self.plot_function = GRAPH[plot_category][plot_name][0]
                self.is_single_output = GRAPH[plot_category][plot_name][1]

                if self.is_single_output:
                    self.file_selector.show()
                else:
                    self.file_selector.hide()

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

    def _base_plot(self, data: Union[str, List[str]]):
        """
        Base function to plot data. Add all aircraft to the given plot.

        :param data: all the aircraft to plot from (names of the aircraft)
        """
        # data contains a list of outputs or a single output, depending on the
        # graph. If there is no data, the rest of the code will be enough to
        # clear the screen.
        if isinstance(data, str):
            sizing_process_to_display = [data]
        else:
            sizing_process_to_display = data

        with self.output:
            # Clear actual graphs :
            clear_output()
            fig: go.Figure = None
            if self.plot_name == "Mission":
                mission_viewer = BetterMissionViewer()

            # Add every aircraft to the plot :
            for sizing_process_to_add in sizing_process_to_display:
                if sizing_process_to_add:

                    path_to_output_file = PathManager.path_to(
                        "output",
                        sizing_process_to_add + OUTPUT_FILE_SUFFIX,
                    )
                    path_to_flight_data_file = PathManager.path_to(
                        "output",
                        sizing_process_to_add + FLIGHT_DATA_FILE_SUFFIX,
                    )

                    # Mission plot works differently
                    if self.plot_name == "Mission":
                        mission_viewer.add_mission(
                            path_to_flight_data_file, sizing_process_to_add
                        )

                    else:
                        fig = self.plot_function(
                            path_to_output_file,
                            path_to_flight_data_file,
                            sizing_process_to_add,
                            fig=fig,
                        )
                        if self.is_single_output:
                            self.file_selector.v_model = sizing_process_to_add
                            break

            # Display the plots
            if fig:
                fig.update_layout(
                    title=None,
                    autosize=True,
                    margin=go.layout.Margin(
                        l=0,
                        r=20,
                        b=0,
                        t=30,
                    ),
                )
                fig.update_annotations(font_size=12)
                display(fig)

            elif self.plot_name == "Mission":
                mission_viewer.update_layout(
                    {
                        "title": None,
                        "margin": go.layout.Margin(
                            l=0,
                            r=20,
                            b=0,
                            t=27,
                        ),
                    }
                )
                if mission_viewer.missions:
                    mission_viewer.display()

    def _update_selection_data(self, widget, event, data):
        """
        Updates the file selector with the pre-selected aircraft to choose
        among them for single aircraft figures.
        """
        self.file_selector.items = self.data
