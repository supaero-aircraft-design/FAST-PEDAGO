"""
Contains the main layout of the app : header, footer, drawer layouts.
"""

import os.path as pth

import ipyvuetify as v

from fast_pedago.utils.functions import _image_from_path
from fast_pedago import gui
from . import (
    GitLinksButton,
    ClearAllButton,
)


DRAWER_WIDTH = "450px"
HEADER_HEIGHT = "64px" 

# Path of the logos used
FAST_OAD_MAIN_MENU_LOGO = "logo_fast_oad_main_menu.jpg"
FAST_OAD_TOP_LAYER_LOGO = "logo_fast_oad_top_layer.jpg"
ISAE_LOGO = "logo_supaero.png"
AIRBUS_LOGO = "logo_airbus.png"

# URLs to websites for hyperlinks on images
SUPAERO_WEBSITE_LINK = "https://www.isae-supaero.fr/"
AIRBUS_WEBSITE_LINK = "https://www.airbus.com/"


class Drawer(v.NavigationDrawer):
    """
    A navigation drawer that expands from the left of the screen,
    that is always displayed on large screens, and hidden on small
    screens (with the possibility to open it temporarely). 
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # The content attributes will be used to change the components
        # displayed easily.
        self.content = v.Container(
            class_="pa-0",
        )
        
        # Some of the components are made to hide when on small screens
        # This is to adjust the layout since the navigation drawer hides
        # on small screens.
        self.close_drawer_button = v.Btn(
            class_="me-5 hidden-lg-and-up",
            icon=True,
            children=[
                v.Icon(children=["fa-times"]),
            ],
        )

        self.app = True
        self.clipped = True
        self.width = DRAWER_WIDTH
        self.v_model = True
        self.children = [
            v.Container(
                style_="padding: " + HEADER_HEIGHT + " 0 0 0;",
                class_="hidden-md-and-down",
            ),
            v.Row(
                justify="end",
                children=[
                    self.close_drawer_button,
                ],
            ),
            self.content,
        ]


class Header(v.AppBar):
    """
    A header for the app.
    Contains a fast-oad logo, github links button and auxiliary buttons.
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
        self.class_ = "px-5"
        self.fixed = True
        self.color = "white"
        
        self.open_drawer_button = v.Btn(
            class_="hidden-lg-and-up",
            icon=True,
            x_large=True,
            children=[
                v.AppBarNavIcon(),
            ],
        )
        
        self.clear_all_button = ClearAllButton()
        
        self.children = [
            v.Row(
                align="center",
                children=[
                    v.Col(
                        class_="py-0",
                        cols=4,
                        children=[
                            v.Row(
                                align="center",
                                justify="start",
                                children=[self.open_drawer_button],
                            ),
                        ],
                    ),
                    v.Col(
                        class_="py-0",
                        cols=4,
                        children=[
                            v.Row(
                                justify="center",
                                children=[self.fast_oad_top_layer_logo_wrapper]
                            ),
                        ],
                    ),
                    v.Col(
                        class_="py-0",
                        children=[
                            v.Row(
                                justify="end",
                                children=[
                                    GitLinksButton(),
                                    self.clear_all_button,
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ]
    
    def _load_images(self):
        """
        Loads header images as instance variables to call them during
        the layout building.
        """
        resources_path = pth.join(pth.dirname(gui.__file__), "resources")
        
        # Get FAST-OAD logo for main menu
        self.fast_oad_main_menu_logo = _image_from_path(pth.join(resources_path, FAST_OAD_MAIN_MENU_LOGO))

        # Get FAST-OAD logo for top layer
        self.fast_oad_top_layer_logo = _image_from_path(pth.join(resources_path, FAST_OAD_TOP_LAYER_LOGO))
        self.fast_oad_top_layer_logo.v_on = 'tooltip.on'
        self.fast_oad_top_layer_logo_wrapper = v.Tooltip(
            absolute=True,
            v_slots=[{
            'name': 'activator',
            'variable': 'tooltip',
            'children': self.fast_oad_top_layer_logo,
            }],
            children=["Return to source file selection"],
        )



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