"""
Utility functions to use punctually in the code.
"""

from typing import Union

from os import PathLike
from pathlib import Path

import openmdao.api as om

import ipywidgets as widgets
import ipyvuetify as v


def _image_from_path(file_path: str, max_height: str = "52px") -> v.Html:
    """
    Creates an Image widgets from ipywidgets from the path to a picture.

    :param file_path: path to the picture to turn into an Image widgets
    :param height: height of the Image widget, must be provided as if provided to a Layout widget
    :param width: width of the Image widget, must be provided as if provided to a Layout widget
    :return: an Image widget
    """

    file = open(file_path, "rb")
    # Remove the "." in the extension string
    file_extension = Path(file_path).suffix.replace(".", "")

    image = file.read()
    # Encapsulate the image in a "a" tag to be able to provide a "click" event and links
    image_widget = v.Html(
        tag="a",
        children=[
            widgets.Image(
                value=image,
                format=file_extension,
                layout=widgets.Layout(
                    max_height=max_height,
                    padding="0px",
                ),
            ),
        ],
    )

    return image_widget


def _extract_residuals(recorder_database_file_path: Union[str, PathLike]) -> list:
    """
    From the file path to a recorder data base, extract the value of the
    relative error of the residuals at each iteration.

    :param recorder_database_file_path: absolute path to the recorder database
    :return: two arrays containing the iterations and the associated values of
        the relative error.
    """

    case_reader = om.CaseReader(str(recorder_database_file_path))

    # Will only work if the recorder was attached to the base solver
    solver_cases = case_reader.list_cases("root.nonlinear_solver")

    # For the display, first iteration will be 1
    iterations, relative_error = zip(
        *[
            (i + 1, case_reader.get_case(case_id).rel_err)
            for i, case_id in enumerate(solver_cases)
        ]
    )

    return iterations, relative_error


def _extract_objective(recorder_database_file_path: Union[str, PathLike]) -> list:
    """
    From the file path to a recorder data base, extract the value of the
    objective at each iteration of the driver.

    :param recorder_database_file_path: absolute path to the recorder database
    :return: an array containing the iterations and the associated values of
        the objective.
    """

    case_reader = om.CaseReader(str(recorder_database_file_path))

    # Will only work if the recorder was attached to the base solver
    solver_cases = case_reader.list_cases("driver")

    # For the display, first iteration will be 1
    iterations, objective = zip(
        *[
            (
                i + 1,
                float(list(case_reader.get_case(case_id).get_objectives().values())[0]),
            )
            for i, case_id in enumerate(solver_cases)
        ]
    )

    return iterations, objective
