# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO


import ipyvuetify as v

import plotly.graph_objects as go

import fastoad.api as oad

from fast_pedago.gui.dropdowns import SelectOutput
from fast_pedago.gui.buttons import MultipleProcessSelectionInfoButton

from fast_pedago.gui.tabs import BaseTab

class ImpactVariableWingGeometryTab(BaseTab):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sizing_process_to_display = []

        # Initialize it with fake values that we will overwrite as we scan through available
        # processes in the launch tab
        self.output_file_selection_widget = SelectOutput()
        self.info_button = MultipleProcessSelectionInfoButton()

        self.selection_and_info_box = v.Row(
            children=[
                v.Col(
                    cols=11,
                    children=[
                        self.output_file_selection_widget,
                    ],
                ),
                v.Col(
                    children=[
                        self.info_button, 
                    ],
                ),
            ],
        )

        self.output_file_selection_widget.on_event(
            "change",
            lambda widget, event, data: self.display_graph(data, oad.wing_geometry_plot)
        )

        self.children = [
            self.selection_and_info_box, 
            self.output_display,
        ]
