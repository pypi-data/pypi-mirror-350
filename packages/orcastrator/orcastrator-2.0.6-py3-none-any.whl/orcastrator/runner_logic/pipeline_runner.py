import json
from pathlib import Path
from typing import Any, Dict, List

from orcastrator.logger import debug, error, info, warning
from orcastrator.molecule import Molecule
from orcastrator.runner_logic.molecule_runner import (
    process_molecules_parallel,
    process_molecules_sequential,
)
from orcastrator.stats import PipelineStats, Timer


class PipelineRunner:
    """Runs a complete molecular calculation pipeline."""

    def __init__(self, config: dict):
        """Initialize the pipeline runner with a configuration.

        Args:
            config: Dictionary containing pipeline configuration
        """
        info("Initializing pipeline runner")
        debug(f"Pipeline configuration: {config}")
        self.config = config
        self.molecules = []
        self._results_cache = self._load_previous_results()

    def load_molecules(self) -> None:
        """Load molecules from XYZ files based on configuration."""
        info(f"Loading molecules from {self.config['molecules']['directory']}")

        all_molecules = Molecule.from_xyz_files(
            self.config["molecules"]["directory"],
        )

        if len(all_molecules) == 0:
            error(f"No molecules found in {self.config['molecules']['directory']}")
            raise ValueError(
                f"No molecules found in {self.config['molecules']['directory']}"
            )

        # Apply molecule filtering
        molecules = self._filter_molecules(all_molecules)

        if not molecules:
            warning("No molecules selected after applying filters!")
            info("Check your include/exclude lists or rerun_failed settings")

        info(f"Selected {len(molecules)} out of {len(all_molecules)} molecules")
        for mol in molecules:
            debug(
                f"Selected molecule: {mol.name} (charge={mol.charge}, mult={mol.mult})"
            )

        self.molecules = molecules

    def run(self) -> PipelineStats:
        """Run the calculation pipeline on all loaded molecules.

        Returns:
            PipelineStats: Statistics for the pipeline execution
        """
        info("Starting calculation pipeline")

        # Create a timer for the entire pipeline
        with Timer("Pipeline") as pipeline_timer:
            # Make sure molecules are loaded
            if not self.molecules:
                debug("No molecules loaded yet, loading now")
                self.load_molecules()

            # Check if we have any molecules to process after filtering
            if not self.molecules:
                warning(
                    "No molecules to process after filtering, pipeline execution aborted"
                )
                stats = PipelineStats()
                stats.complete()
                return stats

            n_workers = self.config["main"]["workers"]
            cpus = self.config["main"]["cpus"]
            debug(f"Configuration: {n_workers} workers, {cpus} total CPUs")

            if cpus < n_workers:
                error(f"Not enough CPU cores ({cpus}) for all workers ({n_workers})")
                raise ValueError(
                    f"Not enough CPU cores ({cpus}) for all workers ({n_workers})"
                )

            pipeline_stats = None

            if n_workers > 1:
                # Calculate CPUs per worker
                worker_cpus = cpus // n_workers
                info(
                    f"Running in parallel mode with {n_workers} workers, {worker_cpus} CPUs per worker"
                )
                # Process molecules in parallel
                pipeline_stats = process_molecules_parallel(
                    self.molecules, n_workers, worker_cpus, self.config
                )
            else:
                # Process molecules sequentially
                info(f"Running in sequential mode with {cpus} CPUs")
                pipeline_stats = process_molecules_sequential(
                    self.molecules, self.config
                )

            info(f"Pipeline execution completed in {pipeline_timer.elapsed_time:.2f}s")
            self._save_results(pipeline_stats)
            return pipeline_stats

    def _filter_molecules(self, all_molecules: List[Molecule]) -> List[Molecule]:
        """Filter molecules based on configuration.

        Args:
            all_molecules: List of all available molecules

        Returns:
            Filtered list of molecules to process
        """
        # Start with all molecules
        filtered_molecules = all_molecules.copy()

        # Apply include filter if specified
        include_list = self.config["molecules"].get("include", [])
        if include_list:
            debug(f"Including only specified molecules: {', '.join(include_list)}")
            found_names = set(mol.name for mol in filtered_molecules)
            missing_molecules = [
                name for name in include_list if name not in found_names
            ]
            if missing_molecules:
                warning(
                    f"The following requested molecules were not found: {', '.join(missing_molecules)}"
                )
            filtered_molecules = [
                mol for mol in filtered_molecules if mol.name in include_list
            ]

        # Apply exclude filter (takes precedence over include)
        exclude_list = self.config["molecules"].get("exclude", [])
        if exclude_list:
            debug(f"Excluding specified molecules: {', '.join(exclude_list)}")
            filtered_molecules = [
                mol for mol in filtered_molecules if mol.name not in exclude_list
            ]

        # Apply rerun_failed filter if enabled
        rerun_failed = self.config["molecules"].get("rerun_failed", False)
        if rerun_failed and self._results_cache:
            debug("Rerun failed mode: only processing previously failed molecules")
            previously_failed = self._results_cache.get("failed_molecules", [])
            if not previously_failed:
                warning(
                    "Rerun-failed mode enabled but no previously failed molecules found"
                )
            filtered_molecules = [
                mol for mol in filtered_molecules if mol.name in previously_failed
            ]

        return filtered_molecules

    def _load_previous_results(self) -> Dict[str, Any]:
        """Load previous results cache if available."""
        output_dir = Path(self.config["main"]["output_dir"])
        cache_file = output_dir / ".results_cache.json"

        if not cache_file.exists():
            debug("No previous results cache found")
            return {}

        try:
            cache_data: Dict[str, Any] = json.loads(cache_file.read_text())
            debug(
                f"Loaded previous results with {len(cache_data.get('successful_molecules', []))} successful and {len(cache_data.get('failed_molecules', []))} failed molecules"
            )
            return cache_data
        except Exception as e:
            warning(f"Failed to load previous results: {e}")
            return {}

    def _save_results(self, stats: PipelineStats) -> None:
        """Save results for future runs."""
        output_dir = Path(self.config["main"]["output_dir"])
        output_dir.mkdir(exist_ok=True, parents=True)
        cache_file = output_dir / ".results_cache.json"

        # Extract key data for caching
        cache_data: Dict[str, Any] = {
            "successful_molecules": [m.name for m in stats.successful_molecules],
            "failed_molecules": [m.name for m in stats.failed_molecules],
            "timestamp": stats.end_time if stats.end_time else None,
            "total_time": stats.elapsed_time,
        }

        try:
            cache_file.write_text(json.dumps(cache_data, indent=2))
            debug(f"Saved results cache to {cache_file}")
        except Exception as e:
            warning(f"Failed to save results cache: {e}")

    @classmethod
    def from_config_file(cls, config_file: Path) -> "PipelineRunner":
        """Create a pipeline runner from a config file.

        Args:
            config_file: Path to the configuration file

        Returns:
            A configured PipelineRunner instance
        """
        info(f"Creating pipeline runner from config file: {config_file}")
        from orcastrator.config import load_config

        config = load_config(config_file)
        debug(f"Config loaded successfully from {config_file}")
        return cls(config)
