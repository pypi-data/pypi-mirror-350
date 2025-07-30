from rdworks import Mol
from rdworks.xtb.wrapper import GFN2xTB

molecules = [
    ('CC(C)C1=C(C(=C(N1CC[C@H](C[C@H](CC(=O)O)O)O)C2=CC=C(C=C2)F)C3=CC=CC=C3)C(=O)NC4=CC=CC=C4', 
    'atorvastatin'),
]


def test_singlepoint():
    for (smiles, name) in molecules:
        mol = Mol(smiles, name).make_confs(n=50).optimize().drop_confs(similar=True, verbose=True).sort_confs()
        
        print("number of conformers=", mol.count())
        print("number of atoms=", mol.confs[0].natoms)

        gfn2xtb = GFN2xTB(mol.confs[0].rdmol, ncores=8)

        print("GFN2xTB.ready():", gfn2xtb.ready())
        print()

        print("GFN2xTB.singlepoint()")
        outdict = gfn2xtb.singlepoint()
        print(outdict)
        print()

        print("GFN2xTB.singlepoint(water='gbsa')")
        outdict = gfn2xtb.singlepoint(water='gbsa')
        print(outdict)
        print()

        print("GFN2xTB.singlepoint(water='alpb')")
        outdict = gfn2xtb.singlepoint(water='alpb')
        print(outdict)
        print()

# Do not use optimize. Fortran runtime error
# def test_optimize():
#      for (smiles, name) in molecules:
#         mol = Mol(smiles, name).make_confs(n=50).optimize().drop_confs(similar=True, verbose=True).sort_confs()
#         print("number of conformers=", mol.count())

#         print("GFN2xTB.optimize()")
#         outdict = GFN2xTB(mol.confs[0].rdmol, ncores=8).optimize(verbose=True)
#         print(outdict)
#         print()


if __name__ == '__main__':
    test_singlepoint()
    # test_optimize()