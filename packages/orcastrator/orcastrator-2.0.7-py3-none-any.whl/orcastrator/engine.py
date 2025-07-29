import os
import shutil
import subprocess
import uuid
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterator, Optional

from orcastrator.logger import debug, error, info, warning


class OrcaEngine:
    """Handles ORCA execution and scratch directory management.

    This class is responsible for:
    1. Finding and managing the ORCA executable
    2. Managing scratch directories for calculations
    3. Executing ORCA processes
    """

    def __init__(
        self,
        orca_executable: Optional[Path] = None,
        scratch_base_dir: Path = Path("/scratch"),
        env_vars: Optional[Dict[str, str]] = None
    ) -> None:
        """Initialize the ORCA engine.

        Args:
            orca_executable: Path to ORCA executable. If None, will search in PATH.
            scratch_base_dir: Base directory for creating scratch directories.
            env_vars: Additional environment variables to set when running ORCA.
        """
        debug("Initializing OrcaEngine")
        self.scratch_base_dir = scratch_base_dir
        self.env_vars = env_vars or {}

        # Check if scratch directory exists
        if not self.scratch_base_dir.exists():
            warning(f"Scratch base directory {self.scratch_base_dir} doesn't exist")

        # Set up ORCA executable
        if orca_executable:
            debug(f"Using provided ORCA executable: {orca_executable}")
            self.orca_executable = Path(orca_executable).resolve()
            if not self.orca_executable.is_file():
                error(f"ORCA executable not found at {self.orca_executable}")
                raise FileNotFoundError(f"ORCA executable not found at {self.orca_executable}")
        else:
            debug("Searching for ORCA executable in PATH")
            found_path = shutil.which("orca")
            if found_path is None:
                error("ORCA executable not found in PATH")
                raise RuntimeError("ORCA executable not found in PATH. Please ensure it's installed and in your PATH, or specify its path.")
            self.orca_executable = Path(found_path).resolve()
            debug(f"Found ORCA executable: {self.orca_executable}")

        # Incorporate SLURM job ID into scratch path if running under SLURM
        if slurm_job_id := os.getenv("SLURM_JOB_ID"):
            self.scratch_base_dir = self.scratch_base_dir / slurm_job_id
            debug(f"Using SLURM-specific scratch directory: {self.scratch_base_dir}")

            # Ensure the SLURM scratch directory exists
            os.makedirs(self.scratch_base_dir, exist_ok=True)

    @contextmanager
    def create_scratch_dir(self, calculation_name: str) -> Iterator[Path]:
        """Create a scratch directory for a calculation.

        Args:
            calculation_name: Name of the calculation for the scratch directory

        Yields:
            Path to the created scratch directory

        Raises:
            NotADirectoryError: If the scratch base directory doesn't exist
        """
        debug(f"Creating scratch directory in {self.scratch_base_dir}")
        if not self.scratch_base_dir.exists():
            error(f"Scratch directory {self.scratch_base_dir.resolve()} does not exist")
            raise NotADirectoryError(
                f"Specified scratch directory {self.scratch_base_dir.resolve()} does not exist"
            )

        run_uuid = str(uuid.uuid4())[:8]
        scratch_dir = self.scratch_base_dir / f"{calculation_name}_{run_uuid}"
        debug(f"Generated scratch directory: {scratch_dir}")

        try:
            # We don't copy anything here - that's the responsibility of the caller
            scratch_dir.mkdir(parents=True, exist_ok=False)
            debug("Created scratch directory")
            yield scratch_dir
        except Exception:
            error("Error setting up scratch directory", exc_info=True)
            raise
        finally:
            if scratch_dir.exists():
                debug(f"Removing scratch directory {scratch_dir}")
                shutil.rmtree(scratch_dir)

    def copy_to_scratch(self, source_dir: Path, scratch_dir: Path) -> None:
        """Copy calculation files to a scratch directory.

        Args:
            source_dir: Source directory containing calculation files
            scratch_dir: Destination scratch directory
        """
        debug(f"Copying files from {source_dir} to {scratch_dir}")
        try:
            shutil.copytree(source_dir, scratch_dir, dirs_exist_ok=True)
            debug("Files copied to scratch directory")
        except Exception as e:
            error(f"Error copying files to scratch directory: {e}", exc_info=True)
            raise

    def copy_from_scratch(self, scratch_dir: Path, dest_dir: Path) -> None:
        """Copy calculation results from scratch directory back to the original directory.

        Args:
            scratch_dir: Source scratch directory
            dest_dir: Destination directory
        """
        debug(f"Copying results from {scratch_dir} to {dest_dir}")
        try:
            # Ensure destination directory exists
            dest_dir.mkdir(exist_ok=True, parents=True)

            shutil.copytree(
                scratch_dir,
                dest_dir,
                ignore=shutil.ignore_patterns("*.tmp", "*.tmp.*"),
                dirs_exist_ok=True,
            )
            debug("Results copied from scratch directory")
        except Exception as e:
            error(f"Error copying results from scratch directory: {e}", exc_info=True)
            raise

    def execute(
        self,
        input_file: Path,
        output_file: Path,
        use_scratch: bool = True
    ) -> subprocess.CompletedProcess:
        """Execute ORCA calculation.

        Args:
            input_file: Path to input file
            output_file: Path for output file
            use_scratch: Whether to use a scratch directory

        Returns:
            CompletedProcess instance with return code and stderr

        Raises:
            FileNotFoundError: If input file or working directory doesn't exist
            ValueError: If the input file is not in the working directory
        """
        debug(f"Preparing to run ORCA on input file: {input_file}")
        working_dir = input_file.parent
        debug(f"Working directory: {working_dir}")

        # Validate input
        if not working_dir.is_dir():
            error(f"Working directory not found: {working_dir}")
            raise FileNotFoundError(f"Working directory not found {working_dir}")

        if not input_file.is_file():
            error(f"Input file not found: {input_file}")
            raise FileNotFoundError(f"Input file not found {input_file}")

        if not input_file.parent == working_dir:
            error(f"Input file {input_file} is not in working directory {working_dir}")
            raise ValueError("Specified input file is not in the working directory")

        cmd = [
            str(self.orca_executable.resolve()),
            input_file.name,
        ]
        debug(f"Executing command: {' '.join(cmd)} > {output_file}")

        # Prepare environment
        env = os.environ.copy()
        env.update(self.env_vars)

        info(f"Starting ORCA process in {working_dir}")
        with open(output_file, 'w') as output_fd:
            result = subprocess.run(
                cmd,
                cwd=working_dir,
                stdout=output_fd,
                stderr=subprocess.PIPE,
                text=True,
                check=False,  # We handle success/failure based on ORCA's output text
                env=env,
                timeout=86400  # Add a 24-hour timeout as a safety measure
            )

        debug(f"ORCA process completed with return code: {result.returncode}")
        debug(f"ORCA stderr: {result.stderr}")
        if result.returncode != 0:
            warning(f"ORCA process returned non-zero exit code: {result.returncode}")
        else:
            debug("ORCA process completed with exit code 0")

        return result

    def run_with_scratch(
        self,
        input_dir: Path,
        input_file: Path,
        output_file: Path
    ) -> subprocess.CompletedProcess:
        """Run ORCA calculation using a scratch directory.

        Args:
            input_dir: Directory containing the calculation files
            input_file: Path to the input file
            output_file: Path where the output will be written

        Returns:
            CompletedProcess instance with return code and stderr
        """
        calc_name = input_dir.name
        info(f"Running ORCA calculation {calc_name} with scratch directory")

        with self.create_scratch_dir(calc_name) as scratch_dir:
            # Copy files to scratch directory
            self.copy_to_scratch(input_dir, scratch_dir)

            # Get scratch paths
            scratch_input = scratch_dir / input_file.name
            debug(f"Scratch input file: {scratch_input}")

            # Execute in scratch directory
            result = self.execute(scratch_input, output_file, use_scratch=False)

            # Copy results back (already handles cleanup in finally block)
            self.copy_from_scratch(scratch_dir, input_dir)

        return result
