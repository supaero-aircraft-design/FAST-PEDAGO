import numpy as np
import plotly.graph_objects as go

from fastoad.io import VariableIO

from ..plot_constants import COLORS


def _flaps_and_slats_plot(
    aircraft_file_path: str,
    name=None,
    fig=None,
    file_formatter=None,
) -> go.FigureWidget:
    """
    Returns a figure plot of the top view of the wing with the flaps and slats
    added.
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
    :return: plot figure of wing the wing with flaps and slats
    """
    variables = VariableIO(aircraft_file_path, file_formatter).read()

    wing_kink_leading_edge_x = variables[
        "data:geometry:wing:kink:leading_edge:x:local"
    ].value[0]
    wing_tip_leading_edge_x = variables[
        "data:geometry:wing:tip:leading_edge:x:local"
    ].value[0]
    wing_root_y = variables["data:geometry:wing:root:y"].value[0]
    wing_kink_y = variables["data:geometry:wing:kink:y"].value[0]
    wing_tip_y = variables["data:geometry:wing:tip:y"].value[0]
    wing_root_chord = variables["data:geometry:wing:root:chord"].value[0]
    wing_kink_chord = variables["data:geometry:wing:kink:chord"].value[0]
    wing_tip_chord = variables["data:geometry:wing:tip:chord"].value[0]
    trailing_edge_kink_sweep_100_outer = variables[
        "data:geometry:wing:sweep_100_outer"
    ].value[0]

    slat_chord_ratio = variables["data:geometry:slat:chord_ratio"].value[0]
    slat_span_ratio = variables["data:geometry:slat:span_ratio"].value[0]

    total_wing_span = variables["data:geometry:wing:span"].value[0]
    flaps_span_ratio = variables["data:geometry:flap:span_ratio"].value[0]
    flaps_chord_ratio = variables["data:geometry:flap:chord_ratio"].value[0]

    mean_aerodynamic_chord = variables["data:geometry:wing:MAC:length"].value[0]
    mac25_x_position = variables["data:geometry:wing:MAC:at25percent:x"].value[0]
    distance_root_mac_chords = variables[
        "data:geometry:wing:MAC:leading_edge:x:local"
    ].value[0]

    # 1) overall wing
    # Part of the code dedicated to the geometry of the general wing

    y = np.array(
        [
            0,
            wing_root_y,
            wing_kink_y,
            wing_tip_y,
            wing_tip_y,
            wing_kink_y,
            wing_root_y,
            0,
            0,
        ]
    )
    y = np.concatenate((-y, y))

    x = np.array(
        [
            0,
            0,
            wing_kink_leading_edge_x,
            wing_tip_leading_edge_x,
            wing_tip_leading_edge_x + wing_tip_chord,
            wing_kink_leading_edge_x + wing_kink_chord,
            wing_root_chord,
            wing_root_chord,
            0,
        ]
    )

    x = x + mac25_x_position - 0.25 * mean_aerodynamic_chord - distance_root_mac_chords
    # pylint: disable=invalid-name # that's a common naming
    x = np.concatenate((x, x))

    # 2) flaps
    # Part of the code dedicated to the flaps

    flap_chord_kink = wing_kink_chord * flaps_chord_ratio
    flap_chord_tip = wing_tip_chord * flaps_chord_ratio

    # Inboard flap
    # Part of the code dedicated to the inboard flap

    y_inboard = np.array(
        [wing_kink_y, wing_kink_y, wing_root_y, wing_root_y, wing_kink_y]
    )
    y_inboard = np.concatenate((-y_inboard, y_inboard))

    x_inboard = np.array(
        [
            wing_root_chord,
            wing_root_chord - flap_chord_kink,
            wing_root_chord - flap_chord_kink,
            wing_root_chord,
            wing_root_chord,
        ]
    )

    x_inboard = (
        x_inboard
        + mac25_x_position
        - 0.25 * mean_aerodynamic_chord
        - distance_root_mac_chords
    )
    # pylint: disable=invalid-name # that's a common naming
    x_inboard = np.concatenate((x_inboard, x_inboard))

    # Outboard flap
    # Part of the code dedicated to the outboard flap

    # The points "_te" are the ones placed on the trailing edge.
    # The points "_ow" are the projection of "_te" on the wing (on wing)
    # This projection is made with a rotation matrix.
    # The points are place respecting the flaps span ratio compared to the
    # total span of the aircraft.

    rotation_matrix = np.array(
        [
            [
                np.cos(trailing_edge_kink_sweep_100_outer * np.pi / 180),
                np.sin(trailing_edge_kink_sweep_100_outer * np.pi / 180),
            ],
            [
                -np.sin(trailing_edge_kink_sweep_100_outer * np.pi / 180),
                np.cos(trailing_edge_kink_sweep_100_outer * np.pi / 180),
            ],
        ]
    )

    y_te_1 = wing_kink_y
    x_te_1 = wing_root_chord

    y_te_2 = wing_root_y + (total_wing_span / 2) * flaps_span_ratio
    x_te_2 = (
        wing_tip_leading_edge_x
        + wing_tip_chord
        - (wing_tip_y - (wing_root_y + (total_wing_span / 2) * flaps_span_ratio))
        * np.tan(trailing_edge_kink_sweep_100_outer * np.pi / 180)
    )

    ow_local_1 = np.array([-flap_chord_tip, 0])
    x_ow_1, y_ow_1 = rotation_matrix @ ow_local_1 + np.array([x_te_2, y_te_2])

    ow_local_2 = np.array([-flap_chord_kink, 0])
    x_ow_2, y_ow_2 = rotation_matrix @ ow_local_2 + np.array([x_te_1, y_te_1])

    y_outboard = np.array([y_te_1, y_te_2, y_ow_1, y_ow_2, y_te_1])
    y_outboard = np.concatenate((-y_outboard, y_outboard))

    x_outboard = np.array([x_te_1, x_te_2, x_ow_1, x_ow_2, x_te_1])

    x_outboard = (
        x_outboard
        + mac25_x_position
        - 0.25 * mean_aerodynamic_chord
        - distance_root_mac_chords
    )
    # pylint: disable=invalid-name # that's a common naming
    x_outboard = np.concatenate((x_outboard, x_outboard))

    # Design line
    # Part of the code dedicated to a lign only used for an aesthetic reason.
    # This line joins the two inboard flaps

    y_design_line = np.array([wing_root_y])
    y_design_line = np.concatenate((-y_design_line, y_design_line))

    x_design_line = np.array([wing_root_chord])

    x_design_line = (
        x_design_line
        + mac25_x_position
        - 0.25 * mean_aerodynamic_chord
        - distance_root_mac_chords
    )
    # pylint: disable=invalid-name # that's a common naming
    x_design_line = np.concatenate((x_design_line, x_design_line))

    # Slats
    # Part of the code dedicated to the slats
    # The dimensions are given by two parameters : span_ratio and chord_ratio
    # Here the span_ratio is given by the span of the airplane minus the
    # fuselage radius the chord_ratio is given by the kink chord

    wing_span_no_fuselage = wing_tip_y - wing_root_y

    slat_y = (
        (1 - slat_span_ratio) / 2.0 * wing_span_no_fuselage
    )  # position in y of the beginning of the slats near the root
    slat_x_root = wing_tip_leading_edge_x * (1 - slat_span_ratio) / 2.0

    y_slats_left = np.array(
        [
            slat_y + wing_root_y,
            slat_y + wing_root_y,
            wing_tip_y - slat_y,
            wing_tip_y - slat_y,
            slat_y + wing_root_y,
        ]
    )

    y_slats_right = -y_slats_left  # slats on the other wing

    x_slats_left = np.array(
        [
            slat_x_root,
            slat_x_root + slat_chord_ratio * wing_kink_chord,
            wing_tip_leading_edge_x * (1 - (1 - slat_span_ratio) / 2.0)
            + slat_chord_ratio * wing_kink_chord,
            wing_tip_leading_edge_x * (1 - (1 - slat_span_ratio) / 2.0),
            slat_x_root,
        ]
    )
    x_slats_left += (
        mac25_x_position - 0.25 * mean_aerodynamic_chord - distance_root_mac_chords
    )
    x_slats_right = x_slats_left

    # 3) Figure
    # Here  the different points are added on the same figure. The wing is in
    # blue and the high lift devices in red.

    if fig is None:
        fig = go.Figure()

    # Same color for a given aircraft
    # It is divided by 14 since their are 14 scatters
    color_index = int(len(fig.data) / 6) % 10

    scatter_wing = go.Scatter(
        x=y,
        y=x,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
    )
    scatter_inboard = go.Scatter(
        x=y_inboard,
        y=x_inboard,
        mode="lines",
        line=dict(color=COLORS[color_index], width=1),
        name=name,
        legendgroup=name,
        showlegend=False,
    )
    scatter_outboard = go.Scatter(
        x=y_outboard,
        y=x_outboard,
        mode="lines",
        line=dict(color=COLORS[color_index], width=1),
        name=name,
        legendgroup=name,
        showlegend=False,
    )
    scatter_design_line = go.Scatter(
        x=y_design_line,
        y=x_design_line,
        mode="lines",
        line=dict(color=COLORS[color_index]),
        name=name,
        legendgroup=name,
        showlegend=False,
    )
    scatter_slats_left = go.Scatter(
        x=y_slats_left,
        y=x_slats_left,
        line=dict(color=COLORS[color_index], width=1),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )
    scatter_slats_right = go.Scatter(
        x=y_slats_right,
        y=x_slats_right,
        line=dict(color=COLORS[color_index], width=1),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    fig.layout = go.Layout(yaxis=dict(scaleanchor="x", scaleratio=1))

    fig.add_trace(scatter_wing)
    fig.add_trace(scatter_outboard)
    fig.add_trace(scatter_inboard)
    fig.add_trace(scatter_design_line)
    fig.add_trace(scatter_slats_left)
    fig.add_trace(scatter_slats_right)

    fig = go.FigureWidget(fig)
    fig.update_xaxes(constrain="domain")
    fig.update_yaxes(constrain="domain")
    fig.update_layout(
        title_text="Flaps and slats",
        title_x=0.5,
        xaxis_title="y",
        yaxis_title="x",
    )

    return fig
