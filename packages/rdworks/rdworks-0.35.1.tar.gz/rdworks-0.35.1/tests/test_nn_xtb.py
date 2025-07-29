from pathlib import Path

import rdworks

datadir = Path(__file__).parent.resolve() / "data"
workdir = Path(__file__).parent.resolve() / "outfiles"
workdir.mkdir(exist_ok=True)

# library for single point and optimization
libr1 = rdworks.MolLibr(["N=C1O[C@@H](CN1)CN2C[C@H](O[C@H](C2)C)C"], ["stereoisomer"])
libr1 = libr1.make_confs(progress=False).drop_confs(similar=True, similar_rmsd=0.3).rename()

# Lahey, S.-L. J., Thien Phuc, T. N. & Rowley, C. N. 
# Benchmarking Force Field and the ANI Neural Network Potentials for the 
# Torsional Potential Energy Surface of Biaryl Drug Fragments. 
# J. Chem. Inf. Model. 60, 6258–6268 (2020)

torsion_dataset_smiles = [
    "C1(C2=CC=CN2)=CC=CC=C1",
    "C1(C2=NC=CN2)=CC=CC=C1",
    "C1(N2C=CC=C2)=NC=CC=N1",
    "C1(C2=NC=NC=N2)=CC=CC=C1",
    "C1(N2C=CC=C2)=CC=CC=C1",
    "O=C(N1)C=CC=C1C2=COC=C2",
    "C1(C2=NC=CC=N2)=NC=CC=N1",
    "O=C(N1)C=CC=C1C2=NC=CN2",
    ]

torsion_dataset_names=["07", "09","20", "39", "10", "23", "12", "29"]

# library for torsion scan
libr2 = rdworks.MolLibr(torsion_dataset_smiles, torsion_dataset_names)
libr2 = libr2.make_confs(n=50, progress=False)



def test_single_point_xtb():
    xtb = libr1.xtb_singlepoint(method="GFN2-xTB").sort_confs()
    xtb.align_confs().to_sdf(workdir / "test_single_point_gfn2_xtb.sdf", confs=True)

def test_single_point_aimnet2():
    aimnet2 = libr1.nn_singlepoint(model='AIMNET').sort_confs()
    aimnet2.align_confs().to_sdf(workdir / "test_single_point_aimnet2.sdf", confs=True)
    
def test_single_point_ani2x():
    ani2x = libr1.nn_singlepoint(model='ANI-2x').sort_confs()
    ani2x.align_confs().to_sdf(workdir / "test_single_point_ani2x.sdf", confs=True)

def test_optimize_xtb():
    xtb = libr1.xtb_opt(method="GFN2-xTB", log=workdir / "test_optimize_xtb.log")
    xtb = xtb.drop_confs(similar=True, similar_rmsd=0.3, k=1).rename()
    xtb.align_confs().to_sdf(workdir / "test_optimize_xtb.sdf", confs=True)


def test_optimize_nn():
    aimnet2 = libr1.nn_opt(model="AIMNET", gpu=True, log=workdir / "test_optimize_aimnet2.log")
    aimnet2.align_confs().to_sdf(workdir / "test_torsion_aimnet2.sdf", confs=True)
    # with open(workdir / "test_torsion_nn.html", "w") as f:
    #     f.write(libr_nn.to_html())

    ani2x = libr1.nn_opt(model="ANI-2x", gpu=True, log=workdir / "test_optimize_ani2x.log")
    ani2x = ani2x.drop_confs(similar=True, similar_rmsd=0.3, k=1).rename()
    ani2x.align_confs().to_sdf(workdir / "test_optimize_ani2x.sdf", confs=True)
    # with open(workdir / 'test_optimize_nn.html', 'w') as f:
    #     f.write(libr.to_html())


def test_torsion_rd():
    rd = libr2.rd_torsion()
    rd.align_confs().to_sdf(workdir / "test_torsion_rd.sdf", confs=True)
    # with open(workdir / "test_torsion_rd.html", "w") as f:
    #     f.write(libr_rd.to_html())


def test_torsion_xtb():
    xtb = libr2.xtb_torsion(method="GFN2-xTB")
    xtb.align_confs().to_sdf(workdir / "test_torsion_xtb.sdf", confs=True)
    # with open(workdir / "test_torsion_xtb.html", "w") as f:
    #     f.write(libr_xtb.to_html())


def test_torsion_nn():
    aimnet2 = libr2.nn_torsion(model="AIMNET")
    aimnet2.align_confs().to_sdf(workdir / "test_torsion_aimnet2.sdf", confs=True)
    # with open(workdir / "test_torsion_nn.html", "w") as f:
    #     f.write(libr_nn.to_html())

    ani2x = libr2.nn_torsion(model="ANI-2x")
    ani2x.align_confs().to_sdf(workdir / "test_torsion_ani2x.sdf", confs=True)
    # with open(workdir / "test_torsion_nn.html", "w") as f:
    #     f.write(libr_nn.to_html())
