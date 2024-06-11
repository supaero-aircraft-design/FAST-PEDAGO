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
from . import Header, Footer
from . import InputsContainer


DRAWER_WIDTH = "450px"
HEADER_HEIGHT = "64px" 

# As there are margins and padding in the voila template, 
# I have to adjust the padding considering both the spacings
# in the voila template and the other components sizes.
TOP_PADDING = "36px"
LEFT_PADDING = "426px"


DEFAULT_SOURCE_DATA_FILE = "reference aircraft"


class Interface(v.App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
        self.source_data_file = DEFAULT_SOURCE_DATA_FILE
        
        self._configure_paths()
        self._build_layout()
        
        self.to_inputs()


    def to_inputs(self):
        self.drawer_content.children = [self.inputs]
        self.main_content.children = [self.default_content]


    def _build_layout(self):
        """
        Builds the layout of the app.
        """
        self.inputs = InputsContainer()
        self.default_content = v.Html(tag="div", children=["Lorem ipsum"])
        
        # The content attributes will be used to change the components
        # displayed depending on the phase of the app : inputs, outputs, 
        # source file selection.
        self.drawer_content = v.Container(
            class_="pa-0",
        )
        
        self.main_content = v.Container(
            class_="pt-0",
            fluid=True,
            fill_height=True,
        )
        
        # Some of the components are made to hide when on small screens
        # This is to adjust the layout since the navigation drawer hides
        # on small screens.
        header = Header()
        header.open_drawer_button.on_event("click.stop", self._open_close_drawer)
        
        close_drawer_button = v.Btn(
            class_="me-5 hidden-lg-and-up",
            icon=True,
            children=[
                v.Icon(children=["fa-times"]),
            ],
        )
        close_drawer_button.on_event("click", self._open_close_drawer)

        self.children = [
            header,
            v.NavigationDrawer(
                app=True,
                clipped=True,
                width=DRAWER_WIDTH,
                v_model=True,
                children=[
                    v.Container(
                        style_="padding: " + HEADER_HEIGHT + " 0 0 0;",
                        class_="hidden-md-and-down",
                    ),
                    v.Row(
                        justify="end",
                        children=[
                            close_drawer_button,
                        ],
                    ),
                    self.drawer_content,
                ],
            ),
            # Main content : to display graphs
            v.Html(
                tag="main",
                class_="v-main",
                children=[
                    v.Row(
                    style_="padding: " + TOP_PADDING + " 0 0 0;",
                    ),
                    v.Row(
                        children=[
                            v.Col(
                                cols="1",
                                style_="padding: 100px 0 0 " + LEFT_PADDING + ";",
                                class_="hidden-md-and-down",
                            ),
                            v.Col(
                                children=[self.main_content],
                            ),
                        ],
                    ),
                ],
            ),
            Footer()
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
    

    def _open_close_drawer(self, widget, event, data):
            self.drawer.v_model = not self.drawer.v_model

    
