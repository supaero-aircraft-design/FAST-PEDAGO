# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import ipyvuetify as v

from fast_pedago.gui.dropdowns import SelectOutput
from fast_pedago.utils import (
    _OutputsCategory,
    _list_available_sizing_process_results,
)


class OutputsSelectionContainer(v.List):
    """
    An output container to select which output graph to show.
    """
    def __init__(self, working_directory_path: str, **kwargs):
        """
        :param working_directory_path: the path to the working directory to get output data.
        """
        super().__init__(**kwargs)
        
        self.class_ = "pa-0"
        self.expand = True
        
        self.working_directory_path = working_directory_path

        self._build_layout()


    def get_main_output_name(self):
        return self.main_output_selection.v_model


    def get_other_outputs_names(self):
        return self.other_output_selection.v_model


    def _build_layout(self):
        self.main_output_selection = SelectOutput(is_single_output=True)
        self.other_output_selection = SelectOutput(is_single_output=False)
        
        # TODO
        # Disable other selection while no main output is selected
        
        self.main_output_selection.on_event("click", self._browse_available_process)
        self.other_output_selection.on_event("click", self._browse_available_process)

        self.children=[
            v.ListGroup(
                value=True,
                v_slots=[{
                    'name': 'activator',
                    'children': [
                        v.ListItemTitle(
                            children=[
                                "Outputs selection",
                            ],
                        ),
                    ],
                }],
                children=[
                    v.ListItem(
                        children=[
                            self.main_output_selection,
                        ],
                    ),
                    v.ListItem(
                        children=[
                            self.other_output_selection,
                        ],
                    ),
                ],
            ),
            _OutputsCategory("General",
                [
                    "Variables",
                ],
            ),
            _OutputsCategory("Geometry",
                [
                    "Aircraft",
                    "Wing",
                ],
            ),
            _OutputsCategory("Aerodynamics",
                [
                    "Polar",
                ]
            ),
            _OutputsCategory("Mass",
                [
                    "Bar breakdown",
                    "Sun breakdown",
                ],
            ),
            _OutputsCategory("Performances",
                [
                    "Payload-Range",
                    "Mission",
                ]            
            )
       ]


    def _browse_available_process(self, widget, event, data):
        
        available_process = (
            _list_available_sizing_process_results(
                pth.join(self.working_directory_path, "outputs")
            )
        )
        
        self.main_output_selection.items = available_process
        self.other_output_selection.items = available_process