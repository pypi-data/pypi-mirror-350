import io
import copy
import json
import numpy as np
import ase

from collections.abc import Callable
from typing import Self

from mendeleev import element
from ase.optimize import FIRE

from rdkit import Chem
from rdkit.Chem import rdMolTransforms, AllChem, rdMolAlign, rdmolops
from rdkit.Chem.Draw import rdMolDraw2D
from PIL import Image

from rdworks.units import ev2kcalpermol, pm2angstrom
from rdworks.utils import recursive_round
from rdworks.xtb.wrapper import GFN2xTB
from rdworks.display import render_png, render_svg


class Conf:
    """Container for 3D conformers."""
    
    def __init__(self, molecule: str | Chem.Mol | None = None, name: str='') -> None:
        """Initialize.

        Args:
            molecule (Chem.Mol | MolBlock string): Molecule for 3D conformer.
            name (str): Name prefix of the generated conformers. Defaults to ''.

        Raises:
            ValueError: if `molecule` is not rdkit.Chem.Mol object.
        """
        assert isinstance(molecule, str | Chem.Mol) or molecule is None

        self.rdmol = None # must contain one and only one rdkit conformer
        self.name = name
        self.natoms = 0
        self.charge = 0 # molecular charge
        self.spin = 1 # molecular spin multiplicity for ASE
        self.props = {}

        if molecule is None:
            return

        if isinstance(molecule, str): # 3-D MolBLock string
            try:
                self.rdmol = Chem.MolFromMolBlock(molecule)
            except:
                ValueError(f'Conf() Error: invalid MolBlock string')

        elif isinstance(molecule, Chem.Mol): # 3-D
            try:
                self.rdmol = molecule
            except:
                ValueError(f'Conf() Error: invalid Chem.Mol object')

        num_atoms = self.rdmol.GetNumAtoms()
        tot_atoms = self.rdmol.GetNumAtoms(onlyExplicit=False)
        assert num_atoms == tot_atoms, "Conf() Error: missing hydrogens"
        self.natoms = num_atoms
        self.charge = rdmolops.GetFormalCharge(self.rdmol)
        self.props.update({'atoms': num_atoms})
     
        assert self.rdmol.GetConformer().Is3D(), "Conf() Error: not 3D"

        

    def __str__(self) -> str:
        """Returns a string representation.

        Returns:
            str: string representation.
        """
        return f"<rdworks.Conf({self.rdmol} name={self.name} atoms={self.natoms})>"
       

    def copy(self) -> Self:
        """Returns a copy of self.

        Returns:
            Self: `rdworks.Conf` object.
        """
        return copy.deepcopy(self)
    

    def rename(self, name:str) -> Self:
        """Rename and returns self.

        Args:
            name (str): a new name for conformers.

        Raises:
            ValueError: if `name` is not given.

        Returns:
            Self: `rdworks.Conf` object.
        """
        if not name:
            raise ValueError('rdworks.Conf.rename() expects a name')
        self.name = name
        self.rdmol.SetProp('_Name', name)
        return self
    

    def sync(self, coord: np.ndarray | list) -> Self:
        """Synchronize the conformer coordinates with the provided `coord`.

        Args:
            coord (np.array): 3D coordinates.

        Raises:
            ValueError: if `coord` does not have the correct shape (natoms, 3).

        Returns:
            Self: `rdworks.Conf` object.
        """
        if isinstance(coord, np.ndarray) and coord.shape != (self.natoms, 3):
            raise ValueError(f"`coord.shape` should be ({self.natoms},3)")
        elif isinstance(coord, list) and len(coord) != self.natoms:
            raise ValueError(f"`coord` should be length of {self.natoms}")
        for i, a in enumerate(self.rdmol.GetAtoms()):
            self.rdmol.GetConformer().SetAtomPosition(a.GetIdx(), coord[i])
        
        return self


    def set_torsion(self, i:int, j:int, k:int, l:int, degree:float) -> Self:
        """Set dihedral angle (i-j-k-l) in degrees.

        Args:
            i (int): atom index
            j (int): atom index
            k (int): atom index
            l (int): atom index
            degree (float): dihedral angle in degrees

        Returns:
            Self: modified Conf object
        """
        rdMolTransforms.SetDihedralDeg(self.rdmol.GetConformer(), i, j, k, l, degree)

        return self
    

    
    def optimize(self, 
                 calculator: str | Callable = 'MMFF94',
                 fmax:float=0.05, 
                 max_iter:int=1000,
                 **kwargs) -> Self:
        """Optimize 3D geometry.

        Args:
            calculator (str | Callable): MMFF94 (= MMFF), MMFF94s, UFF, or ASE calculator.
                `MMFF94` or `MMFF` - Intended for general use, including organic molecules and proteins, 
                    and primarily relies on data from quantum mechanical calculations. 
                    It's often used in molecular dynamics simulations.
                `MMFF94s` - A "static" variant of MMFF94, with adjusted parameters for out-of-plane 
                    bending and dihedral torsions to favor planar geometries for specific nitrogen atoms. 
                    This makes it better suited for geometry optimization studies where a static, 
                    time-averaged structure is desired. The "s" stands for "static".
                `UFF` - UFF refers to the "Universal Force Field," a force field model used for 
                    molecular mechanics calculations. It's a tool for geometry optimization, 
                    energy minimization, and exploring molecular conformations in 3D space. 
                    UFF is often used to refine conformers generated by other methods, 
                    such as random conformer generation, to produce more physically plausible 
                    and stable structures.
            fmax (float, optional): fmax for the calculator convergence. Defaults to 0.05.
            max_iter (int, optional): max iterations for the calculator. Defaults to 1000.
            
        Args for xTB:
            water (str, optional): water solvation model (choose 'gbsa' or 'alpb')
                alpb: ALPB solvation model (Analytical Linearized Poisson-Boltzmann).
                gbsa: generalized Born (GB) model with Surface Area contributions.

        Returns:
            Self: self
        """
        if isinstance(calculator, str) :
            
            PE_start = self.potential_energy(calculator)
            
            if calculator.lower() == 'xTB'.lower():
                water = kwargs.get('water', None)
                PE_final, self.rdmol = GFN2xTB(self.rdmol).optimize(water=water)

            elif calculator.lower() == 'MMFF94'.lower() or calculator.lower() == 'MMFF'.lower():
                retcode = Chem.rdForceFieldHelpers.MMFFOptimizeMolecule(self.rdmol, 
                                                                        mmffVariant='MMFF94',
                                                                        maxIters=max_iter)
                # returns 0 if the optimization converged
            elif calculator.lower() == 'MMFF94s'.lower():
                retcode = Chem.rdForceFieldHelpers.MMFFOptimizeMolecule(self.rdmol, 
                                                                        mmffVariant='MMFF94s',
                                                                        maxIters=max_iter)
                # returns 0 if the optimization converged
            elif calculator.lower() == 'UFF'.lower():
                retcode = Chem.rdForceFieldHelpers.UFFOptimizeMolecule(self.rdmol,
                                                                       maxIters=max_iter)
                # returns 0 if the optimization converged

            PE_final = self.potential_energy(calculator)
            
            self.props.update({
                'E_tot_init(kcal/mol)': PE_start , # energy before optimization
                'E_tot(kcal/mol)': PE_final, # energy after optimization
                'Converged' : retcode == 0, # True or False
            })
            
            return self

        else:
            # assuming ASE calculator
            with io.StringIO() as logfile:
                ase_atoms = ase.Atoms(symbols=self.symbols(), positions=self.positions())
                ase_atoms.info['charge'] = self.charge
                ase_atoms.info['spin'] = self.spin
                ase_atoms.calc = calculator
                FIRE(ase_atoms, logfile=logfile).run(fmax=fmax)
                lines = [l.strip().split()[1:] for l in logfile.getvalue().split('\n') if l.startswith('FIRE')]
                data = [(float(e), float(f)) for (_, _, e, f) in lines]
                self.props.update({
                    'E_tot_init(kcal/mol)': data[0][0] * ev2kcalpermol, # energy before optimization
                    'E_tot(kcal/mol)': data[-1][0] * ev2kcalpermol, # energy after optimization
                    'Converged' : data[-1][1] < fmax, # True or False
                })
                
                # update atomic coordinates
                return self.sync(ase_atoms.get_positions())
 
    

    ##################################################
    ### Endpoint methods
    ##################################################

    def check_bonds(self, tolerance:float=0.25) -> bool:
        """Check bond lengths.

        Args:
            tolerance (float, optional): tolerance from the sum of 
                van der Waals radii of bonded atoms. Defaults to 0.25 (A).

        Returns:
            bool: True if all bond lengths are accceptable.
        """

        for bond in self.rdmol.GetBonds():
            idx1 = bond.GetBeginAtomIdx()
            idx2 = bond.GetEndAtomIdx()
            nuc1 = self.rdmol.GetAtomWithIdx(idx1).GetAtomicNum()
            nuc2 = self.rdmol.GetAtomWithIdx(idx2).GetAtomicNum()
            sum_radii = (element(nuc1).vdw_radius + element(nuc2).vdw_radius) * pm2angstrom
            bond_length = rdMolTransforms.GetBondLength(self.rdmol.GetConformer(), idx1, idx2)
            if abs(bond_length - sum_radii) > tolerance:
                return False
            
        return True
    

    def positions(self) -> np.array:
        """Returns the coordinates.

        Returns:
            np.array: the coordinates.
        """
        return np.array(self.rdmol.GetConformer().GetPositions().tolist())


    def symbols(self) -> list[str]:
        """Returns the element symbols.

        Returns:
            list: list of element symbols.
        """
        return [ a.GetSymbol() for a in self.rdmol.GetAtoms() ]


    def numbers(self) -> list[int]:
        """Returns the atomic numbers.

        Returns:
            list: list of atomic numbers.
        """
        return [ a.GetAtomicNum() for a in self.rdmol.GetAtoms() ]


    def cog(self) -> np.array:
        """Returns the center of geometry (COG).

        Returns:
            np.array: the center of geometry (COG).
        """
        xyz = []
        for i in range(0, self.natoms):
            pos = self.rdmol.GetConformer().GetAtomPositions(i)
            xyz.append([pos.x, pos.y, pos.z])
        return np.mean(xyz, axis=0)


    def rg(self) -> float:
        """Returns the radius of gyration (Rg).

        Returns:
            float: the radius of gyration (Rg).
        """
        xyz = []
        for i in range(0, self.natoms):
            pos = self.rdmol.GetConformer().GetAtomPositions(i)
            xyz.append([pos.x, pos.y, pos.z])
        xyz = np.array(xyz)
        cog = np.mean(xyz, axis=0)
        a = xyz-cog
        b = np.einsum('ij,ij->i', a, a)
        return np.sqrt(np.mean(b))


    def potential_energy(self, calculator: str | Callable = 'MMFF94', **kwargs) -> float:
        """Get potential energy and set `E_tot(kcal/mol)` in the self.props.

        Args:
            calculator (str | Callable): MMFF94 (= MMFF), MMFF94s, UFF, or ASE calculator.
                `MMFF94` or `MMFF` - Intended for general use, including organic molecules and proteins, 
                    and primarily relies on data from quantum mechanical calculations. 
                    It's often used in molecular dynamics simulations.
                `MMFF94s` - A "static" variant of MMFF94, with adjusted parameters for out-of-plane 
                    bending and dihedral torsions to favor planar geometries for specific nitrogen atoms. 
                    This makes it better suited for geometry optimization studies where a static, 
                    time-averaged structure is desired. The "s" stands for "static".
                `UFF` - UFF refers to the "Universal Force Field," a force field model used for 
                    molecular mechanics calculations. It's a tool for geometry optimization, 
                    energy minimization, and exploring molecular conformations in 3D space. 
                    UFF is often used to refine conformers generated by other methods, 
                    such as random conformer generation, to produce more physically plausible 
                    and stable structures.

        Returns:
            float | None: potential energy in kcal/mol or None.
        """

        if isinstance(calculator, str):
            if calculator.lower() == 'xTB'.lower():
                water = kwargs.get('water', None)
                PE = GFN2xTB(self.rdmol).singlepoint(water=water)
            
            elif calculator.lower() == 'MMFF94'.lower() or calculator.lower() == 'MMFF'.lower():
                mp = Chem.rdForceFieldHelpers.MMFFGetMoleculeProperties(self.rdmol, mmffVariant='MMFF94')
                ff = Chem.rdForceFieldHelpers.MMFFGetMoleculeForceField(self.rdmol, mp)
                PE = ff.CalcEnergy()
            
            elif calculator.lower() == 'MMFF94s'.lower():
                mp = Chem.rdForceFieldHelpers.MMFFGetMoleculeProperties(self.rdmol, mmffVariant='MMFF94s')
                ff = Chem.rdForceFieldHelpers.MMFFGetMoleculeForceField(self.rdmol, mp)
                PE = ff.CalcEnergy()
            
            elif calculator.lower() == 'UFF'.lower():
                ff = Chem.rdForceFieldHelpers.UFFGetMoleculeForceField(self.rdmol)
                PE = ff.CalcEnergy()
            
            else:
                raise ValueError("Unsupported calculator")                
            
            self.props.update({'E_tot(kcal/mol)': PE})

            return PE
        
        else:
            try:
                ase_atoms = ase.Atoms(symbols=self.symbols(), positions=self.positions())
                ase_atoms.info['charge'] = self.charge
                ase_atoms.info['spin'] = self.spin
                ase_atoms.calc = calculator
                PE = ase_atoms.get_potential_energy() # np.array
                if isinstance(PE, float):
                    PE = ev2kcalpermol * PE
                elif isinstance(PE, np.ndarray | list):
                    PE = ev2kcalpermol * float(PE[0]) # np.float64 to float
                self.props.update({'E_tot(kcal/mol)': PE})
            
                return PE
            
            except:
                raise RuntimeError("ASE calculator error")


    def torsion_angle(self, i:int, j:int, k:int, l:int) -> float:
        """Get dihedral angle (i-j-k-l) in degrees.

        Args:
            i (int): atom index
            j (int): atom index
            k (int): atom index
            l (int): atom index

        Returns:
            float: dihedral angle in degrees.
        """
        degree = rdMolTransforms.GetDihedralDeg(self.rdmol.GetConformer(), i, j, k, l)

        return degree


    def dumps(self, key:str='') -> str:
        """Returns JSON dumps of the `props`.

        Args:
            key (str): a key for the `props` dictionary. Defaults to '' (all).

        Returns:
            str: JSON dumps.
        """
        if key:
            return json.dumps({key:self.props[key]})
        else:
            return json.dumps(self.props)
    

    def serialize(self, decimals:int=3) -> str:
        """Serialize information necessary to rebuild.

        Returns:
            str: serialized string for json.loads()
        """
        serialized = json.dumps({
            'name' : self.name, 
            'natoms': self.natoms, 
            'props' : recursive_round(self.props, decimals),
            'molblock' : self.to_molblock(),
            })

        return serialized


    def deserialize(self, serialized:str) -> Self:
        """De-serialize information and rebuild.

        Args:
            serialized (str): _description_

        Returns:
            Self: _description_
        """
        data = json.loads(serialized)

        self.name = data['name']
        self.natoms = data['natoms']
        self.props = data['props']
        self.rdmol = Chem.MolFromMolBlock(data['molblock'], sanitize=False, removeHs=False)

        return self


    def to_molblock(self) -> str:
        """Returns MolBlock"""
        return Chem.MolToMolBlock(self.rdmol)


    def to_xyz(self) -> str:
        """Returns XYZ formatted strings.

        Returns:
            str: XYZ formatted strings.
        """
        lines = [f'{self.natoms}', ' ']
        for e, (x, y, z) in zip(self.symbols(), self.positions()):
            lines.append(f'{e:5} {x:23.14f} {y:23.14f} {z:23.14f}')
        
        return '\n'.join(lines)


    def to_sdf(self, props:bool=True) -> str:
        """Returns the SDF-formatted strings.

        Args:
            props (bool, optional): include `props as SDF properties. Defaults to True.

        Returns:
            str: strings in the SDF format.
        """
        in_memory = io.StringIO()
        with Chem.SDWriter(in_memory) as f:
            rdmol = Chem.Mol(self.rdmol)
            rdmol.SetProp('_Name', self.name)
            if props:
                for k,v in self.props.items():
                    rdmol.SetProp(k, str(v))
            f.write(rdmol)
        return in_memory.getvalue()
    

    def to_png(self,
               width: int = 300, 
               height: int = 300,
               legend: str = '', 
               atom_index: bool = False, 
               highlight_atoms: list[int] | None = None,
               highlight_bonds: list[int] | None = None,
               redraw: bool = False,
               coordgen: bool = False,
               trim: bool = True) -> Image.Image:
        """Draw 2D molecule in PNG format.

        Args:
            width (int, optional): width. Defaults to 300.
            height (int, optional): height. Defaults to 300.
            legend (str, optional): legend. Defaults to ''.
            atom_index (bool, optional): whether to show atom index. Defaults to False.
            highlight_atoms (list[int] | None, optional): atom(s) to highlight. Defaults to None.
            highlight_bonds (list[int] | None, optional): bond(s) to highlight. Defaults to None.
            redraw (bool, optional): whether to redraw. Defaults to False.
            coordgen (bool, optional): whether to use coordgen. Defaults to False.
            trim (bool, optional): whether to trim white margins. Default to True.
        
        Returns:
            Image.Image: output PIL Image object.
        """
        
        return render_png(self.rdmol,
                          width = width, 
                          height = height, 
                          legend = legend, 
                          atom_index = atom_index, 
                          highlight_atoms = highlight_atoms,
                          highlight_bonds = highlight_bonds,
                          redraw = redraw, 
                          coordgen = coordgen, 
                          trim = trim)
    
    
    def to_svg(self,
               width: int = 300,
               height: int = 300,
               legend: str = '', 
               atom_index: bool = False, 
               highlight_atoms: list[int] | None = None,
               highlight_bonds: list[int] | None = None,
               redraw: bool = False,
               coordgen: bool = False,
               optimize: bool = True) -> str:
        """Draw 2D molecule in SVG format.

        Examples:
            For Jupyternotebook, wrap the output with SVG:

            >>> from IPython.display import SVG
            >>> SVG(libr[0].to_svg())

        Args:
            width (int, optional): width. Defaults to 300.
            height (int, optional): height. Defaults to 300.
            legend (str, optional): legend. Defaults to ''.
            atom_index (bool, optional): whether to show atom index. Defaults to False.
            highlight_atoms (list[int] | None, optional): atom(s) to highlight. Defaults to None.
            highlight_bonds (list[int] | None, optional): bond(s) to highlight. Defaults to None.
            redraw (bool, optional): whether to redraw. Defaults to False.
            coordgen (bool, optional): whether to use coordgen. Defaults to False.
            optimize (bool, optional): whether to optimize SVG string. Defaults to True.

        Returns:
            str: SVG string
        """
        return render_svg(self.rdmol, 
                          width = width, 
                          height = height, 
                          legend = legend, 
                          atom_index = atom_index, 
                          highlight_atoms = highlight_atoms,
                          highlight_bonds = highlight_bonds,
                          redraw = redraw, 
                          coordgen = coordgen, 
                          optimize = optimize)