# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets

from IPython.display import display, clear_output, HTML

from fast_pedago.buttons.github_links_buttons import (
    get_fast_oad_core_git_button,
    get_fast_oad_cs25_git_button,
    get_fast_oad_cs23_git_button,
)

# Create a custom CSS background to have a nice picture in the main menu
CUSTOM_CSS_BACKGROUND = f""" .vbox-with-background {{
                        background-image: url("{"../BlockImage/Images/Wing.jpg"}");
                        background-size: cover;
                        background-position: center;
                        background-repeat: no-repeat;
                        width: 100%;
                        height: 100%;
                        }}
                        """

# Create a withe box behind the info button
display(widgets.HTML("""<style>.white-vbox {background-color: white;}</style>"""))


class SensitivityAnalysisInterface:
    def __init__(self):

        self.main_menu = None

    def init_main_menu(self):

        # Creating and instantiating an info button
        info_button = widgets.Button(description="")
        info_button.icon = "fa-info-circle"
        info_button.layout.width = "auto"
        info_button.layout.height = "auto"

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

        fast_core_git_button = get_fast_oad_core_git_button()
        fast_cs25_git_button = get_fast_oad_cs25_git_button()
        fast_cs23_git_button = get_fast_oad_cs23_git_button()

        box_buttons_git = widgets.HBox(
            children=[fast_core_git_button, fast_cs25_git_button, fast_cs23_git_button],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                justify_content="center",
                align_items="center",
                width="100%",
                height="10%",
            ),
        )

        box_info_button = widgets.Box(
            children=[info_button, output],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                align_items="center",
                width="100",
                height="12%",
            ),
        )

        # Add a filler box to force the buttons on the bottom and so that the picture appear clearly
        filler_box = widgets.Box(
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                align_items="center",
                width="100",
                height="78%",
            ),
        )

        self.main_menu = widgets.VBox(
            children=[filler_box, box_buttons_git, box_info_button],
            layout=widgets.Layout(
                border="6px solid black",
                margin="100 20 50 100px",
                padding="10px",
                align_items="center",
                width="940px",
                height="665px",
                justify_content="center",
            ),
        )

        # Displays the background picture
        self.main_menu.add_class("vbox-with-background")
        display(HTML(f"<style>{CUSTOM_CSS_BACKGROUND}</style>"))

        # Returning the menu make it appear on the screen, else nothing happens
        return self.main_menu
