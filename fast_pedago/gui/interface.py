# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os
import os.path as pth
import shutil

import ipyvuetify as v

import fastoad.api as oad

from fast_pedago import (
    configuration,
    source_data_files,
)
from . import Header


DRAWER_WIDTH = "35%"
HEADER_WIDTH = "52px"


DEFAULT_SOURCE_DATA_FILE = "reference aircraft"


class Interface(v.App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        self.source_data_file = DEFAULT_SOURCE_DATA_FILE
        
        self._configure_paths()
        self._build_layout()


    def _build_layout(self):
        self.drawer = v.NavigationDrawer(
            app=True,
            clipped=True,
            width=DRAWER_WIDTH,
        )
        self.main = v.Container(
            style_="padding: " + HEADER_WIDTH + " 0px 0px " + DRAWER_WIDTH + ";",
            fluid=True,
            tag="main",
        )

        self.children = [
            Header(),
            self.drawer,
            self.main,
        ]


    def _configure_paths(self):
        # The configuration file path, source file path and input file path will be shared by
        # children tab, so we will define them there and pass them on. The file for the
        # sensitivity analysis is specific. Consequently, we won't generate it from
        # fast-oad_cs25. Additionally, to make it simpler to handle relative path from the
        # configuration file, instead of using this one directly we will make a copy of it in a
        # data directory of the active directory.

        self.working_directory_path = pth.join(os.getcwd(), "workdir")
        self.data_directory_path = pth.join(os.getcwd(), "data")

        # Create an attribute to store the converged sizing processes, it will be updated each
        # time we exit the launch tab.
        self.available_sizing_process = []

        if not pth.exists(self.working_directory_path):
            os.mkdir(self.working_directory_path)

        if not pth.exists(self.data_directory_path):
            os.mkdir(self.data_directory_path)

        # Please note here that I'm using a different configuration file from the original one
        # because I wanted to use the one from fast-oad_cs25 and change some paths
        self.mda_configuration_file_path = pth.join(
            self.data_directory_path, "oad_sizing_sensitivity_analysis.yml"
        )
        self.mdo_configuration_file_path = pth.join(
            self.data_directory_path, "oad_optim_sensitivity_analysis.yml"
        )

        self.reference_input_file_path = pth.join(
            self.working_directory_path,
            pth.join("inputs", "reference_aircraft_input_file.xml"),
        )

        # Avoid operation if we don't have to
        if not pth.exists(self.mda_configuration_file_path):
            shutil.copy(
                pth.join(
                    pth.dirname(configuration.__file__),
                    "oad_sizing_sensitivity_analysis.yml",
                ),
                self.mda_configuration_file_path,
            )

        if not pth.exists(self.mdo_configuration_file_path):
            shutil.copy(
                pth.join(
                    pth.dirname(configuration.__file__),
                    "oad_optim_sensitivity_analysis.yml",
                ),
                self.mdo_configuration_file_path,
            )

        # Technically, we could simply copy the reference file because I already did the input
        # generation but to be more generic we will do it like this which will make it longer on
        # the first execution.
        if not pth.exists(self.reference_input_file_path):
            oad.generate_inputs(
                configuration_file_path=self.mda_configuration_file_path,
                source_data_path=pth.join(
                    pth.dirname(source_data_files.__file__),
                    "reference_aircraft_source_data_file.xml",
                ),
            )

    
