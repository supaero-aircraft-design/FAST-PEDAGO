# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os
import os.path as pth
import shutil

from typing import List

import ipywidgets as widgets

from .impact_variable_inputs_tab import (
    ImpactVariableInputLaunchTab,
    OUTPUT_FILE_SUFFIX,
    FLIGHT_DATA_FILE_SUFFIX,
)
from .impact_variable_outputs_tab import ImpactVariableOutputTab
from .impact_variable_wing_geometry_tab import ImpactVariableWingGeometryTab
from .impact_variable_aircraft_geometry_tab import ImpactVariableAircraftGeometryTab
from .impact_variable_drag_polar_tab import ImpactVariableDragPolarTab
from .impact_variable_mass_bar_plot_tab import ImpactVariableMassBarBreakdownTab
from .impact_variable_mass_sun_plot_tab import ImpactVariableMassSunBreakdownTab
from .impact_variable_payload_range_tab import ImpactVariablePayloadRangeTab

import fastoad.api as oad

from fast_pedago import configuration, source_data_files

TABS_NAME = [
    "Inputs & Launch",
    "Outputs",
    "Geometry - Wing",
    "Geometry - Aircraft",
    "Aerodynamics - Polar",
    "Mass - Bar breakdown",
    "Mass - Sun breakdown",
    "Performances - Payload/Range",
]


class ParentTab(widgets.Tab):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # The configuration file path, source file path and input file path will be shared by
        # children tab, so we will define them there and pass them on. The file for the
        # sensitivity analysis is specific. Consequently, we won't generate it from
        # fast-oad_cs25. Additionally, to make it simpler to handle relative path from the
        # configuration file, instead of using this one directly we will make a copy of it in a
        # data directory of the active directory.

        self.working_directory_path = pth.join(os.getcwd(), "workdir")
        self.data_directory_path = pth.join(os.getcwd(), "data")

        # Create an attribute to store the converged sizing processes, it will be updated each
        # time we exit the launch tab.
        self.available_sizing_process = []

        if not pth.exists(self.working_directory_path):
            os.mkdir(self.working_directory_path)

        if not pth.exists(self.data_directory_path):
            os.mkdir(self.data_directory_path)

        # Please note here that I'm using a different configuration file from the original one
        # because I wanted to use the one from fast-oad_cs25 and change some paths
        self.configuration_file_path = pth.join(
            self.data_directory_path, "oad_sizing_sensitivity_analysis.yml"
        )
        self.reference_input_file_path = pth.join(
            self.working_directory_path,
            "inputs/reference_aircraft_input_file.xml",
        )

        # Avoid operation if we don't have to
        if not pth.exists(self.configuration_file_path):
            shutil.copy(
                pth.join(
                    pth.dirname(configuration.__file__),
                    "oad_sizing_sensitivity_analysis.yml",
                ),
                self.configuration_file_path,
            )

        # Technically, we could simply copy the reference file because I already did the input
        # generation but to be more generic we will do it like this which will make it longer on
        # the first execution.
        if not pth.exists(self.reference_input_file_path):
            oad.generate_inputs(
                configuration_file_path=self.configuration_file_path,
                source_path=pth.join(
                    pth.dirname(source_data_files.__file__),
                    "reference_aircraft_source_data_file.xml",
                ),
            )

        self.impact_variable_input_tab = ImpactVariableInputLaunchTab(
            configuration_file_path=self.configuration_file_path,
            reference_input_file_path=self.reference_input_file_path,
        )
        self.impact_variable_output_tab = ImpactVariableOutputTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_wing_geometry_tab = ImpactVariableWingGeometryTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_aircraft_geometry_tab = ImpactVariableAircraftGeometryTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_drag_polar_tab = ImpactVariableDragPolarTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_mass_bar_breakdown_tab = ImpactVariableMassBarBreakdownTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_mass_sun_breakdown_tab = ImpactVariableMassSunBreakdownTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_payload_range_tab = ImpactVariablePayloadRangeTab(
            working_directory_path=self.working_directory_path
        )

        def browse_available_sizing_process(change=None):

            # On tab change, we browse the output folder of the workdir to check all completed
            # sizing processes. Additionally instead of doing it on all tab change, we will only
            # do it if the old tab was the tab from which we can launch a sizing process, i.e the
            # first tab
            if change["name"] == "selected_index":
                if change["old"] == 0:
                    self.available_sizing_process = (
                        list_available_sizing_process_results(
                            pth.join(self.working_directory_path, "outputs")
                        )
                    )

                    # Update the available value for each tab while making sure to leave the None
                    # option as it will always be the selected value
                    for tab_index, _ in enumerate(TABS_NAME):

                        # Nothing to update in the first tab (the launch tab)
                        if tab_index != 0:

                            # This assumes that all tabs except the first will have an attribute
                            # named "output_file_selection_widget"
                            self.children[
                                tab_index
                            ].output_file_selection_widget.options = [
                                "None"
                            ] + self.available_sizing_process

        self.observe(browse_available_sizing_process)

        self.children = [
            self.impact_variable_input_tab,
            self.impact_variable_output_tab,
            self.impact_variable_wing_geometry_tab,
            self.impact_variable_aircraft_geometry_tab,
            self.impact_variable_drag_polar_tab,
            self.impact_variable_mass_bar_breakdown_tab,
            self.impact_variable_mass_sun_breakdown_tab,
            self.impact_variable_payload_range_tab,
        ]

        # Add a title for each tab
        for i, tab_name in enumerate(TABS_NAME):
            self.set_title(i, tab_name)


def list_available_sizing_process_results(path_to_scan: str) -> List[str]:
    """
    Parses the name of all the file in the provided path and scan for the one that would match the
    results of an OAD sizing process. Is meant to work only on a path containing both the output
    file and flight data file

    :param path_to_scan: path to look for the results of sizing process in
    :return: a list of available process names
    """

    list_files = os.listdir(path_to_scan)
    available_sizing_process = []

    for file in list_files:

        # Delete the suffix corresponding to the output file and flight data file because that's
        # how they were built. Also, we will ignore the .sql file

        if file.endswith(".sql"):
            continue

        associated_sizing_process_name = file.replace(OUTPUT_FILE_SUFFIX, "").replace(
            FLIGHT_DATA_FILE_SUFFIX, ""
        )

        if associated_sizing_process_name not in available_sizing_process:
            available_sizing_process.append(associated_sizing_process_name)

    return available_sizing_process
