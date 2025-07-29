# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""A connector to directly use circuits as PyTorch modules.
This part code is inspired by tensorcircuit.
"""

from __future__ import annotations

from typing import Any, Callable

try:
    import torch
    from torch import Tensor
    from torch.nn import Module, Parameter
except Exception:
    Module = object
    Tensor = Any


class TorchLayerError(Exception):
    """Torch layer exception."""


class TorchLayer(Module):
    """Apply a transformation of quantum circuits to the incoming data"""

    __constants__ = ["num_weights"]
    num_weights: int

    def __init__(
        self,
        circuit: Callable[..., Any],
        num_weights: int,
        *,
        is_vmap: bool = True,
        in_dims: tuple[int | None, int | None] = (0, None),
        initial_weights: Tensor | None = None,
    ) -> None:
        super().__init__()

        # vamp is used, pytorch > 2.0
        self.is_vmap = is_vmap
        if is_vmap:
            circuit = torch.vmap(circuit, in_dims=in_dims)
            self.in_dims = in_dims

        # initialize weights
        if isinstance(initial_weights, Tensor):
            self.weights = Parameter(initial_weights)
        else:
            self.weights = Parameter(torch.randn(num_weights))

        self.circuit = circuit
        self.num_weights = num_weights

    def forward(self, inputs: Tensor) -> Tensor:
        return self.circuit(inputs, self.weights)

    def extra_repr(self) -> str:
        """Nice print this layer."""
        if self.is_vmap:
            return (
                f"num_weights={self.num_weights}, "
                f"is_vmap={self.is_vmap}, "
                f"vmap_in_dims={self.in_dims}"
            )
        else:
            return f"num_weights={self.num_weights}, is_vmap={self.is_vmap}"
