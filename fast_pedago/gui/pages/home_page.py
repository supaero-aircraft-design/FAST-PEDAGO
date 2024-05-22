# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import ipywidgets as widgets

import fastoad.api as oad

from fast_pedago import source_data_files

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


class HomePage(BasePage):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.set_footer([MainMenuInfoButton()])


        # Add a filler box to force the buttons on the bottom and so that the picture appear clearly
        self.main_menu_filler_box = widgets.Box(
            layout = widgets.Layout(
                border = "0px solid black",
                margin = "0 0 0 0px",
                padding = "0px",
                align_items = "center",
                width = "100",
                height = "10%",
            ),
        )
        

        # Source file selection
        self.reference_file_text_box = widgets.VBox(
            children = [
                widgets.HTML(value=f"<u><b><font size=3>Select a reference file</b></u>")
            ],

            layout = widgets.Layout(
                align_items="center", width="100%", height="4%"
            ),
        )
        
        self.reference_file_list = _list_available_reference_file(
            pth.dirname(source_data_files.__file__)
        )

        # This reference file should always be there and is always taken as reference
        self.reference_file_selector_widget = widgets.Dropdown(
            options = self.reference_file_list,
            value = "reference_aircraft_source_data_file",
            disabled = False,
            style = {"description_width": "initial"},

            layout = widgets.Layout(
                width = "80%",
                height = "auto",
            ),
        )

        self.reference_file_selector_box = widgets.VBox(
            children = [
                self.reference_file_selector_widget
            ],

            layout = widgets.Layout(
                align_items = "center", 
                width = "100%", 
                height = "4%"
            ),
        )
        

        # Add a box for the start button
        self.main_menu_box_start_button = widgets.Box(
            children = [
                StartButton(self.pages["analysis"])
            ],

            layout = widgets.Layout(
                display = "flex",
                flex_flow = "column",
                align_items = "center",
                width = "100%",
                height = "12%",
            ),
        )


        # Add a box for the GitHub links
        self.main_menu_box_buttons_git = widgets.HBox(
            children = [
                FastOadCoreGitButton(), 
                FastOadCS25GitButton(), 
                FastOadCS23GitButton()
            ],

            layout = widgets.Layout(
                border = "0px solid black",
                margin = "0 0 0 0px",
                padding = "0px",
                justify_content = "center",
                align_items = "center",
                width = "100%",
                height = "10%",
            ),
        )



        # The default appearance of the box should be the main menu hence the following line
        self.children = [
            self.main_menu_filler_box,
            self.fast_oad_main_menu_logo_widget,
            self.reference_file_text_box,
            self.reference_file_selector_box,
            self.main_menu_box_start_button,
            self.main_menu_box_buttons_git,
            self.bottom_layer_box,
        ]

        # Main layout
        self.layout = widgets.Layout(
            border = "6px solid black",
            margin = "100 20 50 100px",
            padding = "10px",
            align_items = "center",
            width = "1302px",
            height = "900px",
            justify_content = "center",
        )