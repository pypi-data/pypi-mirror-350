import logging
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

import click

from orcastrator import __version__
from orcastrator.config import load_config
from orcastrator.logger import (
    clear_context,
    configure_from_config,
    debug,
    error,
    info,
    setup_file_logging,
    warning,
)
from orcastrator.runner_logic import PipelineRunner
from orcastrator.slurm import SlurmConfig


@click.group()
@click.version_option(version=__version__, prog_name="orcastrator")
def cli():
    """Orcastrator CLI - orchestrate ORCA calculations."""
    pass


@cli.command()
@click.argument(
    "config_file", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.option(
    "--include",
    "-i",
    multiple=True,
    help="Include only specified molecules (can be used multiple times)",
)
@click.option(
    "--exclude",
    "-e",
    multiple=True,
    help="Exclude specified molecules (can be used multiple times)",
)
@click.option(
    "--rerun-failed",
    is_flag=True,
    help="Only rerun molecules that failed in the previous run",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Set log level to DEBUG",
)
def run(
    config_file: Path, include: tuple, exclude: tuple, rerun_failed: bool, debug: bool
) -> None:
    """Run a calculation pipeline defined in a TOML config file."""
    # Reset any previous logger context
    clear_context()

    # Load config first to determine debug level
    config = load_config(config_file)

    # Apply CLI overrides to config
    if include:
        config["molecules"]["include"] = list(include)
    if exclude:
        config["molecules"]["exclude"] = list(exclude)
    if rerun_failed:
        config["molecules"]["rerun_failed"] = True
    if debug:
        config["main"]["debug"] = True

    # Set up log directory
    log_dir = config_file.parent / "logs"
    try:
        log_dir.mkdir(exist_ok=True, parents=True)
        setup_file_logging(log_dir=log_dir, log_level=logging.DEBUG)
    except Exception as e:
        error(f"Failed to create logs directory {log_dir}: {e}")
        # Try to set up logging in the current directory as fallback
        setup_file_logging(log_dir=None, log_level=logging.DEBUG)

    # Configure logging based on debug flag from config
    configure_from_config(config)

    info(f"Starting orcastrator run with config: {config_file}")
    try:
        # Create and run the pipeline using the PipelineRunner (with config already loaded)
        pipeline = PipelineRunner(config)
        stats = pipeline.run()
        info("Calculation pipeline completed successfully")

        # Log summary statistics
        total_molecules = len(stats.molecules)
        successful = len(stats.successful_molecules)
        failed = len(stats.failed_molecules)
        minutes = stats.elapsed_time / 60

        info(f"Summary: Processed {total_molecules} molecules in {minutes:.2f} minutes")
        info(f"         {successful} successful, {failed} failed")
    except Exception:
        error("Error running pipeline", exc_info=True)
        info("Calculation pipeline failed")
        sys.exit(1)


@cli.command()
@click.argument(
    "config_file", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.option(
    "--no-submit",
    is_flag=True,
    help="Generate the SLURM script but don't submit it with sbatch",
)
@click.option(
    "--debug",
    "debug_",
    is_flag=True,
    help="Set log level to DEBUG",
)
def slurm(config_file: Path, no_submit: bool, debug_: bool) -> None:
    """Generate a SLURM batch script and optionally submit it with sbatch."""
    # Reset any previous logger context
    clear_context()

    info(f"Generating SLURM script for config file: {config_file}")
    try:
        config = load_config(config_file)
        debug(f"Loaded configuration: {config['main']}")

        slurm_config = SlurmConfig(
            job_name=config_file.stem,
            ntasks=config["main"]["cpus"],
            mem_per_cpu_gb=config["main"]["mem_per_cpu_gb"],
            orcastrator_command=f"uvx orcastrator run {'--debug' if debug_ else ''} {config_file.resolve()}",
            config_file=config_file.resolve(),
        )
        debug(f"Created SLURM config: {slurm_config}")

        slurm_script_file = config_file.with_suffix(".slurm")
        slurm_config.write_to(slurm_script_file)
        info(f"SLURM script written to {slurm_script_file}")

        if not no_submit and shutil.which("sbatch"):
            debug("Submitting SLURM job with sbatch")
            result = subprocess.run(
                ["sbatch", str(slurm_script_file)], capture_output=True, text=True
            )
            if result.returncode == 0:
                slurm_job_id = result.stdout.strip().split()[-1]
                info(f"Submitted {config_file.name} with ID: {slurm_job_id}")
                print(f"Submitted {config_file.name} with ID: {slurm_job_id}")
            else:
                error(f"Failed to submit job: {result.stderr}")
                sys.exit(1)
        elif no_submit:
            info("Script generated but not submitted (--no-submit flag used)")
        else:
            warning("sbatch not found in PATH, cannot submit job")
    except Exception:
        error("Error generating SLURM script", exc_info=True)
        sys.exit(1)


@cli.command()
@click.argument(
    "config_file", type=click.Path(dir_okay=False, path_type=Path), required=False
)
@click.option("--slim", "-s", is_flag=True, help="Write a slim version of the template")
@click.option(
    "--force", "-f", is_flag=True, help="Overwrite the output file if it already exists"
)
def init(
    config_file: Optional[Path] = None, slim: bool = False, force: bool = False
) -> None:
    """Create a template configuration file for Orcastrator.

    If OUTPUT_FILE is not specified, creates 'orcastrator.toml' in the current directory.
    """
    if config_file is None:
        config_file = Path("orcastrator.toml")

    if config_file.exists() and not force:
        error(f"File {config_file} already exists. Use --force to overwrite.")
        sys.exit(1)

    molecules_dir = config_file.parent / "molecules"
    molecules_dir.mkdir(exist_ok=True)

    long_template = f"""# Orcastrator Configuration Template (v{__version__})

[main]
# Directory where calculation results will be saved
output_dir = "output"
# Total number of CPU cores to use
cpus = 4
# Memory in GB per CPU core
mem_per_cpu_gb = 2
# Set to true to overwrite existing calculations
overwrite = false
# Number of parallel workers (molecules processed simultaneously)
workers = 1
# Scratch directory for temporary files
scratch_dir = "/scratch"
# Set to true for more verbose logging
debug = false

[molecules]
# Directory containing molecule XYZ files
directory = "molecules"

# Optional: List of specific molecules to include (by name without .xyz extension)
# include = ["molecule1", "molecule2"]
# Optional: List of molecules to exclude
# exclude = ["molecule3"]
# Optional: Only rerun molecules that failed in the previous run
rerun_failed = false

# Define calculation steps (executed in order)
[[step]]
name = "opt"
keywords = ["D4", "TPSS", "def2-SVP", "OPT"]
# Optional: Additional ORCA blocks
blocks = ["%scf maxiter 150 end"]

[[step]]
name = "freq"
keywords = ["D4", "TPSS", "def2-SVP", "FREQ"]
# Optional: Use a different multiplicity for this step
# mult = 3

[[step]]
name = "sp"
keywords = ["D4", "TPSSh", "def2-TZVP"]
"""

    slim_template = """
[main]
output_dir = "output"
cpus = 4
mem_per_cpu_gb = 2
workers = 1


[molecules]
directory = "molecules"


[[step]]
name = "opt"
keywords = ["D4", "TPSS", "def2-SVP", "OPT"]

[[step]]
name = "freq"
keywords = ["D4", "TPSS", "def2-SVP", "FREQ"]

[[step]]
name = "sp"
keywords = ["D4", "TPSSh", "def2-TZVP"]
"""

    try:
        template = slim_template if slim else long_template
        config_file.write_text(template)
        info(f"Template configuration written to {config_file}")
        info("Edit this file to customize your calculation settings, then run:")
        info(f"  orcastrator run {config_file}")
    except Exception as e:
        error(f"Failed to write template: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
