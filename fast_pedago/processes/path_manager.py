

import os
import os.path as pth
import shutil

from typing import List

import fastoad.api as oad

from fast_pedago import (
    configuration,
    gui,
    source_data_files,
)

from fast_pedago.objects.paths import(
    WORK_DIRECTORY,
    DATA_DIRECTORY,
    INPUTS_DIRECTORY,
    OUTPUTS_DIRECTORY,
    RESOURCES_DIRECTORY,
    TUTORIAL_DIRECTORY,
    MDA_CONFIGURATION_FILE,
    MDO_CONFIGURATION_FILE,
    REFERENCE_AIRCRAFT,
    INPUT_FILE_SUFFIX,
    OUTPUT_FILE_SUFFIX,
    SOURCE_FILE_SUFFIX,
    FLIGHT_DATA_FILE_SUFFIX,
    SEPARATOR,
)


class PathManager():
    """
    Contains all the paths and generates the needed directory, to pass them on to
    the other components that need it.
    """
    working_directory_path = ""
    data_directory_path = ""

    reference_aircraft = ""
    reference_input_file_name = ""
    reference_output_file_name = ""
    reference_source_file_name = ""
    reference_flight_data_file_name = ""
    
    reference_input_file_path = ""
    
    mda_configuration_file_path = ""
    mdo_configuration_file_path = ""
    
    input_directory_path = ""
    output_directory_path = ""
    
    resources_path = ""
    tutorial_resources_path = ""


    @staticmethod
    def _build_working_directory():
        """
        Creates the working directory if not already created, and sets the path to it.
        Working directory contains input and output files (.xml and .csv).
        """
        PathManager.working_directory_path = pth.join(os.getcwd(), WORK_DIRECTORY)
        if not pth.exists(PathManager.working_directory_path):
            os.mkdir(PathManager.working_directory_path)

        PathManager.input_directory_path = pth.join(
            PathManager.working_directory_path, INPUTS_DIRECTORY)
        PathManager.output_directory_path = pth.join(
            PathManager.working_directory_path, OUTPUTS_DIRECTORY)


    @staticmethod
    def _sets_reference_files():
        def build_name(suffix: str) -> str:
            return REFERENCE_AIRCRAFT + suffix

        PathManager.reference_aircraft = REFERENCE_AIRCRAFT
        PathManager.reference_input_file_name = build_name(INPUT_FILE_SUFFIX)
        PathManager.reference_output_file_name = build_name(OUTPUT_FILE_SUFFIX)
        PathManager.reference_source_file_name = build_name(SOURCE_FILE_SUFFIX)
        PathManager.reference_flight_data_file_name = build_name(FLIGHT_DATA_FILE_SUFFIX)


    @staticmethod
    def _build_reference_input_file():
        """
        Generates the reference input file with the reference aircraft source file
        and the MDA configuration file if not created, and sets the path to it.
        """
        PathManager.reference_input_file_path = pth.join(
            PathManager.working_directory_path,
            pth.join(INPUTS_DIRECTORY, PathManager.reference_input_file_path),
        )
        
        # Technically, we could simply copy the reference file because I already did the input
        # generation but to be more generic we will do it like this which will make it longer on
        # the first execution.
        if not pth.exists(PathManager.reference_input_file_path):
            oad.generate_inputs(
                configuration_file_path=PathManager.mda_configuration_file_path,
                source_data_path=pth.join(
                    pth.dirname(source_data_files.__file__),
                    PathManager.reference_source_file_name,
                ),
            )


    @staticmethod
    def _build_data_directory():
        """
        Creates the data directory if not already created, and sets the path to it.
        Data directory contains configuration files (copied from original configuration
        files), and N2/XDSM graphs
        """
        PathManager.data_directory_path = pth.join(os.getcwd(), DATA_DIRECTORY)
        if not pth.exists(PathManager.data_directory_path):
            os.mkdir(PathManager.data_directory_path)
        
        # To make it simpler to handle relative path from the configuration file, instead 
        # of using this one directly we will make a copy of it in a data directory of the 
        # active directory
        PathManager.mda_configuration_file_path = PathManager._build_configuration_file(
            MDA_CONFIGURATION_FILE)
        PathManager.mdo_configuration_file_path = PathManager._build_configuration_file(
            MDO_CONFIGURATION_FILE)


    @staticmethod
    def _build_configuration_file(configuration_file_name: str) -> str:
        """
        Copy the given configuration file from "configuration" directory to data
        directory.

        :param configuration_file_name: the given configuration file.
        :return the path to the copied configuration file.
        """
        configuration_file_path = pth.join(
            PathManager.data_directory_path, configuration_file_name
        )
        if not pth.exists(configuration_file_path):
            shutil.copy(
                pth.join(
                    pth.dirname(configuration.__file__),
                    configuration_file_name
                ),
                configuration_file_path,
            )
        
        return configuration_file_path


    @staticmethod
    def _build_resources_directory():
        PathManager.resources_path = pth.join(pth.dirname(gui.__file__), RESOURCES_DIRECTORY)
        PathManager.tutorial_resources_path = pth.join(PathManager.resources_path, TUTORIAL_DIRECTORY)


    @staticmethod
    def build_paths():
        """
        Generates all directories and files needed, and saves their path.
        """
        # The file for the sensitivity analysis is specific. Consequently, 
        # we won't generate it from fast-oad_cs25.
        PathManager._build_data_directory() 
        PathManager._build_working_directory() 
        PathManager._sets_reference_files()
        PathManager._build_reference_input_file()
        PathManager._build_resources_directory()


    @staticmethod
    def list_available_reference_file() -> List[str]:
        """
        Parses the name of all the file in the source files folder and scan 
        for reference file that can be selected for the rest of the analysis

        :return: a list of available reference files names
        """

        list_files = os.listdir(pth.dirname(source_data_files.__file__))
        available_reference_files = []

        for file in list_files:
            if file.endswith(".xml"):
                associated_sizing_process_name = file.replace(SOURCE_FILE_SUFFIX, "").replace(SEPARATOR, " ")
                available_reference_files.append(associated_sizing_process_name)

        return available_reference_files