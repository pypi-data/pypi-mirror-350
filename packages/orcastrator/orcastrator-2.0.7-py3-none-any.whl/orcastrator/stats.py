import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from orcastrator.logger import info


@dataclass
class StepStats:
    """Statistics for a single calculation step."""

    name: str
    success: bool
    elapsed_time: float  # in seconds


@dataclass
class MoleculeStats:
    """Statistics for processing a single molecule."""

    name: str
    success: bool
    elapsed_time: float  # total time in seconds
    steps: List[StepStats] = field(default_factory=list)


@dataclass
class PipelineStats:
    """Statistics for the entire calculation pipeline."""

    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    molecules: List[MoleculeStats] = field(default_factory=list)

    @property
    def elapsed_time(self) -> float:
        """Get the total elapsed time for the pipeline."""
        if self.end_time is None:
            return time.time() - self.start_time
        return self.end_time - self.start_time

    @property
    def successful_molecules(self) -> List[MoleculeStats]:
        """Get list of successfully processed molecules."""
        return [m for m in self.molecules if m.success]

    @property
    def failed_molecules(self) -> List[MoleculeStats]:
        """Get list of molecules that failed processing."""
        return [m for m in self.molecules if not m.success]

    def complete(self) -> None:
        """Mark the pipeline as complete by setting the end time."""
        self.end_time = time.time()

    def add_molecule_stats(self, molecule_stats: MoleculeStats) -> None:
        """Add statistics for a processed molecule."""
        self.molecules.append(molecule_stats)

    def print_summary(self) -> None:
        """Print a summary of the pipeline statistics."""
        total_molecules = len(self.molecules)
        successful = len(self.successful_molecules)
        failed = len(self.failed_molecules)

        # Calculate step statistics
        step_times: Dict[str, List[float]] = defaultdict(list)
        step_success: Dict[str, List[bool]] = defaultdict(list)

        for mol in self.molecules:
            for step in mol.steps:
                step_times[step.name].append(step.elapsed_time)
                step_success[step.name].append(step.success)

        info("=" * 60)
        info("PIPELINE EXECUTION SUMMARY")
        info("=" * 60)
        info(
            f"Total runtime: {self.elapsed_time:.2f} seconds ({self.elapsed_time / 60:.2f} minutes)"
        )
        info(f"Molecules processed: {total_molecules}")
        info(
            f"  - Successful: {successful} ({successful / total_molecules * 100:.1f}%)"
        )
        info(f"  - Failed: {failed} ({failed / total_molecules * 100:.1f}%)")

        if total_molecules > 0:
            avg_time = sum(m.elapsed_time for m in self.molecules) / total_molecules
            info(
                f"Average time per molecule: {avg_time:.2f} seconds ({avg_time / 60:.2f} minutes)"
            )

            # Show fastest and slowest molecules if we have more than one
            if total_molecules > 1:
                sorted_by_time = sorted(self.molecules, key=lambda m: m.elapsed_time)
                fastest = sorted_by_time[0]
                slowest = sorted_by_time[-1]
                info(
                    f"Fastest molecule: {fastest.name} ({fastest.elapsed_time:.2f} seconds)"
                )
                info(
                    f"Slowest molecule: {slowest.name} ({slowest.elapsed_time:.2f} seconds)"
                )

        # Step statistics
        info("")
        info("STEP STATISTICS")
        info("-" * 60)
        info(
            f"{'Step Name':<20} {'Success Rate':<15} {'Avg Time':<15} {'Min Time':<15} {'Max Time':<15}"
        )
        info("-" * 60)

        for step_name in sorted(step_times.keys()):
            times = step_times[step_name]
            success_rate = (
                sum(step_success[step_name]) / len(step_success[step_name]) * 100
            )
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)

            info(
                f"{step_name:<20} {success_rate:>6.1f}%         {avg_time:>6.2f}s         {min_time:>6.2f}s         {max_time:>6.2f}s"
            )

        # List failed molecules if any
        if failed > 0:
            info("\nFAILED MOLECULES")
            info("-" * 60)
            for mol in self.failed_molecules:
                # Find the first failed step
                failed_step = next(
                    (s.name for s in mol.steps if not s.success), "Unknown"
                )
                info(f"{mol.name:<30} Failed at step: {failed_step}")

        info("=" * 60)


class Timer:
    """Context manager for timing code execution."""

    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = 0
        self.elapsed = 0

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        self.elapsed = time.time() - self.start_time

    @property
    def elapsed_time(self) -> float:
        """Get the elapsed time in seconds."""
        return self.elapsed
