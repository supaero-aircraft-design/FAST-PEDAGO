# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipyvuetify as v

from fast_pedago.processes import (
    PathManager, 
    OutputGraphsPlotter, 
    GRAPH
)
from .input_widgets import SelectOutput


class OutputsGraphsContainer(v.Col):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self._build_layout()

    
    def _build_layout(self):
        self.output_selection = SelectOutput()

        self.general_graph = _OutputFigure('General', is_full_screen=True)
        self.geometry_graph = _OutputFigure('Geometry')
        self.aerodynamics_graph = _OutputFigure('Aerodynamics')
        self.mass_graph = _OutputFigure('Mass')
        self.performances_graph = _OutputFigure('Performances')

        self.output_selection.on_event("click", self._browse_available_process)
        self.output_selection.on_event("change", self._update_data)
        self._hide_graphs()
        
        self.children = [
            v.Row(
                class_="px-4 pb-3",
                children=[self.output_selection],
            ),
            v.Row(
                no_gutters=True,
                align="top",
                children=[
                    self.geometry_graph,
                    self.aerodynamics_graph,
                    self.mass_graph,
                    self.performances_graph,
                    self.general_graph,
                ],
            ),
        ]
    
    def _hide_graphs(self):
        """
        Hides graphs containers (for when no result file is selected).
        """
        self.general_graph.hide()
        self.geometry_graph.hide()
        self.aerodynamics_graph.hide()
        self.mass_graph.hide()
        self.performances_graph.hide()
    
    
    def _show_graphs(self):
        """
        Re-displays graphs.
        """
        self.general_graph.show()
        self.geometry_graph.show()
        self.aerodynamics_graph.show()
        self.mass_graph.show()
        self.performances_graph.show()
    
    
    def _update_data(self, widget, event, data):
        if data :
            self.general_graph.plotter.plot(data)
            self.geometry_graph.plotter.plot(data)
            self.aerodynamics_graph.plotter.plot(data)
            self.mass_graph.plotter.plot(data)
            self.performances_graph.plotter.plot(data)
            
            self._show_graphs()
            
        else:
            self._hide_graphs()
            


    def _browse_available_process(self, widget, event, data):
        self.output_selection.items = PathManager.list_available_process_results()



class _OutputFigure(v.Col):
    def __init__(self, title, is_full_screen: bool = False, **kwargs):
        """
        :param title: The title of the graph. Corresponds to a graph category.
        :param is_full_screen: if True, the card will take all the screen space.
        """
        super().__init__(**kwargs)

        self.cols = 12
        if not is_full_screen:
            self.md = 6

        self.plotter = OutputGraphsPlotter(PathManager.working_directory_path)
        select = v.Select(
            dense=True,
            hide_details=True,
            
            items = GRAPH[title],
            v_model = GRAPH[title][0],
        )
        select.on_event("change", 
            lambda widget, event, data: self.plotter.change_graph(data)
        )
        self.plotter.change_graph(GRAPH[title][0])

        self.children = [
            v.Card(
                outlined=True,
                flat=True,
                children=[
                    v.CardTitle(
                        children=[
                            v.Row(
                                children=[
                                    v.Col(
                                        cols=6,
                                        children=[title],
                                    ),
                                    v.Col(
                                        children=[select],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    v.CardText(
                        class_="pa-0",
                        children=[self.plotter.output_display]
                    ),
                ],
            ),
        ]
        
        