from rdkit.Chem.MolStandardize import rdMolStandardize

from .mol import Mol
from .mollibr import MolLibr


def complete_tautomers(mol:Mol, **kwargs) -> MolLibr:
    """Returns a library of enumerated tautomers.

    Args:
        mol (Mol): input molecule.

    Returns:
        MolLibr: a library of enumerated tautomers.
    """
    enumerator = rdMolStandardize.TautomerEnumerator()
    rdmols = list(enumerator.Enumerate(mol.rdmol))
    if len(rdmols) > 1: 
        return MolLibr(rdmols).unique().rename(mol.name, sep='.').compute(**kwargs)
    return MolLibr(rdmols).compute(**kwargs)