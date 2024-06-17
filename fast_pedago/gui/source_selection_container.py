# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import ipyvuetify as v

from fast_pedago import source_data_files
from fast_pedago.utils import (
    _list_available_reference_file
)


class SourceSelectionContainer(v.Col):
    """
    An container that contains explanations on the app and a source file
    selector to start using the app.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self._build_layout()
    


    def _build_layout(self):
        self.class_ = "pa-8"
        reference_file_list = [
            file.replace("_source_data_file", "").replace("_", " ") 
            for file in _list_available_reference_file(pth.dirname(source_data_files.__file__))
        ]

        # This reference file should always be there and is always taken as reference
        self.source_data_file_selector = v.Select(
            outlined=True,
            hide_details=True,
            label="Select a reference file",
            items=reference_file_list,
        )
        
        # TODO: Write tutorial/explanations on fast-oad
        self.children=[
            v.Row(
                justify="center",
                children=["Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                          "Sed non risus. Suspendisse lectus tortor, dignissim sit amet, "
                          "adipiscing nec, ultricies sed, dolor. Cras elementum ultrices diam. "
                          "Maecenas ligula massa, varius a, semper congue, euismod non, mi. "
                          "Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, "
                          "non fermentum diam nisl sit amet erat. Duis semper. Duis arcu massa, "
                ],
            ),
            v.Row(
                class_="mt-10",
                justify="center",
                children=[
                    self.source_data_file_selector,
                ],
            ),
        ]