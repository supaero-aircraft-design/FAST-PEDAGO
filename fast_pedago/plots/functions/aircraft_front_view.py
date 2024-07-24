import numpy as np
import plotly.graph_objects as go

from fastoad.io import VariableIO

from ..plot_constants import (
    COLORS,
    HT_HEIGHT,
    HT_DIHEDRAL,
    ENGINE_HEIGHT,
    WING_ROOT_HEIGHT,
)


def _aircraft_front_view_plot(
    aircraft_file_path: str,
    name=None,
    fig=None,
    file_formatter=None,
) -> go.FigureWidget:
    """
    Returns a figure plot of the front view of the aircraft with the engines,
    the flaps, the slats and the elevator.
    Different designs can be superposed by providing an existing fig.
    Each design can be provided a name.

    :param aircraft_file_path: path of data file
    :param name: name to give to the trace added to the figure
    :param fig: existing figure to which add the plot
    :param file_formatter: the formatter that defines the format of data file.
        If not provided,
        default format will be assumed.
    :param height : height of the image
    :param width : width of the image
    :return: wing plot figure
    """
    variables = VariableIO(aircraft_file_path, file_formatter).read()

    # Wing parameters
    wing_tip_y = variables["data:geometry:wing:tip:y"].value[0]

    # Horizontal tail parameters
    ht_span = variables["data:geometry:horizontal_tail:span"].value[0]

    # Vertical tail parameters
    vt_span = variables["data:geometry:vertical_tail:span"].value[0]

    # Fuselage parameters
    fuselage_max_height = variables["data:geometry:fuselage:maximum_height"].value[0]
    fuselage_max_width = variables["data:geometry:fuselage:maximum_width"].value[0]

    # Nacelle and pylon values parameters :
    nacelle_diameter = variables["data:geometry:propulsion:nacelle:diameter"].value[0]
    nacelle_y = variables["data:geometry:propulsion:nacelle:y"].value[0]

    # Front view (y-z)

    y_fuselage = np.linspace(
        -fuselage_max_width / 2.0,
        fuselage_max_width / 2.0,
        100,
    )
    z_fuselage = (
        np.sqrt(1 - (y_fuselage / (fuselage_max_width / 2.0)) ** 2)
        * fuselage_max_height
        / 2.0
    )
    y_fuselage2 = y_fuselage
    z_fuselage2 = -z_fuselage
    y_fuselage3, z_fuselage3 = _make_circle(
        0, -fuselage_max_height * 1 / 10, fuselage_max_height / 8.0
    )

    z_wing = np.array(
        [
            -fuselage_max_height * WING_ROOT_HEIGHT,
            0.0,
        ]
    )

    y_wing = np.array(
        [
            np.sqrt(1 - (z_wing[0] / (fuselage_max_height / 2.0)) ** 2)
            * fuselage_max_width
            / 2.0,
            wing_tip_y,
        ]
    )

    z_wing2 = 1 * z_wing
    y_wing2 = -1 * y_wing

    z_engine_center = -fuselage_max_height * ENGINE_HEIGHT
    y_engine_center = nacelle_y

    y_engine, z_engine = _make_circle(
        y_engine_center, z_engine_center, nacelle_diameter / 2.0
    )
    y_engine2, z_engine2 = _make_circle(
        -y_engine_center, z_engine_center, nacelle_diameter / 2.0
    )
    y_engine3, z_engine3 = _make_circle(
        y_engine_center, z_engine_center, nacelle_diameter / 8.0
    )
    y_engine4, z_engine4 = _make_circle(
        -1 * y_engine_center, z_engine_center, nacelle_diameter / 8.0
    )

    z_ht = np.array(
        [
            fuselage_max_height * HT_HEIGHT,
            fuselage_max_height * HT_DIHEDRAL,
        ]
    )

    y_ht = np.array(
        [
            np.sqrt(1 - (z_ht[0] / (fuselage_max_height / 2.0)) ** 2)
            * fuselage_max_width
            / 2.0,
            ht_span / 2.0,
        ]
    )

    y_ht2 = -1 * y_ht
    z_ht2 = 1 * z_ht

    y_vt = np.array([0, 0])
    z_vt = np.array(
        [fuselage_max_height / 2.0, fuselage_max_height / 2.0 + vt_span],
    )

    y_cockpit = np.array(
        [
            fuselage_max_width / 2.0 * 2.5 / 5,
            fuselage_max_width / 2.0 * 3.5 / 5,
            -fuselage_max_width / 2.0 * 3.5 / 5,
            -fuselage_max_width / 2.0 * 2.5 / 5,
            fuselage_max_width / 2.0 * 2.5 / 5,
        ]
    )

    z_cockpit = np.array(
        [
            fuselage_max_height / 2.0 * 3.5 / 5,
            fuselage_max_height / 2.0 * 1 / 5,
            fuselage_max_height / 2.0 * 1 / 5,
            fuselage_max_height / 2.0 * 3.5 / 5,
            fuselage_max_height / 2.0 * 3.5 / 5,
        ]
    )

    y_cockpit2 = np.array([0, 0])
    z_cockpit2 = np.array(
        [
            fuselage_max_height / 2.0 * 3.5 / 5,
            fuselage_max_height / 2.0 * 1 / 5,
        ]
    )

    if fig is None:
        fig = go.Figure()

    # Same color for a given aircraft
    # It is divided by 14 since their are 14 scatters
    color_index = int(len(fig.data) / 14) % 10

    scatter_fuselage = go.Scatter(
        x=y_fuselage,
        y=z_fuselage,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
    )

    scatter_fuselage2 = go.Scatter(
        x=y_fuselage2,
        y=z_fuselage2,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_wing = go.Scatter(
        x=y_wing,
        y=z_wing,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_wing2 = go.Scatter(
        x=y_wing2,
        y=z_wing2,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_engine = go.Scatter(
        x=y_engine,
        y=z_engine,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_engine2 = go.Scatter(
        x=y_engine2,
        y=z_engine2,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_engine3 = go.Scatter(
        x=y_engine3,
        y=z_engine3,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_engine4 = go.Scatter(
        x=y_engine4,
        y=z_engine4,
        line=dict(color=COLORS[color_index]),
        fill="tonexty",
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_fuselage3 = go.Scatter(
        x=y_fuselage3,
        y=z_fuselage3,
        line=dict(color=COLORS[color_index]),
        fill="tonexty",
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_ht = go.Scatter(
        x=y_ht,
        y=z_ht,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_ht2 = go.Scatter(
        x=y_ht2,
        y=z_ht2,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )
    scatter_vt = go.Scatter(
        x=y_vt,
        y=z_vt,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_cockpit = go.Scatter(
        x=y_cockpit,
        y=z_cockpit,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_cockpit2 = go.Scatter(
        x=y_cockpit2,
        y=z_cockpit2,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    fig.add_trace(scatter_fuselage)
    fig.add_trace(scatter_fuselage2)
    fig.add_trace(scatter_wing)
    fig.add_trace(scatter_wing2)
    fig.add_trace(scatter_ht)
    fig.add_trace(scatter_ht2)
    fig.add_trace(scatter_vt)
    fig.add_trace(scatter_cockpit)
    fig.add_trace(scatter_cockpit2)
    fig.add_trace(scatter_engine)
    fig.add_trace(scatter_engine2)
    fig.add_trace(scatter_engine3)
    fig.add_trace(scatter_fuselage3)
    fig.add_trace(scatter_engine4)

    fig.layout = go.Layout(yaxis=dict(scaleanchor="x", scaleratio=1))

    if name is None:
        fig.update_layout(
            title_text="Aircraft Geometry (front view)",
            title_x=0.5,
            xaxis_title="y",
            yaxis_title="z",
        )
    if name is not None:
        fig.update_layout(
            title_text="Aircraft Geometry (front view)",
            title_x=0.5,
            xaxis_title="y",
            yaxis_title="z",
        )

    fig = go.FigureWidget(fig)

    return fig


def _make_circle(center_x: float, center_y: float, radius: float):
    """
    Inner function used in the functions above
    returns 2 ndarrays containing a the x and y coordinates of a circle of
    radius centered in (center_x,center_y)

    :param center_x: x coordinate of the circle's center
    :param center_y: y coordinate of the circle's center
    :param radius: radius of the circle

    :return: 2 ndarrays with the circle coordinates
    """

    x = np.linspace(-radius, radius, 50)
    y = np.sqrt(radius ** 2 - x ** 2)
    x = np.concatenate((x, np.flip(x)))
    y = np.concatenate((y, -y))

    x = np.append(x, x[0])
    y = np.append(y, y[0])

    x += center_x
    y += center_y

    return x, y
