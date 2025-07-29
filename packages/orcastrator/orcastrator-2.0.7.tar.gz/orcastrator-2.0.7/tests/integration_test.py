import shutil
from pathlib import Path

import pytest

from orcastrator.runner_logic.pipeline_runner import PipelineRunner

# Define paths for the test
TEST_CONFIG_FILE = Path("/Users/freddy/Documents/Projects/orcastrator/tests/test.toml")
MOLECULES_DIR = Path("/Users/freddy/Documents/Projects/orcastrator/tests/molecules")
OUTPUT_DIR = Path("tests/test_scratch")


@pytest.fixture(scope="function")
def clean_output_dir():
    """Fixture to clean up the output directory before and after each test."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    yield
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)


def test_pipeline_runner_integration(clean_output_dir):
    """Integration test for the PipelineRunner."""
    # Initialize the pipeline runner with the test configuration
    runner = PipelineRunner.from_config_file(TEST_CONFIG_FILE)

    # Load molecules
    runner.load_molecules()
    assert len(runner.molecules) > 0, "No molecules were loaded for the test."

    # Run the pipeline
    stats = runner.run()

    # Assertions
    assert len(stats.molecules) > 0, "No molecules were processed."
    assert len(stats.successful_molecules) > 0, (
        "No molecules were successfully processed."
    )
    assert len(stats.failed_molecules) == 0, "Some molecules failed to process."

    # Verify output files
    for molecule in runner.molecules:
        molecule_output_dir = OUTPUT_DIR / molecule.name
        print(molecule_output_dir)
        print(molecule_output_dir.resolve())
        assert molecule_output_dir.exists(), (
            f"Output directory for {molecule.name} does not exist."
        )
        for step in runner.config["step"]:
            step_output_dir = molecule_output_dir / step["name"]
            assert step_output_dir.exists(), (
                f"Step directory {step['name']} for {molecule.name} does not exist."
            )
            input_file = step_output_dir / f"{step_output_dir.name}.inp"
            output_file = step_output_dir / f"{step_output_dir.name}.out"
            assert input_file.exists(), (
                f"Input file for step {step['name']} does not exist."
            )
            assert output_file.exists(), (
                f"Output file for step {step['name']} does not exist."
            )
