# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets

from IPython.display import display

# Create a withe box behind the info button
display(widgets.HTML("""<style>.white-vbox {background-color: white;}</style>"""))


def get_main_menu_info_button():

    # Creating and instantiating an info button
    info_button = widgets.Button(description="")
    info_button.icon = "fa-info-circle"
    info_button.layout.width = "auto"
    info_button.layout.height = "auto"
    info_button.tooltip = (
        "Welcome to the training branch of FAST-OAD.\n This is the main menu which can lead you "
        "to the different activities to be performed. You'll also find some links to the source "
        "code of FAST-OAD and its plugins."
    )

    return info_button


def get_sensitivity_analysis_info_button():

    # Creating and instantiating an info button
    info_button = widgets.Button(description="")
    info_button.icon = "fa-info-circle"
    info_button.layout.width = "auto"
    info_button.layout.height = "auto"
    info_button.tooltip = (
        "This is the sensitivity analysis part of the training branch.\n"
        "In this part, you'll study the influence of a few select aircraft design "
        "parameters on the mass, aerodynamics and performances of the aircraft "
    )

    return info_button
