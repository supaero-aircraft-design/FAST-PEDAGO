# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

from typing import Tuple

import numpy as np
import pandas as pd

import scipy.constants as sc
from scipy.optimize import root

import plotly
import plotly.graph_objects as go

from fastoad.io import VariableIO

COLS = plotly.colors.DEFAULT_PLOTLY_COLORS


# pylint: disable-msg=too-many-locals
def simplified_payload_range_plot(
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
    reserve = variables["data:mission:sizing:reserve:fuel"].value[0]

    nominal_range = variables["data:TLAR:range"].value[0]
    nominal_payload = variables["data:weight:aircraft:payload"].value[0]

    if fig is None:
        fig = go.Figure()
        color_counter = 0
    else:
        color_counter = len(fig.data)

    trace_colour = COLS[color_counter]

    mean_tas, mean_sfc, mean_l_over_d = _extract_value_from_flight_data_file(
        flight_data_file_path=flight_data_file_path
    )

    takeoff_mass_array = np.array([mtow, mtow, owe + mfw])
    payload_array = np.array([max_payload, mtow - owe - mfw, 0.0])
    landing_mass_array = payload_array + owe + reserve

    # Solve only for points B, D, E
    range_array = (
        root(
            fun=_delta_range,
            x0=np.array([3704.0e3, 4074.0e3, 5556.0e3]),
            args=(
                takeoff_mass_array,
                landing_mass_array,
                mean_tas * mean_l_over_d / (mean_sfc * sc.g),
            ),
            options={"xtol": 1e-3},
        ).x
        / 1852.0
    )

    payload_array_for_display = np.concatenate((np.array([max_payload]), payload_array))
    range_array_for_display = np.concatenate((np.zeros(1), range_array))

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
        name=name + "- Design range",
        legendgroup=name,
        line=dict(color=trace_colour),
    )

    fig.add_trace(scatter_external_bound)
    fig.add_trace(scatter_nominal_mission)
    fig = go.FigureWidget(fig)
    fig.update_layout(
        title_text="Payload-Range diagram",
        title_x=0.5,
        xaxis_title="Range [Nm]",
        yaxis_title="Payload [Kg]",
    )

    return fig


def _range_correction(mission_range: np.ndarray) -> np.ndarray:
    """
    Computes a corrective factor to adjust Breguet's range equation

    :param mission_range: range of the mission in m
    :return: corrective factor
    """
    # Convert in nm to use the correction coefficient in the proper unit
    mission_range_nm = mission_range * 1.0 / 1852.0
    k_ra = 1 - 0.895 * np.exp(-(mission_range_nm / 814.0))

    return k_ra


def _delta_range(
    mission_range: np.ndarray,
    takeoff_mass: np.ndarray,
    landing_mass: np.ndarray,
    prop_coeff: float,
) -> np.ndarray:
    """
    Rewriting of Breguet's range equation under the form f(x) = 0 with x the range

    :param mission_range: range of the different points of the payload-range diagram in m
    :param takeoff_mass: mass at the start of the flight for the different points
    :param landing_mass: mass at the end of the flight for the different points
    :param prop_coeff: correspond to V * f/(sfc * g), which is considered constant on all points
    :return: deltas at the different point to drive to 0.0
    """

    delta = mission_range / _range_correction(mission_range) - prop_coeff * np.log(
        takeoff_mass / landing_mass
    )

    return delta


def _extract_value_from_flight_data_file(
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


# TODO: Implement a way to get the mean sfc, cruise speed and lift-to_drag ratio based on the
#  flight data
# TODO: Implement a function that computes the correction coefficient for Breguet's range equation
