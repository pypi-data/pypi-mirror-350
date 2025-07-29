# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""A Quantum Neural Network implemented by autograd.
"""

from __future__ import annotations

import logging
from typing import Any, Callable

import numpy as np

from .neural_network import NeuralNetwork

try:
    import autograd.numpy as anp
    from autograd import jacobian
except ImportError as e:
    logging.error(f"Failed to import autograd modules: {e}")


Tensor = Any


class QNNAutograd(NeuralNetwork):
    """Use autograd's automatic differentiation (autodiff) to implement the
    ``forward`` and ``backward``of the neural network.
    """

    def __init__(
        self,
        circuit: Callable[[Tensor, Tensor], Tensor],
        num_inputs: int,
        num_weights: int,
        output_shape: int | tuple[int, ...],
        input_gradients: bool = True,
        sparse: bool = False,
    ) -> None:
        super().__init__(
            num_inputs=num_inputs,
            num_weights=num_weights,
            sparse=sparse,
            output_shape=output_shape,
            input_gradients=input_gradients,
        )

        self.circuit = circuit

    def _forward(
        self,
        inputs: Tensor,
        weights: Tensor,
    ) -> Tensor:
        """The implementation of forward calculation."""
        inputs = anp.array(inputs)
        weights = anp.array(weights)

        output_data = [self.circuit(input, weights) for input in inputs]
        return np.array(output_data).reshape(-1, len(inputs))

    def _backward(
        self,
        inputs: Tensor,
        weights: Tensor,
    ) -> Tensor:
        """The implementation of backward calculation."""
        inputs = anp.array(inputs)
        weights = anp.array(weights)

        inputs_grad = np.array(
            [jacobian(self.circuit, 0)(input, weights) for input in inputs]
        )
        inputs_shape = inputs_grad.shape

        weights_grad = np.array(
            [jacobian(self.circuit, 1)(input, weights) for input in inputs]
        )
        weights_shape = weights_grad.shape

        if not self._input_gradients:
            return None, np.array(weights_grad)

        return (
            inputs_grad.reshape(-1, *inputs_shape),
            weights_grad.reshape(-1, *weights_shape),
        )
