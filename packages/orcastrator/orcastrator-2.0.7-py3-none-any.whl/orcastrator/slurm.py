from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from jinja2 import Template

SLURM_SCRIPT_TEMPLATE = """\
#!/bin/bash
#SBATCH --job-name={{ job_name }}
#SBATCH --partition={{ partition }}
#SBATCH --nodes={{ nodes }}
#SBATCH --ntasks={{ ntasks }}
#SBATCH --cpus-per-task={{ cpus_per_task }}
#SBATCH --mem-per-cpu={{ mem_per_cpu_gb }}GB
#SBATCH --time={{ time_h }}:00:00
#SBATCH --output=%x-%j.slurm.log
#SBATCH --error=%x-%j.slurm.log
{% if account %}#SBATCH --account={{ account }}{% endif %}
{% if email %}
#SBATCH --mail-user={{ email }}
#SBATCH --mail-type={{ email_type | default("END,FAIL") }}
{% endif %}

echo "======================================================"
echo "Job started at $(date)"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "SLURM Job Name: $SLURM_JOB_NAME"
echo "Running on nodes: $SLURM_JOB_NODELIST"
echo "Working directory: $(pwd)"
echo "Memory per CPU: {{ mem_per_cpu_gb }}GB"
echo "======================================================"
echo ""

# Environment setup
echo "Setting up environment..."
export ORCA_INSTALL_DIR="{{ orca_install_dir }}"
export OPENMPI_INSTALL_DIR="{{ openmpi_install_dir }}"

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
CONFIG_DIR=$(dirname "{{ config_file }}")
LOG_DIR="${CONFIG_DIR}/logs"
echo "Creating logs directory: ${LOG_DIR}"
mkdir -p "${LOG_DIR}"

# Enable debug logging
export ORCASTRATOR_DEBUG=1
export ORCASTRATOR_LOG_DIR="${LOG_DIR}"

# Run Orcastrator
uvx orcastrator --version
echo "Executing Orcastrator: {{ orcastrator_command }}"
echo "------------------------------------------------------"
{{ orcastrator_command }}
ORCASTRATOR_EXIT_CODE=$?
echo "------------------------------------------------------"
echo "Orcastrator finished with exit code: $ORCASTRATOR_EXIT_CODE"
echo ""

echo "======================================================"
echo "Job finished at $(date)"
echo "======================================================"

exit $ORCASTRATOR_EXIT_CODE
"""


@dataclass
class SlurmConfig:
    """Configuration class for SLURM job parameters."""

    job_name: str
    ntasks: int
    mem_per_cpu_gb: int
    orcastrator_command: str
    config_file: Path
    nodes: int = 1
    partition: str = "normal"
    cpus_per_task: int = 1
    time_h: int = 168  # 7 days
    orca_install_dir: str = "/soft/orca/orca_6_0_1_linux_x86-64_shared_openmpi416_avx2"
    openmpi_install_dir: str = "/soft/openmpi/openmpi-4.1.6"
    account: Optional[str] = None
    email: Optional[str] = None
    email_type: Optional[str] = None

    def compile(self) -> str:
        template: Template = Template(SLURM_SCRIPT_TEMPLATE)
        return template.render(asdict(self))

    def write_to(self, file: Path) -> None:
        script = self.compile()
        # Write the rendered script to the output path
        file.write_text(script)
        # Make the script executable
        file.chmod(0o755)
