# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import ipywidgets as widgets


def get_select_multiple_sizing_process_dropdown():

    # Originally I planned on using a dropdown but it takes too much space as it will be as long
    # as there are available sizing process. Instead what we will do is use a Dropdown and each
    # time a new sizing process is clicked on it will add to the picture and we will add a None
    # button that clear the display.
    select_multiple_sizing_process_dropdown = widgets.Dropdown(
        options=["None"],
        value="None",
        description="Select an output file to add to the display:",
        disabled=False,
        style={"description_width": "initial"},
    )

    select_multiple_sizing_process_dropdown.layout = widgets.Layout(
        width="95%",
        height="auto",
        justify_content="space-between",
        align_items="flex-start",
    )

    return select_multiple_sizing_process_dropdown
