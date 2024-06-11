"""
Utilitary layout classes for widgets to avoid repeating code
"""
# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipyvuetify as v

import plotly.graph_objects as go

from . import FIGURE_HEIGHT


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
    def __init__(self, name: str, inputs: v.VuetifyWidget = [], **kwargs):
        """
        :param name: the name of the category
        :param inputs: a list of input widgets 
        """
        super().__init__(**kwargs)

        self.value = True
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


# FIXME 
# Tooltip doesn't work
class _TooltipButton(v.Btn):
    """
    Internal class to factorize layout of a button
    with a tooltip
    """
    def __init__(self, text: str, tooltip: str, **kwargs):
        """
        :param text: text of the button
        :param tooltip: text of the tooltip
        """
        super().__init__(**kwargs)

        self.update(text, tooltip)
        
    
    def update(self, text:str, tooltip: str):
        self.children = [
            text,
            v.Tooltip(
                activator="parent",
                location="top",
                children=tooltip,
            ),
        ]
