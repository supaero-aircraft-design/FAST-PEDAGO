from typing import Tuple

import numpy as np
import pandas as pd
import scipy.constants as sc

import plotly.graph_objects as go

from fastoad.io import VariableIO

from ..plot_constants import COLORS


def _simplified_payload_range_plot(
    aircraft_file_path: str,
    flight_data_file_path: str,
    name=None,
    fig=None,
    *,
    file_formatter=None
) -> go.FigureWidget:
    """
    Returns a figure plot of the payload range diagram of the aircraft. Relies
    on Breguet's range equation.
    Different designs can be superposed by providing an existing fig.
    Each design can be provided a name.

    :param aircraft_file_path: path of the aircraft data file
    :param flight_data_file_path: path of flight data file
    :param name: name to give to the trace added to the figure
    :param fig: existing figure to which add the plot
    :param file_formatter: the formatter that defines the format of data file.
        If not provided,
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

    mean_tas, mean_sfc, mean_l_over_d = _extract_value_from_flight_data_file(
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

    # Readjust so that the design point end up on the [B, D] segment. First
    # find the linear function that represent the [B, D] segment under the
    # form y = a * x + b.

    coeff_a = (payload_array[0] - payload_array[1]) / (range_array[0] - range_array[1])
    coeff_b = payload_array[0] - coeff_a * range_array[0]

    # ow we readjust the range so that that function match the design point
    k_ra = (nominal_payload - coeff_b) / (coeff_a * nominal_range)

    payload_array_for_display = np.concatenate(
        (np.array([max_payload]), payload_array),
    )
    range_array_for_display = np.concatenate((np.zeros(1), range_array)) / k_ra

    if fig is None:
        fig = go.Figure()

    # Same color for each aircraft configuration
    color_index = int(len(fig.data) / 2) % 10

    scatter_external_bound = go.Scatter(
        x=range_array_for_display,
        y=payload_array_for_display,
        mode="lines",
        name=name + " | · = Design",
        legendgroup=name,
        line=dict(color=COLORS[color_index]),
    )
    scatter_nominal_mission = go.Scatter(
        x=[nominal_range],
        y=[nominal_payload],
        mode="markers",
        legendgroup=name,
        showlegend=False,
        line=dict(color=COLORS[color_index]),
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


def _extract_value_from_flight_data_file(
    flight_data_file_path: str,
) -> Tuple[float, float, float]:
    """
    Extract from the flight data point file the average value during cruise to
    compute Breguet's range equation.

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
