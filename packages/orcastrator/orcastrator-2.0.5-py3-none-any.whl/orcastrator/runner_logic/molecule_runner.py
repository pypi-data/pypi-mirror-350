import threading
import time
from pathlib import Path
from typing import List, Optional

from orcastrator.calculation import OrcaCalculation
from orcastrator.engine import OrcaEngine
from orcastrator.logger import clear_context, debug, error, info, set_context, warning
from orcastrator.molecule import Molecule
from orcastrator.stats import MoleculeStats, PipelineStats, StepStats


def process_molecule(
    molecule: Molecule, config: dict, cpus: Optional[int] = None
) -> tuple[bool, MoleculeStats]:
    """Process a single molecule with the given configuration.

    Args:
        molecule: The molecule to process
        config: Dictionary containing calculation configuration
        cpus: Optional number of CPUs to use for this calculation. If None,
              will use the default from the config.

    Returns:
        bool: True if all calculation steps completed successfully, False otherwise
    """
    # Set molecule context for logging
    set_context(molecule=molecule.name)
    info(
        f"Processing molecule: {molecule.name} (charge={molecule.charge}, mult={molecule.mult})"
    )

    # Initialize molecule statistics
    molecule_stats = MoleculeStats(name=molecule.name, success=True, elapsed_time=0.0)

    # Start timing the molecule processing
    start_time = time.time()

    # Set up directories
    output_dir = Path(config["main"]["output_dir"]) / molecule.name
    output_dir.mkdir(parents=True, exist_ok=True)
    debug(f"Created output directory: {output_dir}")

    # Create ORCA engine with configured scratch directory
    engine = OrcaEngine(scratch_base_dir=Path(config["main"]["scratch_dir"]))
    debug(f"Created ORCA engine with scratch in: {engine.scratch_base_dir}")

    # Get the CPU count for this calculation
    cpu_count = cpus if cpus is not None else config["main"]["cpus"]
    debug(f"Using {cpu_count} CPUs for calculation")

    # Process each step in the calculation pipeline
    previous_calc = None
    success = True

    try:
        for step in config["step"]:
            # Set step context for logging
            set_context(molecule=molecule.name, step=step["name"])
            info(f"Starting calculation step: {step['name']}")
            step_dir = output_dir / step["name"]
            step_dir.mkdir(exist_ok=True)
            debug(f"Created step directory: {step_dir}")

            # Create calculation for this step (either initial or chained from previous)
            if previous_calc is None:
                debug(f"Creating initial calculation for step {step['name']}")
                calc = OrcaCalculation(
                    directory=step_dir,
                    molecule=molecule,
                    keywords=step["keywords"],
                    blocks=step.get("blocks", []),
                    overwrite=config["main"]["overwrite"],
                    cpus=cpu_count,
                    mem_per_cpu_gb=config["main"]["mem_per_cpu_gb"],
                    engine=engine,
                )
            else:
                # Chain from previous calculation
                charge = step.get("charge", molecule.charge)
                mult = step.get("mult", molecule.mult)
                debug(
                    f"Chaining calculation from previous step with charge={charge}, mult={mult}"
                )

                calc = previous_calc.chain(
                    directory=step_dir,
                    keywords=step["keywords"],
                    blocks=step.get("blocks", []),
                    charge=charge,
                    mult=mult,
                )

            debug(f"Running calculation step {step['name']} for {molecule.name}")
            calc_success, step_time = calc.run()

            # Record step statistics
            step_stats = StepStats(
                name=step["name"], success=calc_success, elapsed_time=step_time
            )
            molecule_stats.steps.append(step_stats)

            if not calc_success:
                warning("Calculation failed at current step")
                success = False
                molecule_stats.success = False
                break

            info(f"Step {step['name']} completed successfully")
            previous_calc = calc
    except Exception:
        error("Error processing molecule", exc_info=True)
        success = False

    # Calculate total processing time
    elapsed_time = time.time() - start_time
    molecule_stats.elapsed_time = elapsed_time

    if success:
        info(f"All calculation steps completed successfully (took {elapsed_time:.2f}s)")
    else:
        warning(f"Calculation pipeline failed (took {elapsed_time:.2f}s)")

    return success, molecule_stats


def process_molecules_parallel(
    molecules: List[Molecule], n_workers: int, worker_cpus: int, config: dict
) -> PipelineStats:
    """Process molecules in parallel by simply starting multiple ORCA processes.

    This uses a simple approach where we just keep track of running calculations
    and start new ones as slots become available.

    Args:
        molecules: List of molecules to process
        n_workers: Number of parallel workers (max concurrent ORCA processes)
        worker_cpus: Number of CPUs to allocate to each worker
        config: Dictionary containing calculation configuration
    """
    # Clear any previous context when starting pipeline
    clear_context()
    info(f"Starting parallel processing of up to {n_workers} molecules at a time")
    debug(f"Each calculation will use {worker_cpus} CPUs")

    # Initialize pipeline statistics
    pipeline_stats = PipelineStats()

    # Process results from a thread and update stats
    def process_thread_result(thread, molecule_name, result_list):
        thread.join()  # Make sure thread is done
        if result_list:  # Check if the thread actually produced a result
            success, mol_stats = result_list[0]
            status = "completed successfully" if success else "failed"
            info(f"Molecule {molecule_name} {status}")
            pipeline_stats.add_molecule_stats(mol_stats)
        else:
            # Something went wrong - the thread didn't produce a result
            warning(f"No results from thread processing {molecule_name}")
            pipeline_stats.add_molecule_stats(
                MoleculeStats(name=molecule_name, success=False, elapsed_time=0.0)
            )

    # Use a simple list to collect the running threads
    running = []
    molecules_queue = list(molecules)  # Make a copy we can modify

    # Process molecules until none are left and all threads complete
    while molecules_queue or running:
        # Start new calculations if we have capacity and molecules to process
        while molecules_queue and len(running) < n_workers:
            molecule = molecules_queue.pop(0)
            results = []  # List to collect the result from the thread

            # Create and start a thread for this molecule
            thread = threading.Thread(
                target=lambda m, cfg, cpus, res: res.append(
                    process_molecule(m, cfg, cpus)
                ),
                args=(molecule, config, worker_cpus, results),
            )
            thread.start()

            info(f"Started calculation for {molecule.name}")
            running.append((thread, molecule.name, results))

        # Check for completed threads and collect results
        still_running = []
        for thread, mol_name, results in running:
            if not thread.is_alive():
                process_thread_result(thread, mol_name, results)
            else:
                still_running.append((thread, mol_name, results))

        running = still_running

        # Small sleep to prevent CPU spinning if we still have running processes
        if running:
            time.sleep(1)

    # All threads complete
    pipeline_stats.complete()
    pipeline_stats.print_summary()

    return pipeline_stats


def process_molecules_sequential(
    molecules: List[Molecule], config: dict
) -> PipelineStats:
    """Process molecules sequentially.

    This function processes each molecule one after another, using all available
    resources for each calculation.

    Args:
        molecules: List of molecules to process
        config: Dictionary containing calculation configuration
    """
    # Clear any previous context when starting pipeline
    clear_context()
    info(f"Starting sequential processing of {len(molecules)} molecules")

    # Initialize pipeline statistics
    pipeline_stats = PipelineStats()

    for i, molecule in enumerate(molecules):
        set_context(molecule=molecule.name)
        info(f"Processing molecule {i + 1}/{len(molecules)}: {molecule.name}")
        try:
            success, mol_stats = process_molecule(molecule, config)
            status = "completed successfully" if success else "failed"
            info(f"Molecule {status}")
            # Clear context after processing this molecule
            clear_context()
            pipeline_stats.add_molecule_stats(mol_stats)
        except Exception:
            error("Error processing molecule", exc_info=True)
            # Clear context after processing this molecule
            clear_context()
            # Add a failed molecule stat when exception occurs
            pipeline_stats.add_molecule_stats(
                MoleculeStats(name=molecule.name, success=False, elapsed_time=0.0)
            )

    # Mark the pipeline as complete and record end time
    pipeline_stats.complete()

    # Print statistics summary
    pipeline_stats.print_summary()

    return pipeline_stats
