# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets

from IPython.display import display, HTML

from fast_pedago.buttons import (
    get_fast_oad_core_git_button,
    get_fast_oad_cs25_git_button,
    get_fast_oad_cs23_git_button,
    get_info_button,
    get_start_button,
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


class SensitivityAnalysisInterface:
    def __init__(self):

        self.main_menu = None

    def init_main_menu(self):

        # Add a filler box to force the buttons on the bottom and so that the picture appear clearly
        filler_box = widgets.Box(
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                align_items="center",
                width="100",
                height="68%",
            ),
        )

        start_button = get_start_button()

        # Add a box for the start button
        box_start_button = widgets.Box(
            children=[start_button],
            layout=widgets.Layout(
                display="flex",
                flex_flow="column",
                align_items="center",
                width="100%",
                height="12%",
            ),
        )

        fast_core_git_button = get_fast_oad_core_git_button()
        fast_cs25_git_button = get_fast_oad_cs25_git_button()
        fast_cs23_git_button = get_fast_oad_cs23_git_button()

        # Add a box for the GitHub links
        box_buttons_git = widgets.HBox(
            children=[fast_core_git_button, fast_cs25_git_button, fast_cs23_git_button],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                justify_content="center",
                align_items="center",
                width="100%",
                height="8%",
            ),
        )

        info_button, output = get_info_button()

        # Add a box for the info button
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

        # Create the main interface
        self.main_menu = widgets.VBox(
            children=[filler_box, box_start_button, box_buttons_git, box_info_button],
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
