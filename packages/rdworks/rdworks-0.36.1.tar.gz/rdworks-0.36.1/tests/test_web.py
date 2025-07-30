import pathlib
import unittest
from typing import List, Tuple

from rdkit import Chem

import rdworks

datadir = pathlib.Path('/home/shbae/bucket/rdworks/data')
# python >=3.12 raises SyntaxWarning: invalid escape sequence
# To address this warning in general, we can make the string literal a raw string literal r"...". 
# Raw string literals do not process escape sequences. 
# For example, r"\n" is treated simply as the characters \ and n and not as a newline escape sequence.
drug_smiles = [
    "Fc1cc(c(F)cc1F)C[C@@H](N)CC(=O)N3Cc2nnc(n2CC3)C(F)(F)F", # [0]
    r"O=C(O[C@@H]1[C@H]3C(=C/[C@H](C)C1)\C=C/[C@@H]([C@@H]3CC[C@H]2OC(=O)C[C@H](O)C2)C)C(C)(C)CC",
    "C[C@@H](C(OC(C)C)=O)N[P@](OC[C@@H]1[C@H]([C@@](F)([C@@H](O1)N2C=CC(NC2=O)=O)C)O)(OC3=CC=CC=C3)=O",
    "C1CNC[C@H]([C@@H]1C2=CC=C(C=C2)F)COC3=CC4=C(C=C3)OCO4",
    "CC1=C(C=NO1)C(=O)NC2=CC=C(C=C2)C(F)(F)F",
    "CN1[C@@H]2CCC[C@H]1CC(C2)NC(=O)C3=NN(C4=CC=CC=C43)C", # [5] - Granisetron
    "CCCN1C[C@@H](C[C@H]2[C@H]1CC3=CNC4=CC=CC2=C34)CSC",
    "CCC1=C(NC2=C1C(=O)C(CC2)CN3CCOCC3)C", # [7] Molidone
    r"C[C@H]1/C=C/C=C(\C(=O)NC2=C(C(=C3C(=C2O)C(=C(C4=C3C(=O)[C@](O4)(O/C=C/[C@@H]([C@H]([C@H]([C@@H]([C@@H]([C@@H]([C@H]1O)C)O)C)OC(=O)C)C)OC)C)C)O)O)/C=N/N5CCN(CC5)C)/C",
    r"C=CC1=C(N2[C@@H]([C@@H](C2=O)NC(=O)/C(=N\O)/C3=CSC(=N3)N)SC1)C(=O)O",
    "CC1=C(N=CN1)CSCCNC(=NC)NC#N", # [10] - Cimetidine
    """C1=C(N=C(S1)N=C(N)N)CSCC/C(=N/S(=O)(=O)N)/N""",
    "C1CC(CCC1C2=CC=C(C=C2)Cl)C3=C(C4=CC=CC=C4C(=O)C3=O)O",
    "CN(CC/C=C1C2=CC=CC=C2SC3=C/1C=C(Cl)C=C3)C",
    "CN(C)CCCN1C2=CC=CC=C2CCC3=C1C=C(C=C3)Cl",
    "CN1CCCC(C1)CC2C3=CC=CC=C3SC4=CC=CC=C24", # [15] - Methixene
    "CCN(CC)C(C)CN1C2=CC=CC=C2SC3=CC=CC=C31",
    "CC(=O)OC1=CC=CC=C1C(=O)O",
    "C1=CC(=C(C=C1F)F)C(CN2C=NC=N2)(CN3C=NC=N3)O",
    "CC(=O)NC[C@H]1CN(C(=O)O1)C2=CC(=C(C=C2)N3CCOCC3)F", # [19]
    ]

drug_names = [
    "Sitagliptin", "Simvastatin", "Sofosbuvir", "Paroxetine", "Leflunomide",
    "Granisetron", "Pergolide", "Molindone", "Rifampin", "Cefdinir",
    "Cimetidine", "Famotidine", "Atovaquone", "Chlorprothixene", "Clomipramine",
    "Methixene",  "Ethopropazine", "Aspirin", "Fluconazole", "Linezolid",
    ]

# Lahey, S.-L. J., Thien Phuc, T. N. & Rowley, C. N. 
# Benchmarking Force Field and the ANI Neural Network Potentials for the 
# Torsional Potential Energy Surface of Biaryl Drug Fragments. 
# J. Chem. Inf. Model. 60, 6258–6268 (2020)

torsion_dataset_smiles = [
    "C1(N2C=CC=C2)=NC=CC=N1",
    "C1(C2=NC=NC=N2)=CC=CC=C1",
    "C1(N2C=CC=C2)=CC=CC=C1",
    "O=C(N1)C=CC=C1C2=COC=C2",
    "C1(C2=CC=CN2)=CC=CC=C1",
    "C1(C2=NC=CN2)=CC=CC=C1",
    "C1(C2=NC=CC=N2)=NC=CC=N1",
    "O=C(N1)C=CC=C1C2=NC=CN2",
    ]

torsion_dataset_names=["20", "39", "10", "23", "07", "09",  "12", "29"]


from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit.Chem import BRICS, AllChem


def fragmented(rdmol:Chem.Mol, 
                  min_atoms:int=5, 
                  max_atoms:int=17) -> List[Chem.Mol]:
    """BRICS decompose and returns fragments"""
    dummy = Chem.MolFromSmiles('*')
    hydro = Chem.MolFromSmiles('[H]')
    frag_set = BRICS.BRICSDecompose(rdmol)
    lfrag_rdmol = []
    for frag_smi in frag_set:
        # if '.' in frag_smi :
        (_, frag_rdmol) = rdworks.desalt_smiles(frag_smi)
        # replace dummy atom(s) with [H]
        frag_rdmol_H = AllChem.ReplaceSubstructs(frag_rdmol, dummy, hydro, True)[0]
        frag_rdmol = Chem.RemoveHs(frag_rdmol_H)
        frag_smi = Chem.MolToSmiles(frag_rdmol)
        # filter out molecules which are too small or too big
        na = frag_rdmol.GetNumAtoms()
        if na < min_atoms or na > max_atoms : 
            continue
        lfrag_rdmol.append(frag_rdmol)
    return lfrag_rdmol


class TestRdwork(unittest.TestCase):


    def test_80(self):
        libr = rdworks.MolLibr(drug_smiles, drug_names).qed(progress=False)
        for mol in libr:
            print(mol.dumps(decimals=2))


    def test_81(self):
        libr = rdworks.MolLibr(torsion_dataset_smiles[:2], torsion_dataset_names[:2])
        libr = libr.make_confs(n_rel=2.0, progress=False)
        libr = libr.nn_opt(gpu=True, log="unittest_81.log")
        libr = libr.drop_confs(similar=True, similar_rmsd=0.3, window=15.0).rename()
        for mol in libr:
            print(mol.to_sdf(confs=True, props=False))
            print()


    def test_82(self):
        libr = rdworks.MolLibr(torsion_dataset_smiles, torsion_dataset_names)
        libr = libr.make_confs(n_rel=2.0, progress=False)
        libr = libr.drop_confs(similar=True).rename()
        libr = libr.rd_torsion(interval=15)
        with open('unittest_82_MMFF94.html', 'w') as f:
            f.write(libr.to_html())
        for mol in libr:
            print(mol.dumps('torsion', decimals=2))


    def test_83(self):
        libr = rdworks.MolLibr(
            [torsion_dataset_smiles[0], 
             torsion_dataset_smiles[1],
             torsion_dataset_smiles[0],
             ]
            ,[torsion_dataset_names[0], 
              torsion_dataset_names[1],
              torsion_dataset_names[0],
              ])
        libr = libr.make_confs(n_rel=2.0, progress=False)
        libr = libr.nn_opt(model='ANI-2x', gpu=True, log="unittest_83.log")
        libr = libr.drop_confs(similar=True).rename()
        libr.to_sdf("unittest_83.sdf", confs=True)
        libr = libr.nn_torsion()
        with open('unittest_83.html', 'w') as f:
            f.write(libr.to_html())
        for mol in libr:
            print(mol.dumps('torsion', decimals=2))


    def test_84(self):
        libr = rdworks.MolLibr(drug_smiles[:4], drug_names[:4])
        for mol in libr:
            adhoc_libr = rdworks.MolLibr(rdworks.scaffold_tree(mol.rdmol)).rename(prefix=mol.name)
            adhoc_libr.to_png(f'unittest_84_{mol.name}.png')


    def test_85(self):
        libr = rdworks.MolLibr(drug_smiles[:4], drug_names[:4])
        for mol in libr:
            adhoc_libr = rdworks.MolLibr(rdworks.scaffold_network(mol.rdmol)).rename(prefix=mol.name)
            adhoc_libr.to_png(f'unittest_85_{mol.name}.png')


    def test_86(self):
        libr = rdworks.MolLibr(drug_smiles[:1], drug_names[:1])
        libr = libr.make_confs(n_rel=1.5, progress=False)
        libr = libr.align_confs()
        libr.to_sdf('unittest_86.sdf', confs=True)


    def test_87(self):
        mol = rdworks.Mol("N=C1O[C@@H](CN1)CN2C[C@H](O[C@H](C2)C)C", "stereoisomer")
        mol = mol.make_confs()
        mol.confs[0].props.update({'atoms': 64, 'E_tot(kcal/mol)': 165.7063872640784, 'E_tot(eV)': -52747.664965882745, 'Converged': True, 'E_rel(kcal/mol)': 4.2511657967033765, 'cluster': 2})
        mol.confs[1].props.update({'atoms': 64, 'E_tot(kcal/mol)': 186.8104697966623, 'E_tot(eV)': -52747.81861570482, 'Converged': False, 'E_rel(kcal/mol)': 0.7079167256014014, 'cluster': 3})
        mol.confs[2].props.update({'atoms': 64, 'E_tot(kcal/mol)': 168.38130165387048, 'E_tot(eV)': -52747.82449193913, 'Converged': True, 'E_rel(kcal/mol)': 0.5724075432187451, 'cluster': 0})
        out = mol.drop_confs()


    def test_89(self):
        from rdkit.Chem import AllChem
        from rdkit import Chem

        mol = rdworks.Mol('Cc1nc2c(-c3ccc(C(F)(F)F)cc3F)nc(N3C[C@@H](C)O[C@@H](c4cnn(C5CC5)c4)C3)nc2c(=O)n1C', 'ER')
        fraglist = fragmented(mol.rdmol)
        for _ in fraglist:
            print(Chem.MolToSmiles(_))
        # mol = mol.make_confs()
        # scaffolds = []
        # rdmol = mol.rdmol # 3D and hydrogens
        # dummy = Chem.MolFromSmiles('*')
        # hydro = Chem.MolFromSmiles('[H]')
        # for _ in rdworks.scaffold_network(rdmol):
        #     print(Chem.MolToSmiles(_))
        #     _H = AllChem.ReplaceSubstructs(_, dummy, hydro, True)[0]
        #     _ = Chem.RemoveHs(_H)
        #     scaffolds.append((mol.descriptor_f['RotBonds'](_), 
        #                     mol.descriptor_f['HAC'](_), 
        #                     mol.descriptor_f['MolWt'](_),
        #                     _))
        # print()
        # for _ in sorted(scaffolds, key=lambda v: (v[0], -v[1], -v[2])):
        #     print(_[0], _[1], _[2], Chem.MolToSmiles(_[3]))

        # smallest number of rotatable bonds (i.e. 0)
        # largest HAC or MolWt
        # rigid_core = sorted(scaffolds, key=lambda v: (v[0], -v[1], -v[2]))[0][-1]
        # try:
        #     indices = rdmol.GetSubstructMatches(rigid_core)[0]
        #     atomMap = [(i, i) for i in indices]
        #     for conf in self.confs:
        #         # rdMolAlign.AlignMol does not take symmetry into account
        #         # but we will use atom indices for alignment anyway.
        #         rmsd = rdMolAlign.AlignMol(prbMol=conf.rdmol, refMol=rdmol, atomMap=atomMap)
        # except:
        #     print("align_confs(to_scaffold=True) failed:")
        #     print("  rdmol=", Chem.MolToSmiles(rdmol))
        #     print("  rigid_core=", Chem.MolToSmiles(rigid_core))
        #     print("  rdmol.GetSubstructMatches(rigid_core)=", rdmol.GetSubstructMatches(rigid_core))
        #     pass


    def test_90(self):
        from rdworks import mae_to_dict

        d = mae_to_dict(datadir / "ligprep-SJ506rev-out.mae")
        print(len(d))

        i = 0 # molecule index

        for molecule in d:
            print(molecule['f_m_ct']['i_epik_Tot_Q'])
            print(molecule['f_m_ct']['r_epik_Population'])
            print(molecule['f_m_ct']['s_epik_macro-pKa'])

        while True:
            try:
                data = []
                basic_pKa = []
                acidic_pKa = []
                for iv, (v, dv) in enumerate(zip(d[i]['f_m_ct']['m_atom']['r_epik_H2O_pKa'], 
                                           d[i]['f_m_ct']['m_atom']['r_epik_H2O_pKa_uncertainty'])):
                    try:
                        pKa = float(v) # empty value = <>
                        dpKa = float(dv) # empty value = <>
                        print(iv, pKa, dpKa)
                    except:
                        continue

                    atomic_number = int(d[i]['f_m_ct']['m_atom']['i_m_atomic_number'][iv])
                    formal_charge = int(d[i]['f_m_ct']['m_atom']['i_m_formal_charge'][iv])
                    if atomic_number != 1 and pKa >= 5.0: # basic
                        basic_pKa.append(pKa)
                    if atomic_number == 1 and pKa <= 9.0: # acidic (already protonated by Epik)
                        acidic_pKa.append(pKa)
                    # data.append(pKa)
                    print(iv+1, atomic_number, formal_charge, pKa, "basic=", basic_pKa, "acidic=", acidic_pKa)
                if basic_pKa :
                    molecule_pKa = max(basic_pKa)
                elif acidic_pKa:
                    molecule_pKa = min(acidic_pKa)
                else:
                    molecule_pKa = 8.81
                print("Row=",i+1, "pKa=", molecule_pKa, data, "basic=", basic_pKa, "acidic=", acidic_pKa)
                # print()
                i += 1
            except:
                break


    def test_91(self):
        from rdworks.nnbatchtorsion import get_torsion_atom_indices
        import ast
        with Chem.MaeMolSupplier((datadir / "ligprep-SJ506rev-out.mae").as_posix(),
                                 removeHs=False) as supp:
            for m in supp:
                # print()
                # smiles = Chem.MolToSmiles(m) # creates _smilesAtomOutputOrder
                # print(smiles)
                # idxord = ast.literal_eval(m.GetProp("_smilesAtomOutputOrder"))
                # print(idxord)
                # idxmap = {a.GetIdx():idxord.index(a.GetIdx()) for a in m.GetAtoms()}
                # print(idxmap)
                # for a in m.GetAtoms():
                #     if a.GetSymbol() in ['O','F']:
                #         print(a.GetSymbol(), a.GetIdx(), idxmap[a.GetIdx()], idxord.index(a.GetIdx()))
                # print("="*60)

                # n = Chem.MolFromSmiles(smiles)
                # n = Chem.AddHs(n)
                # _ = Chem.MolToSmiles(n) # creates _smilesAtomOutputOrder
                # print(_)
                # idxord = ast.literal_eval(n.GetProp("_smilesAtomOutputOrder"))
                # for a in n.GetAtoms():
                #     if a.GetSymbol() in ['O','F']:
                #         print(a.GetSymbol(), a.GetIdx(), idxord.index(a.GetIdx()))
                # old_atom_index = list(map(int, m.GetProp("_smilesAtomOutputOrder")[1:-2].split(",")))

                m_2d = Chem.RemoveHs(m)
                AllChem.Compute2DCoords(m_2d)
                libr = rdworks.MolLibr([m_2d]).rd_torsion(interval=15)
                # libr = rdworks.MolLibr([smiles]).rd_torsion(interval=15)
                print(get_torsion_atom_indices(libr[0].confs[0].rdmol))
                with open('unittest_91x_MMFF94.html', 'w') as f:
                    f.write(libr.to_html())

        #         smiles = Chem.MolToSmiles(m)
        #         print(smiles)
        #         mol = rdworks.Mol(smiles, 'untitiled')
        #         new_atom_index = list(map(int, mol.rdmol.GetProp("_smilesAtomOutputOrder")[1:-2].split(",")))
                
        #         libr = rdworks.MolLibr([mol]).rd_torsion()
        #         last_atom_index = list(map(int, libr[0].confs[0].rdmol.GetProp("_smilesAtomOutputOrder")[1:-2].split(",")))
        #         # print("old=", old_atom_index)
        #         print("new=", new_atom_index)
        #         print("last=", last_atom_index)

        #         with open("unittest_91c_MMFF94.html", "w") as f:
        #             f.write(libr.to_html())
        # libr = rdworks.read_mae(datadir / "ligprep-SJ506rev-out.mae", confs=True)
        # with open("unittest_91.svg", "w") as svg:
        #     svg.write(libr.to_image(width=400, height=400, index=True))
        # print(libr[0].props['idxmap'])
        # libr.to_sdf("unittest_91.sdf", confs=True)
        # new_atom_index = list(map(int, libr[0].confs[0].rdmol.GetProp("_smilesAtomOutputOrder")[1:-2].split(",")))
        # print(new_atom_index)

        

    def test_93(self):
        d = rdworks.mae_to_dict(datadir / "ligprep-SJ506rev-out.mae")
        print(len(d))
        print(type(d[0]['f_m_ct']['m_atom']['r_epik_H2O_pKa']))
        print(len(d[0]['f_m_ct']['m_atom']['r_epik_H2O_pKa']))
        print(d[0]['f_m_ct']['m_atom']['r_epik_H2O_pKa'])
        print(d[0]['f_m_ct']['m_bond'])


    def test_94(self):
        # mol = rdworks.Mol('CCC(CC(C)CC1CCC1)C(CC(=O)O)N', 'ex')
        mol = rdworks.Mol('FC(C(C#N)=C1)=CC=C1NC([C@@H](C2=C3C=CC=C2)[C@@H](C4=CC=C[N+]([O-])=C4)N(CC(F)(F)F)C3=O)=O', 'SJ506')
        with open("unittest_94.svg", "w") as f:
            f.write(mol.to_svg(index=True))


    def test_95(self):
        import uuid
        from rdworks.schrodinger import ligprep_qikprop, qp_desc

        workdir = pathlib.Path("/home/shbae/bucket/rdworks/test/workdir")
        
        print(qp_desc)

        infile = workdir / f'ligprep_{uuid.uuid1()}.smi'
        libr = rdworks.MolLibr(['FC(C(C#N)=C1)=CC=C1NC([C@@H](C2=C3C=CC=C2)[C@@H](C4=CC=C[N+]([O-])=C4)N(CC(F)(F)F)C3=O)=O'], ['SJ506'])
        libr.to_smi(infile)
        
        # # ionized/tautomerized states
        results = ligprep_qikprop(infile, remove_files=True)
        for name, states in results.items():
            for state in states:
                print(name, state)

    def test_96(self):
        from rdworks import fix_decimals_in_dict, fix_decimals_in_list
        state_mol = rdworks.Mol('Cc1nc2cc(Cl)nc(Cl)c2nc1C', 'A-1250')
        state_mol = state_mol.make_confs(method='ETKDG').optimize('MMFF94')
        state_mol = state_mol.rename() # rename conformers
        state_mol = state_mol.drop_confs(similar=True, similar_rmsd=0.3)
        state_mol = state_mol.sort_confs().rename()
        state_mol = state_mol.align_confs(method='rigid_fragment')
        state_mol = state_mol.cluster_confs('QT', threshold=1.0, sort='energy')
        print(state_mol.name, {k:v for k,v in state_mol.props.items()})
        for conf in state_mol.confs:
            conf.props = fix_decimals_in_dict(conf.props, decimals=2)
            print(conf.name, {k:v for k,v in conf.props.items()})
    


if __name__ == '__main__':
    print(f'rdworks version {rdworks.__version__}')
    unittest.main(verbosity=2)

    # for single test
    # ex. $ python test.py TestRdwork.test_25_make_confs
