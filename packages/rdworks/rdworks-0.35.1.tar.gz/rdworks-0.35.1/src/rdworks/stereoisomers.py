from typing import List, Tuple, Union, Optional

from rdkit import Chem
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions

from .mol import Mol
from .mollibr import MolLibr


def _enum_stereoisomers(rdmol:Chem.Mol) -> List[Chem.Mol]:
    """Returns enumerated stereoisomers.

    Args:
        rdmol (Chem.Mol): input molecule.

    Returns:
        List[Chem.Mol]: a list of enumerated stereoisomers.
    """
    return list(EnumerateStereoisomers(
        rdmol, 
        options=StereoEnumerationOptions(
            tryEmbedding=False,
            onlyUnassigned=True,
            maxIsomers=1024,
            rand=None,
            unique=True,
            onlyStereoGroups=False,
            )))


def _enum_ring_bond_stereo(rdmol:Chem.Mol, ring_bond_stereo_info:List[Tuple], 
                           override:bool=False) -> List[Chem.Mol]:
    """Enumerates unspecified double bond stereochemistry (cis/trans).

    <pre>
    a1        a4  a1
      \      /      \
       a2=a3         a2=a3 
                          \
                          a4
    </pre>

    Args:
        rdmol (Chem.Mol): input molecule.
        ring_bond_stereo_info (List[Tuple]): 
            ring_bond_stereo_info will be set when .remove_stereo() is called.
            bond_stereo_info = [(bond_idx, bond_stereo_descriptor), ..] where
            bond_stereo_descriptor is `Chem.StereoDescriptor.Bond_Cis` or
            `Chem.StereoDescriptor.Bond_Trans`, or `Chem.StereoDescriptor.NoValue`.
        override (bool, optional): _description_. Defaults to False.

    Returns:
        List[Chem.Mol]: list of enumerated stereoisomers.
    """
    isomers = []
    for bond_idx, bond_stereo_desc in ring_bond_stereo_info:
        if (bond_stereo_desc == Chem.StereoDescriptor.NoValue) or override:
            bond = rdmol.GetBondWithIdx(bond_idx)
            (a2,a3) = (bond.GetBeginAtom(), bond.GetEndAtom())
            a2_idx = a2.GetIdx()
            a3_idx = a3.GetIdx()
            a1_idx = sorted([(a.GetIdx(), a.GetAtomicNum()) for a in a2.GetNeighbors() if a.GetIdx() != a3_idx], key=lambda x: x[1], reverse=True)[0][0]
            a4_idx = sorted([(a.GetIdx(), a.GetAtomicNum()) for a in a3.GetNeighbors() if a.GetIdx() != a2_idx], key=lambda x: x[1], reverse=True)[0][0]
            bond.SetStereoAtoms(a1_idx, a4_idx) # need to set reference atoms
            # cis
            bond.SetStereo(Chem.BondStereo.STEREOCIS)
            isomers.append(Chem.Mol(rdmol))
            # trans
            bond.SetStereo(Chem.BondStereo.STEREOTRANS)
            isomers.append(Chem.Mol(rdmol))
    return isomers


def complete_stereoisomers(molecular_input:Union[Mol, str, Chem.Mol], name:Optional[str]=None, 
                           std:bool=False, override:bool=False, **kwargs) -> MolLibr:
    """Completes stereoisomers and returns a rdworks.MolLibr.

    Args:
        molecular_input (Union[Mol, str, Chem.Mol]): input molecule.
        name (Optional[str], optional): name of the molecule. Defaults to None.
        std (bool, optional): whether to standardize the input. Defaults to False.
        override (bool, optional): whether to override input stereoisomers. Defaults to False.

    Raises:
        TypeError: if `molecular_input` is not rdworks.Mol, SMILES, or rdkit.Chem.Mol object.

    Returns:
        MolLibr: a library of complete stereoisomers.
    """
    if isinstance(molecular_input, Mol):
        if name:
            mol = molecular_input.rename(name)
        else:
            mol = molecular_input
    elif isinstance(molecular_input, str) or isinstance(molecular_input, Chem.Mol):
        mol = Mol(molecular_input, name, std)
    else:
        raise TypeError('complete_stereoisomers() expects rdworks.Mol, SMILES or rdkit.Chem.Mol object')
    
    ring_bond_stereo_info = mol.get_ring_bond_stereo()
    
    if override:
        mol = mol.remove_stereo()
    
    rdmols = _enum_stereoisomers(mol.rdmol)
    # ring bond stereo is not properly enumerated
    # cis/trans information is lost if stereochemistry is removed,
    # which cannot be enumerated by EnumerateStereoisomers() function
    # so _enum_bond_stereo() is introduced
    if len(ring_bond_stereo_info) > 0:
        ring_cis_trans = []
        for rdmol in rdmols:
            ring_cis_trans += _enum_ring_bond_stereo(rdmol,
                                                     ring_bond_stereo_info,
                                                     override=override)
        if len(ring_cis_trans) > 0:
            rdmols = ring_cis_trans
    
    if len(rdmols) > 1:
        libr = MolLibr(rdmols).unique().rename(mol.name, sep='.').compute(**kwargs)
    else:
        libr = MolLibr(rdmols).rename(mol.name).compute(**kwargs)
    
    for _ in libr:
        _.props.update(mol.props)
    
    return libr