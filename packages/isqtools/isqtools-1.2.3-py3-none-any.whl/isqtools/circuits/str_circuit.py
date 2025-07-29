# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Python quantum circuit class.
We recommend using ``isqc`` to compile and generate the Qics instruction set to
build quantum circuits. However, to guarantee support for building circuits
via python, we built ``StrCircuit``. This class constructs quantum circuits in
the form of strings. This method cannot use the advanced features of ``isqc``
and is not recommended.
"""

from __future__ import annotations

import itertools
import re
from collections.abc import Sequence
from typing import Any

from isqtools.backend import AbstractBackend

from .abstract_circuit import AbstractCircuit

Tensor = Any


class StrCircuitError(Exception):
    """Python string quantum circuits error."""


class StrCircuit(AbstractCircuit):
    """Python string quantum circuit class.

    Attributes:
        num_qubits: Number of qubits simulated.
        backend: The backend on which the task runs can be a simulator or
                 hardware.
        sample: Whether to enable sampling mode. When the backend is a
                simulator, you can ``sample`` or ``probs``. If the backend is
                hardware, you can only enable the sampling mode.
        shots: When the sampling mode is enabled, this parameter can specify
               the shots number.
        qcis_list: Use list to record each Qcis instruction set.

    """

    def __init__(
        self,
        num_qubits: int | None,
        backend: AbstractBackend,
        sample: bool = False,
        shots: int = 100,
    ) -> None:
        super().__init__(
            backend=backend,
            sample=sample,
            shots=shots,
        )

        self.qcis_list = []  # to record qcis
        self._qbit_init(num_qubits)
        self.num_qubits = num_qubits

    @property
    def qcis(self) -> str:
        """Join ``qcis_list`` to get qcis strings."""
        return "\n".join(self.qcis_list)

    def __len__(self) -> int:
        return len(self.qcis_list)

    def __getitem__(self, key: int) -> str:
        return self.qcis_list[key]

    def __iter__(self):
        return (item for item in self.qcis_list)

    def _qbit_init(
        self,
        num_qubits: int,
    ) -> None:
        """Qubits initialization.

        Raises:
            StrCircuitError: Guarantee that the number of qubits is not
            negative.

        """
        if num_qubits < 0:
            raise StrCircuitError(f"Number of inputs cannot be negative: {num_qubits}!")

    def _one_qubit_op(
        self,
        qubit_idx: int,
        operation: str,
    ) -> None:
        """General one qubit operations."""
        self.qcis_list.append(f"{operation} Q{qubit_idx}")

    def h(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "H"
        self._one_qubit_op(qubit_idx, operation)

    def x(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "X"
        self._one_qubit_op(qubit_idx, operation)

    def y(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "Y"
        self._one_qubit_op(qubit_idx, operation)

    def z(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "Z"
        self._one_qubit_op(qubit_idx, operation)

    def s(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "S"
        self._one_qubit_op(qubit_idx, operation)

    def sd(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "SD"
        self._one_qubit_op(qubit_idx, operation)

    def t(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "T"
        self._one_qubit_op(qubit_idx, operation)

    def td(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "TD"
        self._one_qubit_op(qubit_idx, operation)

    def x2p(
        self,
        qubit_idx: int,
    ) -> None:
        """X rotate pi/2"""
        operation = "X2P"
        self._one_qubit_op(qubit_idx, operation)

    def x2m(
        self,
        qubit_idx: int,
    ) -> None:
        """X rotate -pi/2"""
        operation = "X2M"
        self._one_qubit_op(qubit_idx, operation)

    def y2p(
        self,
        qubit_idx: int,
    ) -> None:
        """Y rotate pi/2"""
        operation = "Y2P"
        self._one_qubit_op(qubit_idx, operation)

    def y2m(
        self,
        qubit_idx: int,
    ) -> None:
        """Y rotate -pi/2"""
        operation = "Y2M"
        self._one_qubit_op(qubit_idx, operation)

    def m(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "M"
        self._one_qubit_op(qubit_idx, operation)

    def H(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "H"
        self._one_qubit_op(qubit_idx, operation)

    def X(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "X"
        self._one_qubit_op(qubit_idx, operation)

    def Y(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "Y"
        self._one_qubit_op(qubit_idx, operation)

    def Z(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "Z"
        self._one_qubit_op(qubit_idx, operation)

    def S(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "S"
        self._one_qubit_op(qubit_idx, operation)

    def SD(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "SD"
        self._one_qubit_op(qubit_idx, operation)

    def T(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "T"
        self._one_qubit_op(qubit_idx, operation)

    def TD(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "TD"
        self._one_qubit_op(qubit_idx, operation)

    def X2P(
        self,
        qubit_idx: int,
    ) -> None:
        """X rotate pi/2"""
        operation = "X2P"
        self._one_qubit_op(qubit_idx, operation)

    def X2M(
        self,
        qubit_idx: int,
    ) -> None:
        """X rotate -pi/2"""
        operation = "X2M"
        self._one_qubit_op(qubit_idx, operation)

    def Y2P(
        self,
        qubit_idx: int,
    ) -> None:
        """Y rotate pi/2"""
        operation = "Y2P"
        self._one_qubit_op(qubit_idx, operation)

    def Y2M(
        self,
        qubit_idx: int,
    ) -> None:
        """Y rotate -pi/2"""
        operation = "Y2M"
        self._one_qubit_op(qubit_idx, operation)

    def M(
        self,
        qubit_idx: int,
    ) -> None:
        operation = "M"
        self._one_qubit_op(qubit_idx, operation)

    def _two_qubits_op(
        self,
        qubit_control: int,
        qubit_target: int,
        operation: str,
    ) -> None:
        """
        General two qubit operations.
        """
        self.qcis_list.append(f"{operation} Q{qubit_control} Q{qubit_target}")

    def cnot(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        # FIX: not supported in hardware, just for simulation
        operation = "CX"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def cx(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        # FIX: not supported in hardware, just for simulation
        operation = "CX"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def cy(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        # FIX: not supported in hardware, just for simulation
        operation = "CY"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def cz(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        operation = "CZ"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def CNOT(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        # FIX: not supported in hardware, just for simulation
        operation = "CX"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def CX(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        # FIX: not supported in hardware, just for simulation
        operation = "CX"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def CY(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        # FIX: not supported in hardware, just for simulation
        operation = "CY"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def CZ(
        self,
        qubit_control: int,
        qubit_target: int,
    ) -> None:
        operation = "CZ"
        self._two_qubits_op(qubit_control, qubit_target, operation)

    def _rotate_gate(
        self,
        param: float | str,
        qubit_idx: int,
        operation: str,
    ) -> None:
        """
        General rotion operations.
        """
        self.qcis_list.append(f"{operation} Q{qubit_idx} {param}")

    def rx(
        self,
        param: float | str,
        qubit_idx: int,
    ) -> None:
        operation = "RX"
        self._rotate_gate(param, qubit_idx, operation)

    def ry(
        self,
        param: float | str,
        qubit_idx: int,
    ) -> None:
        operation = "RY"
        self._rotate_gate(param, qubit_idx, operation)

    def rz(
        self,
        param: float | str,
        qubit_idx: int,
    ) -> None:
        operation = "RZ"
        self._rotate_gate(param, qubit_idx, operation)

    def RX(
        self,
        param: float | str,
        qubit_idx: int,
    ) -> None:
        operation = "RX"
        self._rotate_gate(param, qubit_idx, operation)

    def RY(
        self,
        param: float | str,
        qubit_idx: int,
    ) -> None:
        operation = "RY"
        self._rotate_gate(param, qubit_idx, operation)

    def RZ(
        self,
        param: float | str,
        qubit_idx: int,
    ) -> None:
        operation = "RZ"
        self._rotate_gate(param, qubit_idx, operation)

    def rxy(
        self,
        phi: float | str,
        theta: float | str,
        qubit_idx: int,
    ) -> None:
        self.qcis_list.append(f"RXY Q{qubit_idx} {phi} {theta}")

    RXY = rxy

    def mqbit(
        self,
        *qubit_idx: Sequence[int] | int,
    ) -> None:
        """Specifies the object to be measured."""

        for idx in qubit_idx:
            self.qcis_list.append(f"M Q{idx}")

    def measure(
        self,
        **kw,
    ):
        """Forward calculation."""
        # TODO: check qubit_num
        if not self.sample:
            measure_result = self.backend.probs(self.qcis, **kw)
        else:
            measure_result = self.backend.sample(self.qcis, self.shots, **kw)
        return measure_result

    def pauli(
        self,
        gates: str | tuple,
        format: str = "str",
    ) -> None:
        """Pauli measurement."""

        if format == "str":
            if not isinstance(gates, str):
                raise TypeError(f"Strings are needs but get f{type(gates)}")
            gate_op = re.findall("[a-zA-Z]+", gates)
            gate_idx = [int(idx) for idx in re.findall("[0-9]+", gates)]
            if len(gate_op) != len(gate_idx):
                raise ValueError("Illegal pauli measurement.")
            gates = zip(gate_idx, gate_op)

        elif format == "openfermion":
            pass

        else:
            raise StrCircuitError(f"Unsupported format {format!s}")

        for gate in gates:
            if gate[1].upper() == "X":
                self._measure_recording.append(
                    f"H Q{gate[0]}",
                )
                self._measure_recording.append(
                    f"M Q{gate[0]}",
                )
            elif gate[1].upper() == "Y":
                self._measure_recording.append(
                    f"X2P Q{gate[0]}",
                )
                self._measure_recording.append(
                    f"M Q{gate[0]}",
                )
            elif gate[1].upper() == "Z":
                self._measure_recording.append(
                    f"M Q{gate[0]}",
                )
            else:
                raise ValueError("Please input correct Pauli gates.")

    def pauli_measure(self, **kw) -> Tensor:
        """Pauli measurement."""
        # TODO: check qubit_num

        if self.sample:
            measure_result_dict = self.measure(**kw)
            result = 0
            for res_index, frequency in measure_result_dict.items():
                parity = (-1) ** (res_index.count("1") % 2)
                # e.g. {"011": 222}, to count "1"
                result += parity * frequency / self.shots
            return result
        else:
            measure_result_array = self.measure(**kw)
            parity = [
                (-1) ** (str(bin(int(index))).count("1") % 2)
                for index in range(len(measure_result_array))
            ]
            return self.backend.dot(
                measure_result_array,
                self.backend.as_tensor(parity),
            )

    def chain(
        self,
        gate_name: str,
        qubit_idx: Sequence[int] | None = None,
    ) -> None:
        """Act on each qubit and the next in turn"""
        if qubit_idx is None:
            qubit_idx = list(range(self.num_qubits - 1))
        operation = getattr(self, gate_name)
        for idx in qubit_idx:
            operation(idx, idx + 1)

    def ring(
        self,
        gate_name: str,
        num_qubits: int | None = None,
    ) -> None:
        """Act on all qubits via a ring"""
        if num_qubits is None:
            num_qubits = self.num_qubits
        if num_qubits < 2:
            raise ValueError(
                f"Number of qubits have to be larger than 1 but given " f"{num_qubits}"
            )
        operation = getattr(self, gate_name)
        for num_qubit in range(num_qubits - 1):
            operation(num_qubit, num_qubit + 1)
        operation(num_qubits - 1, 0)

    def single(
        self,
        gate_name: str,
        qubit_idx: Sequence[int] | None = None,
    ) -> None:
        """Act on each qubit in turn"""
        if qubit_idx is None:
            qubit_idx = list(range(self.num_qubits))
        operation = getattr(self, gate_name)
        for idx in qubit_idx:
            # self._one_qubit_op(idx, gate_name)
            operation(idx)

    def perm(
        self,
        gate_name: str,
        qubit_idx: Sequence[int] | None = None,
    ) -> None:
        """Permutation of all."""
        if qubit_idx is None:
            qubit_idx = list(range(self.num_qubits))
        operation = getattr(self, gate_name)
        for idx in itertools.permutations(qubit_idx, 2):
            operation(*idx)

    def comb(
        self,
        gate_name: str,
        qubit_idx: Sequence[int] | None = None,
    ) -> None:
        """combinations of all."""
        if qubit_idx is None:
            qubit_idx = list(range(self.num_qubits))
        operation = getattr(self, gate_name)
        for idx in itertools.combinations(qubit_idx, 2):
            operation(*idx)

    def param(
        self,
        gate_name: str,
        qubit_idx: Sequence[int] | None = None,
        param_name: str = "x",
        param_idx: Sequence[int] | None = None,
    ) -> None:
        """Quickly build parameterized circuits"""
        if qubit_idx is None:
            qubit_idx = list(range(self.num_qubits))
        if param_idx is None:
            param_idx = qubit_idx
        operation = getattr(self, gate_name)
        for pidx, qidx in zip(param_idx, qubit_idx):
            operation(f"{param_name}[{pidx}]", qidx)
