# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""A Quantum Neural Network using parameter shift to get gradients, which is
useful for sampling measurement.
"""

from __future__ import annotations

from typing import Any, Callable

import numpy as np

from .neural_network import NeuralNetwork

Tensor = Any


class QNNParamShift(NeuralNetwork):
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

    def parameter_shift_input_element(self, input, weights, i):
        input = input.copy()
        input[i] += np.pi / 2
        forwards = np.array([self.circuit(input, weights)]).reshape(-1)
        input[i] -= np.pi
        backwards = np.array([self.circuit(input, weights)]).reshape(-1)
        return 0.5 * (forwards - backwards)

    def parameter_shift_weights_element(self, input, weights, i):
        weights = weights.copy()
        weights[i] += np.pi / 2
        forwards = np.array([self.circuit(input, weights)]).reshape(-1)
        weights[i] -= np.pi
        backwards = np.array([self.circuit(input, weights)]).reshape(-1)
        return 0.5 * (forwards - backwards)

    def parameter_shift_input(self, input, weights):
        input_len = len(input)
        for i in range(input_len):
            if i == 0:
                input_grad = self.parameter_shift_input_element(input, weights, i)
                continue

            input_grad = np.append(
                input_grad,
                self.parameter_shift_input_element(input, weights, i),
            )
        input_grad = input_grad.reshape(input_len, -1).T
        return input_grad

    def parameter_shift_weights(self, input, weights):
        weights_len = len(weights)
        for i in range(weights_len):
            if i == 0:
                weights_grad = self.parameter_shift_weights_element(input, weights, i)
                continue

            weights_grad = np.append(
                weights_grad,
                self.parameter_shift_weights_element(input, weights, i),
            )
        weights_grad = weights_grad.reshape(weights_len, -1).T
        return weights_grad

    def _forward(
        self,
        inputs: Tensor,
        weights: Tensor,
    ) -> Tensor:
        """The implementation of forward calculation."""

        inputs = np.array(inputs)
        weights = np.array(weights)

        for idx, input in enumerate(inputs):
            if idx == 0:
                output_data = np.array([self.circuit(input, weights)]).reshape(-1)
                continue
            output_data = np.append(
                output_data,
                np.array([self.circuit(input, weights)]).reshape(-1),
            )

        output_data = output_data.reshape(-1, len(inputs))

        return output_data

    def _backward(
        self,
        inputs: Tensor,
        weights: Tensor,
    ) -> Tensor:
        """The implementation of backward calculation."""

        inputs = np.array(inputs)
        weights = np.array(weights)

        for idx, input in enumerate(inputs):
            if idx == 0:
                inputs_grad = self.parameter_shift_input(input, weights)
                inputs_shape = inputs_grad.shape
                continue

            inputs_grad = np.append(
                inputs_grad, self.parameter_shift_input(input, weights), axis=0
            )

        for idx, input in enumerate(inputs):
            if idx == 0:
                weights_grad = self.parameter_shift_weights(input, weights)
                weights_shape = weights_grad.shape
                continue

            weights_grad = np.append(
                weights_grad,
                self.parameter_shift_weights(input, weights),
                axis=0,
            )

        inputs_grad = inputs_grad.reshape(-1, *inputs_shape)
        weights_grad = weights_grad.reshape(-1, *weights_shape)

        if not self._input_gradients:
            return None, weights_grad

        return inputs_grad, weights_grad
