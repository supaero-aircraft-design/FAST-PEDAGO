# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os.path as pth

import ipyvuetify as v

from fast_pedago.utils import (
    _OutputCard,
    _list_available_sizing_process_results,
)
from . import SelectOutput


class OutputsGraphsContainer(v.Col):
    def __init__(self, working_directory_path, **kwargs):
        super().__init__(**kwargs)

        self.working_directory_path = working_directory_path
        self._build_layout(working_directory_path)

    
    def _build_layout(self, working_directory_path):
        self.output_selection = SelectOutput()

        self.general_graph = _OutputCard('General', working_directory_path)
        self.geometry_graph = _OutputCard('Geometry', working_directory_path)
        self.aerodynamics_graph = _OutputCard('Aerodynamics', working_directory_path)
        self.mass_graph = _OutputCard('Mass', working_directory_path)
        self.performances_graph = _OutputCard('Performances', working_directory_path)

        self.output_selection.on_event("click", self._browse_available_process)
        self.output_selection.on_event("change", self._update_data)
        
        self.children = [
            v.Row(
                class_="px-4",
                children=[self.output_selection],
            ),
            v.Row(
                align="center",
                children=[
                    self.general_graph,
                    self.geometry_graph,
                    self.aerodynamics_graph,
                    self.mass_graph,
                    self.performances_graph,
                ],
            ),
        ]
    
    
    def _update_data(self, widget, event, data):
        if data :
            self.general_graph.plotter.plot(data)
            self.geometry_graph.plotter.plot(data)
            self.aerodynamics_graph.plotter.plot(data)
            self.mass_graph.plotter.plot(data)
            self.performances_graph.plotter.plot(data)
            
            self.general_graph.show()
            self.geometry_graph.show()
            self.aerodynamics_graph.show()
            self.mass_graph.show()
            self.performances_graph.show()
        
        else:
            self.general_graph.hide()
            self.geometry_graph.hide()
            self.aerodynamics_graph.hide()
            self.mass_graph.hide()
            self.performances_graph.hide()


    def _browse_available_process(self, widget, event, data):
        
        available_process = (
            _list_available_sizing_process_results(
                pth.join(self.working_directory_path, "outputs")
            )
        )
        
        self.output_selection.items = available_process