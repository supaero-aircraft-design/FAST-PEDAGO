from typing import Union

import numpy as np
import shutil

from os import PathLike
from pathlib import Path

from time import sleep
from threading import Event

from fast_pedago.utils import (
    _extract_objective,
    _extract_residuals,
    RECORDER_FILE_SUFFIX,
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
        recorder_database_file_path: Union[str, PathLike],
        is_MDO: bool = False,
        aircraft_name: str = None,
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
        :param aircraft_name: name of the aircraft to plot, if it contains green
            the plot will be green
        """

        temp_recorder_database_file_path = str(recorder_database_file_path).replace(
            RECORDER_FILE_SUFFIX,
            "_temp" + RECORDER_FILE_SUFFIX,
        )

        is_aircraft_green = (
            "green" in aircraft_name.lower() or "vert" in aircraft_name.lower()
        )

        main = None
        if is_MDO:
            limit = None
        else:
            # If the target residuals haven't been set by the mda
            # launcher, nothing will be plotted
            limit = self.target_residuals
        iterations = None

        while not process_ended.is_set():
            sleep(0.1)
            try:
                # Copy the db file before reading it to avoid reading when an
                # other thread is writing, which could cause the code to fail.
                shutil.copyfile(
                    recorder_database_file_path, temp_recorder_database_file_path
                )

                if not is_MDO:
                    # Here "main" is the residuals.
                    iterations, main = np.array(
                        _extract_residuals(
                            recorder_database_file_path=temp_recorder_database_file_path
                        )
                    )

                else:
                    # Here "main" is the objective
                    iterations, main = np.array(
                        _extract_objective(
                            recorder_database_file_path=temp_recorder_database_file_path
                        )
                    )

                if self.figure:
                    self.figure.plot(iterations, main, limit, is_aircraft_green)

            except Exception:
                pass

        # Plot the min objective reached after the end of the process only
        if is_MDO:
            limit = min(main)
            if self.figure:
                self.figure.plot(iterations, main, limit, is_aircraft_green)

        Path.unlink(Path(temp_recorder_database_file_path))
