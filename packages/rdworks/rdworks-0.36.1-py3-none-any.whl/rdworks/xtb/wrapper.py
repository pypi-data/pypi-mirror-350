import os
import resource
import subprocess
import json
import tempfile
import logging

from pathlib import Path
from types import SimpleNamespace

from rdkit import Chem
from rdkit.Geometry import Point3D


main_logger = logging.getLogger()

# In ASE, the default energy unit is eV (electron volt).
# It will be converted to kcal/mol
# CODATA 2018 energy conversion factor
hartree2ev = 27.211386245988
hartree2kcalpermol = 627.50947337481
ev2kcalpermol = 23.060547830619026


class GFN2xTB:
    def __init__(self, molecule: Chem.Mol | None = None, ncores: int = 4):
        if isinstance(molecule, Chem.Mol):
            assert molecule.GetConformer().Is3D(), "requires 3D coordinates"
            self.rdmol = molecule
            self.natoms = molecule.GetNumAtoms()
            self.symbols = [ atom.GetSymbol() for atom in molecule.GetAtoms() ]
            self.positions = molecule.GetConformer().GetPositions().tolist()

        # Parallelisation
        os.environ['OMP_STACKSIZE'] = '4G'
        os.environ['OMP_NUM_THREADS'] = f'{ncores},1'
        os.environ['OMP_MAX_ACTIVE_LEVELS'] = '1'
        os.environ['MKL_NUM_THREADS'] = f'{ncores}'
        
        # unlimit the system stack
        resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))


    def version(self) -> str | None:
        """Check xtb version.

        Returns:
            str | None: version statement.
        """
        cmd = ['xtb', '--version']
        proc = subprocess.run(cmd, capture_output=True, text=True)
        assert proc.returncode == 0, "GFN2xTB() Error: xtb not available"
        for line in proc.stdout.split('\n'):
            line = line.strip()
            if 'version' in line:
                return line
        
        return None


    def to_xyz(self) -> str:
        """Export to XYZ formatted string.

        Returns:
            str: XYZ formatted string
        """
        lines = [f'{self.natoms}', ' ']
        for e, (x, y, z) in zip(self.symbols, self.positions):
            lines.append(f'{e:5} {x:23.14f} {y:23.14f} {z:23.14f}')
        
        return '\n'.join(lines)


    def load_xyz(self, geometry_path: Path) -> Chem.Mol:
        """Load geometry.

        Args:
            geometry_path (Path): pathlib.Path to the xyz 

        Returns:
            Chem.Mol: rdkit Chem.Mol object.
        """
        rdmol_opt = Chem.Mol(self.rdmol)
        with open(geometry_path, 'r') as f:
            for lineno, line in enumerate(f):
                if lineno == 0:
                    assert int(line.strip()) == self.natoms
                    continue
                elif lineno == 1: # comment or title
                    continue
                (symbol, x, y, z) = line.strip().split()
                x, y, z = float(x), float(y), float(z)
                atom = rdmol_opt.GetAtomWithIdx(lineno-2)
                assert symbol == atom.GetSymbol()
                rdmol_opt.GetConformer().SetAtomPosition(atom.GetIdx(), Point3D(x, y, z))
        
        return rdmol_opt


    def load_wbo(self, wbo_path: Path) -> dict[tuple[int, int], float]:
        """Load Wiberg bond order.

        Args:
            wbo_path (Path): path to the wbo file.

        Returns:
            dict(tuple[int, int], float): { (i, j) : wbo, ... } where i and j are atom indices for a bond.
        """

        with open(wbo_path, 'r') as f:
            # Wiberg bond order (WBO)
            Wiberg_bond_orders = {}
            for line in f:
                line = line.strip()
                if line:
                    # wbo output has 1-based indices
                    (i, j, wbo) = line.split()
                    # changes to 0-based indices
                    i = int(i) - 1
                    j = int(j) - 1
                    # wbo ouput indices are ascending order
                    ij = (i, j) if i < j else (j, i)
                    Wiberg_bond_orders[ij] = float(wbo)

            return Wiberg_bond_orders


    def singlepoint(self, water: str | None = None, verbose: bool = False) -> SimpleNamespace:
        """Calculate single point energy.
        
        Total energy from xtb output in atomic units (Eh, hartree) is converted to kcal/mol.

        Args:
            water (str, optional) : water solvation model (choose 'gbsa' or 'alpb')
                alpb: ALPB solvation model (Analytical Linearized Poisson-Boltzmann).
                gbsa: generalized Born (GB) model with Surface Area contributions.

        Returns:
            SimpleNamespace(PE(total energy in kcal/mol), charges, wbo) 
        """

        with tempfile.TemporaryDirectory() as temp_dir: # tmpdir is a string
            workdir = Path(temp_dir)
            if verbose:
                main_logger.info(f'xtb.singlepoint workdir= {temp_dir}')
            
            geometry_path = workdir / 'geometry.xyz'
            xtbout_path = workdir / 'xtbout.json'
            wbo_path = workdir / 'wbo'
            
            with open(geometry_path, 'w') as geometry:
                geometry.write(self.to_xyz())
            
            cmd = ['xtb', geometry_path.as_posix()]
            
            options = ['--gfn', '2', '--json']
            
            if water is not None and isinstance(water, str):
                if water == 'gbsa':
                    options += ['--gbsa', 'H2O']
                elif water == 'alpb':
                    options += ['--alpb', 'water']
            
            # 'xtbout.json', 'xtbrestart', 'xtbtopo.mol', 'charges', and 'wbo' files will be 
            # created in the current working directory.
            proc = subprocess.run(cmd + options, cwd=temp_dir, capture_output=True, text=True)

            # if proc.returncode == 0:
            #     print("Standard Output:")
            #     print(proc.stdout)
            # else:
            #     print("Error:")
            #     print(proc.stderr)
            
            if proc.returncode == 0 and xtbout_path.is_file():
                with open(xtbout_path, 'r') as f:
                    datadict = json.load(f) # takes the file object as input

                Wiberg_bond_orders = self.load_wbo(wbo_path)

                return SimpleNamespace(
                    PE = datadict['total energy'] * hartree2kcalpermol, 
                    charges = datadict['partial charges'], 
                    wbo = Wiberg_bond_orders, 
                    ) 
        
        # something went wrong if it reaches here          
        return SimpleNamespace()
                        


    def optimize(self, water: str | None = None, verbose: bool = False) -> SimpleNamespace:
        """Optimize geometry.

        Fortran runtime errror:
            At line 852 of file ../src/optimizer.f90 (unit = 6, file = 'stdout')
            Fortran runtime error: Missing comma between descriptors
            (1x,"("f7.2"%)")
                        ^
            Error termination.

        Args:
            water (str, optional) : water solvation model (choose 'gbsa' or 'alpb')
                alpb: ALPB solvation model (Analytical Linearized Poisson-Boltzmann).
                gbsa: generalized Born (GB) model with Surface Area contributions.

        Returns:
            (total energy in kcal/mol, optimized geometry)
        """
        with tempfile.TemporaryDirectory() as temp_dir: # tmpdir is a string
            workdir = Path(temp_dir)
            if verbose:
                main_logger.info(f'xtb.optimize workdir= {temp_dir}')
            
            geometry_path = workdir / 'geometry.xyz'
            xtbout_path = workdir / 'xtbout.json'
            xtbopt_path = workdir / 'xtbopt.xyz'
            wbo_path = workdir / 'wbo'
            
            with open(geometry_path, 'w') as geometry:
                geometry.write(self.to_xyz())

            cmd = ['xtb', geometry_path.as_posix()]

            options = ['--opt', '--gfn', '2', '--json']

            if water is not None and isinstance(water, str):
                if water == 'gbsa':
                    options += ['--gbsa', 'H2O']
                elif water == 'alpb':
                    options += ['--alpb', 'water']

            proc = subprocess.run(cmd + options, cwd=temp_dir, capture_output=True, text=True)

            if proc.returncode == 0 and xtbout_path.is_file():
                with open(xtbout_path, 'r') as f:
                    datadict = json.load(f) # takes the file object as input
                
                Wiberg_bond_orders = self.load_wbo(wbo_path)
                rdmol_opt = self.load_xyz(xtbopt_path)
            
                return SimpleNamespace(
                        PE = datadict['total energy'] * hartree2kcalpermol,
                        charges = datadict['partial charges'],
                        wbo = Wiberg_bond_orders,
                        geometry = rdmol_opt,
                )

        # something went wrong if it reaches here
        return SimpleNamespace()
    

    def esp(self, water: str | None = None, verbose: bool = False) -> None:
        """Calculate electrostatic potential
        
        Example:
            v = py3Dmol.view()
            v.addVolumetricData(dt,
                                "cube.gz", {
                                    'isoval': 0.005,
                                    'smoothness': 2,
                                    'opacity':.9,
                                    'voldata': esp,
                                    'volformat': 'cube.gz',
                                    'volscheme': {
                                        'gradient':'rwb',
                                        'min':-.1,
                                        'max':.1,
                                        }
                                    });
            v.addModel(dt,'cube')
            v.setStyle({'stick':{}})
            v.zoomTo()
            v.show()
        """
        with tempfile.TemporaryDirectory() as temp_dir: # tmpdir is a string
            workdir = Path(temp_dir)
            if verbose:
                main_logger.info(f'xtb.optimize workdir= {temp_dir}')
            
            geometry_path = workdir / 'geometry.xyz'
            xtb_esp_dat = workdir / 'xtb_esp_dat'

            with open(geometry_path, 'w') as geometry:
                geometry.write(self.to_xyz())

            cmd = ['xtb', geometry_path.as_posix()]

            options = ['--esp', '--gfn', '2']

            if water is not None and isinstance(water, str):
                if water == 'gbsa':
                    options += ['--gbsa', 'H2O']
                elif water == 'alpb':
                    options += ['--alpb', 'water']

            proc = subprocess.run(cmd + options, cwd=temp_dir, capture_output=True, text=True)
            # output files: xtb_esp.cosmo, xtb_esp.dat, xtb_esp_profile.dat

            if proc.returncode == 0 and xtb_esp_dat.is_file():
                with open(xtb_esp_dat, 'r') as f:
                    pass
        
        return None