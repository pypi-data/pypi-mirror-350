# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Numpy backend.
NumPy is the fundamental package for scientific computing in Python.
It is a Python library that provides a multidimensional array object,
various derived objects (such as masked arrays and matrices), and an
assortment of routines for fast operations on arrays, including
mathematical, logical, shape manipulation, sorting, selecting, I/O,
discrete Fourier transforms, basic linear algebra, basic statistical
operations, random simulation and much more.
For more information, check out: https://numpy.org/
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np

from .state_vector_simulator import StateVectorSimulator

Tensor = Any


class NumpyBackend(StateVectorSimulator):
    """This method inherits the ``StateVectorSimulator``, and uses
    autograd to perform the mathematical calculation.
    """

    def as_tensor(self, tensor: Tensor) -> Tensor:
        return np.array(tensor)

    def H(self) -> Tensor:
        return (
            1
            / np.sqrt(2)
            * np.array(
                [
                    [1, 1],
                    [1, -1],
                ],
                dtype=complex,
            )
        )

    def X(self) -> Tensor:
        return np.array(
            [
                [0, 1],
                [1, 0],
            ],
            dtype=complex,
        )

    def Y(self) -> Tensor:
        return np.array(
            [
                [0, -1j],
                [1j, 0],
            ],
            dtype=complex,
        )

    def Z(self) -> Tensor:
        return np.array(
            [
                [1, 0],
                [0, -1],
            ],
            dtype=complex,
        )

    def S(self) -> Tensor:
        return np.array(
            [
                [1, 0],
                [0, 1j],
            ],
            dtype=complex,
        )

    def T(self) -> Tensor:
        return np.array(
            [
                [np.exp(-1j * np.pi / 8), 0],
                [0, np.exp(1j * np.pi / 8)],
            ],
            dtype=complex,
        )

    def SD(self) -> Tensor:
        return np.array(
            [
                [1, 0],
                [0, -1j],
            ],
            dtype=complex,
        )

    def TD(self) -> Tensor:
        return np.array(
            [
                [np.exp(1j * np.pi / 8), 0],
                [0, np.exp(-1j * np.pi / 8)],
            ],
            dtype=complex,
        )

    def X2M(self) -> Tensor:
        return (
            np.sqrt(2)
            / 2
            * np.array(
                [
                    [1, 1j],
                    [1j, 1],
                ],
                dtype=complex,
            )
        )

    def X2P(self) -> Tensor:
        return (
            np.sqrt(2)
            / 2
            * np.array(
                [
                    [1, -1j],
                    [-1j, 1],
                ],
                dtype=complex,
            )
        )

    def Y2M(self) -> Tensor:
        return (
            np.sqrt(2)
            / 2
            * np.array(
                [
                    [1, 1],
                    [-1, 1],
                ],
                dtype=complex,
            )
        )

    def Y2P(self) -> Tensor:
        return (
            np.sqrt(2)
            / 2
            * np.array(
                [
                    [1, -1],
                    [1, 1],
                ],
                dtype=complex,
            )
        )

    def RX(self, theta: Tensor) -> Tensor:
        theta /= 2
        return np.array(
            [
                [np.cos(theta), -1j * np.sin(theta)],
                [-1j * np.sin(theta), np.cos(theta)],
            ],
            dtype=complex,
        )

    def RY(self, theta: Tensor) -> Tensor:
        theta /= 2
        return np.array(
            [
                [np.cos(theta), -1 * np.sin(theta)],
                [np.sin(theta), np.cos(theta)],
            ],
            dtype=complex,
        )

    def RZ(self, theta: Tensor) -> Tensor:
        theta /= 2
        return np.array(
            [
                [np.exp(-1j * theta), 0],
                [0, np.exp(1j * theta)],
            ],
            dtype=complex,
        )

    def RXY(self, theta: Tensor, phi: Tensor) -> Tensor:
        theta /= 2
        return np.array(
            [
                [np.cos(theta), -1j * np.exp(-1j * phi) * np.sin(theta)],
                [-1j * np.exp(1j * phi) * np.sin(theta), np.cos(theta)],
            ],
            dtype=complex,
        )

    def get_zero_state(self, qnum: int) -> Tensor:
        state = np.zeros(1 << qnum, dtype=complex)
        state[0] = 1
        return state

    def reshape(self, state: Tensor, shape: Sequence) -> Tensor:
        return np.reshape(state, shape)

    def ravel(self, state: Tensor) -> Tensor:
        return np.ravel(state)

    def stack(self, states: Sequence[Tensor], axis: int = 0) -> Tensor:
        return np.stack(states, axis=axis)

    def real(self, state: Tensor) -> Tensor:
        return np.real(state)

    def sum(self, state: Tensor, axis: int | None = None) -> Tensor:
        return np.sum(state, axis=axis)

    def conj(self, state: Tensor) -> Tensor:
        return np.conj(state)

    def sqrt(self, state: Tensor) -> Tensor:
        return np.sqrt(state)

    def copy(self, state: Tensor) -> Tensor:
        return state.copy()

    def dot(self, state1: Tensor, state2: Tensor) -> Tensor:
        return np.dot(state1, state2)
