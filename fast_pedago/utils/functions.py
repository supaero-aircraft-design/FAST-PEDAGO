import os
import os.path as pth

from typing import List

import ipywidgets as widgets


def _image_from_path(file_path: str, height: str, width: str) -> widgets.Image:
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
    image_widget = widgets.Image(value=image, format=file_extension)
    image_widget.layout = widgets.Layout(
        border="0px solid black",
        margin="0 0 0 0px",
        padding="0px",
        align_items="center",
        height=height,
        width=width,
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