# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""State vector simulation backend."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from typing import Any

import numpy as np

from .abstract_backend import AbstractBackend

Tensor = Any

gate_list: list[str] = [
    "H",
    "X",
    "Y",
    "Z",
    "S",
    "T",
    "RZ",
    "RX",
    "RY",
    "SD",
    "TD",
    "X2M",
    "X2P",
    "Y2M",
    "Y2P",
    "CZ",
    "CY",
    "CX",
    "CNOT",
    "M",
    "RXY",
]


class StateVectorSimulatorError(Exception):
    """state vector simulation error"""


class StateVectorSimulator(AbstractBackend):
    """Simulate quantum circuits using state vector methods. Abstract the
    mathematical operations required for the simulation process, and the
    specific implementation methods need to be implemented in its subclasses.
    """

    def as_tensor(self, Tensor) -> Tensor:
        raise NotImplementedError

    def H(self) -> Tensor:
        raise NotImplementedError

    def X(self) -> Tensor:
        raise NotImplementedError

    def Y(self) -> Tensor:
        raise NotImplementedError

    def Z(self) -> Tensor:
        raise NotImplementedError

    def S(self) -> Tensor:
        raise NotImplementedError

    def T(self) -> Tensor:
        raise NotImplementedError

    def SD(self) -> Tensor:
        raise NotImplementedError

    def TD(self) -> Tensor:
        raise NotImplementedError

    def X2M(self) -> Tensor:
        raise NotImplementedError

    def X2P(self) -> Tensor:
        raise NotImplementedError

    def Y2M(self) -> Tensor:
        raise NotImplementedError

    def Y2P(self) -> Tensor:
        raise NotImplementedError

    def RX(self, theta: Tensor) -> Tensor:
        raise NotImplementedError

    def RY(self, theta: Tensor) -> Tensor:
        raise NotImplementedError

    def RZ(self, theta: Tensor) -> Tensor:
        raise NotImplementedError

    def RXY(self, theta: Tensor, phi: Tensor) -> Tensor:
        raise NotImplementedError

    def reshape(self, state: Tensor, shape: Sequence) -> Tensor:
        raise NotImplementedError

    def ravel(self, state: Tensor) -> Tensor:
        raise NotImplementedError

    def stack(self, states: Sequence[Tensor], axis: int = 0) -> Tensor:
        raise NotImplementedError

    def real(self, state: Tensor) -> Tensor:
        raise NotImplementedError

    def sum(self, state: Tensor, axis: int | None = None) -> Tensor:
        raise NotImplementedError

    def conj(self, state: Tensor) -> Tensor:
        raise NotImplementedError

    def sqrt(self, state: Tensor) -> Tensor:
        raise NotImplementedError

    def copy(self, state: Tensor) -> Tensor:
        raise NotImplementedError

    def dot(self, state1: Tensor, state2: Tensor) -> Tensor:
        raise NotImplementedError

    def get_zero_state(self, qnum: int) -> Tensor:
        raise NotImplementedError

    def reshape_single(
        self,
        state: Tensor,
        qnum: int,
        target: int,
    ) -> Tensor:
        """Before the single-qubit operation is performed, reshape the state
        vector into the required dimension for matrix multiplication.

        Args:
            state: Initial state vector.
            qnum: Number of qubits.
            target: The target qubit corresponding to the action of a
                    single-qubit operation.

        Returns:
            Reshaped state vector.

        """

        shape = (1 << target, 2, 1 << (qnum - target - 1))
        return self.reshape(state, shape)

    def reshape_double(
        self,
        state: Tensor,
        qnum: int,
        target1: int,
        target2: int,
    ) -> Tensor:
        """Before the double-qubit operation is performed, reshape the state
        vector into the required dimension for matrix multiplication.

        Args:
            state: Initial state vector.
            qnum: Number of qubits.
            target1: The first target qubit corresponding to the action of a
                     double-qubit operation.
            target2: The second target qubit corresponding to the action of a
                     double-qubit operation.

        Returns:
            Reshaped state vector.

        """
        shape = (
            1 << target1,
            2,
            1 << (target2 - target1 - 1),
            2,
            1 << (qnum - target2 - 1),
        )
        return self.reshape(state, shape)

    def single_gate(
        self,
        state: Tensor,
        gate: str,
        qnum: int,
        target: int,
    ) -> Tensor:
        """Using matrix multiplication, single-qubit gates act on quantum state
        vectors.

        Args:
            state: Initial state vector before operation.
            gate: Specific gates acting on the qubit.
            qnum: Number of qubits.
            target: The target qubit corresponding to the action.

        Returns:
            Final state vector.

        """
        state = self.reshape_single(state, qnum, target)
        if gate in gate_list:
            state = getattr(self, gate)() @ state[:,]
        else:
            raise StateVectorSimulatorError("non-existent quantum gate")

        return self.ravel(state)

    def single_rotate_gate(
        self,
        state: Tensor,
        gate: str,
        qnum: int,
        target: int,
        theta: Tensor,
    ) -> Tensor:
        """Using matrix multiplication, single-qubit-rotate gates act on
        quantum state vectors.

        Args:
            state: Initial state vector before operation.
            gate: Specific gates acting on the qubit.
            qnum: Number of qubits.
            target: The target qubit corresponding to the action.
            theta: Angle of rotation. Extra dimensions after the parameter
                   needed will be discarded.

        Returns:
            Final state vector.

        """
        state = self.reshape_single(state, qnum, target)
        if gate in ["RX", "RY", "RZ"]:
            state = getattr(self, gate)(theta[0]) @ state[:,]
        elif gate == "RXY":
            state = self.RXY(theta[0], theta[1]) @ state[:,]
        return self.ravel(state)

    def multi_gate(
        self,
        state: Tensor,
        gate: str,
        qnum: int,
        ctrl: int,
        target: int,
    ) -> Tensor:
        """Using matrix multiplication, multi-qubit gates act on quantum state
        vectors.

        Args:
            state: Initial state vector before operation.
            gate: Specific gates acting on the qubit.
            qnum: Number of qubits.
            ctrl: The control qubit corresponding to the action.
            target: The target qubit corresponding to the action.

        Returns:
            Final state vector.

        """

        if ctrl < target:
            state = self.reshape_double(state, qnum, ctrl, target)
            if gate in ["CX", "CNOT"]:
                a, b = state[:, 1, :, 0, :], state[:, 1, :, 1, :]
                u = self.stack([b, a], axis=2)
                state = self.stack([state[:, 0, :, :, :], u], axis=1)
            elif gate == "CY":
                a, b = 1j * state[:, 1, :, 0, :], -1j * state[:, 1, :, 1, :]
                u = self.stack([b, a], axis=2)
                state = self.stack([state[:, 0, :, :, :], u], axis=1)
            elif gate == "CZ":
                a, b = state[:, 0, :, 1, :], -1 * state[:, 1, :, 1, :]
                u = self.stack([a, b], axis=1)
                state = self.stack([state[:, :, :, 0, :], u], axis=3)
            return self.ravel(state)
        else:
            state = self.reshape_double(state, qnum, target, ctrl)
            if gate in ["CX", "CNOT"]:
                a, b = state[:, 0, :, 1, :], state[:, 1, :, 1, :]
                u = self.stack([b, a], axis=1)
                state = self.stack([state[:, :, :, 0, :], u], axis=3)
            elif gate == "CY":
                a, b = 1j * state[:, 0, :, 1, :], -1j * state[:, 1, :, 1, :]
                u = self.stack([b, a], axis=1)
                state = self.stack([state[:, :, :, 0, :], u], axis=3)
            elif gate == "CZ":
                a, b = state[:, 0, :, 1, :], -1 * state[:, 1, :, 1, :]
                u = self.stack([a, b], axis=1)
                state = self.stack([state[:, :, :, 0, :], u], axis=3)
            return self.ravel(state)

    def swap(
        self,
        state: Tensor,
        qnum: int,
        q1: int,
        q2: int,
    ) -> Tensor:
        """The state vector is swapped, and the sequence number of the qubit
        is exchanged.

        Args:
            state: State vector before swap.
            qnum: Number of qubits.
            q1, q2: Indexed of qubits to exchange.

        Returns:
            State vector after swap.

        """
        q1, q2 = min(q1, q2), max(q1, q2)
        state = self.reshape_double(state, qnum, q1, q2)
        a, b, c, d = (
            state[:, 0, :, 0, :],
            state[:, 0, :, 1, :],
            state[:, 1, :, 0, :],
            state[:, 1, :, 1, :],
        )
        u = self.stack([a, c], axis=2)
        v = self.stack([b, d], axis=2)
        state = self.stack([u, v], axis=1)
        return self.ravel(state)

    def shift(
        self,
        state: Tensor,
        qnum: int,
        mq: Sequence[int],
    ) -> Tensor:
        """Qubits are swapped multiple times for ``probs``.

        Args:
            state: State vector before shift.
            qnum: Number of qubits.
            mq: The number of qubits to be measured.

        Returns:
            State vector after shift.

        """

        qidx = {}
        idxq = {}
        for i in range(qnum):
            qidx[i] = i
            idxq[i] = i

        for i, m in enumerate(mq):
            if qidx[m] == i:
                continue
            state = self.swap(state, qnum, i, qidx[m])
            q = idxq[i]
            qidx[q] = qidx[m]
            qidx[m] = i
            idxq[i] = m
            idxq[qidx[q]] = q
        return state

    @staticmethod
    def check(line_data: Iterable) -> tuple[int, dict]:
        """Traverse the entire qcis to get circuit information for simulation.

        Args:
            line_data: Each line of the qcis file.

        Returns:
            qnum: The number of qubits required for the circuit.
            qdic: The number corresponding to the qubit.

        Raises:
            StateVectorSimulatorError: Check the rationality of the qcis file.

        """

        qdic = {}
        qnum = 0
        for idx, line in enumerate(line_data):
            line = line.strip()
            if not line:
                continue
            strArr = line.split(" ")
            if strArr[0] not in gate_list:
                raise StateVectorSimulatorError(
                    f"simulate error: in line {idx}, gate error"
                )
            if len(strArr) < 2 or len(strArr) > 4:
                raise StateVectorSimulatorError(
                    f"simulate error: in line {idx}, qbit number error"
                )
            if strArr[1][0] != "Q" or not strArr[1][1:].isdigit():
                raise StateVectorSimulatorError(
                    f"simulate error: in line {idx}, qbit syntax error"
                )

            if strArr[1] not in qdic:
                qdic[strArr[1]] = qnum
                qnum += 1

            if strArr[0] in ["CZ", "CY", "CX", "CNOT"]:
                if len(strArr) != 3:
                    raise StateVectorSimulatorError(
                        f"simulate error: in line {idx}, qbit number error"
                    )

                if strArr[2][0] != "Q" or not strArr[2][1:].isdigit():
                    raise StateVectorSimulatorError(
                        f"simulate error: in line {idx}, qbit syntax error"
                    )

                if strArr[2] not in qdic:
                    qdic[strArr[2]] = qnum
                    qnum += 1
            if strArr[0] in ["RX", "RY", "RZ"]:
                if len(strArr) != 3:
                    raise StateVectorSimulatorError(
                        f"simulate error: in line {idx}, qbit number error"
                    )
            if strArr[0] == "RXY":
                if len(strArr) != 4:
                    raise StateVectorSimulatorError(
                        f"simulate error: in line {idx}, qbit number error"
                    )

        if qnum > 30:
            raise StateVectorSimulatorError(
                f"simulate error: qbit number `{qnum}` is too large, "
                "can not simulate."
            )

        if qnum > 22:
            print(
                f"Warning: current number of qubits is {qnum}, "
                "which may require a lot of memory."
            )

        return qnum, qdic

    def getstate(
        self,
        line_data: Iterable,
        qnum: int,
        qdic: dict,
        **kwargs,
    ) -> tuple[Tensor, list]:
        """Initialize the state vector, traverse the qcis file, apply all gate
        operations to the state vector, obtain the state after the action,
        and obtain the number of the measurement qubit.

        Args:
            line_data: Each line of the qcis file.
            qnum: The number of qubits.
            qdic: The number corresponding to the qubit.
            **kwargs: The parameters of the rotation gates.

        Returns:
            state: Final state vector.
            mq: The sequence number of the qubit to be measured.

        """

        state = self.get_zero_state(qnum)
        mq = []
        for line in line_data:
            line = line.strip()
            if not line:
                continue
            strArr = line.split(" ")
            qid1 = qdic[strArr[1]]
            if strArr[0] == "M":
                mq.append(qid1)
            else:
                if strArr[0] in ["CZ", "CY", "CX", "CNOT"]:
                    qid2 = qdic[strArr[2]]
                    state = self.multi_gate(state, strArr[0], qnum, qid1, qid2)
                elif strArr[0] in ["RX", "RY", "RZ", "RXY"]:
                    theta = []
                    for v in strArr[2:]:
                        theta.append(eval(v, kwargs))
                    state = self.single_rotate_gate(state, strArr[0], qnum, qid1, theta)
                else:
                    state = self.single_gate(state, strArr[0], qnum, qid1)
        return state, mq

    def sample(
        self,
        data: str,
        shots: int = 100,
        rng_seed: int | None = None,
        **kwargs,
    ) -> dict[str, int]:
        """This method can get the sampling result of the specified qubit
        measurement. Unlike the ``probs`` method, this method obtains the
        measurement results of the quantum circuit by sampling, and the results
        are related to shots.

        Returns:
            This method returns a dictionary, the key in the dictionary is
            the quantum state, and the value is the shots of the quantum state.

        """
        line_data = data.split("\n")
        qnum, qdic = self.check(line_data)
        state, mq = self.getstate(line_data, qnum, qdic, **kwargs)
        state = self.shift(state, qnum, mq)
        state = self.conj(state) * state
        mq_len = len(mq)
        state = self.reshape(state, [1 << mq_len, 1 << (qnum - mq_len)])
        p = self.real(self.sum(state, axis=1))
        p_norm = p / sum(p)
        if not isinstance(p_norm, np.ndarray):
            p_norm = p_norm.cpu().numpy()
        if rng_seed is not None:
            np.random.seed(int(rng_seed))
        r = np.random.choice(1 << mq_len, shots, p=p_norm)
        return {bin(k)[2:].zfill(mq_len): v for k, v in Counter(r).items()}

    def probs(
        self,
        data: str,
        **kwargs,
    ) -> Tensor:
        """This method can get all the probability distributions after the
        measurement of the specified qubit. The probability distribution
        obtained by this method is the theoretical value after the state vector
        simulation, and shots are not considered.

        Args:
            data: Qcis data.

        Returns:
            Tensor(array) distribution. Sort by the size of the binary.

        """
        line_data = data.split("\n")
        qnum, qdic = self.check(line_data)
        state, mq = self.getstate(line_data, qnum, qdic, **kwargs)
        state = self.shift(state, qnum, mq)
        state = self.conj(state) * state
        mq_len = len(mq)
        state = self.reshape(state, [1 << mq_len, 1 << (qnum - mq_len)])
        return self.real(self.sum(state, axis=1))

    def state(
        self,
        data: str,
        **kwargs,
    ) -> Tensor:
        """This method can get the quantum state after operation.

        Args:
            data: Qcis data.

        Returns:
            State as tensor(array).

        """

        line_data = data.split("\n")
        qnum, qdic = self.check(line_data)
        state, _ = self.getstate(line_data, qnum, qdic, **kwargs)
        return state
