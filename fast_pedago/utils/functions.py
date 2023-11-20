import os.path as pth

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
