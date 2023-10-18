# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets

import fastoad.api as oad


class ImpactVariableInputTab(widgets.VBox):
    def __init__(self, reference_input_file_path: str, **kwargs):

        super().__init__(**kwargs)

        self.reference_input_file_path = reference_input_file_path

        # Read the reference input file path so that we can give first accurate first value
        reference_inputs = oad.DataFile(self.reference_input_file_path)

        # Define attribute to store variable value and give them an initial value corresponding to the reference inputs
        self.n_pax = reference_inputs["data:TLAR:NPAX"].value[0]

        # Define a common layout for all the data widgets
        self.input_widget_layout = widgets.Layout(
            width="75%",
            height="50px",
            justify_content="space-between",
        )

        # Create the widgets to change the value of the parameters in the sensitivity analysis
        self.n_pax_input_widget = widgets.BoundedFloatText(
            min=19.0,
            max=500.0,
            step=1.0,
            value=self.n_pax,
            description="N_PAX",
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
