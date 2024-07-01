"""
Utility layout classes for widgets to avoid repeating code
"""
# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipyvuetify as v

from fast_pedago.processes import (
    OutputGraphsPlotter,
    GRAPH,
)


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