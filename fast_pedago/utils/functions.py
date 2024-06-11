import os
import os.path as pth

import openmdao.api as om

from typing import List

import ipywidgets as widgets
import ipyvuetify as v

from .constants import (
    OUTPUT_FILE_SUFFIX,
    FLIGHT_DATA_FILE_SUFFIX,
)


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
    file_extension = pth.splitext(file_path)[1].replace(".", "")

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
                    padding = "0px",
                ),
            ),
        ],
    )
    

    return image_widget


def _list_available_reference_file(path_to_scan: str) -> List[str]:
    """
    Parses the name of all the file in the provided path and scan for reference file that can be
    selected for the rest of the analysis

    :param path_to_scan: path to look for reference file in
    :return: a list of available reference files
    """

    list_files = os.listdir(path_to_scan)
    available_reference_files = []

    for file in list_files:

        if file.endswith(".xml"):

            associated_sizing_process_name = file.replace(".xml", "")
            available_reference_files.append(associated_sizing_process_name)

    return available_reference_files


def _list_available_sizing_process_results(path_to_scan: str) -> List[str]:
    """
    Parses the name of all the file in the provided path and scan for the one that would match the
    results of an OAD sizing process. Is meant to work only on a path containing both the output
    file and flight data file

    :param path_to_scan: path to look for the results of sizing process in
    :return: a list of available process names
    """

    list_files = os.listdir(path_to_scan)
    available_sizing_process = []

    for file in list_files:

        # Delete the suffix corresponding to the output file and flight data file because that's
        # how they were built. Also, we will ignore the .sql file

        if file.endswith(".sql"):
            continue

        associated_sizing_process_name = file.replace(OUTPUT_FILE_SUFFIX, "").replace(
            FLIGHT_DATA_FILE_SUFFIX, ""
        )

        if associated_sizing_process_name not in available_sizing_process:
            available_sizing_process.append(associated_sizing_process_name)

    return available_sizing_process


def _extract_residuals(recorder_database_file_path: str) -> list:
    """
    From the file path to a recorder data base, extract the value of the relative error of the
    residuals at each iteration.

    :param recorder_database_file_path: absolute path to the recorder database
    :return: two arrays containing the iterations and the associated values of the relative error
    """

    case_reader = om.CaseReader(recorder_database_file_path)

    # Will only work if the recorder was attached to the base solver
    solver_cases = case_reader.list_cases("root.nonlinear_solver")
    
    # For the display, first iteration will be 1
    iterations, relative_error = zip(*[
        (i + 1, case_reader.get_case(case_id).rel_err) 
        for i, case_id in enumerate(solver_cases)
        ])

    return iterations, relative_error


def _extract_objective(recorder_database_file_path: str) -> list:
    """
    From the file path to a recorder data base, extract the value of the objective at each
    iteration of the driver.

    :param recorder_database_file_path: absolute path to the recorder database
    :return: an array containing the iterations and the associated values of the objective
    """

    case_reader = om.CaseReader(recorder_database_file_path)

    # Will only work if the recorder was attached to the base solver
    solver_cases = case_reader.list_cases("driver")
    
    # For the display, first iteration will be 1
    iterations, objective = zip(*[
        (i + 1, float(list(case_reader.get_case(case_id).get_objectives().values())[0])) 
        for i, case_id in enumerate(solver_cases)
    ])

    return iterations, objective


def _n2_xdsm_to_vue_template(html_file_path: str):
    html_file = open(html_file_path, "r")
    content = html_file.readlines()
    content = [
        item
        .replace("<body>", "<template>")
        .replace("</body>", "</template>")
        .replace("body", "div")
        .replace("<head>", "")
        .replace("</head>", "")
        .replace("<!doctype html>", "")
        .replace("</html>", "")
        .replace('<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">', "")
        for item in content
    ]
    html_file.close()
    
    # Remove the extension in the file name
    vue_file_path = html_file_path.replace('.html' , '.vue')
    vue_file = open(vue_file_path, "+w")
    vue_file.writelines(content)
    vue_file.close()
    
    return vue_file_path