import numpy as np
from openfermion.transforms import get_fermion_operator
from pyscf import gto, scf

from isqtools.chem.utils import (
    get_molecular_hamiltonian,
    openfermion_to_pauligates,
    parity,
)

bond_length = 1.30

atom = f"""
 H 0 0 0
 Li 0 0 {bond_length}
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
# print("Qubit hamiltonian:", qubit_hamiltonian)
coeffs, gates_group = openfermion_to_pauligates(qubit_hamiltonian)
print("Coefficients:", coeffs)
print("Gates:", gates_group)
