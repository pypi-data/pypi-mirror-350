import gzip
from io import BytesIO
from pathlib import Path

import biotite.structure.io as structio
import biotite.structure.io.pdb as pdb
from biotite.structure.io.pdbx import BinaryCIFFile, get_structure, set_structure

from apb.structure.utils import RECOGNIZED_STRUCTURE_FILETYPES, structure_name_and_extension
from apb.types import Pathish, ProteinStructure


def save_structure(path: Pathish, structure: ProteinStructure) -> Path:
    path = Path(path)

    _, ext = structure_name_and_extension(path)
    if ext is None:
        raise ValueError(
            f"Unsupported file format {path}. Supported extensions are: "
            f"{RECOGNIZED_STRUCTURE_FILETYPES}"
        )

    if ext == ".pdb.gz":
        # Biotite doesn't manage gzip ops, so we do it ourselves
        with gzip.open(path, "wt") as gz_file:
            pdbfile = pdb.PDBFile()
            pdb.set_structure(pdbfile, structure)
            pdbfile.write(gz_file)
    else:
        # Otherwise delegate to biotite's high-level IO API
        structio.save_structure(path, structure)

    return path


def load_structure(path: Pathish) -> ProteinStructure:
    path = Path(path)

    _, ext = structure_name_and_extension(path)
    if ext is None:
        raise ValueError(
            f"Unsupported file format {path}. Supported extensions are: "
            f"{RECOGNIZED_STRUCTURE_FILETYPES}"
        )

    if ext == ".pdb.gz":
        # Biotite doesn't manage gzip ops, so we do it ourselves
        with gzip.open(path, "rt") as gz_file:
            pdbfile = pdb.PDBFile.read(gz_file)
            structure = pdb.get_structure(pdbfile, model=1)
    else:
        # Otherwise delegate to biotite's high-level IO API
        structure = structio.load_structure(path)

    assert isinstance(structure, ProteinStructure)
    return structure


def structure_to_bytes(structure: ProteinStructure) -> bytes:
    with BytesIO() as buffer:
        bcif = BinaryCIFFile()
        set_structure(bcif, structure)
        bcif.write(buffer)
        return buffer.getvalue()


def structure_from_bytes(byte_representation: bytes) -> ProteinStructure:
    with BytesIO(byte_representation) as buffer:
        file = BinaryCIFFile.read(buffer)
        structure = get_structure(file, model=1)
        assert isinstance(structure, ProteinStructure)
        return structure
