from gypsum_dl import GypsumDL

def test_gypsum_dl():
    for i, smiles in enumerate([
        'Oc1ccccc1',
        'CCC=O',
        'ClC(C[C@@](Cl)(C)F)(F)C(C(C)C)=O',
        'FC(C(I)=C(CC(I)(Cl)C)CC)=C(Cl)C',
        'CC(CC)=C(C/C(I)=C(C)/F)Cl',
        'CC([C@@H]1CC[C@H](C(C)(C)C)CC1)(C)C',
        ]):
        st = GypsumDL(smiles)
        print(smiles)
        for state in st:
            print(state)