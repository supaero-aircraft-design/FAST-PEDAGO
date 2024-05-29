# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets
import ipyvuetify as v

class SelectOutput(v.Select):
    def __init__(self, is_single_output=False, **kwargs):
        super().__init__(**kwargs)
        
        self.outlined = True
        self.is_single_output = is_single_output
        
        if is_single_output:
            self.label = "Select an output file to display"
        else:
            self.label = "Select an output file to add to the display"
