import pathlib

import plotly.graph_objects as go

import openmdao.api as om

from fast_pedago.utils import RECORDER_FILE_SUFFIX, OUTPUT_FILE_SUFFIX


def _residuals_viewer(
    aircraft_file_path: str | pathlib.Path,
    name=None,
    fig=None,
    *,
    file_formatter=None,
) -> go.FigureWidget:
    """
    Returns a figure plot of the residuals of the design problem.
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

    # Only return something if the corresponding output file is actually an MDA, otherwise, just
    # do an empty graph or don't update the data

    if fig is None:
        fig = go.Figure()

    if not type(aircraft_file_path) is str:
        aircraft_file_path = str(aircraft_file_path)

    # We check if it is an MDA based on the contents of the SQL file otherwise we might miss the
    # .sql of the reference aircraft
    hypothetical_sql_file_path = pathlib.Path(
        aircraft_file_path.replace(OUTPUT_FILE_SUFFIX, RECORDER_FILE_SUFFIX)
    )
    if hypothetical_sql_file_path.exists():
        case_reader = om.CaseReader(hypothetical_sql_file_path.as_posix())
        if "root.nonlinear_solver" in case_reader.list_sources(out_stream=None):
            solver_cases = case_reader.list_cases(
                "root.nonlinear_solver", out_stream=None
            )
            iterations, relative_error = zip(
                *[
                    (i + 1, case_reader.get_case(case_id).rel_err)
                    for i, case_id in enumerate(solver_cases)
                ]
            )
            residuals_scatter = go.Scatter(
                x=iterations,
                y=relative_error,
                name=name,
            )
            fig.add_trace(residuals_scatter)

            # Extract the target residuals, there should only be one solver that satisfies
            # those constraints
            root_non_linear_solver = [
                solver
                for solver in case_reader.solver_metadata.keys()
                if "root" in solver and "Nonlinear" in solver
            ]
            rtol = case_reader.solver_metadata[root_non_linear_solver[0]][
                "solver_options"
            ]["rtol"]
            fig.add_hline(
                rtol,
                line_width=2,
                line_dash="dash",
                line_color="red",
            )

    fig = go.FigureWidget(fig)
    fig.update_layout(
        title_text="Residuals viewer",
        title_x=0.5,
        xaxis_title="Number of iterations",
        yaxis_title="Relative value of residuals",
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
        range=[-7.0, 1.0],
    )

    return fig
