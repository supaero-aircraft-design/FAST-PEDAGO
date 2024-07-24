"""
This file is used to make sure all the plotting functions have the same signature:
aircraft_file_path, flight_data_file_path, name, fig, and return go.FigureWidget
so they can be plotted using the same base function.
"""

import plotly.graph_objects as go

from .functions import (
    _aircraft_front_view_plot,
    _aircraft_side_view_plot,
    _aircraft_top_view_plot,
    _flaps_and_slats_plot,
    _polar_with_L_R_ratio_plot,
    _simplified_payload_range_plot,
    _stability_diagram_plot,
    _static_margin_plot,
    _wing_plot,
)

import fastoad.api as oad


# TODO: Have a decorator to convert an aircraft name directly into aircraft_file_path and
# TODO: flight_data_file_path to avoid having long signatures ?


def aircraft_front_view_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return _aircraft_front_view_plot(aircraft_file_path, name, fig)


def aircraft_side_view_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return _aircraft_side_view_plot(aircraft_file_path, name, fig)


def aircraft_top_view_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return _aircraft_top_view_plot(aircraft_file_path, name, fig)


def flaps_and_slats_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return _flaps_and_slats_plot(aircraft_file_path, name, fig)


def simplified_payload_range_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return _simplified_payload_range_plot(
        aircraft_file_path, flight_data_file_path, name, fig
    )


def stability_diagram_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return _stability_diagram_plot(aircraft_file_path, name, fig)


def wing_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return _wing_plot(aircraft_file_path, name, fig)


def variable_viewer(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return oad.variable_viewer(aircraft_file_path)


def aircraft_geometry_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return oad.aircraft_geometry_plot(aircraft_file_path, name, fig)


def drag_polar_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return oad.drag_polar_plot(aircraft_file_path, name, fig)


def mass_breakdown_bar_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return oad.mass_breakdown_bar_plot(aircraft_file_path, name, fig)


def mass_breakdown_sun_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return oad.mass_breakdown_sun_plot(aircraft_file_path)


def wing_geometry_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return oad.wing_geometry_plot(aircraft_file_path, name, fig)


def polar_with_L_R_ratio_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return _polar_with_L_R_ratio_plot(aircraft_file_path, name, fig)


def static_margin_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name: str = None,
    fig: go.Figure = None,
) -> go.FigureWidget:
    return _static_margin_plot(aircraft_file_path, name, fig)
