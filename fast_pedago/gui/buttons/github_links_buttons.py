# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipyvuetify as v

GITHUB_FAST_CORE = "https://github.com/fast-aircraft-design/FAST-OAD"
GITHUB_FAST_CS25 = "https://github.com/fast-aircraft-design/FAST-OAD_CS25"
GITHUB_FAST_CS23 = "https://github.com/supaero-aircraft-design/FAST-GA"

class GitLinksButton(v.Menu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.offset_y = True
        self.rounded = True
        self.open_on_hover = True
        self.v_slots = [{
            "name": "activator",
            "variable": "button",
            "children": v.Btn(
                v_bind="button.attrs",
                v_on="button.on",
                icon=True,
                x_large=True,
                children=[
                    v.Icon(
                        x_large=True,
                        children=["fa-github"],
                    ),
                ],
            ),   
        }]
        self.children = [
            v.List(
                class_="pa-0",
                children=[
                    _GitLinkButtonItem(GITHUB_FAST_CORE, "FAST-OAD_core"),
                    _GitLinkButtonItem(GITHUB_FAST_CS25, "FAST-OAD_cs25"),
                    _GitLinkButtonItem(GITHUB_FAST_CS23, "FAST-OAD_cs23"),
                ],
            ),
        ]

class _GitLinkButtonItem(v.ListItem):
    """
    A button with a git icon that is clickable and opens the link provided

    :arg href: The url to the web page to open
    """
    
    def __init__(self, href, text, **kwargs):
        super().__init__(**kwargs)

        self.class_ = "pa-0"
        self.children = [
            v.Btn(
                text=True,
                href=href,
                children=[
                    text,
                ],
            ),
        ]