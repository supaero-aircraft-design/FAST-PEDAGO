# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os
import os.path as pth

import ipywidgets as widgets

from typing import List

import fastoad.api as oad

from fast_pedago import source_data_files
from fast_pedago import gui

from fast_pedago.gui.buttons import (
    BackHomeButton,
    ClearAllButton,
    SensitivityAnalysisInfoButton,
)

from fast_pedago.gui.tabs import ParentTab
from fast_pedago.utils.functions import _image_from_path  # noqa

from fast_pedago.gui.pages.base_page import BasePage

BOTTOM_BOX_LAYOUT = widgets.Layout(
    border="0px solid black",
    margin="0 0 0 0px",
    padding="0px",
    align_items="center",
    width="100%",
    height="10%",
)

class WorkPage(BasePage):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.set_footer([
            BackHomeButton(self.pages["home"]),
            SensitivityAnalysisInfoButton(),
            ClearAllButton(self.pages["analysis"]),
        ])
        

        fast_oad_logo_top_layer_file_path = pth.join(
            pth.dirname(gui.__file__), "resources", "logo_fast_oad_top_layer.jpg"
        )
        self.fast_oad_top_layer_logo_widget = _image_from_path(
            file_path=fast_oad_logo_top_layer_file_path,
            height="12%",
            width="100",
        )

        self.sensitivity_analysis_tab = ParentTab()
        self.sensitivity_analysis_tab.layout = widgets.Layout(
            border="0px solid black",
            margin="0 0 0 0px",
            padding="0px",
            align_items="flex-start",
            width="98%",
            height="78%",
        )

        self.sensitivity_analysis_tab.selected_index = 0

        self.children = [
            self.fast_oad_top_layer_logo_widget,
            self.sensitivity_analysis_tab,
            self.bottom_layer_box,
        ]
