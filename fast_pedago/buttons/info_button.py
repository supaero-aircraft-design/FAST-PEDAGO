# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets

from IPython.display import display

# Create a withe box behind the info button
display(widgets.HTML("""<style>.white-vbox {background-color: white;}</style>"""))


def get_info_button():

    # Creating and instantiating an info button
    info_button = widgets.Button(description="")
    info_button.icon = "fa-info-circle"
    info_button.layout.width = "auto"
    info_button.layout.height = "auto"

    # Creating a widget to display an info message
    output = widgets.Output()
    output.add_class("white-vbox")

    # Define what happens when you click on the info button
    def info_message(event):

        with output:

            # If the message is displayed, we clear the message
            if len(output.outputs) > 0:
                output.clear_output()

            # Else we print the message
            else:
                print(
                    "Welcome to the training branch of FAST-OAD.\n"
                    "This is the main menu which can lead you to the different activities to be performed. You'll "
                    "also find some links to the source code of FAST-OAD and its plugins."
                )

    info_button.on_click(info_message)

    return info_button, output