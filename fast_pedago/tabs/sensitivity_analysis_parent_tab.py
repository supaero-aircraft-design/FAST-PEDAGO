# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os
import os.path as pth
import shutil

import ipywidgets as widgets

from .impact_variable_inputs_tab import ImpactVariableInputLaunchTab

import fastoad.api as oad

from fast_pedago import configuration, source_data_files

TABS_NAME = ["Inputs & Launch"]


class ParentTab(widgets.Tab):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # The configuration file path, source file path and input file path will be shared by
        # children tab, so we will define them there and pass them on. The file for the
        # sensitivity analysis is specific. Consequently, we won't generate it from
        # fast-oad_cs25. Additionally, to make it simpler to handle relative path from the
        # configuration file, instead of using this one directly we will make a copy of it in a
        # data directory of the active directory.

        self.working_directory_path = pth.join(os.getcwd(), "workdir")
        self.data_directory_path = pth.join(os.getcwd(), "data")

        if not pth.exists(self.working_directory_path):
            os.mkdir(self.working_directory_path)

        if not pth.exists(self.data_directory_path):
            os.mkdir(self.data_directory_path)

        # Please note here that I'm using a different configuration file from the original one
        # because I wanted to use the one from fast-oad_cs25 and change some paths
        self.configuration_file_path = pth.join(
            self.data_directory_path, "oad_sizing_sensitivity_analysis.yml"
        )
        self.reference_input_file_path = pth.join(
            self.working_directory_path,
            "inputs/reference_aircraft_input_file.xml",
        )

        # Avoid operation if we don't have to
        if not pth.exists(self.configuration_file_path):
            shutil.copy(
                pth.join(
                    pth.dirname(configuration.__file__),
                    "oad_sizing_sensitivity_analysis.yml",
                ),
                self.configuration_file_path,
            )

        # Technically, we could simply copy the reference file because I already did the input
        # generation but to be more generic we will do it like this which will make it longer on
        # the first execution.
        if not pth.exists(self.reference_input_file_path):
            oad.generate_inputs(
                configuration_file_path=self.configuration_file_path,
                source_path=pth.join(
                    pth.dirname(source_data_files.__file__),
                    "reference_aircraft_source_data_file.xml",
                ),
            )

        self.impact_variable_input_tab = ImpactVariableInputLaunchTab(
            reference_input_file_path=self.reference_input_file_path
        )

        self.children = [self.impact_variable_input_tab]

        # Add a title for each tab
        for i, tab_name in enumerate(TABS_NAME):
            self.set_title(i, tab_name)
