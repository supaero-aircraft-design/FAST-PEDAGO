# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipyvuetify as v
import ipywidgets as widgets

from fast_pedago.gui.buttons import (
    BackHomeButton,
    ClearAllButton,
    SensitivityAnalysisInfoButton,
)

from fast_pedago.gui.tabs.sensitivity_analysis_parent_tab import ParentTab

from fast_pedago.gui.pages.base_page import BasePage


class WorkPage(BasePage):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.set_footer([
            BackHomeButton(self.pages["home"]),
            SensitivityAnalysisInfoButton(),
            ClearAllButton(),
        ])
        

        self.header = v.Row(
            align="top",
            justify="center",
            children=[
                self.fast_oad_top_layer_logo,
            ],
        )

        self.sensitivity_analysis_tabs = v.Row(
            align="top",
            justify="center",
            children=[
                ParentTab()
            ]
        )


        self.children = [
            v.Container(
                fluid=True,
                class_="fill-height pt-0",
                children=[
                    self.header,
                    self.sensitivity_analysis_tabs,
                    self.footer,
                ],
            ),
        ]
