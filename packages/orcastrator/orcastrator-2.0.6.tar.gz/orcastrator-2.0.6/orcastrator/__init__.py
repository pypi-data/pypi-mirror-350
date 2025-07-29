"""Orcastrator - A tool for orchestrating ORCA quantum chemistry calculations"""

from orcastrator.stats import MoleculeStats, PipelineStats, StepStats, Timer

__version__ = "2.0.6"
__all__ = ["MoleculeStats", "PipelineStats", "StepStats", "Timer"]

# Note: Do not initialize the logger here to prevent duplicate logging
# Logger should be initialized only when needed by the individual modules
