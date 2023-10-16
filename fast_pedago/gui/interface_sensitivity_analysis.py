# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets

from IPython.display import display, HTML, clear_output

from fast_pedago.buttons import (
    get_fast_oad_core_git_button,
    get_fast_oad_cs25_git_button,
    get_fast_oad_cs23_git_button,
    get_main_menu_info_button,
    get_sensitivity_analysis_info_button,
    get_start_button,
)
from fast_pedago.tabs import ParentTab

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
        self.sensitivity_analysis_menu = None

        self.display_main_menu()

    def display_main_menu(self, event=None):
        """
        Title of the function says it all, this display the main menu of the sensitivity analysis
        interface, in practice, it contains links to GitHub repos, a info button and a button to
        start the exercise.
        """

        clear_output(wait=True)

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
        # Trigger the start of the exercise when the button is pressed
        start_button.on_click(self.display_sensitivity_analysis_menu)

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

        info_button = get_main_menu_info_button()

        # Add a box for the info button
        box_info_button = widgets.Box(
            children=[info_button],
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
        display(HTML(f"<style>{CUSTOM_CSS_BACKGROUND}</style>"), self.main_menu)

    def display_sensitivity_analysis_menu(self, event):

        clear_output(wait=True)

        # Create a button to go back home
        back_home_button = widgets.Button(description="")
        back_home_button.icon = "fa-home"
        back_home_button.layout.width = "auto"
        back_home_button.layout.height = "auto"
        # Interestingly enough, if you put parens at the end of display_main_menu it is actually
        # going to display it regardless of whether or not you clicked on the button
        back_home_button.on_click(self.display_main_menu)

        # A small info button
        info_button = get_sensitivity_analysis_info_button()

        # Create a header with an info button and a button to go back home
        top_layer_box = widgets.Box(
            children=[back_home_button, info_button],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                align_items="flex-start",
                width="100",
                height="12%",
            ),
        )

        sensitivity_analysis_tab = ParentTab()

        # Create the main interface
        self.sensitivity_analysis_menu = widgets.VBox(
            children=[top_layer_box, sensitivity_analysis_tab],
            layout=widgets.Layout(
                border="6px solid black",
                margin="100 20 50 100px",
                padding="10px",
                align_items="flex-start",
                width="940px",
                height="665px",
                justify_content="flex-start",
            ),
        )
        self.sensitivity_analysis_menu.add_class("vbox-with-background")
        display(
            HTML(f"<style>{CUSTOM_CSS_BACKGROUND}</style>"),
            self.sensitivity_analysis_menu,
        )
