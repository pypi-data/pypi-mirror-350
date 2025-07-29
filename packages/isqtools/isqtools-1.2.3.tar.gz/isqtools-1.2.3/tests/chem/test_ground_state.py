import pytest

pyscf = pytest.importorskip("pyscf")
openfermion = pytest.importorskip("openfermion")


import numpy as np
from openfermion.linalg import get_ground_state, get_sparse_operator
from openfermion.transforms import get_fermion_operator
from pyscf import gto, scf

from isqtools.chem.utils import get_molecular_hamiltonian, parity


def test_gs():
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
    myhf = scf.RHF(mymol).run()
    molecular_hamiltonian = get_molecular_hamiltonian(myhf)
    fermion_hamiltonian = get_fermion_operator(molecular_hamiltonian)
    qubit_hamiltonian = parity(fermion_hamiltonian, nao * 2, nao)
    qubit_hamiltonian.compress()
    sparse_operator = get_sparse_operator(qubit_hamiltonian)
    energy, _ = get_ground_state(sparse_operator)
    assert np.isclose(energy, -1.1371170673457314)
    # print("Energy:", energy)
