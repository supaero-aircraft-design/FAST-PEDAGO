# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets


def get_select_single_sizing_process_dropdown():

    select_single_sizing_process_dropdown = widgets.Dropdown(
        options=["None"],
        value="None",
        description="Select an output file to display:",
        disabled=False,
        style={"description_width": "initial"},
    )

    select_single_sizing_process_dropdown.layout = widgets.Layout(
        width="98%",
        height="5%",
        justify_content="space-between",
        align_items="flex-start",
    )

    return select_single_sizing_process_dropdown
