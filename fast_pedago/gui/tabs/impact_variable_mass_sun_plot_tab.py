# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipyvuetify as v

import fastoad.api as oad

from fast_pedago.gui.dropdowns import SelectOutput
from fast_pedago.gui.buttons import SingleProcessSelectionInfoButton

from fast_pedago.gui.tabs import BaseTab

class ImpactVariableMassSunBreakdownTab(BaseTab):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize it with fake values that we will overwrite as we scan through available
        # processes in the launch tab
        self.output_file_selection_widget = SelectOutput(is_single_output=True)
        self.info_button = SingleProcessSelectionInfoButton()

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
            lambda widget, event, data: self.display_graph(widget, data, oad.mass_breakdown_sun_plot)
        )

        self.children = [
            self.selection_and_info_box, 
            self.output_display,
        ]
