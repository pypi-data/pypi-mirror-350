# type: ignore

try:
    import toml
except ModuleNotFoundError:
    import tomllib as toml
from pathlib import Path

from cerberus import Validator

SCHEMA = {
    "main": {
        "type": "dict",
        "required": True,
        "schema": {
            "output_dir": {"type": "string", "required": True, "default": "output"},
            "cpus": {"type": "integer", "min": 1, "required": True, "default": 1},
            "mem_per_cpu_gb": {
                "type": "integer",
                "min": 1,
                "required": True,
                "default": 1,
            },
            "overwrite": {"type": "boolean", "required": True, "default": False},
            "workers": {"type": "integer", "min": 1, "required": True, "default": 1},
            "scratch_dir": {"type": "string", "required": False, "default": "/scratch"},
            "debug": {"type": "boolean", "required": False, "default": False},
        },
    },
    "molecules": {
        "type": "dict",
        "required": True,
        "schema": {
            "directory": {"type": "string", "required": True, "default": "molecules"},
            "include": {
                "type": "list",
                "schema": {"type": "string"},
                "required": False,
                "default": [],
            },
            "exclude": {
                "type": "list",
                "schema": {"type": "string"},
                "required": False,
                "default": [],
            },
            "rerun_failed": {
                "type": "boolean",
                "required": False,
                "default": False,
            },
        },
    },
    "step": {
        "type": "list",
        "required": True,
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string", "required": True},
                "keywords": {
                    "type": "list",
                    "schema": {"type": "string"},
                    "required": True,
                },
                "blocks": {
                    "type": "list",
                    "schema": {"type": "string"},
                    "required": False,
                    "default": [],
                },
                "mult": {
                    "type": "integer",
                    "min": 1,
                    "required": False,
                },
            },
        },
    },
}


def load_config(config_file: Path) -> dict:
    """Load configuration from a TOML file."""
    config = toml.loads(config_file.read_text())

    # Create a custom validator with path normalization
    class ConfigValidator(Validator):
        def _normalize_coerce_relativepath(self, value):
            path = Path(value)
            if not path.is_absolute():
                return str((config_file.parent / path).resolve())
            return str(path)

    # Update schema for path fields
    schema = dict(SCHEMA)
    schema["main"]["schema"]["output_dir"]["coerce"] = "relativepath"
    schema["molecules"]["schema"]["directory"]["coerce"] = "relativepath"

    # Register custom coercion type
    v = ConfigValidator(schema=schema, allow_unknown=False, purge_unknown=True)
    v.types_mapping["relativepath"] = lambda x: isinstance(x, (str, Path))

    if not v.validate(config, normalize=True):
        raise ValueError(f"Config validation failed: {v.errors}")

    return v.document
