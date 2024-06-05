# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipyvuetify as v

from fast_pedago.gui.tabs import BaseTab

from fast_pedago.gui.graph_visualization_container import GraphVisualizationContainer
from fast_pedago.gui.inputs_container import InputsContainer


DEFAULT_PROCESS_NAME = "aircraft"


class ImpactVariableInputLaunchTab(BaseTab):
    def __init__(self, source_data_file_name: str, **kwargs):
        super().__init__(**kwargs)
        
        self._set_layout(source_data_file_name)
        
    
    def _set_layout(self, source_data_file_name):
        # Name used for the process when none is given
        self.process_name = DEFAULT_PROCESS_NAME
        
        # Text box to give a name to the run
        self.process_name_field = v.TextField(
            outlined=True,
            hide_details=True,
            label="Sizing name",
            placeholder="Write a name for your sizing process",
        )
        self.process_name_field.on_event("change", self._update_process_name)

        # Create a button to launch the sizing
        self.launch_button = v.Btn(
            block=True,
            color="#32cd32",
            width="31%",
            children=[
                v.Icon(class_="px-3", children=["fa-plane"]),
                "Launch sizing process"
            ],
        )

        # Create a button to trigger the MDO "mode"
        self.process_selection_switch = v.Switch(
            v_model=False,
            class_="mt-0 pt-2",
            label="MDO",
            tooltip="Check that box to swap in optimization mode",
        )
        self.process_selection_switch.on_event("change", self._switch_process)
        
        self.inputs = InputsContainer(source_data_file_name)
        self.graphs = GraphVisualizationContainer(self.configuration_file_path)
        
        self.children = [
            v.Row(
                children=[
                    v.Col(
                        cols=2,
                        children=[
                            self.process_selection_switch,
                        ],
                    ),
                    v.Col(
                        cols=8,
                        children=[
                            self.process_name_field,
                        ],
                    ),
                    v.Col(
                        children=[
                            self.launch_button,
                        ],
                    ),
                ],
            ),
            v.Row(
                children=[
                    self.inputs,
                    self.graphs,
                ],
            ),
        ]
        

    def _switch_process(self, widget, event, data):

        # If the switch is true, switch to MDO
        if data:
            self.inputs.to_MDO()
            self.graphs.to_MDO()
            
            self.launch_button.children =[
                v.Icon(class_="px-3", children=["fa-plane"]),
                "Launch optimization process",
            ]
            self.process_name_field.label = "Opimization name"
            self.process_name_field.placeholder = "Write a name for your optimization process"

        else:
            self.inputs.to_MDA()
            self.graphs.to_MDA()
            
            self.launch_button.children =[
                v.Icon(class_="px-3", children=["fa-plane"]),
                "Launch sizing process",
            ]
            self.process_name_field.label = "Sizing name"
            self.process_name_field.placeholder = "Write a name for your sizing process"
    
    
    def _update_process_name(self, widget, event, data):
        """
        Changes process name when a new name is written
        in the input text field.

        To be used with a "on_event" of a text field ipyvuetify 
        """
        self.process_name = data