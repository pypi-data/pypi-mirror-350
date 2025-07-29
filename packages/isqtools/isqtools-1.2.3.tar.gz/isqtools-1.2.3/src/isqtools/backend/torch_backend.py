# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""PyTorch backend.
PyTorch is a machine learning framework based on the Torch library, used for
applications such as computer vision and natural language processing,
originally developed by Meta AI and now part of the Linux Foundation umbrella.
It is free and open-source software released under the modified BSD license.
For more information, check out: https://pytorch.org/
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from .state_vector_simulator import StateVectorSimulator

try:
    import torch

    torch_dtype = torch.complex64
except Exception:
    # pytorch is an optional backend
    torch_dtype = None


Tensor = Any


class TorchBackend(StateVectorSimulator):
    """This method inherits the ``StateVectorSimulator``, and uses
    pytorch to perform the mathematical calculation.
    """

    def __init__(self, dtype=None) -> None:
        if dtype is None:
            self.dtype = torch_dtype
        else:
            self.dtype = dtype

    def as_tensor(self, tensor: Tensor) -> Tensor:
        return torch.as_tensor(tensor)

    def H(self) -> Tensor:
        return (
            1
            / torch.sqrt(torch.tensor(2))
            * torch.tensor(
                [
                    [1, 1],
                    [1, -1],
                ],
                dtype=self.dtype,
            )
        )

    def X(self) -> Tensor:
        return torch.tensor(
            [
                [0, 1],
                [1, 0],
            ],
            dtype=self.dtype,
        )

    def Y(self) -> Tensor:
        return torch.tensor(
            [
                [0, -1j],
                [1j, 0],
            ],
            dtype=self.dtype,
        )

    def Z(self) -> Tensor:
        return torch.tensor(
            [
                [1, 0],
                [0, -1],
            ],
            dtype=self.dtype,
        )

    def S(self) -> Tensor:
        return torch.tensor(
            [
                [1, 0],
                [0, 1j],
            ],
            dtype=self.dtype,
        )

    def T(self) -> Tensor:
        return torch.tensor(
            [
                [torch.exp(torch.tensor(-1j * torch.pi / 8)), 0],
                [0, torch.exp(torch.tensor(1j * torch.pi / 8))],
            ],
            dtype=self.dtype,
        )

    def SD(self) -> Tensor:
        return torch.tensor(
            [
                [1, 0],
                [0, -1j],
            ],
            dtype=self.dtype,
        )

    def TD(self) -> Tensor:
        return torch.tensor(
            [
                [torch.exp(torch.tensor(1j * torch.pi / 8)), 0],
                [0, torch.exp(torch.tensor(-1j * torch.pi / 8))],
            ],
            dtype=self.dtype,
        )

    def X2M(self) -> Tensor:
        return (
            torch.sqrt(torch.tensor(2))
            / 2
            * torch.tensor(
                [
                    [1, 1j],
                    [1j, 1],
                ],
                dtype=self.dtype,
            )
        )

    def X2P(self) -> Tensor:
        return (
            torch.sqrt(torch.tensor(2))
            / 2
            * torch.tensor(
                [
                    [1, -1j],
                    [-1j, 1],
                ],
                dtype=self.dtype,
            )
        )

    def Y2M(self) -> Tensor:
        return (
            torch.sqrt(torch.tensor(2))
            / 2
            * torch.tensor(
                [
                    [1, 1],
                    [-1, 1],
                ],
                dtype=self.dtype,
            )
        )

    def Y2P(self) -> Tensor:
        return (
            torch.sqrt(torch.tensor(2))
            / 2
            * torch.tensor(
                [
                    [1, -1],
                    [1, 1],
                ],
                dtype=self.dtype,
            )
        )

    def RX(self, theta: Tensor) -> Tensor:
        theta = self.as_tensor(theta)
        theta = torch.div(theta, 2).reshape(-1)
        return (
            torch.cat(
                (
                    torch.cos(theta),
                    -1j * torch.sin(theta),
                    -1j * torch.sin(theta),
                    torch.cos(theta),
                ),
            )
            .reshape(2, 2)
            .type(self.dtype)
        )

    def RY(self, theta: Tensor) -> Tensor:
        theta = self.as_tensor(theta)
        theta = torch.div(theta, 2).reshape(-1)
        return (
            torch.cat(
                (
                    torch.cos(theta),
                    -1 * torch.sin(theta),
                    torch.sin(theta),
                    torch.cos(theta),
                ),
            )
            .reshape(2, 2)
            .type(self.dtype)
        )

    def RZ(self, theta: Tensor) -> Tensor:
        theta = self.as_tensor(theta)
        theta = torch.div(theta, 2).reshape(-1)
        return (
            torch.cat(
                (
                    torch.exp(-1j * theta),
                    torch.zeros(1),
                    torch.zeros(1),
                    torch.exp(1j * theta),
                ),
            )
            .reshape(2, 2)
            .type(self.dtype)
        )

    def RXY(self, theta: Tensor, phi: Tensor) -> Tensor:
        theta = self.as_tensor(theta)
        phi = self.as_tensor(phi)
        theta = torch.div(theta, 2).reshape(-1)
        phi = phi.reshape(-1)

        return (
            torch.cat(
                (
                    torch.cos(theta),
                    -1j * torch.exp(-1j * phi) * torch.sin(theta),
                    -1j * torch.exp(1j * phi) * torch.sin(theta),
                    torch.cos(theta),
                ),
            )
            .reshape(2, 2)
            .type(self.dtype)
        )

    def get_zero_state(self, qnum: int) -> Tensor:
        state = torch.zeros(
            torch.pow(torch.tensor(2), torch.tensor(qnum)),
            dtype=self.dtype,
        )
        state[0] = 1
        return state

    def reshape(self, state: Tensor, shape: Sequence) -> Tensor:
        return torch.reshape(state, shape)

    def ravel(self, state: Tensor) -> Tensor:
        return torch.ravel(state)

    def stack(self, states: Sequence[Tensor], axis: int = 0) -> Tensor:
        return torch.stack(states, axis=axis)

    def real(self, state: Tensor) -> Tensor:
        return torch.real(state)

    def sum(self, state: Tensor, axis: int | None = None) -> Tensor:
        return torch.sum(state, axis=axis)

    def conj(self, state: Tensor) -> Tensor:
        return torch.conj(state)

    def sqrt(self, state: Tensor) -> Tensor:
        return torch.sqrt(state)

    def copy(self, state: Tensor) -> Tensor:
        return state.clone()

    def dot(self, state1: Tensor, state2: Tensor) -> Tensor:
        state1 = torch.as_tensor(state1)
        state2 = torch.as_tensor(state2).type_as(state1)
        return torch.dot(state1, state2)
