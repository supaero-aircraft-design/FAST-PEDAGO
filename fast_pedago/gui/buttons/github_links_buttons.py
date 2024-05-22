# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets

import webbrowser

GITHUB_FAST_CORE = "https://github.com/fast-aircraft-design/FAST-OAD"
GITHUB_FAST_CS25 = "https://github.com/fast-aircraft-design/FAST-OAD_CS25"
GITHUB_FAST_CS23 = "https://github.com/supaero-aircraft-design/FAST-GA"


class BaseGitButton(widgets.Button):
    
    def __init__(self, link, **kwargs):
        super().__init__(**kwargs)

        self.link = link

        self.icon = "fa-github"
        self.layout.width = "auto"
        self.layout.height = "auto"

        self.on_click(self.open_github)

    def open_github(self, event):
            webbrowser.open_new_tab(self.link)

class FastOadCoreGitButton(BaseGitButton):
    def __init__(self, **kwargs):
        super().__init__(GITHUB_FAST_CORE, **kwargs)

        self.description = "FAST-OAD_core"

class FastOadCS25GitButton(BaseGitButton):
    def __init__(self, **kwargs):
        super().__init__(GITHUB_FAST_CS25, **kwargs)

        self.description = "FAST-OAD_cs25"

class FastOadCS23GitButton(BaseGitButton):
    def __init__(self, **kwargs):
        super().__init__(GITHUB_FAST_CS23, **kwargs)

        self.description = "FAST-OAD_cs23"