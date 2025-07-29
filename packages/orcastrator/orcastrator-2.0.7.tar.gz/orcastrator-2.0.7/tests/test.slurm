#!/bin/bash
#SBATCH --job-name=test
#SBATCH --partition=normal
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4GB
#SBATCH --time=72:00:00
#SBATCH --output=%x-%j.slurm.log
#SBATCH --error=%x-%j.slurm.log



echo "======================================================"
echo "Job started at $(date)"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "SLURM Job Name: $SLURM_JOB_NAME"
echo "Running on nodes: $SLURM_JOB_NODELIST"
echo "Working directory: $(pwd)"
echo "Memory per CPU: 4GB"
echo "======================================================"
echo ""

# Environment setup
echo "Setting up environment..."
export ORCA_INSTALL_DIR="/soft/orca/orca_6_0_1_linux_x86-64_shared_openmpi416_avx2"
export OPENMPI_INSTALL_DIR="/soft/openmpi/openmpi-4.1.6"

export PATH="${ORCA_INSTALL_DIR}:${OPENMPI_INSTALL_DIR}/bin:${PATH}"
export LD_LIBRARY_PATH="${ORCA_INSTALL_DIR}/lib:${OPENMPI_INSTALL_DIR}/lib64:${LD_LIBRARY_PATH}"

echo "ORCA_INSTALL_DIR: $ORCA_INSTALL_DIR"
echo "OPENMPI_INSTALL_DIR: $OPENMPI_INSTALL_DIR"
echo "PATH: $PATH"
echo "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
echo ""
echo "Checking ORCA executable:"
which orca
echo ""

# Create logs directory
CONFIG_DIR=$(dirname "/Users/freddy/Documents/Projects/orcastrator/tests/test.toml")
LOG_DIR="${CONFIG_DIR}/logs"
echo "Creating logs directory: ${LOG_DIR}"
mkdir -p "${LOG_DIR}"

# Enable debug logging
export ORCASTRATOR_DEBUG=1
export ORCASTRATOR_LOG_DIR="${LOG_DIR}"

# Run Orcastrator
echo "Executing Orcastrator: uvx orcastrator run /Users/freddy/Documents/Projects/orcastrator/tests/test.toml"
echo "------------------------------------------------------"
uvx orcastrator run /Users/freddy/Documents/Projects/orcastrator/tests/test.toml
ORCASTRATOR_EXIT_CODE=$?
echo "------------------------------------------------------"
echo "Orcastrator finished with exit code: $ORCASTRATOR_EXIT_CODE"
echo ""

echo "======================================================"
echo "Job finished at $(date)"
echo "======================================================"

exit $ORCASTRATOR_EXIT_CODE