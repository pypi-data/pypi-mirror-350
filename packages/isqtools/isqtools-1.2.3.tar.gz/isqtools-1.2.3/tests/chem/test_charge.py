import pytest

pyscf = pytest.importorskip("pyscf")


from pyscf import gto


def test_charge():
    bond_length = 0.75

    atom = f"""
     H 0 0 0
     H 0 0 {bond_length}
    """

    basis = "sto-3g"
    charge = 0
    spin = 0
    mymol = gto.M(atom=atom, basis=basis, charge=charge, spin=spin, verbose=3)
    myhf = mymol.HF()
    myhf.kernel()
    myhf.analyze()
