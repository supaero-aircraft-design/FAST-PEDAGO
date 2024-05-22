import ipywidgets as widgets


def get_back_home_button(display_home_page):

    back_home_button = widgets.Button(description="")
    back_home_button.icon = "fa-home"
    back_home_button.layout.width = "auto"
    back_home_button.layout.height = "auto"

    
    back_home_button.on_click(display_home_page)

    return back_home_button
