"""
The runner_logic package provides functionality for running ORCA calculations
on molecules in both sequential and parallel modes.

This package separates the computational logic from the CLI interface,
allowing for better modularity and testability.
"""

from orcastrator.runner_logic.pipeline_runner import PipelineRunner

__all__ = ["PipelineRunner"]
