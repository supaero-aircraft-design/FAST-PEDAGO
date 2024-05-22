# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipyvuetify as v


class StartButton(v.Btn):
    """
    A button that opens the sensitivity analysis page

    :arg analysis_page: The function that changes the current children
        of the app to display the sensitivity analysis page
    """

    def __init__(self, analysis_page, **kwargs):
        super().__init__(**kwargs)  

        self.block = True
        self.color = "#33caff99" # Slight note, if you add two numbers after the hexadecimal code, you can make it transparent
        self.children = ["Get started!"]
        
        self.on_event("click", analysis_page)
