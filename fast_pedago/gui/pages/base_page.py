# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets

class BasePage(widgets.VBox):
    def __init__(self, pages, **kwargs):

        super().__init__(**kwargs)

        self.pages = pages
