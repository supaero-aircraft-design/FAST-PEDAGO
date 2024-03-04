# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os
import os.path as pth

import ipywidgets as widgets

from typing import List

import fastoad.api as oad

from fast_pedago import source_data_files
from fast_pedago.buttons import (
    get_fast_oad_core_git_button,
    get_fast_oad_cs25_git_button,
    get_fast_oad_cs23_git_button,
    get_main_menu_info_button,
    get_sensitivity_analysis_info_button,
    get_start_button,
    get_back_home_button,
    get_clear_all_button,
)
from fast_pedago.tabs import ParentTab
from fast_pedago.utils.functions import _image_from_path  # noqa

BOTTOM_BOX_LAYOUT = widgets.Layout(
    border="0px solid black",
    margin="0 0 0 0px",
    padding="0px",
    align_items="center",
    width="100%",
    height="10%",
)


class FASTOADInterface(widgets.VBox):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.layout = widgets.Layout(
            border="6px solid black",
            margin="100 20 50 100px",
            padding="10px",
            align_items="center",
            width="1302px",
            height="900px",
            justify_content="center",
        )

        # With Voila it seems impossible to clear and re-display contrarily to Jupyter Notebook.
        # Instead, we'll use the workaround from
        # https://stackoverflow.com/questions/73972010/voila-not-clearing-output-dispalying-new
        # -output which suggests having a VBox as the main interface and change the children of
        # that VBox based on which button we use

        self.reference_file_list = list_available_reference_file(
            pth.dirname(source_data_files.__file__)
        )

        # Add a filler box to force the buttons on the bottom and so that the picture appear clearly
        self.main_menu_filler_box = widgets.Box(
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                align_items="center",
                width="100",
                height="10%",
            ),
        )

        fast_oad_logo_main_menu_file_path = pth.join(
            pth.dirname(__file__), "resources", "logo_fast_oad_main_menu.jpg"
        )
        self.fast_oad_main_menu_logo_widget = _image_from_path(
            fast_oad_logo_main_menu_file_path, height="50%", width="100"
        )

        self.reference_file_text_box = widgets.VBox()
        self.reference_file_text_box.children = [
            widgets.HTML(value=f"<u><b><font size=3>Select a reference file</b></u>")
        ]
        self.reference_file_text_box.layout = widgets.Layout(
            align_items="center", width="100%", height="4%"
        )

        # This reference file should always be there and is always taken as reference
        self.reference_file_selector_widget = widgets.Dropdown(
            options=self.reference_file_list,
            value="reference_aircraft_source_data_file",
            disabled=False,
            style={"description_width": "initial"},
        )
        self.reference_file_selector_widget.layout = widgets.Layout(
            width="80%",
            height="auto",
        )

        def reference_file_setter(change):

            new_file_name = change["new"] + ".xml"
            path_to_reference_file = pth.join(
                pth.dirname(source_data_files.__file__), new_file_name
            )
            self.sensitivity_analysis_tab.impact_variable_input_tab.reference_inputs = (
                oad.DataFile(path_to_reference_file)
            )

        self.reference_file_selector_widget.observe(
            reference_file_setter, names="value"
        )

        self.reference_file_selector_box = widgets.VBox()
        self.reference_file_selector_box.children = [
            self.reference_file_selector_widget
        ]
        self.reference_file_selector_box.layout = widgets.Layout(
            align_items="center", width="100%", height="4%"
        )

        self.start_button = get_start_button()

        # Add a box for the start button
        self.main_menu_box_start_button = widgets.Box(
            children=[self.start_button],
            layout=widgets.Layout(
                display="flex",
                flex_flow="column",
                align_items="center",
                width="100%",
                height="12%",
            ),
        )
        self.start_button.on_click(self.display_sensitivity_analysis_menu)

        fast_core_git_button = get_fast_oad_core_git_button()
        fast_cs25_git_button = get_fast_oad_cs25_git_button()
        fast_cs23_git_button = get_fast_oad_cs23_git_button()

        # Add a box for the GitHub links
        self.main_menu_box_buttons_git = widgets.HBox(
            children=[fast_core_git_button, fast_cs25_git_button, fast_cs23_git_button],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                justify_content="center",
                align_items="center",
                width="100%",
                height="10%",
            ),
        )

        info_button = get_main_menu_info_button()

        # Create a bottom layer for the main menu it will be consisting of box of size 40%/20%/40% which will allow
        # me to center the info button in the middle box AND justify the logo to the right. The same distribution
        # will be used everywhere
        self.bottom_layer_info_box = widgets.widgets.Box(
            children=[info_button],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                justify_content="center",
                align_items="center",
                width="20%",
                height="100%",
            ),
        )

        isae_logo_file_path = pth.join(
            pth.dirname(__file__), "resources", "logo_supaero.png"
        )
        self.isae_logo_widget = _image_from_path(
            isae_logo_file_path, height="100%", width="100"
        )

        self.bottom_layer_logo_filler_box = widgets.Box(
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                justify_content="flex-start",
                width="5%",
                height="100%",
            ),
        )

        airbus_logo_file_path = pth.join(
            pth.dirname(__file__), "resources", "logo_airbus.png"
        )
        self.airbus_logo_widget = _image_from_path(
            airbus_logo_file_path, height="50%", width="100"
        )

        # The idea is to be able to have the logos in the same place and the buttons center. Thus, we will save the
        # logo box and the filler box to reuse them later
        self.logo_box = widgets.HBox(
            children=[
                self.isae_logo_widget,
                self.bottom_layer_logo_filler_box,
                self.airbus_logo_widget,
            ],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                justify_content="flex-end",
                align_items="center",
                width="40%",
                height="100%",
            ),
        )

        self.bottom_layer_filler_box = widgets.Box(
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                justify_content="flex-start",
                width="40%",
                height="100%",
            ),
        )

        # Add a box for the info button and the logos
        self.main_menu_box_bottom_layer = widgets.Box(
            children=[
                self.bottom_layer_filler_box,
                self.bottom_layer_info_box,
                self.logo_box,
            ],
            layout=BOTTOM_BOX_LAYOUT,
        )

        # The default appearance of the box should be the main menu hence the following line
        self.children = [
            self.main_menu_filler_box,
            self.fast_oad_main_menu_logo_widget,
            self.reference_file_text_box,
            self.reference_file_selector_box,
            self.main_menu_box_start_button,
            self.main_menu_box_buttons_git,
            self.main_menu_box_bottom_layer,
        ]

        # Create a button to go back home
        self.analysis_back_home_button = get_back_home_button()
        self.analysis_back_home_button.on_click(self.display_main_menu)

        # A small info button
        self.analysis_info_button = get_sensitivity_analysis_info_button()

        # A button to clear all files generated by user when running this app, this will not
        # clear the reference results
        self.clear_all_button = get_clear_all_button()
        self.clear_all_button.on_click(self.clear_all_files)

        fast_oad_logo_top_layer_file_path = pth.join(
            pth.dirname(__file__), "resources", "logo_fast_oad_top_layer.jpg"
        )
        self.fast_oad_top_layer_logo_widget = _image_from_path(
            file_path=fast_oad_logo_top_layer_file_path,
            height="12%",
            width="100",
        )

        self.sensitivity_analysis_tab = ParentTab()
        self.sensitivity_analysis_tab.layout = widgets.Layout(
            border="0px solid black",
            margin="0 0 0 0px",
            padding="0px",
            align_items="flex-start",
            width="98%",
            height="78%",
        )

        # Create a header with an info button and a button to go back home. Put it at the bottom
        # to match what is done on the main menu
        self.sensitivity_bottom_layer_button_box = widgets.Box(
            children=[
                self.analysis_back_home_button,
                self.analysis_info_button,
                self.clear_all_button,
            ],
            layout=widgets.Layout(
                border="0px solid black",
                margin="0 0 0 0px",
                padding="0px",
                justify_content="center",
                align_items="center",
                width="20%",
                height="100%",
            ),
        )

        self.sensitivity_bottom_layer_box = widgets.Box(
            children=[
                self.bottom_layer_filler_box,
                self.sensitivity_bottom_layer_button_box,
                self.logo_box,
            ],
            layout=BOTTOM_BOX_LAYOUT,
        )

    def display_main_menu(self, event):

        self.children = [
            self.main_menu_filler_box,
            self.fast_oad_main_menu_logo_widget,
            self.reference_file_text_box,
            self.reference_file_selector_box,
            self.main_menu_box_start_button,
            self.main_menu_box_buttons_git,
            self.main_menu_box_bottom_layer,
        ]

    def display_sensitivity_analysis_menu(self, event):

        self.sensitivity_analysis_tab.selected_index = 0

        self.children = [
            self.fast_oad_top_layer_logo_widget,
            self.sensitivity_analysis_tab,
            self.sensitivity_bottom_layer_box,
        ]

    def clear_all_files(self, event):

        # First, we switch back to the main tab of the sensitivity analysis screen which will
        # force a new check of available output file
        self.sensitivity_analysis_tab.selected_index = 0

        working_directory_path = pth.join(os.getcwd(), "workdir")
        input_directory_path = pth.join(working_directory_path, "inputs")
        output_directory_path = pth.join(working_directory_path, "outputs")

        # Remove all input files in the inputs directory
        input_file_list = os.listdir(input_directory_path)
        for file_name in input_file_list:
            file_path = pth.join(input_directory_path, file_name)

            # We keep the reference input_file and avoid deleting subdirectory
            if file_name != "reference_aircraft_input_file.xml" and not pth.isdir(
                file_path
            ):
                os.remove(file_path)

        # Remove all input files in the outputs directory, we can remove all .sql because they
        # are re-generated anyway
        output_file_list = os.listdir(output_directory_path)
        for file_name in output_file_list:
            file_path = pth.join(output_directory_path, file_name)

            # We keep the reference input_file and avoid deleting subdirectory
            if (
                file_name != "reference_aircraft_output_file.xml"
                and file_name != "reference_aircraft_flight_points.csv"
                and not pth.isdir(file_path)
            ):
                os.remove(file_path)


def list_available_reference_file(path_to_scan: str) -> List[str]:
    """
    Parses the name of all the file in the provided path and scan for reference file that can be
    selected for the rest of the analysis

    :param path_to_scan: path to look for reference file in
    :return: a list of available reference files
    """

    list_files = os.listdir(path_to_scan)
    available_reference_files = []

    for file in list_files:

        if file.endswith(".xml"):

            associated_sizing_process_name = file.replace(".xml", "")
            available_reference_files.append(associated_sizing_process_name)

    return available_reference_files
