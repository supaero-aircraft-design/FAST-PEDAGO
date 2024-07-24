from os import PathLike
from typing import Union

import numpy as np
import plotly.graph_objects as go

from fastoad.io import VariableIO

from ..plot_constants import COLORS


def _polar_with_L_R_ratio_plot(
    aircraft_file_path: Union[str, PathLike],
    name=None,
    fig=None,
    *,
    file_formatter=None
) -> go.FigureWidget:
    """
    Returns a figure plot of the aircraft drag polar.
    Different designs can be superposed by providing an existing fig.
    Each design can be provided a name.

    :param aircraft_file_path: path of data file
    :param name: name to give to the trace added to the figure
    :param fig: existing figure to which add the plot
    :param file_formatter: the formatter that defines the format of data file. If not provided,
                           default format will be assumed.
    :return: wing plot figure
    """
    variables = VariableIO(aircraft_file_path, file_formatter).read()

    # pylint: disable=invalid-name # that's a common naming
    cd = np.asarray(variables["data:aerodynamics:aircraft:cruise:CD"].value)
    # pylint: disable=invalid-name # that's a common naming
    cl = np.asarray(variables["data:aerodynamics:aircraft:cruise:CL"].value)

    L_D_max = variables["data:aerodynamics:aircraft:cruise:L_D_max"].value[0]

    # TODO: remove filtering one models provide proper bounds
    cd_short = cd[cd <= 2.0]
    cl_short = cl[cd <= 2.0]

    L_D_max_index = [
        i
        for i in range(len(cd_short))
        if cd_short[i] != 0 and cl_short[i] / cd_short[i] == L_D_max
    ][0]

    if fig is None:
        fig = go.Figure()

    # Same color for each aircraft configuration
    color_index = int(len(fig.data) / 2) % 10

    scatter = go.Scatter(
        x=cd_short,
        y=cl_short,
        mode="lines",
        name=name + " | L/R max = " + str(round(L_D_max, 3)),
        legendgroup=name,
        line=dict(color=COLORS[color_index]),
    )

    scatter_L_R_max = go.Scatter(
        x=[cd_short[L_D_max_index]],
        y=[cl_short[L_D_max_index]],
        mode="markers",
        name="L/R max",
        legendgroup=name,
        showlegend=False,
        line=dict(color=COLORS[color_index]),
    )

    scatter_tangent = go.Scatter(
        x=[0, cd_short[L_D_max_index]],
        y=[0, cl_short[L_D_max_index]],
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
        line=dict(color=COLORS[color_index], width=1),
    )

    fig.add_trace(scatter)
    fig.add_trace(scatter_L_R_max)
    fig.add_trace(scatter_tangent)

    fig = go.FigureWidget(fig)

    fig.update_layout(
        title_text="Drag Polar", title_x=0.5, xaxis_title="Cd", yaxis_title="Cl"
    )

    return fig
