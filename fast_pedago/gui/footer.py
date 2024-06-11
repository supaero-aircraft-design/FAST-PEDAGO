# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import ipyvuetify as v

from fast_pedago.utils.functions import _image_from_path
from fast_pedago import gui

# Path of the logos used
ISAE_LOGO = "logo_supaero.png"
AIRBUS_LOGO = "logo_airbus.png"

# URLs to websites for hyperlinks on images
SUPAERO_WEBSITE_LINK = "https://www.isae-supaero.fr/"
AIRBUS_WEBSITE_LINK = "https://www.airbus.com/"


class Footer(v.Footer):
    """
    A footer for the app.
    """
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._load_images()
        self._build_layout()

    
    def _build_layout(self):
        """
        Builds the layout of the header : ISAE-Supaero and Airbus logos
        followed by FAST-OAD logo, github links buttons and utilitary
        buttons.
        """
        self.padless = True
        self.app = True
        self.color = "white"
        
        self.children = [
            v.Row(
                align="center",
                justify="end",
                children=[
                    v.Col(
                        cols="1",
                        children=[self.isae_logo]
                    ),
                    v.Col(
                        class_="pe-6",
                        cols=2,
                        children=[self.airbus_logo]
                    ),
                ],
            ),
        ]

    
    # TODO
    # Implement clicking on the the fast-oad logo to go back to main menu
    def _load_images(self):
        """
        Loads header images as instance variables to call them during
        the layout building.
        """
        resources_path = pth.join(pth.dirname(gui.__file__), "resources")

        # Get ISAE logo
        self.isae_logo = _image_from_path(pth.join(resources_path, ISAE_LOGO))
        # Sets the link to supaero website, to open in a new tab
        self.isae_logo.attributes = {'href': SUPAERO_WEBSITE_LINK, "target": "_blank"}

        # Get Airbus logo
        self.airbus_logo = _image_from_path(pth.join(resources_path, AIRBUS_LOGO))
        # Sets the link to airbus website, to open in a new tab
        self.airbus_logo.attributes = {'href': AIRBUS_WEBSITE_LINK, "target": "_blank"}