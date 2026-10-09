import pathlib

import openmdao.api as om
import plotly.colors as cols
import plotly.graph_objects as go

from fast_pedago.utils import OUTPUT_FILE_SUFFIX, RECORDER_FILE_SUFFIX

COLS = cols.DEFAULT_PLOTLY_COLORS


def _objectives_viewer(
    aircraft_file_path: str | pathlib.Path,
    name=None,
    fig=None,
    *,
    file_formatter=None,
) -> go.FigureWidget:
    """
    Returns a figure plot of the evolution of the objective of the optimization problem.
    Different residuals can be superposed by providing an existing fig.
    Each design can be provided a name.

    :param aircraft_file_path: path of data file
    :param name: name to give to the trace added to the figure
    :param fig: existing figure to which add the plot
    :param file_formatter: the formatter that defines the format of data file. If not provided,
                           default format will be assumed.
    :return: residuals graph
    """

    # TODO: The stupid workaround I will use here will be to use output file names to reconstruct
    #  the path to .sql files.

    # Only return something if the corresponding output file is actually an MDO, otherwise, just
    # do an empty graph or don't update the data

    if fig is None:
        fig = go.Figure()

    if type(aircraft_file_path) is not str:
        aircraft_file_path = str(aircraft_file_path)

    # We check if it is an MDO based on the contents of the SQL file
    hypothetical_sql_file_path = pathlib.Path(
        aircraft_file_path.replace(OUTPUT_FILE_SUFFIX, RECORDER_FILE_SUFFIX)
    )
    if hypothetical_sql_file_path.exists():
        case_reader = om.CaseReader(hypothetical_sql_file_path.as_posix())
        if "driver" in case_reader.list_sources(out_stream=None):
            solver_cases = case_reader.list_cases("driver", out_stream=None)
            iterations, objective = zip(
                *[
                    (
                        i + 1,
                        list(case_reader.get_case(case_id).get_objectives().values())[
                            0
                        ].item(),
                    )
                    for i, case_id in enumerate(solver_cases)
                ]
            )

            # h_line do not increment the length of data
            scatter_color = COLS[len(fig.data) % len(COLS)]

            objective_scatter = go.Scatter(
                x=iterations,
                y=objective,
                mode="lines",
                name="Objective",
                legendgrouptitle_text=name,
                legendgroup=name,
                line=dict(color=scatter_color),
            )
            fig.add_trace(objective_scatter)

            fig.add_hline(
                min(objective),
                line_width=2,
                line_dash="dash",
                line_color=scatter_color,
                legendgroup=name,
                name="Optimal value",
            )

    fig = go.FigureWidget(fig)
    fig.update_layout(
        title_text="Objective viewer",
        title_x=0.5,
        xaxis_title="Number of function calls",
        yaxis_title="Value of the objective",
        autosize=True,
        margin=go.layout.Margin(
            l=0,
            r=20,
            b=0,
            t=30,
        ),
        width=900,
    )
    fig.update_yaxes(
        type="log",
    )

    return fig
