# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets

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
                        background-image: url("{"../gui/resources/background.jpg"}");
                        background-size: cover;
                        background-position: center;
                        background-repeat: no-repeat;
                        width: 100%;
                        height: 100%;
                        }}
                        """


class FASTOADInterface(widgets.VBox):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.layout = widgets.Layout(
            border="6px solid black",
            margin="100 20 50 100px",
            padding="10px",
            align_items="center",
            width="1302px",
            height="920px",
            justify_content="center",
        )

        # With Voila it seems impossible to clear and re-display contrarily to Jupyter Notebook.
        # Instead, we'll use the workaround from
        # https://stackoverflow.com/questions/73972010/voila-not-clearing-output-dispalying-new
        # -output which suggests having a VBox as the main interface and change the children of
        # that VBox based on which button we use

        # Add a filler box to force the buttons on the bottom and so that the picture appear clearly
        self.main_menu_filler_box = widgets.Box(
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                align_items="center",
                width="100",
                height="68%",
            ),
        )

        self.start_button = get_start_button()

        # Add a box for the start button
        self.main_menu_box_start_button = widgets.Box(
            children=[self.start_button],
            layout=widgets.Layout(
                display="flex",
                flex_flow="column",
                align_items="center",
                width="100%",
                height="12%",
            ),
        )
        self.start_button.on_click(self.display_sensitivity_analysis_menu)

        fast_core_git_button = get_fast_oad_core_git_button()
        fast_cs25_git_button = get_fast_oad_cs25_git_button()
        fast_cs23_git_button = get_fast_oad_cs23_git_button()

        # Add a box for the GitHub links
        self.main_menu_box_buttons_git = widgets.HBox(
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

        info_button = get_main_menu_info_button()

        # Add a box for the info button
        self.main_menu_box_info_button = widgets.Box(
            children=[info_button],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                align_items="center",
                width="100",
                height="10%",
            ),
        )

        # The default appearance of the box should be the main menu hence the following line
        self.children = [
            self.main_menu_filler_box,
            self.main_menu_box_start_button,
            self.main_menu_box_buttons_git,
            self.main_menu_box_info_button,
        ]

        # Create a button to go back home, can't externalize because the on-click depends on a
        # function defined here
        self.analysis_back_home_button = widgets.Button(description="")
        self.analysis_back_home_button.icon = "fa-home"
        self.analysis_back_home_button.layout.width = "auto"
        self.analysis_back_home_button.layout.height = "auto"

        self.analysis_back_home_button.on_click(self.display_main_menu)

        # A small info button
        self.analysis_info_button = get_sensitivity_analysis_info_button()

        # Create a filler bow so that we still see the FAST-OAD logo
        self.sensitivity_filler_box = widgets.Box(
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                align_items="center",
                width="100",
                height="12%",
            ),
        )

        self.sensitivity_analysis_tab = ParentTab()
        self.sensitivity_analysis_tab.layout = widgets.Layout(
            border="0px solid black",
            margin="0 0 0 0px",
            padding="0px",
            align_items="flex-start",
            width="98%",
            height="78%",
        )

        # Create a header with an info button and a button to go back home. Put it at the bottom
        # to match what is done on the main menu
        self.sensitivity_bottom_layer_box = widgets.Box(
            children=[self.analysis_back_home_button, self.analysis_info_button],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                align_items="center",
                width="100",
                height="10%",
            ),
        )

        self.add_class("vbox-with-background")

    def display_main_menu(self, event):

        self.children = [
            self.main_menu_filler_box,
            self.main_menu_box_start_button,
            self.main_menu_box_buttons_git,
            self.main_menu_box_info_button,
        ]

    def display_sensitivity_analysis_menu(self, event):
        self.children = [
            self.sensitivity_filler_box,
            self.sensitivity_analysis_tab,
            self.sensitivity_bottom_layer_box,
        ]
