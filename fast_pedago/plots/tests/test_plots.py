import os
import pathlib

from ..functions.wing import _wing_plot

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"
DATA_FOLDER_PATH = pathlib.Path(__file__).parent / "data"


def test_detailed_wing_plot():

    datafile_path = DATA_FOLDER_PATH / "reference_aircraft_output_file.xml"

    fig = _wing_plot(datafile_path)
    fig.show()
