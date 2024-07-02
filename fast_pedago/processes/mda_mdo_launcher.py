
import os
import os.path as pth

import numpy as np

from threading import Thread, Event
from time import sleep

import copy
import warnings

import openmdao.api as om

import fastoad.api as oad

from . import ResidualsObjectivesPlotter
from .path_manager import PathManager
from fast_pedago.objects.paths import (
    MDA_FILE_SUFFIX,
    MDO_FILE_SUFFIX,
    INPUT_FILE_SUFFIX,
    OUTPUT_FILE_SUFFIX,
    FLIGHT_DATA_FILE_SUFFIX,
    RECORDER_FILE_SUFFIX,
    DEFAULT_PROCESS_NAME,
)


class MDAMDOLauncher():
    def __init__(self,
            plotter: ResidualsObjectivesPlotter,
            **kwargs):
        """
        :param plotter: the ResidualsObjectivesPlotter to plot with.
        """
        super().__init__(**kwargs)

        self.process_name = DEFAULT_PROCESS_NAME
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
        """
        Create a new FAST-OAD problem based on the reference configuration file.
        Sets the paths to inputs/outputs files.
        The files names and the configuration depend on the type of process.
        
        :param is_MDO: true if the process is a MDO.
        """
        if is_MDO:
            problem_type = MDO_FILE_SUFFIX
            self.configurator = oad.FASTOADProblemConfigurator(PathManager.mdo_configuration_file_path)
        else :
            problem_type = MDA_FILE_SUFFIX
            self.configurator = oad.FASTOADProblemConfigurator(PathManager.mda_configuration_file_path)
        
        # Save orig file path and name so that we can replace them with the optim process
        # name
        orig_input_file_path = self.configurator.input_file_path
        orig_input_file_name = pth.basename(orig_input_file_path)
        orig_output_file_path = self.configurator.output_file_path
        orig_output_file_name = pth.basename(orig_output_file_path)
        
        # Save inputs and outputs file paths
        self.new_input_file_path = orig_input_file_path.replace(
            orig_input_file_name,
            self.process_name + problem_type + INPUT_FILE_SUFFIX,
        )
        self.new_output_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.process_name + problem_type + OUTPUT_FILE_SUFFIX,
        )

        # Change the input and output file path in the configurator
        self.configurator.input_file_path = self.new_input_file_path
        self.configurator.output_file_path = self.new_output_file_path

        # The recorder file path is declared with "self" to be able to retrieve
        # it from the plot function in an other thread. There might be better
        # ways to pass it from a thread to an other.
        self.recorder_database_file_path = orig_output_file_path.replace(
            orig_output_file_name,
            self.process_name + problem_type + RECORDER_FILE_SUFFIX,
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
            self.process_name + problem_type + FLIGHT_DATA_FILE_SUFFIX,
        )


    def _configure_mdo(self) :
        """
        Sets the MDO problem and the design variables, objective and constraints, 
        with the reference MDO configuration.
        """
        # Create the input file with the reference value, except for sweep
        new_inputs = copy.deepcopy(self.reference_inputs)
        # Save as the new input file. We overwrite always, may need to put a warning for
        # students
        new_inputs.save_as(self.new_input_file_path, overwrite=True)

        # Get the problem, no need to write inputs. The fact that the reference was created
        # based on the same configuration we will always use should ensure the completion of
        # the input file
        self.problem = self.configurator.get_problem(read_inputs=True)
        
        # The objective is found using the v-model of the button group
        # 0: fuel sizing, 1: MTOW, 2: OWE
        if self.objective == 0:
            objective_name = "data:mission:sizing:block_fuel"
        elif self.objective == 1:
            objective_name = "data:weight:aircraft:MTOW"
        else:
            objective_name = "data:weight:aircraft:OWE"

        self.problem.model.add_objective(
                name=objective_name,
                units="kg",
                scaler=1e-4,
            )

        if self.is_aspect_ratio_design_variable:
            self.problem.model.add_design_var(
                name="data:geometry:wing:aspect_ratio",
                lower=self.aspect_ratio_lower_bound,
                upper=self.aspect_ratio_upper_bound,
            )

        if self.is_wing_sweep_design_variable:
            self.problem.model.add_design_var(
                name="data:geometry:wing:sweep_25",
                units="deg",
                lower=self.wing_sweep_lower_bound,
                upper=self.wing_sweep_upper_bound,
            )

        if self.is_wing_span_constrained:
            self.problem.model.add_constraint(
                name="data:geometry:wing:span",
                units="m",
                lower=0.0,
                upper=self.wing_span_upper_bound,
            )
            
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


    def _configure_mda(self) -> float:
        """
        Sets the MDA problem and all the user inputs, with the reference MDA configuration
        
        :return the targeted residual to achieve MDA convergence
        """
        # Create the input file with the current value
        new_inputs = copy.deepcopy(self.reference_inputs)

        # No need to provide list or numpy array for scalar values.
        new_inputs["data:TLAR:NPAX"].value = self.n_pax

        new_inputs["data:TLAR:approach_speed"].value = self.v_app
        new_inputs["data:TLAR:approach_speed"].units = "kn"  # Unit from the widget

        # If the Mach get too high and because we originally didn't plan on changing sweep,
        # the compressibility drag might get too high causing the code to not converge ! We
        # will thus adapt the sweep based on the mach number with a message to let the
        # student know about it. We'll keep the product M_cr * cos(phi_25) constant at the
        # value obtain with M_cr = 0.78 and phi_25 = 24.54 deg
        if self.cruise_mach > 0.78:
            cos_phi_25 = (
                0.78
                / self.cruise_mach
                * np.cos(np.deg2rad(24.54))
            )
            phi_25 = np.arccos(cos_phi_25)
            new_inputs["data:geometry:wing:sweep_25"].value = phi_25
            new_inputs["data:geometry:wing:sweep_25"].units = "rad"

        new_inputs["data:TLAR:cruise_mach"].value = self.cruise_mach

        new_inputs["data:TLAR:range"].value = self.range
        new_inputs["data:TLAR:range"].units = "NM"  # Unit from the widget

        new_inputs["data:weight:aircraft:payload"].value = self.payload
        new_inputs["data:weight:aircraft:payload"].units = "kg"  # Unit from the widget

        new_inputs["data:weight:aircraft:max_payload"].value = self.max_payload
        new_inputs["data:weight:aircraft:max_payload"].units = "kg"  # Unit from the widget

        new_inputs[ "data:geometry:wing:aspect_ratio"].value = self.wing_aspect_ratio

        new_inputs["data:propulsion:rubber_engine:bypass_ratio"].value = self.bypass_ratio

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
        
        :param is_MDO: runs the driver if MDO, and the model if MDA.
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

    
    def set_mdo_inputs(
        self,
        objective: int,
        is_aspect_ratio_design_variable: bool,
        aspect_ratio_lower_bound: float,
        aspect_ratio_upper_bound: float,
        is_wing_sweep_design_variable: bool,
        wing_sweep_lower_bound: float,
        wing_sweep_upper_bound: float,
        is_wing_span_constrained: bool,
        wing_span_upper_bound: float,
        ):
        """
        Sets the MDO inputs as variables to use it later in in the MDO configuration function.
        """
        self.objective = objective
        self.is_aspect_ratio_design_variable = is_aspect_ratio_design_variable
        self.aspect_ratio_lower_bound = aspect_ratio_lower_bound
        self.aspect_ratio_upper_bound = aspect_ratio_upper_bound
        self.is_wing_sweep_design_variable = is_wing_sweep_design_variable
        self.wing_sweep_lower_bound = wing_sweep_lower_bound
        self.wing_sweep_upper_bound = wing_sweep_upper_bound
        self.is_wing_span_constrained = is_wing_span_constrained
        self.wing_span_upper_bound = wing_span_upper_bound


    def set_mda_inputs(
        self,
        n_pax: int,
        v_app: float,
        cruise_mach: float,
        range: float,
        payload: float,
        max_payload: float,
        wing_aspect_ratio: float,
        bypass_ratio: float,
        ):
        """
        Sets the MDA inputs as variables to use it later in in the MDA configuration function.
        """
        self.n_pax = n_pax
        self.v_app = v_app
        self.cruise_mach = cruise_mach
        self.range = range
        self.payload = payload
        self.max_payload = max_payload
        self.wing_aspect_ratio = wing_aspect_ratio
        self.bypass_ratio = bypass_ratio


    def get_reference_inputs(self, source_data_file_name: str):
        """
        Takes the inputs from the source file

        :param source_data_file_name: the source file name (with spaces and without extension)
        :return a list of int or float inputs from the source file
        """
        # Read the source data file
        source_data_file_path = PathManager.to_full_source_file_name(source_data_file_name)
        self.reference_inputs = oad.DataFile(source_data_file_path)
        
        n_pax = self.reference_inputs["data:TLAR:NPAX"].value[0]
        v_app = om.convert_units(
            self.reference_inputs["data:TLAR:approach_speed"].value[0],
            self.reference_inputs["data:TLAR:approach_speed"].units,
            "kn",
        )
        cruise_mach = self.reference_inputs["data:TLAR:cruise_mach"].value[0]
        range = om.convert_units(
            self.reference_inputs["data:TLAR:range"].value[0],
            self.reference_inputs["data:TLAR:range"].units,
            "NM",
        )
        payload = om.convert_units(
            self.reference_inputs["data:weight:aircraft:payload"].value[0],
            self.reference_inputs["data:weight:aircraft:payload"].units,
            "kg",
        )
        max_payload = om.convert_units(
            self.reference_inputs["data:weight:aircraft:max_payload"].value[0],
            self.reference_inputs["data:weight:aircraft:max_payload"].units,
            "kg",
        )
        wing_aspect_ratio = self.reference_inputs["data:geometry:wing:aspect_ratio"].value[0]
        bypass_ratio = self.reference_inputs["data:propulsion:rubber_engine:bypass_ratio"].value[0]

        return  n_pax, v_app, cruise_mach, range, payload, max_payload, wing_aspect_ratio, bypass_ratio