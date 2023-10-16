# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import ipywidgets as widgets

import fastoad.api as oad

from .impact_variable_tab import ImpactVariableTab

TABS_NAME = ["Sensitivity analysis"]


class ParentTab(widgets.Tab):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # The configuration file path, source file path and input file path will be shared by children tab, so we will
        # define them there and pass them on. Also, in cas anyone does back and forth between the main menu and this
        # tab, we will check whether the file exists before regenerating it.
        self.configuration_file_path = (
            "data/configuration_file_sensitivity_analysis.yml"
        )

        if not pth.exists(pth.abspath(self.configuration_file_path)):
            oad.generate_configuration_file(
                configuration_file_path=self.configuration_file_path,
                overwrite=True,  # Does not matter since we check whether it exists and don't recreate it if it does
                distribution_name="fast-oad-cs25",
                sample_file_name="cs25_base.yaml",
            )

        self.children = [ImpactVariableTab()]

        # Add a title for each tab
        for i, tab_name in enumerate(TABS_NAME):
            self.set_title(i, tab_name)
