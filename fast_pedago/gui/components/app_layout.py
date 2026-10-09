"""
Contains the main layout of the app : header, footer, drawer layouts.
"""

import ipyvuetify as v

from fast_pedago.utils import PathManager, _image_from_path

from .input_widgets import (
    ClearAllButton,
    GitLinksButton,
)

# Components sizes
# Vuetify 3 parses the drawer width as a number of pixels
DRAWER_WIDTH = 450
HEADER_HEIGHT = "64px"

# Logos image files names
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
    screens (with the possibility to open it temporarily).
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._build_layout()

    def _build_layout(self):
        """
        Generates the drawer layout.
        """
        self.width = DRAWER_WIDTH
        self.v_model = True
        self.scrim = False

        # The content attributes will be used to change the components
        # displayed easily.
        self.content = v.Container(
            class_="pa-0",
        )

        # Some of the components are made to hide when on small screens
        # ("hidden-lg-and-up"). This is to adjust the layout since the
        # navigation drawer hides on small screens.
        self.close_drawer_button = v.Btn(
            class_="me-5 hidden-lg-and-up",
            icon=True,
            children=[
                v.Icon(children=["mdi-close"]),
            ],
        )

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
        followed by FAST-OAD logo, github links buttons and utility
        buttons.
        """
        self.class_ = "px-5"
        self.color = "white"

        self.open_drawer_button = v.Btn(
            class_="hidden-lg-and-up",
            icon=True,
            size="x-large",
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
                                children=[
                                    self._fast_oad_logo_wrapper,
                                ],
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
        # Get FAST-OAD logo
        self.fast_oad_logo = _image_from_path(
            PathManager.path_to("resources", FAST_OAD_TOP_LAYER_LOGO)
        )
        self.fast_oad_logo.v_on = "tooltip.on"
        self._fast_oad_logo_wrapper = v.Tooltip(
            location="bottom",
            v_slots=[
                {
                    "name": "activator",
                    "variable": "tooltip",
                    "children": self.fast_oad_logo,
                }
            ],
            children=["Return to tutorial"],
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
        followed by FAST-OAD logo, github links buttons and utility
        buttons.
        """
        self.class_ = "pa-0"
        self.color = "white"

        self.start_button = v.Btn(
            color="#32cd32",
            size="x-large",
            children=["Start making aircraft"],
        )

        self.children = [
            v.Container(
                fluid=True,
                class_="pa-0",
                children=[
                    v.Row(
                        style_="width: 100%;",
                        align="center",
                        justify="center",
                        no_gutters=True,
                        children=[
                            v.Col(
                                cols=4,
                            ),
                            v.Col(
                                cols=4,
                                children=[
                                    v.Row(justify="center", children=[self.start_button]),
                                ],
                            ),
                            v.Col(
                                cols=4,
                                children=[
                                    v.Row(
                                        align="center",
                                        justify="end",
                                        no_gutters=True,
                                        children=[
                                            v.Spacer(),
                                            v.Col(cols=3, children=[self._isae_logo]),
                                            v.Spacer(),
                                            v.Col(
                                                class_="pe-6",
                                                cols=7,
                                                children=[self._airbus_logo],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            )
        ]

    def _load_images(self):
        """
        Loads header images as instance variables to call them during
        the layout building.
        """
        # Get ISAE logo
        self._isae_logo = _image_from_path(
            PathManager.path_to("resources", ISAE_LOGO),
            max_height="10vh",
        )
        # Sets the link to supaero website, to open in a new tab
        self._isae_logo.attributes = {
            "href": SUPAERO_WEBSITE_LINK,
            "target": "_blank",
        }

        # Get Airbus logo
        self._airbus_logo = _image_from_path(
            PathManager.path_to("resources", AIRBUS_LOGO), max_height="10vh"
        )
        # Sets the link to airbus website, to open in a new tab
        self._airbus_logo.attributes = {
            "href": AIRBUS_WEBSITE_LINK,
            "target": "_blank",
        }
