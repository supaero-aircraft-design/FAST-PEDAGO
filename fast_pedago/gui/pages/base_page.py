# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import ipyvuetify as v

from fast_pedago.utils.functions import _image_from_path
from fast_pedago import gui

class BasePage(v.Container):
    def __init__(self, pages, **kwargs):

        super().__init__(**kwargs)
        
        self.class_ = "pa-0"

        self.pages = pages

        self.recover_images()

    
    def set_footer(self, buttons):
        """
        Create a footer of size 42%/16%/42% of screen width to display the git links,
        some buttons, and ISAE and Airbus logos.

        The footer is made to be reusable in all the app, simply changing the buttons

        :param buttons: to add to the center of the footer
        """

        self.footer_main_buttons = v.Col(
            cols=12,
            md=2,
            children=[
                v.Container(
                    class_="fill-height",
                    children=[
                        v.Row(
                            align="center",
                            justify="center",
                            children=[
                                button for button in buttons
                            ],
                        ),
                    ],
                ),
            ],
        )

        self.footer_logos = v.Col(
            cols=12,
            md=5,
            children=[
                v.Row(
                    align="center",
                    justify="center",
                    children=[
                        self.isae_logo,
                        self.airbus_logo,
                    ],
                ),
            ],
        )

        # Row that packs the three columns
        self.footer = v.Row(
            align = "bottom",
            children=[
                # An empty column for spacing
                v.Col(cols=12, md=5),
                self.footer_main_buttons,
                self.footer_logos,
            ],
        )

    
    def recover_images(self):

        # Get FAST-OAD logo for main menu
        fast_oad_logo_main_menu_file_path = pth.join(
            pth.dirname(gui.__file__), "resources", "logo_fast_oad_main_menu.jpg"
        )
        self.fast_oad_main_menu_logo = _image_from_path(
            fast_oad_logo_main_menu_file_path, 
            height="20vw", 
            width="100",
        )

        # Get FAST-OAD logo for top layer
        fast_oad_logo_top_layer_file_path = pth.join(
            pth.dirname(gui.__file__), "resources", "logo_fast_oad_top_layer.jpg"
        )
        self.fast_oad_top_layer_logo = _image_from_path(
                file_path=fast_oad_logo_top_layer_file_path,
                height="10vh",
                width="100",
        )

        # Get ISAE logo
        isae_logo_file_path = pth.join(
            pth.dirname(gui.__file__), "resources", "logo_supaero.png"
        )
        self.isae_logo = _image_from_path(
            isae_logo_file_path, 
            height="10vh", 
            width="100",
        )

        # Get Airbus logo
        airbus_logo_file_path = pth.join(
            pth.dirname(gui.__file__), "resources", "logo_airbus.png"
        )
        self.airbus_logo = _image_from_path(
            airbus_logo_file_path, 
            height="5vh", 
            width="100",
        )