# This file is part of FAST-OAD_CS23-HE : A framework for rapid Overall Aircraft Design of Hybrid
# Electric Aircraft.
# Copyright (C) 2022 ISAE-SUPAERO

import os
import os.path as pth
import shutil

import copy
import warnings

import numpy as np

import openmdao.api as om

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
from .impact_variable_mission_tab import ImpactVariableMissionTab

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
    "Performances - Mission",
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
        self.mdo_configuration_file_path = pth.join(
            self.data_directory_path, "oad_optim_sensitivity_analysis.yml"
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

        self.impact_variable_input_tab = ImpactVariableInputLaunchTab(
            configuration_file_path=self.configuration_file_path,
            reference_input_file_path=self.reference_input_file_path,
        )
        self.impact_variable_input_tab.layout = widgets.Layout(height="600px")

        ############################################################################################
        # Originally the launch button was created inside the impact_variable_input_tab (but is
        # still displayed there). The reason we moved it here is that we want to "disable" the
        # output tabs when the process is running, so that button will have to interact with
        # attributes of the parent tab, this is the reason why it was moved here. It understandably
        # make things a bit more complicated but is seems like it's working.

        dummy_output = widgets.Output()

        def launch_sizing_process(event):

            # "Hide" the output tabs !
            self.impact_variable_input_tab.launch_button_widget.style.button_color = (
                "Red"
            )
            self.children = [self.impact_variable_input_tab]

            # Clear the residuals visualization to make it apparent that a computation is
            # underway.

            residuals_graph = (
                self.impact_variable_input_tab.residuals_visualization_widget.data[0]
            )
            residuals_graph.x = []
            residuals_graph.y = []

            threshold_graph = (
                self.impact_variable_input_tab.residuals_visualization_widget.data[1]
            )
            threshold_graph.x = []
            threshold_graph.y = []

            with dummy_output:

                if not self.impact_variable_input_tab.mdo_selection_widget.value:
                    relative_error, target_residuals = self._launch_mda()

                    # For the display, hte iteration will start at 1 :)
                    iteration_numbers = np.arange(len(relative_error)) + 1

                    residuals_graph.x = iteration_numbers
                    residuals_graph.y = relative_error

                    threshold_graph.x = [1, len(relative_error)]
                    threshold_graph.y = [target_residuals, target_residuals]

                else:
                    _, _ = self._launch_mdo()

                self.impact_variable_input_tab.launch_button_widget.style.button_color = (
                    "LimeGreen"
                )

                self.children = [
                    self.impact_variable_input_tab,
                    self.impact_variable_output_tab,
                    self.impact_variable_wing_geometry_tab,
                    self.impact_variable_aircraft_geometry_tab,
                    self.impact_variable_drag_polar_tab,
                    self.impact_variable_mass_bar_breakdown_tab,
                    self.impact_variable_mass_sun_breakdown_tab,
                    self.impact_variable_payload_range_tab,
                    self.impact_variable_mission_tab,
                ]

        self.impact_variable_input_tab.launch_button_widget.on_click(
            launch_sizing_process
        )

        ############################################################################################

        self.impact_variable_output_tab = ImpactVariableOutputTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_output_tab.layout = widgets.Layout(height="600px")

        self.impact_variable_wing_geometry_tab = ImpactVariableWingGeometryTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_wing_geometry_tab.layout = widgets.Layout(height="600px")

        self.impact_variable_aircraft_geometry_tab = ImpactVariableAircraftGeometryTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_aircraft_geometry_tab.layout = widgets.Layout(
            height="600px"
        )

        self.impact_variable_drag_polar_tab = ImpactVariableDragPolarTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_drag_polar_tab.layout = widgets.Layout(height="600px")

        self.impact_variable_mass_bar_breakdown_tab = ImpactVariableMassBarBreakdownTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_mass_bar_breakdown_tab.layout = widgets.Layout(
            height="600px"
        )

        self.impact_variable_mass_sun_breakdown_tab = ImpactVariableMassSunBreakdownTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_mass_sun_breakdown_tab.layout = widgets.Layout(
            height="600px"
        )

        self.impact_variable_payload_range_tab = ImpactVariablePayloadRangeTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_payload_range_tab.layout = widgets.Layout(height="600px")

        self.impact_variable_mission_tab = ImpactVariableMissionTab(
            working_directory_path=self.working_directory_path
        )
        self.impact_variable_mission_tab.layout = widgets.Layout(height="600px")

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
            self.impact_variable_mission_tab,
        ]

        # Add a title for each tab
        for i, tab_name in enumerate(TABS_NAME):
            self.set_title(i, tab_name)

    def _launch_mdo(self):
        """
        Launches the mdo by reading the design vars, the objective and the constraints from the tab
        and the rest of the input from the reference file except for the sweep which we will fix
        at 30° (M=0.82 which is the max you can enter as the upper bound).

        :return: the residuals at each iterations
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
            self.impact_variable_input_tab.sizing_process_name + "_mdo_input_file.xml",
        )
        new_output_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.impact_variable_input_tab.sizing_process_name
            + "_mdo"
            + OUTPUT_FILE_SUFFIX,
        )

        # Change the input and output file path in the configurator
        configurator.input_file_path = new_input_file_path
        configurator.output_file_path = new_output_file_path

        # Create the input file with the reference value, except for sweep
        new_inputs = copy.deepcopy(self.impact_variable_input_tab.reference_inputs)

        new_inputs["data:geometry:wing:sweep_25"].value = 30.0
        new_inputs["data:geometry:wing:sweep_25"].units = "deg"

        # Save as the new input file. We overwrite always, may need to put a warning for
        # students
        new_inputs.save_as(new_input_file_path, overwrite=True)

        # Get the problem, no need to write inputs. The fact that the reference was created
        # based on the same configuration we will always use should ensure the completion of
        # the input file
        problem = configurator.get_problem(read_inputs=True)

        if self.impact_variable_input_tab.ar_design_var_checkbox.value:

            problem.model.add_design_var(
                name="data:geometry:wing:aspect_ratio",
                lower=self.impact_variable_input_tab.opt_ar_min,
                upper=self.impact_variable_input_tab.opt_ar_max,
            )

        if self.impact_variable_input_tab.sweep_w_design_var_checkbox.value:

            problem.model.add_design_var(
                name="data:geometry:wing:sweep_25",
                units="deg",
                lower=self.impact_variable_input_tab.opt_sweep_w_min,
                upper=self.impact_variable_input_tab.opt_sweep_w_max,
            )

        if (
            self.impact_variable_input_tab.objective_selection_widget.value
            == "Fuel sizing"
        ):
            problem.model.add_objective(
                name="data:mission:sizing:needed_block_fuel", units="kg", scaler=1e-4
            )
        elif self.impact_variable_input_tab.objective_selection_widget.value == "MTOW":
            problem.model.add_objective(
                name="data:weight:aircraft:MTOW", units="kg", scaler=1e-4
            )

        if self.impact_variable_input_tab.wing_span_constraints_checkbox.value:
            problem.model.add_constraint(
                name="data:geometry:wing:span",
                units="m",
                lower=0.0,
                upper=self.impact_variable_input_tab.opt_wing_span_max,
            )

        problem.model.approx_totals()
        problem.setup()
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
            self.impact_variable_input_tab.sizing_process_name
            + "_mdo"
            + FLIGHT_DATA_FILE_SUFFIX,
        )

        # You can't rename to a file which already exists, so if one already exists we
        # delete it before renaming.
        if pth.exists(new_mission_data_file_path):
            os.remove(new_mission_data_file_path)

        os.rename(old_mission_data_file_path, new_mission_data_file_path)

        return [0.0, 0.0], [1.0, 1.0]

    def _launch_mda(self):
        """
        Launches the mda by reading the inputs from the proper tab and extract the value for the
        graph of interest (in this case the residuals and the target residuals)

        :return: the residuals at each iterations
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
            self.impact_variable_input_tab.sizing_process_name + "_input_file.xml",
        )
        new_output_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.impact_variable_input_tab.sizing_process_name + OUTPUT_FILE_SUFFIX,
        )

        # Change the input and output file path in the configurator
        configurator.input_file_path = new_input_file_path
        configurator.output_file_path = new_output_file_path

        # Create the input file with the current value
        new_inputs = copy.deepcopy(self.impact_variable_input_tab.reference_inputs)

        # No need to provide list or numpy array for scalar values.
        new_inputs["data:TLAR:NPAX"].value = self.impact_variable_input_tab.n_pax

        new_inputs[
            "data:TLAR:approach_speed"
        ].value = self.impact_variable_input_tab.v_app
        new_inputs["data:TLAR:approach_speed"].units = "kn"  # Unit from the widget

        # If the Mach get too high and because we originally didn't plan on changing sweep,
        # the compressibility drag might get too high causing the code to not converge ! We
        # will thus adapt the sweep based on the mach number with a message to let the
        # student know about it. We'll keep the product M_cr * cos(phi_25) constant at the
        # value obtain with M_cr = 0.78 and phi_25 = 24.54 deg
        if self.impact_variable_input_tab.cruise_mach > 0.78:
            cos_phi_25 = (
                0.78
                / self.impact_variable_input_tab.cruise_mach
                * np.cos(np.deg2rad(24.54))
            )
            phi_25 = np.arccos(cos_phi_25)
            new_inputs["data:geometry:wing:sweep_25"].value = phi_25
            new_inputs["data:geometry:wing:sweep_25"].units = "rad"

        new_inputs[
            "data:TLAR:cruise_mach"
        ].value = self.impact_variable_input_tab.cruise_mach

        new_inputs["data:TLAR:range"].value = self.impact_variable_input_tab.range
        new_inputs["data:TLAR:range"].units = "NM"  # Unit from the widget

        new_inputs[
            "data:weight:aircraft:payload"
        ].value = self.impact_variable_input_tab.payload
        new_inputs["data:weight:aircraft:payload"].units = "kg"  # Unit from the widget

        new_inputs[
            "data:weight:aircraft:max_payload"
        ].value = self.impact_variable_input_tab.max_payload
        new_inputs[
            "data:weight:aircraft:max_payload"
        ].units = "kg"  # Unit from the widget

        new_inputs[
            "data:geometry:wing:aspect_ratio"
        ].value = self.impact_variable_input_tab.wing_aspect_ratio

        new_inputs[
            "data:propulsion:rubber_engine:bypass_ratio"
        ].value = self.impact_variable_input_tab.bpr
        # Save as the new input file. We overwrite always, may need to put a warning for
        # students
        new_inputs.save_as(new_input_file_path, overwrite=True)

        # Get the problem, no need to write inputs. The fact that the reference was created
        # based on the same configuration we will always use should ensure the completion of
        # the input file
        problem = configurator.get_problem(read_inputs=True)
        problem.setup()

        # Save target residuals
        target_residuals = problem.model.nonlinear_solver.options["rtol"]

        model = problem.model
        recorder_database_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.impact_variable_input_tab.sizing_process_name + "_cases.sql",
        )
        recorder = om.SqliteRecorder(recorder_database_file_path)
        model.nonlinear_solver.add_recorder(recorder)
        model.nonlinear_solver.recording_options["record_solver_residuals"] = True

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
            self.impact_variable_input_tab.sizing_process_name
            + FLIGHT_DATA_FILE_SUFFIX,
        )

        # You can't rename to a file which already exists, so if one already exists we
        # delete it before renaming.
        if pth.exists(new_mission_data_file_path):
            os.remove(new_mission_data_file_path)

        os.rename(old_mission_data_file_path, new_mission_data_file_path)

        # Extract the residuals, build a scatter based on them and plot them along with the
        # threshold set in the configuration file
        relative_error = np.array(
            extract_residuals(recorder_database_file_path=recorder_database_file_path)
        )

        return relative_error, target_residuals


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


def extract_residuals(recorder_database_file_path: str) -> list:
    """
    From the file path to a recorder data base, extract the value of the relative error of the
    residuals at each iteration.

    :param recorder_database_file_path: absolute path to the recorder database
    :return: an array containing the value of the relative error at each iteration
    """

    case_reader = om.CaseReader(recorder_database_file_path)

    # Will only work if the recorder was attached to the base solver
    solver_cases = case_reader.get_cases("root.nonlinear_solver")

    relative_error = []

    for _, case in enumerate(solver_cases):

        relative_error.append(case.rel_err)

    return relative_error
