import os.path as pth

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
                    padding="0px",
                ),
            ),
        ],
    )

    return image_widget


def _n2_xdsm_to_vue_template(html_file_path: str):
    html_file = open(html_file_path, "r")
    content = html_file.readlines()
    content = [
        item.replace("<body>", "<template>")
        .replace("</body>", "</template>")
        .replace("body", "div")
        .replace("<head>", "")
        .replace("</head>", "")
        .replace("<!doctype html>", "")
        .replace("</html>", "")
        .replace(
            '<meta http-equiv="Content-Type" content="text/html;' 'charset=UTF-8">', ""
        )
        for item in content
    ]
    html_file.close()

    # Remove the extension in the file name
    vue_file_path = html_file_path.replace(".html", ".vue")
    vue_file = open(vue_file_path, "+w")
    vue_file.writelines(content)
    vue_file.close()

    return vue_file_path
