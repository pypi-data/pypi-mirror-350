from pathlib import Path
from typing import Optional, Tuple

from orcastrator.engine import OrcaEngine
from orcastrator.logger import debug, error, info, set_context, warning
from orcastrator.molecule import Molecule
from orcastrator.stats import Timer


class OrcaCalculation:
    def __init__(
        self,
        directory: Path,
        molecule: Molecule,
        keywords: list[str],
        engine: Optional[OrcaEngine] = None,
        blocks: list[str] = [],
        overwrite: bool = False,
        cpus: int = 1,
        mem_per_cpu_gb: int = 1,
        scratch_dir: Optional[Path] = None,  # For backwards compatibility
    ) -> None:
        self.directory = directory
        self.molecule = molecule
        self.keywords = keywords
        self.blocks = blocks
        self.overwrite = overwrite
        self.cpus = cpus
        self.mem_per_cpu_gb = mem_per_cpu_gb

        # Create or use provided OrcaEngine
        if engine is None and scratch_dir is not None:
            self.engine = OrcaEngine(scratch_base_dir=scratch_dir)
        else:
            self.engine = engine or OrcaEngine()

        # Log initialization
        debug(
            f"Initialized calculation in {directory} with {cpus} CPUs and {mem_per_cpu_gb}GB per CPU"
        )
        debug(f"Keywords: {', '.join(keywords)}")
        debug(
            f"Molecule: {molecule.name} (charge={molecule.charge}, mult={molecule.mult})"
        )

    @property
    def input_file(self) -> Path:
        return self.directory / (self.directory.name + ".inp")

    @property
    def output_file(self) -> Path:
        return self.input_file.with_suffix(".out")

    def build_input_string(self) -> str:
        # Consistently format keywords for reliable matching between runs
        keywords = f"! {' '.join(sorted(self.keywords))}"
        debug(f"Building input with keywords: {keywords}")

        temp_blocks = self.blocks.copy()
        if self.cpus > 1:
            cpu_block = f"%pal nprocs {self.cpus} end"
            temp_blocks.append(cpu_block)
            debug(f"Added CPU parallel block: {cpu_block}")

        if self.mem_per_cpu_gb:
            # ORCA uses total memory in MB per core for %maxcore
            total_mem_mb = self.mem_per_cpu_gb * 1024

            # Reserve 20% of the memory for when ORCA overextends it alloted memory.
            # suborca uses 25%.
            MEMORY_RESERVE_FRACTION: float = 0.2

            available_mem_mb = int(total_mem_mb * (1 - MEMORY_RESERVE_FRACTION))

            mem_block = f"%maxcore {available_mem_mb}"
            temp_blocks.append(mem_block)
            debug(f"Added memory block: {mem_block}")

        blocks = "\n".join(temp_blocks)
        debug(f"Final blocks configuration: {len(temp_blocks)} blocks")

        molecule = self.molecule.to_orca()
        debug("Molecule format prepared for ORCA")
        return "\n".join([keywords, blocks, molecule])

    def is_cached(self) -> bool:
        """Check if this calculation is already cached with correct inputs."""
        if not self.input_file.exists() or self.overwrite:
            return False

        # Check if input matches what we would generate
        current_input_str = self.build_input_string()
        old_input = self.input_file.read_text()
        input_match = old_input == current_input_str

        if not input_match:
            debug("Previous calculation input doesn't match current settings")
            return False

        # Check if calculation completed successfully
        return self.completed_normally()

    def completed_normally(self) -> bool:
        debug("Checking if calculation completed normally")
        if not self.output_file.exists():
            warning(f"Output file {self.output_file} does not exist")
            return False

        output = self.output_file.read_text()
        debug(f"Read output file, size: {len(output)} bytes")

        # TODO we should probably prove the calculation successful,
        # not the other way around.
        # If we're missing some checks, mistakes can happen silently
        successful = True

        if "opt" in [kw.lower() for kw in self.keywords]:
            debug("Checking optimization convergence")
            convergence_phrases = [
                "THE OPTIMIZATION HAS CONVERGED",
                "OPTIMIZATION RUN DONE",
                "OPTIMIZATION CONVERGED",
                "HURRAY",
            ]
            if not any(phrase in output for phrase in convergence_phrases):
                warning(f"Optimization did not converge in {self.directory}")
                successful = False
            else:
                debug("Optimization converged successfully")

        if "freq" in [kw.lower() for kw in self.keywords]:
            debug("Checking frequency calculation")
            if "***imaginary mode***" in output:
                warning(f"Imaginary mode(s) detected in {self.directory}")
            else:
                debug("No imaginary modes detected")

        if "****ORCA TERMINATED NORMALLY****" not in output:
            warning("ORCA did not terminate normally")
            debug("Missing 'ORCA TERMINATED NORMALLY' message in output")
            successful = False

        if not successful:
            last_lines = "\n".join(output.splitlines()[-20:])
            debug(f"Last lines of output:\n{last_lines}")
            if "[file orca_tools/qcmsg.cpp, line 394]:" in last_lines:
                info(
                    "Detected a 'qcmsg.cpp' error - try increasing the calculation memory"
                )
            return False
        debug("ORCA terminated normally")
        return True

    def run(self) -> Tuple[bool, float]:
        """Run the calculation and return success status and elapsed time."""
        set_context(molecule=self.molecule.name)
        info(f"Starting ORCA calculation in {self.directory}")
        debug(
            f"Calculation parameters: {self.cpus} CPUs, {self.mem_per_cpu_gb}GB per CPU"
        )

        timer = Timer(f"Calculation {self.directory.name}")

        with timer:
            # Check if we already have a valid cached calculation
            if not self.overwrite and self.is_cached():
                info(
                    "Skipping calculation - previous run completed successfully with same input"
                )
                return True, timer.elapsed_time

            # Need to (re)run the calculation
            try:
                # Ensure directory exists
                self.directory.mkdir(exist_ok=True, parents=True)

                # Write the input file
                debug(f"Writing input file to {self.input_file}")
                self.input_file.write_text(self.build_input_string())

                # Run the calculation using the engine
                info("Running ORCA calculation")
                result = self.engine.run_with_scratch(
                    input_dir=self.directory,
                    input_file=self.input_file,
                    output_file=self.output_file,
                )

                debug(f"ORCA process completed with return code: {result.returncode}")
                if result.returncode != 0:
                    warning(
                        f"ORCA process returned non-zero exit code: {result.returncode}"
                    )
                    debug(f"ORCA stderr: {result.stderr}")
            except Exception:
                error("Error during calculation execution", exc_info=True)
                return False, timer.elapsed_time

            success = self.completed_normally()

        # Log results after the timer context has exited
        if success:
            info(f"Calculation completed successfully (took {timer.elapsed_time:.2f}s)")
        else:
            warning(
                f"Calculation did not complete normally (took {timer.elapsed_time:.2f}s)"
            )
            if self.output_file.exists():
                # Get the last few lines of output for easier debugging
                try:
                    with open(self.output_file, "r") as f:
                        last_lines = "".join(f.readlines()[-10:])
                    debug(f"Last lines of failed calculation:\n{last_lines}")
                except Exception as e:
                    debug(f"Could not read last lines of output file: {e}")

        return success, timer.elapsed_time

    def chain(
        self,
        directory: Path,
        keywords: list[str],
        blocks: list[str] = [],
        charge: Optional[int] = None,
        mult: Optional[int] = None,
    ) -> "OrcaCalculation":
        info(f"Chaining new calculation to {directory}")
        debug(f"Chain parameters: keywords={keywords}, blocks={blocks}")

        xyz_file = self.output_file.with_suffix(".xyz")
        debug(f"Loading molecule from {xyz_file}")
        if xyz_file.exists():
            molecule = Molecule.from_xyz_file(
                xyz_file=xyz_file, charge=charge, mult=mult
            )
            debug("Successfully loaded molecule from previous calculation output")
        else:
            # Some calculations don't generate this xyz file
            # In that case, the self.molecule is already the optimized geometry, right?
            debug(
                f"File {xyz_file} does not exist - reusing the inital coordinates from previous calculation"
            )
            molecule = self.molecule.copy(charge=charge, mult=mult)

        debug(
            f"Creating new calculation with same resources: {self.cpus} CPUs, {self.mem_per_cpu_gb}GB per CPU"
        )
        new_calculation = OrcaCalculation(
            directory=directory,
            engine=self.engine,
            molecule=molecule,
            keywords=keywords,
            blocks=blocks,
            overwrite=self.overwrite,
            cpus=self.cpus,
            mem_per_cpu_gb=self.mem_per_cpu_gb,
        )
        return new_calculation
