import pytest

pyscf = pytest.importorskip("pyscf")


import numpy as np
from pyscf import cc, gto, scf


def test_model():
    bond_length = 0.75

    atom = f"""
     H 0 0 0
     H 0 0 {bond_length}
    """

    basis = "sto-3g"
    charge = 0
    spin = 0

    mymol = gto.M(atom=atom, basis=basis, charge=charge, spin=spin, verbose=0)

    nao = int(mymol.nao)
    assert nao == 2
    # print("Spin orbs:", nao)

    # Hartree-Fock calculation
    myhf = scf.RHF(mymol).run()
    print(type(myhf.e_tot))
    assert np.isclose(myhf.e_tot, -1.11615145)
    # print(f"HF energy by pyscf: {myhf.e_tot:.8f}")

    # CCSD(T) calculation
    # mycc = cc.CCSD(myhf).run()
    # et = mycc.ccsd_t()
    # assert np.isclose(mycc.e_tot + et, -1.1371172451631748)
    # print(f"CCSD(T) energy: {mycc.e_tot + et:.8f}")
