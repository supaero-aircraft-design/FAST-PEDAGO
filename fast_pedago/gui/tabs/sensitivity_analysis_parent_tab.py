    # This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO
from IPython.display import clear_output, display
import os
import os.path as pth
import shutil

from threading import Thread, Event
from time import sleep

import copy
import warnings

import numpy as np

import openmdao.api as om

import ipywidgets as widgets
import ipyvuetify as v

from .impact_variable_inputs_tab import ImpactVariableInputLaunchTab
from .impact_variable_outputs_tab import ImpactVariableOutputTab
from .impact_variable_wing_geometry_tab import ImpactVariableWingGeometryTab
from .impact_variable_aircraft_geometry_tab import ImpactVariableAircraftGeometryTab
from .impact_variable_drag_polar_tab import ImpactVariableDragPolarTab
from .impact_variable_mass_bar_plot_tab import ImpactVariableMassBarBreakdownTab
from .impact_variable_mass_sun_plot_tab import ImpactVariableMassSunBreakdownTab
from .impact_variable_payload_range_tab import ImpactVariablePayloadRangeTab
from .impact_variable_mission_tab import ImpactVariableMissionTab

import fastoad.api as oad

from fast_pedago import configuration, source_data_files

from fast_pedago.utils import (
    _list_available_sizing_process_results,
    _extract_residuals,
    _extract_objective,
    OUTPUT_FILE_SUFFIX,
    FLIGHT_DATA_FILE_SUFFIX,
)

TABS_NAME = [
    "Inputs & Launch",
    "Outputs",
    "Geometry - Wing",
    "Geometry - Aircraft",
    "Aerodynamics - Polar",
    "Mass - Bar breakdown",
    "Mass - Sun breakdown",
    "Performances - Payload/Range",
    "Performances - Mission",
]


class ParentTab(v.Card):
    def __init__(self, source_data_file_name: str, **kwargs):

        super().__init__(**kwargs)
        
        self._configure()
        self._set_layout(source_data_file_name)
        
    
    def _configure(self):
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
        self.mdo_configuration_file_path = pth.join(
            self.data_directory_path, "oad_optim_sensitivity_analysis.yml"
        )

        self.reference_input_file_path = pth.join(
            self.working_directory_path,
            pth.join("inputs", "reference_aircraft_input_file.xml"),
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

        if not pth.exists(self.mdo_configuration_file_path):
            shutil.copy(
                pth.join(
                    pth.dirname(configuration.__file__),
                    "oad_optim_sensitivity_analysis.yml",
                ),
                self.mdo_configuration_file_path,
            )

        # Technically, we could simply copy the reference file because I already did the input
        # generation but to be more generic we will do it like this which will make it longer on
        # the first execution.
        if not pth.exists(self.reference_input_file_path):
            oad.generate_inputs(
                configuration_file_path=self.configuration_file_path,
                source_data_path=pth.join(
                    pth.dirname(source_data_files.__file__),
                    "reference_aircraft_source_data_file.xml",
                ),
            )


    def _set_layout(self, source_data_file_name):
        
        self.input_tab = ImpactVariableInputLaunchTab(
            source_data_file_name=source_data_file_name,
            configuration_file_path=self.configuration_file_path,
            reference_input_file_path=self.reference_input_file_path,
        )
        self.input_tab.launch_button.on_event("click",self._launch_process)

        self.tabs_items = [
            self.input_tab,
            ImpactVariableOutputTab(working_directory_path=self.working_directory_path),
            ImpactVariableWingGeometryTab(working_directory_path=self.working_directory_path),
            ImpactVariableAircraftGeometryTab(working_directory_path=self.working_directory_path),
            ImpactVariableDragPolarTab(working_directory_path=self.working_directory_path),
            ImpactVariableMassBarBreakdownTab(working_directory_path=self.working_directory_path),
            ImpactVariableMassSunBreakdownTab(working_directory_path=self.working_directory_path),
            ImpactVariablePayloadRangeTab(working_directory_path=self.working_directory_path),
            ImpactVariableMissionTab(working_directory_path=self.working_directory_path),
        ]

        self.tabs = v.Tabs(
            children=[
                # Tabs titles
                    v.Tab(children=[tab_name]) for tab_name in TABS_NAME
                ]
                + self.tabs_items
                + [
                    v.TabsSlider(),
                ]
        )
        self.tabs.on_event("change", self.browse_available_sizing_process)

        self.children = [
            self.tabs,
        ]


    def _launch_mdo(self, process_started: Event):
        """
        Launches the mdo by reading the design vars, the objective and the constraints from the tab
        and the rest of the input from the reference file except for the sweep which we will fix
        at 30° (M=0.82 which is the max you can enter as the upper bound).
        
        :param process_started: an event that is set just before the beginning of the process,
        after the setup is complete
        """

        # Create a new FAST-OAD problem based on the reference configuration file
        configurator = oad.FASTOADProblemConfigurator(self.mdo_configuration_file_path)

        # Save orig file path and name so that we can replace them with the sizing process
        # name
        orig_input_file_path = configurator.input_file_path
        orig_input_file_name = pth.basename(orig_input_file_path)
        orig_output_file_path = configurator.output_file_path
        orig_output_file_name = pth.basename(orig_output_file_path)

        new_input_file_path = orig_input_file_path.replace(
            orig_input_file_name,
            self.input_tab.process_name + "_mdo_input_file.xml",
        )
        new_output_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.input_tab.process_name
            + "_mdo"
            + OUTPUT_FILE_SUFFIX,
        )
        

        # Change the input and output file path in the configurator
        configurator.input_file_path = new_input_file_path
        configurator.output_file_path = new_output_file_path
        
        # Create the input file with the reference value, except for sweep
        new_inputs = copy.deepcopy(self.input_tab.inputs.reference_inputs)
        # Save as the new input file. We overwrite always, may need to put a warning for
        # students
        new_inputs.save_as(new_input_file_path, overwrite=True)

        problem = self.input_tab.inputs.retrieve_mdo_inputs(configurator)

        problem.model.approx_totals()
        problem.setup()

        # Ran the case with the proper mission and go those coefficient
        problem.set_val(
            name="settings:mission:sizing:breguet:climb:mass_ratio", val=0.975
        )
        problem.set_val(
            name="settings:mission:sizing:breguet:descent:mass_ratio", val=0.993
        )
        problem.set_val(
            name="settings:mission:sizing:breguet:reserve:mass_ratio", val=0.055
        )

        driver = problem.driver
        # The recorder file path is declared with "self" to be able to retrieve
        # it from the plot function in an other thread. There might be better
        # ways to pass it from a thread to an other.
        self.recorder_database_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.input_tab.process_name + "_mdo_cases.sql",
        )
        recorder = om.SqliteRecorder(self.recorder_database_file_path)
        driver.add_recorder(recorder)
        driver.recording_options["record_objectives"] = True

        # Triggers the plot in an other thread
        process_started.set()
        
        problem.run_driver()

        problem.write_outputs()

        # We also need to rename the .csv file which contains the mission data. I don't
        # see a proper way to do it other than that since it is something INSIDE the
        # configuration file which we can't overwrite like the input and output file
        # path. There may be a way to do it by modifying the options of the performances
        # components of the problem but it seems too much

        old_mission_data_file_path = orig_output_file_path.replace(
            orig_output_file_name, "flight_points.csv"
        )
        new_mission_data_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.input_tab.process_name
            + "_mdo"
            + FLIGHT_DATA_FILE_SUFFIX,
        )

        # You can't rename to a file which already exists, so if one already exists we
        # delete it before renaming.
        if pth.exists(new_mission_data_file_path):
            os.remove(new_mission_data_file_path)

        os.rename(old_mission_data_file_path, new_mission_data_file_path)

        # Shut down the recorder so we can delete the .sql file later
        recorder.shutdown()


    def _launch_mda(self, process_started: Event):
        """
        Launches the mda by reading the inputs from the proper tab and extract the value for the
        target residuals
        
        :param process_started: an event that is set just before the beginning of the process,
        after the setup is complete
        """

        # Create a new FAST-OAD problem based on the reference configuration file
        configurator = oad.FASTOADProblemConfigurator(self.configuration_file_path)

        # Save orig file path and name so that we can replace them with the sizing process
        # name
        orig_input_file_path = configurator.input_file_path
        orig_input_file_name = pth.basename(orig_input_file_path)
        orig_output_file_path = configurator.output_file_path
        orig_output_file_name = pth.basename(orig_output_file_path)

        new_input_file_path = orig_input_file_path.replace(
            orig_input_file_name,
            self.input_tab.process_name + "_input_file.xml",
        )
        new_output_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.input_tab.process_name + OUTPUT_FILE_SUFFIX,
        )

        # Change the input and output file path in the configurator
        configurator.input_file_path = new_input_file_path
        configurator.output_file_path = new_output_file_path
        
        new_inputs = self.input_tab.inputs.retrieve_mda_inputs()

        # Save as the new input file. We overwrite always, may need to put a warning for
        # students
        new_inputs.save_as(new_input_file_path, overwrite=True)

        # Get the problem, no need to write inputs. The fact that the reference was created
        # based on the same configuration we will always use should ensure the completion of
        # the input file
        problem = configurator.get_problem(read_inputs=True)
        problem.setup()

        # Save target residuals
        # The "target_residuals" and recorder file path are declared with "self" 
        # to be able to retrieve them from the plot function in an other thread. 
        # There might be better ways to pass them from a thread to an other.
        self.target_residuals = problem.model.nonlinear_solver.options["rtol"]

        model = problem.model
        self.recorder_database_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.input_tab.process_name + "_cases.sql",
        )
        recorder = om.SqliteRecorder(self.recorder_database_file_path)
        model.nonlinear_solver.add_recorder(recorder)
        model.nonlinear_solver.recording_options["record_solver_residuals"] = True

        # Triggers the plot in an other thread
        process_started.set()

        # Run the problem and write output. Catch warning for cleaner interface
        with warnings.catch_warnings():
            warnings.simplefilter(action="ignore", category=FutureWarning)
            problem.run_model()

        problem.write_outputs()

        # We also need to rename the .csv file which contains the mission data. I don't
        # see a proper way to do it other than that since it is something INSIDE the
        # configuration file which we can't overwrite like the input and output file
        # path. There may be a way to do it by modifying the options of the performances
        # components of the problem but it seems too much

        old_mission_data_file_path = orig_output_file_path.replace(
            orig_output_file_name, "flight_points.csv"
        )
        new_mission_data_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.input_tab.process_name
            + FLIGHT_DATA_FILE_SUFFIX,
        )

        # You can't rename to a file which already exists, so if one already exists we
        # delete it before renaming.
        if pth.exists(new_mission_data_file_path):
            os.remove(new_mission_data_file_path)

        os.rename(old_mission_data_file_path, new_mission_data_file_path)

        # Shut down the recorder so we can delete the .sql file later
        recorder.shutdown()
    

    # TODO
    # Factorize code from the two next methods
    def _plot(self, process_started: Event, process_ended: Event, is_MDA: bool=True):
        """
        Plots the relative error of each iteration during MDA process, and the relative error
        threshold. 
        First waits for the process to finish its setup by waiting for the process_started event.

        :param process_started: event triggered in the process when the setup is finished
        :param process_ended: event triggered after the process ends
        :param is_MDA: boolean indicating if the program should plot objectives (MDO) or residuals (MDA)
        """
        # Wait until the beginning of the process.
        # There should be a better way to do it with threading
        # library though.
        while not process_started.is_set():
            sleep(0.1)
        
        temp_recorder_database_file_path = self.recorder_database_file_path.replace(
                "_cases.sql",
                "_temp_cases.sql",
            )
        
        while not process_ended.is_set():
            sleep(0.1)
            
            try :
                # Copy the db file before reading it to avoid reading when an other thread is writing,
                # which could cause the code to fail.
                shutil.copyfile(self.recorder_database_file_path, temp_recorder_database_file_path)
                
                if is_MDA:
                    # Extract the residuals, build a scatter based on them and plot them along with the
                    # threshold set in the configuration file
                    iterations, relative_error = np.array(
                        _extract_residuals(recorder_database_file_path=temp_recorder_database_file_path)
                    )
                    self.input_tab.graphs.plot(iterations, relative_error, self.target_residuals)
                
                else :
                    # Extract the residuals, build a scatter based on them and plot them along with the
                    # threshold set in the configuration file
                    iterations, objective = np.array(
                        _extract_objective(recorder_database_file_path=temp_recorder_database_file_path)
                    )
                    min_objective = min(objective)
                    
                    self.input_tab.graphs.plot(iterations, objective, min_objective)

            except:
                pass


    def _launch_process(self, widget, event, data):

        # "Hide" the output tabs !
        self.input_tab.launch_button.color = (
            "#FF0000"
        )
        self.hide_tabs(self.tabs)
        # TODO
        # Disable the sliders and inputs while process is running
        # Make the launch button a cancel button to stop the process

        # Show a loading widget to make it apparent that a computation is
        # underway.
        self.input_tab.graphs.set_loading("Setup")

        dummy_output = widgets.Output()
        with dummy_output:
            
            # Initialize events to synchronize the process thread and the plotting thread
            process_started = Event()
            process_ended = Event()

            # If the switch is off, MDA, else MDO
            if not self.input_tab.process_selection_switch.v_model:
                process_thread = Thread(target=self._launch_mda, args=(process_started,))
                plotting_thread = Thread(
                    target=self._plot, 
                    args=(process_started, process_ended),
                )

            else:
                process_thread = Thread(target=self._launch_mdo, args=(process_started,))
                plotting_thread = Thread(
                    target=self._plot, 
                    args=(process_started, process_ended, False),
                )

            process_thread.start()
            plotting_thread.start()
            
            process_thread.join()
            # This line is to make sure the plotting ends after the process and plots everything
            sleep(0.5)
            process_ended.set()
            plotting_thread.join()

            self.input_tab.launch_button.color = (
                "#32cd32"
            )

            self.show_tabs(self.tabs)


    def show_tabs(self, tabs: v.Tabs):
        for child in tabs.children:
            child.disabled = False


    def hide_tabs(self, tabs: v.Tabs):
        for child in tabs.children:
            child.disabled = True


    def browse_available_sizing_process(self, widget, event, data):
        # On tab change, we browse the output folder of the workdir to check all completed
        # sizing processes. Additionally instead of doing it on all tab change, we will only
        # do it if the old tab was the tab from which we can launch a sizing process, i.e the
        # first tab
        
        # TODO
        # if change["name"] == "selected_index":
        #     if change["old"] == 0:
        
        self.available_sizing_process = (
            _list_available_sizing_process_results(
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
                self.tabs_items[
                    tab_index
                ].output_file_selection_widget.items = self.available_sizing_process
