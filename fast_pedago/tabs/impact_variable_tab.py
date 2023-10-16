# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets


class ImpactVariableTab(widgets.VBox):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.default_xml_path = None

        # Define attribute to store variable value
        self.n_pax = 150.0

        # Define layout for all the data widgets
        self.input_widget_layout = widgets.Layout(
            width="75%",
            height="50px",
            justify_content="space-between",
        )

        self.n_pax_input_widget = widgets.BoundedFloatText(
            min=19.0,
            max=500.0,
            step=0.1,
            value=self.n_pax,
            description="Npax",
            description_tooltip="Number of Passengers",
            layout=self.input_widget_layout,
        )

        self.children = [self.n_pax_input_widget]
        self.layout = widgets.Layout(
            border="2px solid black",
            align_items="flex-end",
            padding="2px",
            width="40%",
        )
