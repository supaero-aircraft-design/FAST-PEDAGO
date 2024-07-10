import numpy as np
import shutil
import os
from time import sleep
from threading import Event

import openmdao as om


class ResidualsObjectivesPlotter:
    def __init__(self, graph, **kwargs):
        """
        :param graph: The ProcessGraphContainer
            on which to plot the residuals and objectives.
        """
        super().__init__(**kwargs)

        self.graph = graph

        # Target residuals have to be set to plot MDA
        self.target_residuals = None

    def plot(
        self,
        process_ended: Event,
        recorder_database_file_path: str,
        is_MDO: bool = False,
    ):
        """
        Plots the relative error of each iteration during MDA process, and the
        relative error threshold (The threshold 'target_residuals' have to be
        set externally after configuring MDA), or plots the objectives of each
        iteration and the minimum objective reached during an MDO process.
        This method is made to be used in a separated thread from the main
        MDA/MDO process

        :param process_ended: event triggered after the MDA/MDO process ends
        :param recorder_database_file_path: path of the database used to store
            process data
        :param is_MDA: boolean indicating if the program should plot
            objectives (MDO) or residuals (MDA)
        """

        temp_recorder_database_file_path = recorder_database_file_path.replace(
            "_cases.sql",
            "_temp_cases.sql",
        )

        while not process_ended.is_set():
            sleep(0.1)

            try:
                # Copy the db file before reading it to avoid reading when an
                # other thread is writing, which could cause the code to fail.
                shutil.copyfile(
                    recorder_database_file_path, temp_recorder_database_file_path
                )

                if not is_MDO:
                    # Extract the residuals, build a scatter based on them and
                    # plot them along with the threshold set in the
                    # configuration file
                    iterations, relative_error = np.array(
                        self._extract_residuals(
                            recorder_database_file_path=temp_recorder_database_file_path
                        )
                    )
                    # If the target residuals haven't been set by the mda
                    # launcher, nothing will be plotted
                    self.graph.plot(iterations, relative_error, self.target_residuals)

                else:
                    # Extract the residuals, build a scatter based on them and
                    # plot them along with the threshold set in the
                    # configuration file
                    iterations, objective = np.array(
                        self._extract_objective(
                            recorder_database_file_path=temp_recorder_database_file_path
                        )
                    )
                    min_objective = min(objective)

                    self.graph.plot(iterations, objective, min_objective)

            except Exception:
                pass

        os.remove(temp_recorder_database_file_path)

    def _extract_residuals(recorder_database_file_path: str) -> list:
        """
        From the file path to a recorder data base, extract the value of the
        relative error of the residuals at each iteration.

        :param recorder_database_file_path: absolute path to the recorder database
        :return: two arrays containing the iterations and the associated values of
            the relative error.
        """

        case_reader = om.CaseReader(recorder_database_file_path)

        # Will only work if the recorder was attached to the base solver
        solver_cases = case_reader.list_cases("root.nonlinear_solver")

        # For the display, first iteration will be 1
        iterations, relative_error = zip(
            *[
                (i + 1, case_reader.get_case(case_id).rel_err)
                for i, case_id in enumerate(solver_cases)
            ]
        )

        return iterations, relative_error

    def _extract_objective(recorder_database_file_path: str) -> list:
        """
        From the file path to a recorder data base, extract the value of the
        objective at each iteration of the driver.

        :param recorder_database_file_path: absolute path to the recorder database
        :return: an array containing the iterations and the associated values of
            the objective.
        """

        case_reader = om.CaseReader(recorder_database_file_path)

        # Will only work if the recorder was attached to the base solver
        solver_cases = case_reader.list_cases("driver")

        # For the display, first iteration will be 1
        iterations, objective = zip(
            *[
                (
                    i + 1,
                    float(
                        list(case_reader.get_case(case_id).get_objectives().values())[0]
                    ),
                )
                for i, case_id in enumerate(solver_cases)
            ]
        )

        return iterations, objective
