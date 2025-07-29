from apb.structure.features.accessibility.datatypes import MaxSASASource


def get_max_sasa_map(source: MaxSASASource) -> dict[str, float]:
    """Returns a dictionary with keys as residues and maximimum SASA as values

    Args:
        source:
            A source for experimentally determined maximum solvent exposed surface
            areas.
    """
    if source not in _residue_sasa_scales:
        raise NotImplementedError(f"'{source}' has not been implemented.")

    return _residue_sasa_scales[source]


_ahmad: dict[str, float] = {
    "ALA": 110.2,
    "ARG": 229.0,
    "ASN": 146.4,
    "ASP": 144.1,
    "CYS": 140.4,
    "GLN": 178.6,
    "GLU": 174.7,
    "GLY": 78.7,
    "HIS": 181.9,
    "ILE": 183.1,
    "LEU": 164.0,
    "LYS": 205.7,
    "MET": 200.1,
    "PHE": 200.7,
    "PRO": 141.9,
    "SER": 117.2,
    "THR": 138.7,
    "TRP": 240.5,
    "TYR": 213.7,
    "VAL": 153.7,
}

_miller: dict[str, float] = {
    "ALA": 113.0,
    "ARG": 241.0,
    "ASN": 158.0,
    "ASP": 151.0,
    "CYS": 140.0,
    "GLN": 189.0,
    "GLU": 183.0,
    "GLY": 85.0,
    "HIS": 194.0,
    "ILE": 182.0,
    "LEU": 180.0,
    "LYS": 211.0,
    "MET": 204.0,
    "PHE": 218.0,
    "PRO": 143.0,
    "SER": 122.0,
    "THR": 146.0,
    "TRP": 259.0,
    "TYR": 229.0,
    "VAL": 160.0,
}

_sander: dict[str, float] = {
    "ALA": 106.0,
    "ARG": 248.0,
    "ASN": 157.0,
    "ASP": 163.0,
    "CYS": 135.0,
    "GLN": 198.0,
    "GLU": 194.0,
    "GLY": 84.0,
    "HIS": 184.0,
    "ILE": 169.0,
    "LEU": 164.0,
    "LYS": 205.0,
    "MET": 188.0,
    "PHE": 197.0,
    "PRO": 136.0,
    "SER": 130.0,
    "THR": 142.0,
    "TRP": 227.0,
    "TYR": 222.0,
    "VAL": 142.0,
}

_wilke: dict[str, float] = {
    "ALA": 129.0,
    "ARG": 274.0,
    "ASN": 195.0,
    "ASP": 193.0,
    "CYS": 167.0,
    "GLN": 225.0,
    "GLU": 223.0,
    "GLY": 104.0,
    "HIS": 224.0,
    "ILE": 197.0,
    "LEU": 201.0,
    "LYS": 236.0,
    "MET": 224.0,
    "PHE": 240.0,
    "PRO": 159.0,
    "SER": 155.0,
    "THR": 172.0,
    "TRP": 285.0,
    "TYR": 263.0,
    "VAL": 174.0,
}

_residue_sasa_scales: dict[MaxSASASource, dict[str, float]] = {
    MaxSASASource.AHMAD: _ahmad,
    MaxSASASource.MILLER: _miller,
    MaxSASASource.SANDER: _sander,
    MaxSASASource.WILKE: _wilke,
}
