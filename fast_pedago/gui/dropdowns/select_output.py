# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets
import ipyvuetify as v

class SelectOutput(v.Select):
    def __init__(self, is_single_output=False, **kwargs):
        super().__init__(**kwargs)
        
        self.outlined = True
        self.clearable = True
        
        if is_single_output:
            self.label = "Select a main output file to display"
        else:
            self.label = "Select output files for comparison"
            self.multiple = True
            self.chips = True
            self.deletable_chips = True
            self.hide_selected = True
