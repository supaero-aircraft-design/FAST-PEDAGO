# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import ipywidgets as widgets

from fast_pedago.utils.functions import _image_from_path
from fast_pedago import gui

class BasePage(widgets.VBox):
    def __init__(self, pages, **kwargs):

        super().__init__(**kwargs)
        
        self.pages = pages

        self.recover_images()

    
    def set_footer(self, buttons):

        # Create a bottom layer for the main menu it will be consisting of box of size 40%/20%/40% which will allow
        # me to center the info button in the middle box AND justify the logo to the right. The same distribution
        # will be used everywhere
        self.bottom_layer_info_box = widgets.widgets.Box(
            children=[
                button for button in buttons
            ],

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

        
        # Filler box to make space between the logos
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

        # Add a box to make space between the info button and the logos
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
        self.bottom_layer_box = widgets.Box(
            children=[
                self.bottom_layer_filler_box,
                self.bottom_layer_info_box,
                self.logo_box,
            ],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                align_items="center",
                width="100%",
                height="10%",
            ),
        )


    
    def recover_images(self):

        # Get FAST-OAD logo
        fast_oad_logo_main_menu_file_path = pth.join(
            pth.dirname(gui.__file__), "resources", "logo_fast_oad_main_menu.jpg"
        )
        self.fast_oad_main_menu_logo_widget = _image_from_path(
            fast_oad_logo_main_menu_file_path, height="50%", width="100"
        )

        # Get ISAE logo
        isae_logo_file_path = pth.join(
            pth.dirname(gui.__file__), "resources", "logo_supaero.png"
        )
        self.isae_logo_widget = _image_from_path(
            isae_logo_file_path, height="100%", width="100"
        )

        # Get Airbus logo
        airbus_logo_file_path = pth.join(
            pth.dirname(gui.__file__), "resources", "logo_airbus.png"
        )
        self.airbus_logo_widget = _image_from_path(
            airbus_logo_file_path, height="50%", width="100"
        )
