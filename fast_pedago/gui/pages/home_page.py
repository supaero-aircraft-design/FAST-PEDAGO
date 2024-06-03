# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import ipyvuetify as v

from fast_pedago import source_data_files

from fast_pedago.gui.buttons import (
    FastOadCoreGitButton,
    FastOadCS25GitButton,
    FastOadCS23GitButton,
    MainMenuInfoButton,
    StartButton,
)

from fast_pedago.utils.functions import _list_available_reference_file  # noqa

from fast_pedago.gui.pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.set_footer([
                MainMenuInfoButton()
            ])


        self.header_logo = v.Row(
            align="top",
            justify="center",
            children=[
                 self.fast_oad_main_menu_logo,
            ],
        )

        
        self.reference_file_list = [
            file.replace("_source_data_file", "").replace("_", " ") for file in _list_available_reference_file(
            pth.dirname(source_data_files.__file__)
            )
        ]

        # This reference file should always be there and is always taken as reference
        self.source_data_file_selector = v.Select(
            outlined=True,
            hide_details=True,
            label="Select a reference file",
            items=self.reference_file_list,
        )
    
        self.source_data_file_selector.on_event("change", HomePage.set_source_data_file)

        self.start_button = v.Col(
            cols=12,
            md=2,
            children=[
                StartButton(self.pages["analysis"]),
            ],
        )

        # The file selector and the start button are put in the same row
        self.start_box = v.Row(
            class_="px-3 pt-3",
            align="top",
            justify="center",
            children=[
                v.Col(
                    cols=12,
                    md=10,
                    children=[
                        self.source_data_file_selector,
                    ],
                ),
                self.start_button,                
            ],
        )


        self.git_buttons = v.Row(
            class_="pa-2",
            align="center",
            justify="center",
            children=[
                # BtnToggle is used to create a group of buttons nicely rendered
                v.BtnToggle(
                    v_model="toggle_none",
                    rounded=True,
                    children=[
                        FastOadCoreGitButton(), 
                        FastOadCS25GitButton(), 
                        FastOadCS23GitButton(),
                    ],
                ),
            ],
        )


        # The default appearance of the box should be the main menu hence the following line
        self.children = [
            v.Container(
                fluid=True,
                children=[
                    self.header_logo,
                    self.start_box,
                    # A simple divider for esthetics
                    v.Row(children=[v.Divider(class_="pa-2")]),
                    self.git_buttons,
                    self.footer,
                ],
            ),
        ]
        

    def set_source_data_file(widget, event, data):
        """
        Sets the reference file name to use
        
        To be called by a widget event
        """
        BasePage.source_data_file = data