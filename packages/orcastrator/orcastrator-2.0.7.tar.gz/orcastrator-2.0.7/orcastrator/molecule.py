import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Self

from orcastrator.logger import debug, error, info, warning


@dataclass
class Atom:
    """Represents a single atom in a molecule."""

    symbol: str
    x: float
    y: float
    z: float

    def to_xyz_line(self) -> str:
        """Format the atom as an XYZ file line."""
        return (
            f"{self.symbol:4}    {self.x:>12.8f}    {self.y:>12.8f}    {self.z:>12.8f}"
        )


@dataclass
class Molecule:
    """Represents a molecule with its geometry and properties."""

    charge: int
    mult: int
    name: str
    atoms: List[Atom] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        debug(
            f"Initialized molecule: {self.name}, charge={self.charge}, mult={self.mult}"
        )

    def __str__(self) -> str:
        atoms_str = "\n".join(atom.to_xyz_line() for atom in self.atoms)
        return f"{len(self.atoms)}\ncharge={self.charge} mult={self.mult}\n{atoms_str}"

    @property
    def xyz(self) -> str:
        """Get the molecule's geometry as an XYZ format string."""
        return "\n".join(atom.to_xyz_line() for atom in self.atoms)

    def to_orca(self) -> str:
        """Convert molecule to ORCA input format."""
        debug(f"Converting molecule {self.name} to ORCA format")
        return f"* XYZ {self.charge} {self.mult}\n{self.xyz}\n*\n"

    def copy(self, **kwargs) -> "Molecule":
        """Create a copy of this molecule with optional attribute overrides.

        Args:
            **kwargs: Attributes to override in the new molecule instance
                     (e.g., charge, mult, name)

        Returns:
            A new Molecule instance with the same or overridden attributes
        """
        # Create shallow copies of mutable fields
        atoms_copy = [Atom(a.symbol, a.x, a.y, a.z) for a in self.atoms]
        metadata_copy = self.metadata.copy()

        # Start with current values and override with kwargs
        new_attrs = {
            "charge": self.charge,
            "mult": self.mult,
            "name": self.name,
            "atoms": atoms_copy,
            "metadata": metadata_copy,
        }
        new_attrs.update(kwargs)

        debug(f"Creating copy of molecule {self.name} with overrides: {kwargs}")
        return Molecule(**new_attrs)

    @staticmethod
    def _parse_comment(
        comment: str,
    ) -> Dict[str, Any]:
        """Parse XYZ comment line for metadata.

        Supports two formats:
        - Key-value pairs like 'charge=1 mult=1'
        - JSON dict like '{"charge": 1, "mult": 1, "extra": "data"}'

        JSON format is preferred as it allows for easier extension.

        Returns:
            Dict containing all parsed values
        """
        debug(f"Parsing comment: '{comment}'")
        metadata = {}

        # Try to parse as JSON first
        try:
            metadata = json.loads(comment.strip())
            debug(f"Parsed JSON comment: {metadata}")
            return metadata
        except (json.JSONDecodeError, ValueError):
            # Fall back to the original parsing method
            tokens = comment.strip().split()
            for token in tokens:
                if "=" in token:
                    key, value = token.split("=", 1)
                    try:
                        # Try to convert to int if possible
                        metadata[key] = int(value)
                    except ValueError:
                        metadata[key] = value
                    debug(f"Found {key}: {metadata[key]}")
            debug(f"Parse result: {metadata}")
            return metadata

    @classmethod
    def from_xyz_file(
        cls,
        xyz_file: Path,
        charge: Optional[int] = None,
        mult: Optional[int] = None,
    ) -> Self:
        info(f"Creating molecule from XYZ file: {xyz_file}")
        debug(f"Input charge={charge}, mult={mult}")

        xyz_content = xyz_file.read_text()
        debug(f"Read XYZ file, length: {len(xyz_content)} bytes")

        lines = xyz_content.splitlines()
        n_atoms, comment, *atom_lines = lines

        debug(f"XYZ file contains {n_atoms} atoms according to header")
        debug(f"Comment line: '{comment}'")

        if int(n_atoms) != len(atom_lines):
            error(
                f"Invalid XYZ file {xyz_file}: expected {n_atoms} atoms but found {len(atom_lines)}"
            )
            raise ValueError("Invalid XYZ file, mismatch of n_atoms and actual atoms")

        # Parse metadata from comment
        metadata = cls._parse_comment(comment)
        xyz_charge = metadata.get("charge")
        xyz_mult = metadata.get("mult")

        if charge is None:
            charge = xyz_charge
            debug(f"Using charge from XYZ file: {charge}")

        if mult is None:
            mult = xyz_mult
            debug(f"Using mult from XYZ file: {mult}")

        if charge is None or mult is None:
            error(f"Failed to determine charge/mult for {xyz_file}")
            raise ValueError("Missing charge and/or multiplicity")

        debug(f"Final molecule parameters: charge={charge}, mult={mult}")

        # Parse atoms
        atoms = []
        for atom_line in atom_lines:
            parts = atom_line.split()
            if len(parts) < 4:
                error(f"Invalid atom line in XYZ file: {atom_line}")
                continue

            symbol, x, y, z = (
                parts[0],
                float(parts[1]),
                float(parts[2]),
                float(parts[3]),
            )
            atoms.append(Atom(symbol=symbol, x=x, y=y, z=z))

        info(f"Successfully created molecule from {xyz_file}")
        return cls(
            charge=charge, mult=mult, name=xyz_file.stem, atoms=atoms, metadata=metadata
        )

    @classmethod
    def from_xyz_files(
        cls,
        xyz_files_dir: Path,
        default_charge: Optional[int] = None,
        default_mult: Optional[int] = None,
    ) -> list[Self]:
        """Load multiple molecules from XYZ files in a directory.

        Provides default charge and multiplicity if not specified in the XYZ files.

        Args:
            xyz_files_dir: Directory containing XYZ files
            default_charge: Default charge to use if not specified in the XYZ file
            default_mult: Default multiplicity to use if not specified in the XYZ file

        Returns:
            List of Molecule objects
        """
        info(f"Loading molecules from directory: {xyz_files_dir}")
        debug(f"Default charge={default_charge}, default mult={default_mult}")

        xyz_files = list(Path(xyz_files_dir).glob("*.xyz"))
        info(f"Found {len(xyz_files)} XYZ files in directory")

        if not xyz_files:
            warning(f"No XYZ files found in {xyz_files_dir}")

        molecules = []
        for f in xyz_files:
            try:
                debug(f"Processing XYZ file: {f}")
                molecules.append(cls.from_xyz_file(f, default_charge, default_mult))
            except ValueError as e:
                error(f"Error processing XYZ file {f}: {e}")
                continue
            except Exception as e:
                error(f"Unexpected error processing XYZ file {f}: {e}", exc_info=True)
                continue

        info(f"Successfully loaded {len(molecules)} molecules")
        return molecules
