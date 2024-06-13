
import os
import os.path as pth

from threading import Thread, Event
from time import sleep

import copy
import warnings

import openmdao.api as om

import fastoad.api as oad

from . import ResidualsObjectivesPlotter
from fast_pedago.gui import InputsContainer
from fast_pedago.utils import (
    OUTPUT_FILE_SUFFIX,
    FLIGHT_DATA_FILE_SUFFIX,
)


MDA_FILE = "_mda"
MDO_FILE = "_mdo"


class MDAMDOLauncher():
    def __init__(self, 
            mda_configuration_file_path: str, 
            mdo_configuration_file_path: str, 
            inputs: InputsContainer,
            plotter: ResidualsObjectivesPlotter, 
            **kwargs):
        """
        :param mda_configuration_file_path: the path to MDA configuration.
        :param mdo_configuration_file_path: the path to MDA configuration.
        :param inputs: The inputs container in which the user put the inputs.
        :param plotter: the ResidualsObjectivesPlotter to plot with.
        """
        super().__init__(**kwargs)
        
        self.mda_configuration_file_path = mda_configuration_file_path
        self.mdo_configuration_file_path = mdo_configuration_file_path
        self.inputs = inputs
        self.plotter = plotter


    def launch_processes(self, is_MDO: bool=False):
        """
        Launches the chosen process (MDA or MDO), and launches
        the plot of residuals or objectives depending on the main 
        process.
        
        :param is_MDO: defines if the process is MDO or MDA
            to launch the correct process
        """
        # Initialize event to synchronize the process thread and the plotting thread
        process_ended = Event()
        
        self._configure_paths(is_MDO)

        # If the switch is off, MDA, else MDO
        if is_MDO:
            self._configure_mdo()
        else:
            # Sets the residuals plotter target_residuals attribute after
            # configuring the MDA
            self.plotter.target_residuals = self._configure_mda()
            
        
        process_thread = Thread(target=self._run_problem, 
            args=(is_MDO,),
        )
        plotting_thread = Thread(target=self.plotter.plot, 
            args=(process_ended, self.recorder_database_file_path, is_MDO),
        )
        
        process_thread.start()
        plotting_thread.start()
        
        process_thread.join()
        # This line is to make sure the plotting ends after the process and plots everything
        sleep(1)
        process_ended.set()
        plotting_thread.join()


    def _configure_paths(self, is_MDO: bool=False):
        # Create a new FAST-OAD problem based on the reference configuration file
        if is_MDO:
            problem_type = MDO_FILE
            self.configurator = oad.FASTOADProblemConfigurator(self.mdo_configuration_file_path)
        else :
            problem_type = MDA_FILE
            self.configurator = oad.FASTOADProblemConfigurator(self.mda_configuration_file_path)
        
        # Save orig file path and name so that we can replace them with the optim process
        # name
        orig_input_file_path = self.configurator.input_file_path
        orig_input_file_name = pth.basename(orig_input_file_path)
        orig_output_file_path = self.configurator.output_file_path
        orig_output_file_name = pth.basename(orig_output_file_path)
        
        # Save inputs and outputs file paths
        self.new_input_file_path = orig_input_file_path.replace(
            orig_input_file_name,
            self.inputs.process_name + problem_type + "_input_file.xml",
        )
        self.new_output_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.inputs.process_name + problem_type + OUTPUT_FILE_SUFFIX,
        )

        # Change the input and output file path in the configurator
        self.configurator.input_file_path = self.new_input_file_path
        self.configurator.output_file_path = self.new_output_file_path

        # The recorder file path is declared with "self" to be able to retrieve
        # it from the plot function in an other thread. There might be better
        # ways to pass it from a thread to an other.
        self.recorder_database_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.inputs.process_name + problem_type + "_cases.sql",
        )
        
        # We also need to rename the .csv file which contains the mission data. I don't
        # see a proper way to do it other than that since it is something INSIDE the
        # configuration file which we can't overwrite like the input and output file
        # path. There may be a way to do it by modifying the options of the performances
        # components of the problem but it seems too much
        self.old_mission_data_file_path = orig_output_file_path.replace(
            orig_output_file_name, "flight_points.csv"
        )
        self.new_mission_data_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.inputs.process_name + problem_type + FLIGHT_DATA_FILE_SUFFIX,
        )


    def _configure_mdo(self) :
        # Create the input file with the reference value, except for sweep
        new_inputs = copy.deepcopy(self.inputs.reference_inputs)
        # Save as the new input file. We overwrite always, may need to put a warning for
        # students
        new_inputs.save_as(self.new_input_file_path, overwrite=True)

        self.problem = self.inputs.retrieve_mdo_inputs(self.configurator)
        self.problem.model.approx_totals()
        self.problem.setup()

        # Ran the case with the proper mission and go those coefficient
        self.problem.set_val(
            name="settings:mission:sizing:breguet:climb:mass_ratio", val=0.975
        )
        self.problem.set_val(
            name="settings:mission:sizing:breguet:descent:mass_ratio", val=0.993
        )
        self.problem.set_val(
            name="settings:mission:sizing:breguet:reserve:mass_ratio", val=0.055
        )

        driver = self.problem.driver
        
        self.recorder = om.SqliteRecorder(self.recorder_database_file_path)
        driver.add_recorder(self.recorder)
        driver.recording_options["record_objectives"] = True


    def _configure_mda(self) -> str:
        
        new_inputs = self.inputs.retrieve_mda_inputs()

        # Save as the new input file. We overwrite always, may need to put a warning for
        # students
        new_inputs.save_as(self.new_input_file_path, overwrite=True)

        # Get the problem, no need to write inputs. The fact that the reference was created
        # based on the same configuration we will always use should ensure the completion of
        # the input file
        self.problem = self.configurator.get_problem(read_inputs=True)
        self.problem.setup()

        # Save target residuals
        # The "target_residuals" and recorder file path are declared with "self" 
        # to be able to retrieve them from the plot function in an other thread. 
        # There might be better ways to pass them from a thread to an other.
        target_residuals = self.problem.model.nonlinear_solver.options["rtol"]

        model = self.problem.model
        
        self.recorder = om.SqliteRecorder(self.recorder_database_file_path)
        model.nonlinear_solver.add_recorder(self.recorder)
        model.nonlinear_solver.recording_options["record_solver_residuals"] = True
        
        return target_residuals


    def _run_problem(self, is_MDO: bool=False):
        """
        Runs the MDA or MDO pre-configured problem, and finish by
        renaming the mission data file and closing the problem recorder.
        """
        if is_MDO:
            self.problem.run_driver()
        else:
            # Run the problem and write output. Catch warning for cleaner interface
            with warnings.catch_warnings():
                warnings.simplefilter(action="ignore", category=FutureWarning)
                self.problem.run_model()

        self.problem.write_outputs()

        # You can't rename to a file which already exists, so if one already exists we
        # delete it before renaming.
        if pth.exists(self.new_mission_data_file_path):
            os.remove(self.new_mission_data_file_path)

        os.rename(self.old_mission_data_file_path, self.new_mission_data_file_path)

        # Shut down the recorder so we can delete the .sql file later
        self.recorder.shutdown()