import importlib.resources
import pandas as pd

from rdkit import Chem

# adapted from https://github.com/dptech-corp/Uni-pKa/enumerator

class IonizedStates:
    # Unreasonable chemical structures
    unreasonable_patterns = [
        Chem.MolFromSmarts(s) for s in [
            "[#6X5]",
            "[#7X5]",
            "[#8X4]",
            "[*r]=[*r]=[*r]",
            "[#1]-[*+1]~[*-1]",
            "[#1]-[*+1]=,:[*]-,:[*-1]",
            "[#1]-[*+1]-,:[*]=,:[*-1]",
            "[*+2]",
            "[*-2]",
            "[#1]-[#8+1].[#8-1,#7-1,#6-1]",
            "[#1]-[#7+1,#8+1].[#7-1,#6-1]",
            "[#1]-[#8+1].[#8-1,#6-1]",
            "[#1]-[#7+1].[#8-1]-[C](-[C,#1])(-[C,#1])",
            # "[#6;!$([#6]-,:[*]=,:[*]);!$([#6]-,:[#7,#8,#16])]=[C](-[O,N,S]-[#1])",
            # "[#6]-,=[C](-[O,N,S])(-[O,N,S]-[#1])",
            "[OX1]=[C]-[OH2+1]",
            "[NX1,NX2H1,NX3H2]=[C]-[O]-[H]",
            "[#6-1]=[*]-[*]",
            "[cX2-1]",
            "[N+1](=O)-[O]-[H]",
        ]]

    smarts_path = importlib.resources.files('rdworks.predefined.ionized')
    protonation_patterns = pd.read_csv(smarts_path / 'simple_smarts_pattern.csv')

    def __init__(self, smiles:str):
        self.smiles = Chem.CanonSmiles(smiles)
        self.rdmol = Chem.MolFromSmiles(self.smiles)
        self.rdmol_H = Chem.AddHs(self.rdmol)
        self.charge = Chem.GetFormalCharge(self.rdmol_H)
        self.charge_max =  2
        self.charge_min = -2
        # initial states
        self.states = {self.smiles : (self.rdmol_H, self.charge)}
        # initial protonation sites
        self.protonation_sites = {self.smiles : self.set_protonation_sites(self.smiles)}
        # generate initial states
        self.protonate(self.smiles)

    
    def get_protonation_sites(self) -> dict:
        return self.protonation_sites

    
    def get_states_by_charge(self) -> dict:
        self.ensemble()
        data = {}
        for smiles, (romol, charge) in self.states.items():
            if charge in data:
                data[charge].append(smiles)
            else:
                data[charge] = [smiles]

        return data

    def get_states(self) -> list:
        return [smiles for smiles in self.states]
    

    def get_states_mol(self) -> list[Chem.Mol]:
        return [romol for smiles, (romol, charge) in self.states.items()]
    

    def get_num_states(self) -> int:
        return len(self.states)

    
    @staticmethod
    def clean_smiles(rdmol:Chem.Mol) -> str:
        Chem.SanitizeMol(rdmol)
        rdmol = Chem.MolFromSmiles(Chem.MolToSmiles(rdmol))
        rdmol_H = Chem.AddHs(rdmol)
        rdmol = Chem.RemoveHs(rdmol_H)
        return Chem.CanonSmiles(Chem.MolToSmiles(rdmol))


    @staticmethod
    def set_protonation_sites(smiles:str) -> tuple:
        subject = Chem.MolFromSmiles(smiles)
        subject = Chem.AddHs(subject)
        charge = Chem.GetFormalCharge(subject)        
        indices = [] # atom indices of protonation/deprotonation site(s)
        for i, name, smarts, smarts_index, acid_or_base in IonizedStates.protonation_patterns.itertuples():
            pattern = Chem.MolFromSmarts(smarts)
            matches = subject.GetSubstructMatches(pattern)
            # returns a list of tuples, where each tuple contains the indices 
            # of the atoms in the molecule that match the substructure query
            # ex. ((1,), (2,), (3,))
            if len(matches) > 0:
                smarts_index = int(smarts_index)
                indices += [(match[smarts_index], acid_or_base) for match in matches]
        return (list(set(indices)), subject, charge)


    @staticmethod
    def reasonable(romol:Chem.Mol) -> bool:
        return all([len(romol.GetSubstructMatches(p)) == 0 for p in IonizedStates.unreasonable_patterns])

        
    def protonate(self, smiles:str) -> int:
        num_added_states = 0
        
        if smiles not in self.protonation_sites:
            self.protonation_sites[smiles] = self.set_protonation_sites(smiles)   
        
        (indices, subject, charge) = self.protonation_sites[smiles]
        
        if (charge >= self.charge_max) or (charge <= self.charge_min):
            # formal charge will be increased or decreased by protonation/deprotonation
            # so, if the charge of current state is already max or min
            # there is nothing to do
            return num_added_states
            
        for (i, acid_or_base) in indices:
            edmol = Chem.RWMol(subject) # edmol preserves Hs
            if acid_or_base == 'A': # de-protonate
                A = edmol.GetAtomWithIdx(i)
                if A.GetAtomicNum() == 1:
                    X = A.GetNeighbors()[0] # there must be only one neighbor
                    charge = X.GetFormalCharge() - 1
                    X.SetFormalCharge(charge)
                    edmol.RemoveAtom(i)
                else:
                    bonded_H_indices = [ H.GetIdx() for H in A.GetNeighbors() if H.GetAtomicNum() == 1 ]
                    nH = len(bonded_H_indices)
                    assert nH > 0, f"Cannot deprotonate an atom (idx={i}; no H)"
                    charge = A.GetFormalCharge() - 1
                    A.SetFormalCharge(charge)
                    edmol.RemoveAtom(bonded_H_indices[0])
            
            elif acid_or_base == 'B': # protonate
                B = edmol.GetAtomWithIdx(i)
                assert B.GetAtomicNum() > 1, f"Cannot protonate an atom (idx={i}; {B.GetAtomicNum()})"
                charge = B.GetFormalCharge() + 1
                B.SetFormalCharge(charge)
                nH = B.GetNumExplicitHs()
                B.SetNumExplicitHs(nH+1)
                edmol = Chem.AddHs(edmol)
            
            # Clean up and save SMILES
            state_smiles = IonizedStates.clean_smiles(edmol)
            state_mol = Chem.MolFromSmiles(state_smiles)
            state_mol = Chem.AddHs(state_mol)
            state_charge = Chem.GetFormalCharge(state_mol)
            if self.reasonable(state_mol):
                if state_smiles in self.states:
                    continue
                self.states[state_smiles] = (state_mol, state_charge)
                num_added_states += 1

        return num_added_states

    
    def ensemble(self) -> None:
        num_added_states = None       
        while num_added_states is None or num_added_states > 0:
            states = self.states.copy()
            for smiles in states:
                num_added_states = self.protonate(smiles)