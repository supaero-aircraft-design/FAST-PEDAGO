import numpy as np
import shutil
import os
from time import sleep
from threading import Event

from fast_pedago.utils import (
    _extract_objective,
    _extract_residuals,
)


class ProcessPlotter:
    """
    Recovers process data from .sql file and provides data to plot.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Target residuals have to be set to plot MDA
        self.target_residuals = None

        # graph to plot on, with a plot function.
        self.figure = None

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
                    self.iterations, self.relative_error = np.array(
                        _extract_residuals(
                            recorder_database_file_path=temp_recorder_database_file_path
                        )
                    )

                    if self.figure:
                        # If the target residuals haven't been set by the mda
                        # launcher, nothing will be plotted
                        self.figure.plot(
                            self.iterations, self.relative_error, self.target_residuals
                        )

                else:
                    # Extract the residuals, build a scatter based on them and
                    # plot them along with the threshold set in the
                    # configuration file
                    self.iterations, self.objective = np.array(
                        _extract_objective(
                            recorder_database_file_path=temp_recorder_database_file_path
                        )
                    )
                    self.min_objective = min(self.objective)

                    if self.figure:
                        self.figure.plot(
                            self.iterations, self.objective, self.min_objective
                        )

            except Exception:
                pass

        os.remove(temp_recorder_database_file_path)
