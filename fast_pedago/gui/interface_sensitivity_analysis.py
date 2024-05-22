# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os
import os.path as pth

import ipywidgets as widgets

from fast_pedago.gui.pages.home_page import HomePage
from fast_pedago.gui.pages.work_page import WorkPage


class FASTOADInterface(widgets.VBox):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        
        self.pages = {
            "home" : self.display_home_page,
            "analysis" : self.display_sensitivity_analysis_menu,
        }

        self.children = [
            HomePage(self.pages),
        ]

        


    def display_home_page(self, event):

        self.children = [
            HomePage(self.pages),
        ]

    def display_sensitivity_analysis_menu(self, event):
        
        self.children = [
            WorkPage(self.pages),
        ]

