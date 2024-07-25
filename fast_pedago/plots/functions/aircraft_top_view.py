import numpy as np
import plotly.graph_objects as go

from fastoad.io import VariableIO

from ..plot_constants import (
    COLORS,
    NACELLE_POSITION,
    HORIZONTAL_TAIL_ROOT,
    HORIZONTAL_TAIL_TIP,
    HORIZONTAL_WIDTH_ELEVATOR,
)


def _aircraft_top_view_plot(
    aircraft_file_path: str,
    name=None,
    fig=None,
    file_formatter=None,
) -> go.FigureWidget:
    """
    Returns a figure plot of the top view of the aircraft with the engines,
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
    nacelle_diameter = variables["data:geometry:propulsion:nacelle:diameter"].value[0]
    nacelle_length = variables["data:geometry:propulsion:nacelle:length"].value[0]
    nacelle_y = variables["data:geometry:propulsion:nacelle:y"].value[0]

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

    # Wing
    y_wing = np.array(
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

    x_wing = np.array(
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

    # Engine
    y_engine = np.array(
        [
            nacelle_y - nacelle_diameter / 2,
            nacelle_y + nacelle_diameter / 2,
            nacelle_y + nacelle_diameter / 2,
            nacelle_y - nacelle_diameter / 2,
            nacelle_y - nacelle_diameter / 2,
        ]
    )
    x_engine = np.array(
        [-nacelle_length, -nacelle_length, 0, 0, -nacelle_length],
    )

    # Horizontal Tail parameters
    ht_root_chord = variables["data:geometry:horizontal_tail:center:chord"].value[0]
    ht_tip_chord = variables["data:geometry:horizontal_tail:tip:chord"].value[0]
    ht_span = variables["data:geometry:horizontal_tail:span"].value[0]
    ht_sweep_0 = variables["data:geometry:horizontal_tail:sweep_0"].value[0]
    ht_sweep_100 = variables["data:geometry:horizontal_tail:sweep_100"].value[0]

    ht_tip_leading_edge_x = ht_span / 2.0 * np.tan(ht_sweep_0 * np.pi / 180.0)

    y_ht = np.array([0, ht_span / 2.0, ht_span / 2.0, 0.0, 0.0])

    x_ht = np.array(
        [
            0,
            ht_tip_leading_edge_x,
            ht_tip_leading_edge_x + ht_tip_chord,
            ht_root_chord,
            0,
        ]
    )

    # Fuselage parameters
    fuselage_max_width = variables["data:geometry:fuselage:maximum_width"].value[0]
    fuselage_length = variables["data:geometry:fuselage:length"].value[0]
    fuselage_front_length = variables["data:geometry:fuselage:front_length"].value[0]
    fuselage_rear_length = variables["data:geometry:fuselage:rear_length"].value[0]

    y_fuselage = np.linspace(0, fuselage_max_width / 2, 10)
    x_fuselage = (
        fuselage_front_length / (0.5 * fuselage_max_width) ** 2 * y_fuselage ** 2
    )  # parabola
    x_fuselage = np.append(
        x_fuselage,
        np.array(
            [
                fuselage_length - fuselage_rear_length,
                fuselage_length,
                fuselage_length,
            ]
        ),
    )

    y_fuselage = np.append(
        y_fuselage,
        np.array(
            [
                fuselage_max_width / 2.0,
                fuselage_max_width / 4.0,
                0.0,
            ]
        ),
    )

    # Flaps
    # Part of the code dedicated to the flaps

    flap_chord_kink = wing_kink_chord * flaps_chord_ratio
    flap_chord_tip = wing_tip_chord * flaps_chord_ratio

    # Inboard flap
    # Part of the code dedicated to the inboard flap

    y_flaps_inboard = np.array(
        [wing_kink_y, wing_kink_y, wing_root_y, wing_root_y, wing_kink_y]
    )
    y_flaps_inboard = np.concatenate((-y_flaps_inboard, y_flaps_inboard))

    x_flaps_inboard = np.array(
        [
            wing_root_chord,
            wing_root_chord - flap_chord_kink,
            wing_root_chord - flap_chord_kink,
            wing_root_chord,
            wing_root_chord,
        ]
    )

    x_flaps_inboard = (
        x_flaps_inboard
        + mac25_x_position
        - 0.25 * mean_aerodynamic_chord
        - distance_root_mac_chords
    )
    # pylint: disable=invalid-name # that's a common naming
    x_flaps_inboard = np.concatenate((x_flaps_inboard, x_flaps_inboard))

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

    y_flaps_outboard = np.array([y_te_1, y_te_2, y_ow_1, y_ow_2, y_te_1])
    y_flaps_outboard = np.concatenate((-y_flaps_outboard, y_flaps_outboard))

    x_flaps_outboard = np.array([x_te_1, x_te_2, x_ow_1, x_ow_2, x_te_1])

    x_flaps_outboard = (
        x_flaps_outboard
        + mac25_x_position
        - 0.25 * mean_aerodynamic_chord
        - distance_root_mac_chords
    )
    # pylint: disable=invalid-name # that's a common naming
    x_flaps_outboard = np.concatenate((x_flaps_outboard, x_flaps_outboard))

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
    # Here the span_ratio is given by the span of the airplane minus the fuselage radius
    # the chord_ratio is given by the kink chord

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

    # CGs
    wing_25mac_x = variables["data:geometry:wing:MAC:at25percent:x"].value[0]
    wing_mac_length = variables["data:geometry:wing:MAC:length"].value[0]
    local_wing_mac_le_x = variables[
        "data:geometry:wing:MAC:leading_edge:x:local"
    ].value[0]
    local_ht_25mac_x = variables[
        "data:geometry:horizontal_tail:MAC:at25percent:x:local"
    ].value[0]
    ht_distance_from_wing = variables[
        "data:geometry:horizontal_tail:MAC:at25percent:x:from_wingMAC25"
    ].value[0]

    x_wing = x_wing + wing_25mac_x - 0.25 * wing_mac_length - local_wing_mac_le_x
    x_engine += (
        wing_25mac_x
        - 0.25 * wing_mac_length
        - local_wing_mac_le_x
        + NACELLE_POSITION * nacelle_length
    )
    x_ht = x_ht + wing_25mac_x + ht_distance_from_wing - local_ht_25mac_x

    # Design of the elevator

    # Constants used for the computation
    x_ht_position = fuselage_length - x_ht[3]
    x_virtual_ht_leading_edge = ht_tip_leading_edge_x + ht_tip_chord - ht_root_chord

    # Constants used for the computation
    tg_alpha = (y_fuselage[-3] - y_fuselage[-2]) / (x_fuselage[-2] - x_fuselage[-3])

    ht_root_tip_x_percent = (
        x_ht[2]
        - (1 - HORIZONTAL_WIDTH_ELEVATOR) * y_ht[1] * np.tan(ht_sweep_100 * np.pi / 180)
    ) - (
        x_ht[1]
        - (1 - HORIZONTAL_WIDTH_ELEVATOR) * y_ht[1] * np.tan(ht_sweep_0 * np.pi / 180)
    )
    # Constants used for the computation. Root chord at X percent of the
    # horizontal tail width (depending on the value of the parameter
    # "HORIZONTAL_WIDTH_ELEVATOR").

    delta_l = (
        ht_root_chord
        - np.tan(ht_sweep_0 * np.pi / 180)
        * (fuselage_max_width / 4.0 + x_ht_position * tg_alpha)
    ) / (
        1 + np.tan(ht_sweep_0 * np.pi / 180) * tg_alpha
    )  # constants used for the computation

    delta_y_tot = tg_alpha * (
        x_ht_position + delta_l
    )  # constants used for the computation

    delta_x = (
        x_ht_position * ht_span / 2.0
        - x_virtual_ht_leading_edge * fuselage_max_width / 4.0
    ) / (ht_span / 2.0 + x_virtual_ht_leading_edge * tg_alpha)
    # constants used for the computation

    delta_y = tg_alpha * delta_x  # constants used for the computation

    x_elevator = np.array(
        [
            x_fuselage[-2] - delta_x,
            x_ht[3] - delta_l * HORIZONTAL_TAIL_ROOT,
            x_ht[2]
            - (1 - HORIZONTAL_WIDTH_ELEVATOR)
            * y_ht[1]
            * np.tan(ht_sweep_100 * np.pi / 180)
            - HORIZONTAL_TAIL_TIP * ht_root_tip_x_percent,
            x_ht[2]
            - (1 - HORIZONTAL_WIDTH_ELEVATOR)
            * y_ht[1]
            * np.tan(ht_sweep_100 * np.pi / 180),
            x_fuselage[-2] - delta_x,
        ]
    )
    y_elevator = np.array(
        [
            y_fuselage[-2] + delta_y,
            y_fuselage[-2] + HORIZONTAL_TAIL_ROOT * delta_y_tot,
            y_ht[1] * HORIZONTAL_WIDTH_ELEVATOR,
            y_ht[1] * HORIZONTAL_WIDTH_ELEVATOR,
            y_fuselage[-2] + delta_y,
        ]
    )

    x_fuselage[-2] = x_elevator[-1]
    x_fuselage = x_fuselage[:-1]
    y_fuselage = y_fuselage[:-1]

    x_elev = x_elevator[-1]
    y_elev = y_elevator[-1]

    y_rear = np.flip(np.linspace(0, fuselage_max_width / 4, 10))

    x_rear = fuselage_length + (x_elev - fuselage_length) / y_elev ** 2 * y_rear ** 2

    x_fuselage = np.concatenate((x_fuselage, x_rear))
    y_fuselage = np.concatenate((y_fuselage, y_rear))
    # pylint: disable=invalid-name # that's a common naming
    x_aircraft = np.concatenate((x_fuselage, x_wing, x_ht))
    # pylint: disable=invalid-name # that's a common naming
    y_aircraft = np.concatenate((y_fuselage, y_wing, y_ht))

    # pylint: disable=invalid-name # that's a common naming
    y_aircraft = np.concatenate((-y_aircraft, y_aircraft))

    # pylint: disable=invalid-name # that's a common naming
    x_aircraft = np.concatenate((x_aircraft, x_aircraft))

    if fig is None:
        fig = go.Figure()

    # Same color for a given aircraft
    # It is divided by 10 since their are 10 scatters
    color_index = int(len(fig.data) / 10) % 10

    scatter_aircraft = go.Scatter(
        x=y_aircraft,
        y=x_aircraft,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
    )
    scatter_left_engine = go.Scatter(
        x=y_engine,
        y=x_engine,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )
    scatter_right_engine = go.Scatter(
        x=-y_engine,
        y=x_engine,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )
    scatter_flaps_inboard = go.Scatter(
        x=y_flaps_inboard,
        y=x_flaps_inboard,
        mode="lines",
        line=dict(color=COLORS[color_index], width=1),
        name=name,
        legendgroup=name,
        showlegend=False,
    )
    scatter_flaps_outboard = go.Scatter(
        x=y_flaps_outboard,
        y=x_flaps_outboard,
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
        line=dict(color=COLORS[color_index], width=1),
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
    scatter_elevator_right = go.Scatter(
        x=y_elevator,
        y=x_elevator,
        line=dict(color=COLORS[color_index], width=1),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )
    scatter_elevator_left = go.Scatter(
        x=-y_elevator,
        y=x_elevator,
        line=dict(color=COLORS[color_index], width=1),
        mode="lines",
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    fig.add_trace(scatter_aircraft)
    fig.add_trace(scatter_right_engine)
    fig.add_trace(scatter_left_engine)
    fig.add_trace(scatter_flaps_outboard)
    fig.add_trace(scatter_flaps_inboard)
    fig.add_trace(scatter_design_line)
    fig.add_trace(scatter_slats_left)
    fig.add_trace(scatter_slats_right)
    fig.add_trace(scatter_elevator_right)
    fig.add_trace(scatter_elevator_left)

    fig.layout = go.Layout(yaxis=dict(scaleanchor="x", scaleratio=1))

    if name is None:
        fig.update_layout(
            title_text="Aircraft Geometry (top view)",
            title_x=0.5,
            xaxis_title="y",
            yaxis_title="x",
        )
    else:
        fig.update_layout(
            title_text="Aircraft Geometry (top view)",
            title_x=0.5,
            xaxis_title="y",
            yaxis_title="x",
        )

    fig = go.FigureWidget(fig)

    return fig
