"""
Utilitary layout classes for widgets to avoid repeating code
"""
# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO
import os.path as pth

import ipyvuetify as v

import plotly.graph_objects as go

from . import FIGURE_HEIGHT
from fast_pedago.processes import (
    OutputGraphsPlotter,
    GRAPH,
)


class _Figure(go.FigureWidget):
    """
    A widget to prepare the layout used to plot residuals and
    objectives
    """
    def __init__(
            self,
            main_scatter_name: str,
            limit_scatter_name: str,
            title: str,
            x_axes_label: str,
            y_axes_label: str,
            is_log: bool = True,
            **kwargs,
        ):
        """
        :param main_scatter_name: label for the main plot (residuals or objective)
        :param limit_scatter_name: label for the relative error threshold or the
        minimum objective reached
        :param title: title of the plot
        :param x_axes_label: label of the x axes
        :param y_axes_label: label of the y axes
        :param is_log: true if y is a log axis
        """
        super().__init__(
            data = [
                go.Scatter(x=[], y=[], name=main_scatter_name),
                go.Scatter(x=[], y=[], mode="lines", name=limit_scatter_name),
            ],
            layout = go.Layout(height=FIGURE_HEIGHT),
            **kwargs,
        )
        
        self.update_layout(title_text=title, title_x=0.5)
        self.update_xaxes(title_text=x_axes_label)
        if is_log:
            self.update_yaxes(title_text=y_axes_label, type="log", range=[-7.0, 1.0])
        else:
            self.update_yaxes(title_text=y_axes_label, type="log")


class _InputsCategory(v.ListGroup):
    """
    Internal class to factorize layout of an input category
    such as weight inputs, geometry inputs, TLARs, etc.
    
    It displays the name of the category as a title and
    the input widgets under it.
    """
    def __init__(self, 
            name: str, 
            inputs: v.VuetifyWidget = [], 
            is_open: bool = False,
            **kwargs):
        """
        :param name: the name of the category
        :param inputs: a list of input widgets 
        :param is_open: True if the group is initially open
        """
        super().__init__(**kwargs)

        self.value = is_open
        self.v_slots = [{
            'name': 'activator',
            'children': [
                v.ListItemTitle(
                    children=[
                        name,
                    ],
                ),
            ],
        }]
        self.children = [
            v.ListItem(children=[input]) for input in inputs
        ]


class _OutputCard(v.Col):
    def __init__(self, title, working_directory_path, is_full_screen: bool = False, **kwargs):
        """
        :param title: The title of the graph. Coresponds to a graph category.
        :param is_full_screen: if True, the card will take all the screen space.
        """
        super().__init__(**kwargs)

        self.cols = 12
        if not is_full_screen:
            self.md = 6

        self.plotter = OutputGraphsPlotter(working_directory_path)
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