import numpy as np
import plotly.graph_objects as go

from fastoad.io import VariableIO

from ..plot_constants import (
    COLORS,
    NACELLE_POSITION,
    HT_HEIGHT,
    HT_DIHEDRAL,
    ENGINE_HEIGHT,
    WING_ROOT_HEIGHT,
)


def _aircraft_side_view_plot(
    aircraft_file_path: str,
    name=None,
    fig=None,
    file_formatter=None,
) -> go.FigureWidget:
    """
    Returns a figure plot of the side view of the aircraft with the engines,
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
    wing_tip_leading_edge_x = variables[
        "data:geometry:wing:tip:leading_edge:x:local"
    ].value[0]
    wing_root_chord = variables["data:geometry:wing:root:chord"].value[0]
    wing_tip_chord = variables["data:geometry:wing:tip:chord"].value[0]
    wing_kink_chord = variables["data:geometry:wing:kink:chord"].value[0]
    wing_kink_leading_edge_x = variables[
        "data:geometry:wing:kink:leading_edge:x:local"
    ].value[0]
    mac25_x_position = variables["data:geometry:wing:MAC:at25percent:x"].value[0]
    distance_root_mac_chords = variables[
        "data:geometry:wing:MAC:leading_edge:x:local"
    ].value[0]
    mean_aerodynamic_chord = variables["data:geometry:wing:MAC:length"].value[0]

    # Horizontal tail parameters
    ht_root_chord = variables["data:geometry:horizontal_tail:center:chord"].value[0]
    ht_tip_chord = variables["data:geometry:horizontal_tail:tip:chord"].value[0]
    ht_sweep_0 = variables["data:geometry:horizontal_tail:sweep_0"].value[0]
    local_ht_25mac_x = variables[
        "data:geometry:horizontal_tail:MAC:at25percent:x:local"
    ].value[0]
    ht_distance_from_wing = variables[
        "data:geometry:horizontal_tail:MAC:at25percent:x:from_wingMAC25"
    ].value[0]
    ht_span = variables["data:geometry:horizontal_tail:span"].value[0]

    # Vertical tail parameters
    vt_root_chord = variables["data:geometry:vertical_tail:root:chord"].value[0]
    vt_tip_chord = variables["data:geometry:vertical_tail:tip:chord"].value[0]
    vt_sweep_0 = variables["data:geometry:vertical_tail:sweep_0"].value[0]
    local_vt_25mac_x = variables[
        "data:geometry:vertical_tail:MAC:at25percent:x:local"
    ].value[0]
    vt_distance_from_wing = variables[
        "data:geometry:vertical_tail:MAC:at25percent:x:from_wingMAC25"
    ].value[0]
    vt_span = variables["data:geometry:vertical_tail:span"].value[0]

    # CGs
    wing_25mac_x = variables["data:geometry:wing:MAC:at25percent:x"].value[0]
    wing_mac_length = variables["data:geometry:wing:MAC:length"].value[0]
    local_wing_mac_le_x = variables[
        "data:geometry:wing:MAC:leading_edge:x:local"
    ].value[0]

    # Fuselage parameters
    fuselage_max_height = variables["data:geometry:fuselage:maximum_height"].value[0]
    fuselage_length = variables["data:geometry:fuselage:length"].value[0]
    fuselage_front_length = variables["data:geometry:fuselage:front_length"].value[0]
    fuselage_rear_length = variables["data:geometry:fuselage:rear_length"].value[0]

    # Nacelle and pylon values parameters :
    nacelle_diameter = variables["data:geometry:propulsion:nacelle:diameter"].value[0]
    nacelle_length = variables["data:geometry:propulsion:nacelle:length"].value[0]

    """
    Side view : x-z
    """
    # 1 fuselage

    z_fuselage_front = np.flip(np.linspace(0, fuselage_max_height / 2, 10))
    x_fuselage_front = (
        fuselage_front_length / (0.5 * fuselage_max_height) ** 2 * z_fuselage_front ** 2
    )

    z_nose_cone = np.linspace(
        -fuselage_max_height / 8.0, fuselage_max_height / 8.0, 100
    )
    x_nose_cone = (
        fuselage_front_length / (0.5 * fuselage_max_height) ** 2 * z_nose_cone ** 2
    )

    z_nose_cone = np.append(z_nose_cone, z_nose_cone[0])
    x_nose_cone = np.append(x_nose_cone, x_nose_cone[0])

    z_cockpit = np.linspace(
        fuselage_max_height / 2.0 * 1 / 5,
        fuselage_max_height / 2.0 * 3.5 / 5,
        50,
    )
    x_cockpit = (
        fuselage_front_length / (0.5 * fuselage_max_height) ** 2 * z_cockpit ** 2
    )

    z_cockpit = np.append(z_cockpit, z_cockpit[-1])
    z_cockpit = np.append(z_cockpit, z_cockpit[0])
    z_cockpit = np.append(z_cockpit, z_cockpit[0])
    x_cockpit = np.append(x_cockpit, fuselage_front_length * 4 / 5)
    x_cockpit = np.append(x_cockpit, fuselage_front_length * 4 / 5)
    x_cockpit = np.append(x_cockpit, x_cockpit[0])

    x_fuselage_middle = np.array(
        [
            fuselage_front_length,
            fuselage_length - fuselage_rear_length,
        ]
    )

    z_fuselage_middle = np.array(
        [
            fuselage_max_height / 2.0,
            fuselage_max_height / 2.0,
        ]
    )

    r = fuselage_max_height / 8
    x_fuselage_rear = np.array(
        [fuselage_length - fuselage_rear_length, fuselage_length - r]
    )

    z_fuselage_rear = np.array([fuselage_max_height / 2.0, fuselage_max_height / 2.0])

    z_centre = fuselage_max_height / 2.0 - r
    x_centre = fuselage_length - r

    z_rear = np.linspace(
        fuselage_max_height / 2.0, fuselage_max_height / 2.0 - 2 * r, 10
    )
    x_rear = np.sqrt(abs(r ** 2 - (z_rear - z_centre) ** 2)) + x_centre

    x_fuselage_front = np.concatenate(
        (x_fuselage_front, np.flip(x_fuselage_front)),
    )
    z_fuselage_front = np.concatenate(
        (z_fuselage_front, np.flip(-z_fuselage_front)),
    )

    x_belly = np.array(
        [
            fuselage_front_length,
            fuselage_length - fuselage_rear_length,
            fuselage_length - r,
        ]
    )
    z_belly = np.array(
        [
            -fuselage_max_height / 2.0,
            -fuselage_max_height / 2.0,
            fuselage_max_height / 2.0 - 2 * r,
        ]
    )

    # 2 wing

    x_wing = np.array(
        [
            0.0,
            wing_root_chord,
            wing_kink_leading_edge_x + wing_kink_chord,
            wing_tip_leading_edge_x + wing_tip_chord,
            wing_tip_leading_edge_x,
            0.0,
        ]
    )
    x_wing = x_wing + (
        mac25_x_position - distance_root_mac_chords - 0.25 * mean_aerodynamic_chord
    )

    z_wing = np.array(
        [
            -fuselage_max_height * WING_ROOT_HEIGHT,
            -fuselage_max_height * WING_ROOT_HEIGHT,
            -fuselage_max_height / 8.0,
            0.0,
            0.0,
            -fuselage_max_height * WING_ROOT_HEIGHT,
        ]
    )

    # 3 engine

    x_engine = np.array(
        [-nacelle_length, -nacelle_length, 0, 0, -nacelle_length],
    )

    x_engine += (
        wing_25mac_x
        - 0.25 * wing_mac_length
        - local_wing_mac_le_x
        + NACELLE_POSITION * nacelle_length
    )
    z_engine = np.array(
        [
            -fuselage_max_height * ENGINE_HEIGHT + nacelle_diameter / 2.0,
            -fuselage_max_height * ENGINE_HEIGHT - nacelle_diameter / 2.0,
            -fuselage_max_height * ENGINE_HEIGHT - nacelle_diameter / 2.0,
            -fuselage_max_height * ENGINE_HEIGHT + nacelle_diameter / 2.0,
            -fuselage_max_height * ENGINE_HEIGHT + nacelle_diameter / 2.0,
        ]
    )

    # 4 vertical tail

    x_vt = np.array(
        [
            0.0,
            vt_span * np.tan(vt_sweep_0 * np.pi / 180),
            vt_span * np.tan(vt_sweep_0 * np.pi / 180) + vt_tip_chord,
            vt_root_chord,
            0.0,
        ]
    )
    x_vt += wing_25mac_x + vt_distance_from_wing - local_vt_25mac_x
    z_vt = np.array(
        [
            fuselage_max_height / 2.0,
            fuselage_max_height / 2.0 + vt_span,
            fuselage_max_height / 2.0 + vt_span,
            fuselage_max_height / 2.0,
            fuselage_max_height / 2.0,
        ]
    )

    # 5 horizontal tail

    x_ht = np.array(
        [
            0.0,
            ht_span / 2.0 * np.tan(ht_sweep_0 * np.pi / 180),
            ht_tip_chord + ht_span / 2.0 * np.tan(ht_sweep_0 * np.pi / 180),
            ht_root_chord,
            0.0,
        ]
    )
    x_ht += wing_25mac_x + ht_distance_from_wing - local_ht_25mac_x

    z_ht = np.array(
        [
            fuselage_max_height * HT_HEIGHT,
            fuselage_max_height * HT_DIHEDRAL,
            fuselage_max_height * HT_DIHEDRAL,
            fuselage_max_height * HT_HEIGHT,
            fuselage_max_height * HT_HEIGHT,
        ]
    )

    # Plotting
    if fig is None:
        fig = go.Figure()

    # Same color for a given aircraft
    # It is divided by 14 since their are 14 scatters
    color_index = int(len(fig.data) / 11) % 10

    scatter_front = go.Scatter(
        x=x_fuselage_front,
        y=z_fuselage_front,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
    )

    scatter_middle = go.Scatter(
        x=x_fuselage_middle,
        y=z_fuselage_middle,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_fuselage_rear = go.Scatter(
        x=x_fuselage_rear,
        y=z_fuselage_rear,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_rear = go.Scatter(
        x=x_rear,
        y=z_rear,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_belly = go.Scatter(
        x=x_belly,
        y=z_belly,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_wing = go.Scatter(
        x=x_wing,
        y=z_wing,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_engine = go.Scatter(
        x=x_engine,
        y=z_engine,
        fill="tonexty",
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_ht = go.Scatter(
        x=x_ht,
        y=z_ht,
        line=dict(color=COLORS[color_index]),
        fill="tonexty",
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_vt = go.Scatter(
        x=x_vt,
        y=z_vt,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_nose_cone = go.Scatter(
        x=x_nose_cone,
        y=z_nose_cone,
        line=dict(color=COLORS[color_index]),
        fill="tonexty",
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    scatter_cockpit = go.Scatter(
        x=x_cockpit,
        y=z_cockpit,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    fig.add_trace(scatter_front)
    fig.add_trace(scatter_middle)
    fig.add_trace(scatter_rear)
    fig.add_trace(scatter_fuselage_rear)
    fig.add_trace(scatter_belly)
    fig.add_trace(scatter_vt)
    fig.add_trace(scatter_cockpit)
    fig.add_trace(scatter_wing)
    fig.add_trace(scatter_engine)
    fig.add_trace(scatter_ht)
    fig.add_trace(scatter_nose_cone)

    fig.layout = go.Layout(yaxis=dict(scaleanchor="x", scaleratio=1))

    if name is None:
        fig.update_layout(
            title_text="Aircraft Geometry (side view)",
            title_x=0.5,
            xaxis_title="y",
            yaxis_title="z",
        )
    if name is not None:
        fig.update_layout(
            title_text="Aircraft Geometry (side view)",
            title_x=0.5,
            xaxis_title="y",
            yaxis_title="z",
        )
    fig = go.FigureWidget(fig)
    return fig
