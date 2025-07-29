# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Some useful functions of quantum chemistry.
This file is inspired by TenCirChem and OpenFermion.
TenCirChem: https://github.com/tencent-quantum-lab/TenCirChem
OpenFermion: https://quantumai.google/openfermion
"""

from __future__ import annotations

from itertools import product
from typing import Any

import numpy as np

try:
    from pyscf import ao2mo
    from pyscf.gto import M
    from pyscf.mcscf import CASCI
    from pyscf.scf.hf import RHF
except Exception:
    RHF = Any
    M = Any

try:
    from openfermion import (
        FermionOperator,
        QubitOperator,
        binary_code_transform,
        parity_code,
    )
    from openfermion.ops.representations import InteractionOperator
    from openfermion.utils import hermitian_conjugated
except Exception:
    InteractionOperator = Any
    FermionOperator = Any
    QubitOperator = Any

TOLERANCE = 1e-8


def spin_orb_from_int(
    int1e: np.ndarray,
    int2e: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Spin orbital coefficients obtained from electron integrals.

    Args:
        int1e: Single electron integration.
        int2e: Double electron integration.

    Returns:
        One body coefficients and two body coefficients.

    """

    n_orb = int1e.shape[0]  # orbitals
    if int1e.shape != (n_orb, n_orb):
        raise ValueError(f"Invalid one-body integral array shape: {int1e.shape}")
    if int2e.shape != (n_orb, n_orb, n_orb, n_orb):
        raise ValueError(f"Invalid two-body integral array shape: {int2e.shape}")

    n_sorb = n_orb * 2  # spin orbitals
    one_body_coefficients = np.zeros(
        (
            n_sorb,
            n_sorb,
        )
    )
    two_body_coefficients = np.zeros(
        (
            n_sorb,
            n_sorb,
            n_sorb,
            n_sorb,
        )
    )

    one_body_coefficients[
        :n_orb,
        :n_orb,
    ] = one_body_coefficients[n_orb:, n_orb:] = int1e

    for p, q, r, s in product(range(n_sorb), repeat=4):
        # a_p^\dagger a_q^\dagger a_r a_s
        if ((p < n_orb) == (s < n_orb)) and ((q < n_orb) == (r < n_orb)):
            # note the different orders of the indices
            two_body_coefficients[p, q, r, s] = int2e[
                p % n_orb,
                s % n_orb,
                q % n_orb,
                r % n_orb,
            ]

    # Truncate
    one_body_coefficients[np.absolute(one_body_coefficients) < TOLERANCE] = 0.0
    two_body_coefficients[np.absolute(two_body_coefficients) < TOLERANCE] = 0.0

    return one_body_coefficients, two_body_coefficients


def canonical_mo_coeff(mo_coeff: np.ndarray) -> np.ndarray:
    """Make the first large element positive all elements smaller than 1e-5 is
    highly unlikely (at least 1e10 basis).

    Args:
        mo_coeff: Molecular orbital coefficient.

    Returns:
        Molecular orbital coefficient after truncation.

    """
    largest_elem_idx = np.argmax(1e-5 < np.abs(mo_coeff), axis=0)
    largest_elem = mo_coeff[
        (
            largest_elem_idx,
            np.arange(len(largest_elem_idx)),
        )
    ]

    return mo_coeff * np.sign(largest_elem).reshape(1, -1)


def get_int_from_hf(
    hf: RHF,
    active_space: tuple = None,
) -> tuple[np.ndarray, np.ndarray, float]:
    """Use pyscf to get one- and two-electron integrals, as well as electron
    energies from Hartree-Fock.

    Args:
        hf: Hartree-Fock from ``pyscf``.
        active_space: active space for CASCI calculation.

    Returns:
        Electronic integrals and electronic energy.

    """

    if not isinstance(hf, RHF):
        raise TypeError(f"hf object must be RHF class, got {type(hf)}")

    m = hf.mol
    assert hf.mo_coeff is not None
    hf.mo_coeff = canonical_mo_coeff(hf.mo_coeff)
    if active_space is None:
        nelecas = m.nelectron
        ncas = m.nao
    else:
        nelecas, ncas = active_space
    casci = CASCI(hf, ncas, nelecas)
    int1e, e_core = casci.get_h1eff()
    int2e = ao2mo.restore("s1", casci.get_h2eff(), ncas)

    return int1e, int2e, e_core


def get_int_from_mol(
    mol: M,
    C: np.array,
) -> tuple[np.ndarray, np.ndarray, float]:
    """Use pyscf to get one- and two-electron integrals, as well as electron
    energies from ``mol``. Do not use Hartree-Fock molecular coefficients as a
    starting point.

    Args:
        mol: molecule(mol) from ``pyscf``.
        C: Custom orbital coefficients.

    Returns:
        Electronic integrals and electronic energy.

    """

    e_core = mol.energy_nuc()
    AO = mol.intor("int2e", aosym=1)
    h = mol.get_hcore()
    # h = mol.intor("int1e_kin") + mol.intor("int1e_nuc")
    # C = hf.mo_coeff
    int1e = C.T @ h @ C
    # this can be optimized by ``opt_einsum``
    int2e = np.einsum("uvkl, up, vq, kr, ls -> pqrs", AO, C, C, C, C)
    return int1e, int2e, e_core


def get_molecular_hamiltonian(
    hf: RHF,
) -> InteractionOperator:
    """Get get molecular hamiltonian.

    Args:
        hf: Hartree-Fock from ``pyscf``.

    Returns:
        Molecular hamiltonian by ``openfermion``.

    """
    int1e, int2e, e_core = get_int_from_hf(hf)
    one_body_coefficients, two_body_coefficients = spin_orb_from_int(
        int1e,
        int2e,
    )
    return InteractionOperator(
        e_core, one_body_coefficients, 1 / 2 * two_body_coefficients
    )


def ex_op_to_fop(
    ex_op: list,
    with_conjugation: bool = False,
) -> FermionOperator:
    """Excited operators to Fermion operators.

    Args:
        ex_op: Excitation operators.
        with_conjugation: Conjugate or not.

    Returns:
        Fermion operators.

    """
    if len(ex_op) == 2:
        fop = FermionOperator(f"{ex_op[0]}^ {ex_op[1]}")
    else:
        assert len(ex_op) == 4
        fop = FermionOperator(f"{ex_op[0]}^ {ex_op[1]}^ {ex_op[2]} {ex_op[3]}")
    if with_conjugation:
        fop = fop - hermitian_conjugated(fop)
    return fop


def reverse_qop_idx(
    op: QubitOperator,
    n_qubits: int,
) -> QubitOperator:
    """Reverse qubit operators."""
    ret = QubitOperator()
    for pauli_string, value in op.terms.items():
        # internally QubitOperator assumes ascending index
        pauli_string = tuple(
            reversed(
                [
                    (
                        n_qubits - 1 - idx,
                        symbol,
                    )
                    for idx, symbol in pauli_string
                ]
            )
        )
        ret.terms[pauli_string] = value
    return ret


def reverse_fop_idx(
    op: FermionOperator,
    n_qubits: int,
) -> FermionOperator:
    """Reverse fermion operators."""
    ret = FermionOperator()
    for word, v in op.terms.items():
        word = tuple([(n_qubits - 1 - idx, symbol) for idx, symbol in word])
        ret.terms[word] = v
    return ret


def parity(
    fermion_operator: FermionOperator,
    n_modes: int,
    n_elec: int,
) -> QubitOperator:
    """Performs parity transformation.

    Args:
        fermion_operator: The fermion operator.
        n_modes: The number of spin-orbitals.
        n_elec: The number of electrons.

    Returns:
         Qubit operators.

    """
    qubit_operator = _parity(
        reverse_fop_idx(
            fermion_operator,
            n_modes,
        ),
        n_modes,
    )
    res = 0
    assert n_modes % 2 == 0
    reduction_indices = [n_modes // 2 - 1, n_modes - 1]
    phase_alpha = (-1) ** (n_elec // 2)
    for qop in qubit_operator:
        # qop example: 0.5 [Z1 X2 X3]
        pauli_string, coeff = next(iter(qop.terms.items()))
        # pauli_string example: ((1, 'Z'), (2, 'X'), (3, 'X'))
        # coeff example: 0.5
        new_pauli_string = []
        for idx, symbol in pauli_string:
            is_alpha = idx <= reduction_indices[0]
            if idx in reduction_indices:
                if symbol in ["X", "Y"]:
                    # discard this term because the bit will never change
                    continue
                else:
                    assert symbol == "Z"
                    if is_alpha:
                        coeff *= phase_alpha
                    continue
            if not is_alpha:
                idx -= 1
            new_pauli_string.append((idx, symbol))
        qop.terms = {tuple(new_pauli_string): coeff}
        res += qop
    return res


def _parity(fermion_operator, n_modes):
    return binary_code_transform(fermion_operator, parity_code(n_modes))


def openfermion_to_pauligates(qubit_hamiltonian):
    """Extract coefficients and gates of qubit hamiltonian.

    Args:
        qubit_hamiltonian: Qubit hamiltonian.

    Returns:
        Coefficients and corresponding Pauli operators.

    """
    coeffs = []
    gates_group = []
    for idx, (gate, coeff) in enumerate(qubit_hamiltonian.terms.items()):
        coeffs.append(coeff)
        if idx == 0:
            continue
        gates_group.append(gate)
    return coeffs, gates_group


def get_isq_pauli_gates(
    gates_group: list,
    num_qubits: int,
) -> list:
    """Convert the Pauli operator into a list to facilitate isq recognition.

    Args:
        gates_group: Pauli operators from ``openfermion_to_pauligates``.
        num_qubits: Number of qubits.

    Returns:
        Isq representation of Pauli operator.

    """
    pauli_gates = []
    for gates in gates_group:
        gates_temp = [0] * num_qubits
        for gate in gates:
            if gate[1] == "X":
                gates_temp[gate[0]] = 1
            elif gate[1] == "Y":
                gates_temp[gate[0]] = 2
            elif gate[1] == "Z":
                gates_temp[gate[0]] = 3
        pauli_gates.extend(gates_temp)
    return pauli_gates
