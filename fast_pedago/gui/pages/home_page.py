# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import ipywidgets as widgets

import fastoad.api as oad

from fast_pedago import source_data_files
from fast_pedago import gui

from fast_pedago.gui.buttons import (
    FastOadCoreGitButton,
    FastOadCS25GitButton,
    FastOadCS23GitButton,
    MainMenuInfoButton,
    StartButton,
)

from fast_pedago.gui.tabs import ParentTab
from fast_pedago.utils.functions import _image_from_path, _list_available_reference_file  # noqa

from fast_pedago.gui.pages.base_page import BasePage

BOTTOM_BOX_LAYOUT = widgets.Layout(
    border="0px solid black",
    margin="0 0 0 0px",
    padding="0px",
    align_items="center",
    width="100%",
    height="10%",
)


class HomePage(BasePage):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.layout = widgets.Layout(
            border="6px solid black",
            margin="100 20 50 100px",
            padding="10px",
            align_items="center",
            width="1302px",
            height="900px",
            justify_content="center",
        )

        # With Voila it seems impossible to clear and re-display contrarily to Jupyter Notebook.
        # Instead, we'll use the workaround from
        # https://stackoverflow.com/questions/73972010/voila-not-clearing-output-dispalying-new
        # -output which suggests having a VBox as the main interface and change the children of
        # that VBox based on which button we use

        self.reference_file_list = _list_available_reference_file(
            pth.dirname(source_data_files.__file__)
        )

        # Add a filler box to force the buttons on the bottom and so that the picture appear clearly
        self.main_menu_filler_box = widgets.Box(
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                align_items="center",
                width="100",
                height="10%",
            ),
        )

        fast_oad_logo_main_menu_file_path = pth.join(
            pth.dirname(gui.__file__), "resources", "logo_fast_oad_main_menu.jpg"
        )
        self.fast_oad_main_menu_logo_widget = _image_from_path(
            fast_oad_logo_main_menu_file_path, height="50%", width="100"
        )

        self.reference_file_text_box = widgets.VBox()
        self.reference_file_text_box.children = [
            widgets.HTML(value=f"<u><b><font size=3>Select a reference file</b></u>")
        ]
        self.reference_file_text_box.layout = widgets.Layout(
            align_items="center", width="100%", height="4%"
        )

        # This reference file should always be there and is always taken as reference
        self.reference_file_selector_widget = widgets.Dropdown(
            options=self.reference_file_list,
            value="reference_aircraft_source_data_file",
            disabled=False,
            style={"description_width": "initial"},
        )
        self.reference_file_selector_widget.layout = widgets.Layout(
            width="80%",
            height="auto",
        )

        def reference_file_setter(change):

            new_file_name = change["new"] + ".xml"
            path_to_reference_file = pth.join(
                pth.dirname(source_data_files.__file__), new_file_name
            )
            self.sensitivity_analysis_tab.impact_variable_input_tab.reference_inputs = (
                oad.DataFile(path_to_reference_file)
            )

        self.reference_file_selector_widget.observe(
            reference_file_setter, names="value"
        )

        self.reference_file_selector_box = widgets.VBox()
        self.reference_file_selector_box.children = [
            self.reference_file_selector_widget
        ]
        self.reference_file_selector_box.layout = widgets.Layout(
            align_items="center", width="100%", height="4%"
        )

        self.start_button = StartButton(self.pages["analysis"])

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

        fast_core_git_button = FastOadCoreGitButton()
        fast_cs25_git_button = FastOadCS25GitButton()
        fast_cs23_git_button = FastOadCS23GitButton()

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

        info_button = MainMenuInfoButton()

        # Create a bottom layer for the main menu it will be consisting of box of size 40%/20%/40% which will allow
        # me to center the info button in the middle box AND justify the logo to the right. The same distribution
        # will be used everywhere
        self.bottom_layer_info_box = widgets.widgets.Box(
            children=[info_button],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                justify_content="center",
                align_items="center",
                width="20%",
                height="100%",
            ),
        )

        isae_logo_file_path = pth.join(
            pth.dirname(gui.__file__), "resources", "logo_supaero.png"
        )
        self.isae_logo_widget = _image_from_path(
            isae_logo_file_path, height="100%", width="100"
        )

        self.bottom_layer_logo_filler_box = widgets.Box(
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                justify_content="flex-start",
                width="5%",
                height="100%",
            ),
        )

        airbus_logo_file_path = pth.join(
            pth.dirname(gui.__file__), "resources", "logo_airbus.png"
        )
        self.airbus_logo_widget = _image_from_path(
            airbus_logo_file_path, height="50%", width="100"
        )

        # The idea is to be able to have the logos in the same place and the buttons center. Thus, we will save the
        # logo box and the filler box to reuse them later
        self.logo_box = widgets.HBox(
            children=[
                self.isae_logo_widget,
                self.bottom_layer_logo_filler_box,
                self.airbus_logo_widget,
            ],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                justify_content="flex-end",
                align_items="center",
                width="40%",
                height="100%",
            ),
        )

        self.bottom_layer_filler_box = widgets.Box(
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                justify_content="flex-start",
                width="40%",
                height="100%",
            ),
        )

        # Add a box for the info button and the logos
        self.main_menu_box_bottom_layer = widgets.Box(
            children=[
                self.bottom_layer_filler_box,
                self.bottom_layer_info_box,
                self.logo_box,
            ],
            layout=BOTTOM_BOX_LAYOUT,
        )

        # The default appearance of the box should be the main menu hence the following line
        self.children = [
            self.main_menu_filler_box,
            self.fast_oad_main_menu_logo_widget,
            self.reference_file_text_box,
            self.reference_file_selector_box,
            self.main_menu_box_start_button,
            self.main_menu_box_buttons_git,
            self.main_menu_box_bottom_layer,
        ]