import numpy as np
import plotly.graph_objects as go

from fastoad.io import VariableIO

from ..plot_constants import COLORS


def _static_margin_plot(
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

    mean_thickness = variables["data:geometry:wing:thickness_ratio"].value[0]
    CG_aft = variables["data:weight:aircraft:CG:aft:MAC_position"].value[0]
    CG_range = variables["settings:weight:aircraft:CG:range"].value[0]
    static_margin = variables["data:handling_qualities:static_margin"].value[0]

    xu, yu, xl, yl = _NACA_4_digits(2, 4, round(100 * mean_thickness))

    x_CG_aft = CG_aft
    x_CG_fwd = x_CG_aft - CG_range

    x_AC = x_CG_aft + static_margin

    if fig is None:
        fig = go.Figure()

    # Same color for a given aircraft
    # It is divided by 4 since their are 4 scatters
    color_index = int(len(fig.data) / 4) % 10

    scatter_upper_airfoil_surface = go.Scatter(
        x=xu,
        y=yu,
        line=dict(color=COLORS[color_index]),
        mode="lines",
        name=name,
        legendgroup=name,
    )
    scatter_lower_airfoil_surface = go.Scatter(
        x=xl,
        y=yl,
        mode="lines",
        line=dict(color=COLORS[color_index]),
        name=name,
        legendgroup=name,
        showlegend=False,
    )
    scatter_cg_range = go.Scatter(
        x=[x_CG_fwd, x_CG_aft],
        y=[0, 0],
        mode="lines +markers",
        line=dict(color=COLORS[color_index], width=1),
        name=name,
        legendgroup=name,
        showlegend=False,
    )
    scatter_aerodynamic_center = go.Scatter(
        x=[x_AC],
        y=[0],
        mode="markers",
        marker_symbol="x",
        line=dict(color=COLORS[color_index]),
        name=name,
        legendgroup=name,
        showlegend=False,
    )

    fig.add_annotation(
        x=x_CG_aft,
        y=0,
        text=name + "-CG aft",
    )
    fig.add_annotation(
        x=x_CG_fwd,
        y=0,
        text=name + "-CG fwd",
    )

    fig.add_annotation(
        x=x_AC,
        y=0,
        text=name + "-Aerodynamic center",
    )

    fig.layout = go.Layout(yaxis=dict(scaleanchor="x", scaleratio=1))

    fig.add_trace(scatter_upper_airfoil_surface)
    fig.add_trace(scatter_lower_airfoil_surface)
    fig.add_trace(scatter_cg_range)
    fig.add_trace(scatter_aerodynamic_center)

    fig = go.FigureWidget(fig)
    fig.update_xaxes(constrain="domain")
    fig.update_yaxes(constrain="domain")
    fig.update_layout(
        title_text="Static margin",
        title_x=0.5,
        xaxis_title="x",
        yaxis_title="y",
    )

    return fig


def _NACA_4_digits(
    max_camber: int,
    max_camber_distance: int,
    max_thickness: int,
    chord: int = 1,
    nb_points: int = 200,
):
    """
    Creates a NACA 4 digits airfoil.

    Formulas from https://fr.wikipedia.org/wiki/Profil_NACA

    :param max_camber: max camber in percent of the chord. Only one digit
    :param max_camber_distance: distance of the max camber from the leading edge, in ten percents
        of the chord. Only one digit
    :param max_thickness: max airfoil thickness, in percent of the chord. Only two digits
    :param chord: length of the chord in meters, defaults to 1
    :param nb_points: number of points in the upper and the lower part of the airfoil, defaults to
        200
    :return: a tuple of upper airfoil part x, y coordinates, and lower airfoil part x, y coordinates
    """

    t = max_thickness / 100
    m = max_camber / 100
    p = max_camber_distance / 10

    x = np.linspace(0, 1, nb_points)
    yt = (
        5
        * t
        * (
            0.2969 * np.sqrt(x)
            - 0.1260 * x
            - 0.3516 * (x ** 2)
            + 0.2843 * (x ** 3)
            - 0.1015 * (x ** 4)
        )
    )

    pi = round(p * nb_points)
    yc = np.array(x)
    yc[0:pi] = ((m) / ((p) ** 2)) * (2 * (p) * x[0:pi] - (x[0:pi] ** 2))
    yc[pi:] = ((m) / ((1 - p) ** 2)) * ((1 - 2 * p) + 2 * x[pi:] * p - (x[pi:] ** 2))

    ycp = np.array(x)
    ycp[0:pi] = (2 * m / (p ** 2)) * (p - x[0:pi])
    ycp[pi:] = ((2 * m) / ((1 - p) ** 2)) * (p - x[pi:])

    theta = np.arctan(ycp)

    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)

    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)

    return chord * xu, chord * yu, chord * xl, chord * yl
