# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

from IPython.display import display, HTML
import ipywidgets as widgets

from .impact_variable_tab import ImpactVariableTab

TABS_NAME = ["Sensitivity analysis"]


class ParentTab(widgets.Tab):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.children = [ImpactVariableTab()]

        # Add a title for each tab
        for i, tab_name in enumerate(TABS_NAME):
            self.set_title(i, tab_name)
