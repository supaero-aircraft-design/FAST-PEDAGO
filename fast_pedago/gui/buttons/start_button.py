# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets



class StartButton(widgets.Button):

    def __init__(self, display_sensitivity_analysis_menu, **kwargs):
        super().__init__(**kwargs)    

        # Create a green button which spans almost the full width of the interface
        self.layout = widgets.Layout(
            width="80%",
            height="95%",
            border="4px solid black",
        )

        # Slight note, if you add two numbers after the hexadecimal code, you can make it transparent
        self.description="Get started!"
        self.style=dict(
                button_color="#33caff99",
                font_weight="bold",
                font_size="20px",
        )

        self.on_click(display_sensitivity_analysis_menu)
