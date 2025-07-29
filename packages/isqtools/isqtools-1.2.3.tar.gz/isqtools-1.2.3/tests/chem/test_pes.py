import pytest

pyscf = pytest.importorskip("pyscf")
openfermion = pytest.importorskip("openfermion")


import numpy as np
from openfermion.linalg import get_ground_state, get_sparse_operator
from openfermion.transforms import get_fermion_operator
from pyscf import gto, scf

from isqtools.chem.utils import get_molecular_hamiltonian, parity


def test_pes():
    energies = []

    bond_lengths = [0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.05]
    for bond_length in bond_lengths:

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
        energies.append(energy)
    # print("PES:", energies)
    np.testing.assert_allclose(
        np.array(energies),
        np.array(
            [
                -0.9984155960160171,
                -1.0926299067451068,
                -1.1299047843229142,
                -1.1371170673457303,
                -1.1283618784581126,
                -1.1113394177361482,
                -1.090342176512763,
            ]
        ),
    )
