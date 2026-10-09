import pathlib
from shutil import rmtree

import fastoad.api as oad
import pytest

RESULTS_FOLDER_PATH = pathlib.Path(__file__).parent / "results"
SOURCE_DATA_FILES_FOLDER_PATH = pathlib.Path(__file__).parent.parent / "source_data_files"
CONFIGURATION_FILE_FOLDER_PATH = pathlib.Path(__file__).parent.parent / "configuration"


@pytest.fixture(scope="module")
def cleanup():
    """Empties results folder to avoid any conflicts."""
    rmtree(RESULTS_FOLDER_PATH, ignore_errors=True)
    yield
    rmtree(RESULTS_FOLDER_PATH, ignore_errors=True)


def test_a321_like(cleanup):

    configurator = oad.FASTOADProblemConfigurator(
        CONFIGURATION_FILE_FOLDER_PATH / "oad_sizing_sensitivity_analysis.yml"
    )
    ref_inputs = SOURCE_DATA_FILES_FOLDER_PATH / "A321_like_source_data_file.xml"

    problem = configurator.get_problem()

    # To not alter original files
    problem.input_file_path = RESULTS_FOLDER_PATH / "tmp_in.xml"
    problem.output_file_path = RESULTS_FOLDER_PATH / "tmp_out.xml"

    problem.write_needed_inputs(ref_inputs)
    problem.read_inputs()
    problem.setup()
    problem.run_model()
    problem.write_outputs()

    assert problem.get_val("data:weight:aircraft:MTOW", units="kg") == pytest.approx(
        103279.0, abs=1.0
    )
    assert problem.get_val("data:weight:aircraft:OWE", units="kg") == pytest.approx(
        56348.0, abs=1.0
    )
    assert problem.get_val(
        "data:weight:aircraft:sizing_onboard_fuel_at_input_weight", units="kg"
    ) == pytest.approx(21930.0, abs=1.0)


def test_a350_like(cleanup):

    configurator = oad.FASTOADProblemConfigurator(
        CONFIGURATION_FILE_FOLDER_PATH / "oad_sizing_sensitivity_analysis.yml"
    )
    ref_inputs = SOURCE_DATA_FILES_FOLDER_PATH / "A350_like_source_data_file.xml"

    problem = configurator.get_problem()

    # To not alter original files
    problem.input_file_path = RESULTS_FOLDER_PATH / "tmp_in.xml"
    problem.output_file_path = RESULTS_FOLDER_PATH / "tmp_out.xml"

    problem.write_needed_inputs(ref_inputs)
    problem.read_inputs()
    problem.setup()
    problem.run_model()
    problem.write_outputs()

    assert problem.get_val("data:weight:aircraft:MTOW", units="kg") == pytest.approx(
        303235.0, abs=1.0
    )
    assert problem.get_val("data:weight:aircraft:OWE", units="kg") == pytest.approx(
        148088.0, abs=1.0
    )
    assert problem.get_val(
        "data:weight:aircraft:sizing_onboard_fuel_at_input_weight", units="kg"
    ) == pytest.approx(101146.0, abs=1.0)


def test_ceras(cleanup):

    configurator = oad.FASTOADProblemConfigurator(
        CONFIGURATION_FILE_FOLDER_PATH / "oad_sizing_sensitivity_analysis.yml"
    )
    ref_inputs = SOURCE_DATA_FILES_FOLDER_PATH / "CeRAS01_source_data_file.xml"

    problem = configurator.get_problem()

    # To not alter original files
    problem.input_file_path = RESULTS_FOLDER_PATH / "tmp_in.xml"
    problem.output_file_path = RESULTS_FOLDER_PATH / "tmp_out.xml"

    problem.write_needed_inputs(ref_inputs)
    problem.read_inputs()
    problem.setup()
    problem.run_model()
    problem.write_outputs()

    assert problem.get_val("data:weight:aircraft:MTOW", units="kg") == pytest.approx(
        78393.0, abs=1.0
    )
    assert problem.get_val("data:weight:aircraft:OWE", units="kg") == pytest.approx(
        43502.0, abs=1.0
    )
    assert problem.get_val(
        "data:weight:aircraft:sizing_onboard_fuel_at_input_weight", units="kg"
    ) == pytest.approx(21283.0, abs=1.0)


def test_reference(cleanup):

    configurator = oad.FASTOADProblemConfigurator(
        CONFIGURATION_FILE_FOLDER_PATH / "oad_sizing_sensitivity_analysis.yml"
    )
    ref_inputs = SOURCE_DATA_FILES_FOLDER_PATH / "reference_aircraft_source_data_file.xml"

    problem = configurator.get_problem()

    # To not alter original files
    problem.input_file_path = RESULTS_FOLDER_PATH / "tmp_in.xml"
    problem.output_file_path = RESULTS_FOLDER_PATH / "tmp_out.xml"

    problem.write_needed_inputs(ref_inputs)
    problem.read_inputs()
    problem.setup()
    problem.run_model()
    problem.write_outputs()

    assert problem.get_val("data:weight:aircraft:MTOW", units="kg") == pytest.approx(
        110780.0, abs=1.0
    )
    assert problem.get_val("data:weight:aircraft:OWE", units="kg") == pytest.approx(
        61892.0, abs=1.0
    )
    assert problem.get_val(
        "data:weight:aircraft:sizing_onboard_fuel_at_input_weight", units="kg"
    ) == pytest.approx(30887.0, abs=1.0)


def test_optimization():

    configurator = oad.FASTOADProblemConfigurator(
        CONFIGURATION_FILE_FOLDER_PATH / "oad_optim_sensitivity_analysis.yml"
    )
    ref_inputs = SOURCE_DATA_FILES_FOLDER_PATH / "reference_aircraft_source_data_file.xml"

    problem = configurator.get_problem()

    # To not alter original files
    problem.input_file_path = RESULTS_FOLDER_PATH / "tmp_optim_in.xml"
    problem.output_file_path = RESULTS_FOLDER_PATH / "tmp_optim_out.xml"

    problem.write_needed_inputs(ref_inputs)
    problem.read_inputs()
    problem.model.approx_totals()

    problem.model.add_design_var(
        name="data:geometry:wing:aspect_ratio",
        units="unitless",
        lower=5.0,
        upper=20.0,
    )
    problem.model.add_design_var(
        name="data:geometry:wing:sweep_25",
        units="deg",
        lower=0.0,
        upper=50.0,
    )
    problem.model.add_objective(name="data:weight:aircraft:MTOW", units="kg", scaler=1e-4)

    problem.setup()
    problem.run_driver()
    problem.write_outputs()

    assert problem.get_val("data:weight:aircraft:MTOW", units="kg") == pytest.approx(
        104468.0, abs=1.0
    )
    assert problem.get_val("data:weight:aircraft:OWE", units="kg") == pytest.approx(
        54417.0, abs=1.0
    )
    assert problem.get_val(
        "data:weight:aircraft:sizing_onboard_fuel_at_input_weight", units="kg"
    ) == pytest.approx(32051.0, abs=1.0)
