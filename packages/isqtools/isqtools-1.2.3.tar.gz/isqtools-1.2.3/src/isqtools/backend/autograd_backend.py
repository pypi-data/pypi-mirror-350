# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Autograd backend.
Autograd can automatically differentiate native Python and Numpy code.
It can handle a large subset of Python's features, including loops, ifs,
recursion and closures, and it can even take derivatives of derivatives
of derivatives. It supports reverse-mode differentiation (a.k.a.
backpropagation), which means it can efficiently take gradients of
scalar-valued functions with respect to array-valued arguments, as well as
forward-mode differentiation, and the two can be composed arbitrarily. The main
intended application of Autograd is gradient-based optimization.
For more information, check out: https://github.com/HIPS/autograd
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from .state_vector_simulator import StateVectorSimulator

try:
    import autograd.numpy as anp
except ModuleNotFoundError:
    pass

Tensor = Any


class AutogradBackend(StateVectorSimulator):
    """This method inherits the ``StateVectorSimulator``, and uses
    autograd to perform the mathematical calculation.
    """

    def as_tensor(self, tensor: Tensor) -> Tensor:
        """Convert to the corresponding tensor."""
        return anp.array(tensor)

    def H(self) -> Tensor:
        return (
            1
            / anp.sqrt(2)
            * anp.array(
                [
                    [1, 1],
                    [1, -1],
                ],
                dtype=complex,
            )
        )

    def X(self) -> Tensor:
        return anp.array(
            [
                [0, 1],
                [1, 0],
            ],
            dtype=complex,
        )

    def Y(self) -> Tensor:
        return anp.array(
            [
                [0, -1j],
                [1j, 0],
            ],
            dtype=complex,
        )

    def Z(self) -> Tensor:
        return anp.array(
            [
                [1, 0],
                [0, -1],
            ],
            dtype=complex,
        )

    def S(self) -> Tensor:
        return anp.array(
            [
                [1, 0],
                [0, 1j],
            ],
            dtype=complex,
        )

    def T(self) -> Tensor:
        return anp.array(
            [
                [anp.exp(-1j * anp.pi / 8), 0],
                [0, anp.exp(1j * anp.pi / 8)],
            ],
            dtype=complex,
        )

    def SD(self) -> Tensor:
        return anp.array(
            [
                [1, 0],
                [0, -1j],
            ],
            dtype=complex,
        )

    def TD(self) -> Tensor:
        return anp.array(
            [
                [anp.exp(1j * anp.pi / 8), 0],
                [0, anp.exp(-1j * anp.pi / 8)],
            ],
            dtype=complex,
        )

    def X2M(self) -> Tensor:
        return (
            anp.sqrt(2)
            / 2
            * anp.array(
                [
                    [1, 1j],
                    [1j, 1],
                ],
                dtype=complex,
            )
        )

    def X2P(self) -> Tensor:
        return (
            anp.sqrt(2)
            / 2
            * anp.array(
                [
                    [1, -1j],
                    [-1j, 1],
                ],
                dtype=complex,
            )
        )

    def Y2M(self) -> Tensor:
        return (
            anp.sqrt(2)
            / 2
            * anp.array(
                [
                    [1, 1],
                    [-1, 1],
                ],
                dtype=complex,
            )
        )

    def Y2P(self) -> Tensor:
        return (
            anp.sqrt(2)
            / 2
            * anp.array(
                [
                    [1, -1],
                    [1, 1],
                ],
                dtype=complex,
            )
        )

    def RX(self, theta: Tensor) -> Tensor:
        theta /= 2
        return anp.array(
            [
                [anp.cos(theta), -1j * anp.sin(theta)],
                [-1j * anp.sin(theta), anp.cos(theta)],
            ],
            dtype=complex,
        )

    def RY(self, theta: Tensor) -> Tensor:
        theta /= 2
        return anp.array(
            [
                [anp.cos(theta), -1 * anp.sin(theta)],
                [anp.sin(theta), anp.cos(theta)],
            ],
            dtype=complex,
        )

    def RZ(self, theta: Tensor) -> Tensor:
        theta /= 2
        return anp.array(
            [
                [anp.exp(-1j * theta), 0],
                [0, anp.exp(1j * theta)],
            ],
            dtype=complex,
        )

    def RXY(self, theta: Tensor, phi: Tensor) -> Tensor:
        theta /= 2
        return anp.array(
            [
                [anp.cos(theta), -1j * anp.exp(-1j * phi) * anp.sin(theta)],
                [-1j * anp.exp(1j * phi) * anp.sin(theta), anp.cos(theta)],
            ],
            dtype=complex,
        )

    def get_zero_state(self, qnum: int) -> Tensor:
        state = anp.zeros(1 << qnum, dtype=complex)
        state[0] = 1
        return state

    def reshape(self, state: Tensor, shape: Sequence[int]) -> Tensor:
        return anp.reshape(state, shape)

    def ravel(self, state: Tensor) -> Tensor:
        return anp.ravel(state)

    def stack(self, states: Sequence[Tensor], axis: int = 0) -> Tensor:
        return anp.stack(states, axis=axis)

    def real(self, state: Tensor) -> Tensor:
        return anp.real(state)

    def sum(self, state: Tensor, axis: int | None = None) -> Tensor:
        return anp.sum(state, axis=axis)

    def conj(self, state: Tensor) -> Tensor:
        return anp.conj(state)

    def sqrt(self, state: Tensor) -> Tensor:
        return anp.sqrt(state)

    def copy(self, state: Tensor) -> Tensor:
        return state.copy()

    def dot(self, state1: Tensor, state2: Tensor) -> Tensor:
        return anp.dot(state1, state2)
