# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""TensorFlow backend.
"""

from __future__ import annotations

import math
import os
from collections.abc import Sequence
from typing import Any

from .state_vector_simulator import StateVectorSimulator

if os.environ.get("TF_ENABLE", "0") == "1":
    try:
        import tensorflow as tf

        tf_dtype = tf.complex64
    except Exception:
        tf_dtype = None
else:
    tf_dtype = None


Tensor = Any


class TensorFlowBackend(StateVectorSimulator):
    """This method inherits the ``StateVectorSimulator``, and uses
    tensorflow to perform the mathematical calculation.
    """

    def __init__(self, dtype=None) -> None:
        if dtype is None:
            self.dtype = tf_dtype
        else:
            self.dtype = dtype

    def as_tensor(self, tensor: Tensor) -> Tensor:
        return tf.cast(tf.convert_to_tensor(tensor), self.dtype)

    def H(self) -> Tensor:
        return tf.complex(1.0 / tf.sqrt(2.0), 0.0) * tf.constant(
            [
                [1, 1],
                [1, -1],
            ],
            dtype=self.dtype,
        )

    def X(self) -> Tensor:
        return tf.constant(
            [
                [0, 1],
                [1, 0],
            ],
            dtype=self.dtype,
        )

    def Y(self) -> Tensor:
        return tf.constant(
            [
                [0j, -1j],
                [1j, 0j],
            ],
            dtype=self.dtype,
        )

    def Z(self) -> Tensor:
        return tf.constant(
            [
                [1, 0],
                [0, -1],
            ],
            dtype=self.dtype,
        )

    def S(self) -> Tensor:
        return tf.constant(
            [
                [1 + 0j, 0j],
                [0j, 1j],
            ],
            dtype=self.dtype,
        )

    def T(self) -> Tensor:
        return tf.convert_to_tensor(
            [
                [tf.exp(tf.constant(-1j * math.pi / 8)), 0],
                [0, tf.exp(tf.constant(1j * math.pi / 8))],
            ],
            dtype=self.dtype,
        )

    def SD(self) -> Tensor:
        return tf.constant(
            [
                [1 + 0j, 0j],
                [0j, -1j],
            ],
            dtype=self.dtype,
        )

    def TD(self) -> Tensor:
        return tf.convert_to_tensor(
            [
                [tf.exp(tf.constant(1j * math.pi / 8)), 0],
                [0, tf.exp(tf.constant(-1j * math.pi / 8))],
            ],
            dtype=self.dtype,
        )

    def X2M(self) -> Tensor:
        return tf.complex(tf.sqrt(2.0) / 2.0, 0.0) * tf.constant(
            [
                [1 + 0j, 1j],
                [1j, 1 + 0j],
            ],
            dtype=self.dtype,
        )

    def X2P(self) -> Tensor:
        return tf.complex(tf.sqrt(2.0) / 2.0, 0.0) * tf.constant(
            [
                [1 + 0j, -1j],
                [-1j, 1 + 0j],
            ],
            dtype=self.dtype,
        )

    def Y2M(self) -> Tensor:
        return tf.complex(tf.sqrt(2.0) / 2.0, 0.0) * tf.constant(
            [
                [1, 1],
                [-1, 1],
            ],
            dtype=self.dtype,
        )

    def Y2P(self) -> Tensor:
        return tf.complex(tf.sqrt(2.0) / 2.0, 0.0) * tf.constant(
            [
                [1, -1],
                [1, 1],
            ],
            dtype=self.dtype,
        )

    def RX(self, theta: Tensor) -> Tensor:
        theta = tf.convert_to_tensor(theta)
        theta = tf.cast(tf.math.divide(theta, 2.0), self.dtype)
        return tf.reshape(
            tf.convert_to_tensor(
                (
                    tf.cos(theta),
                    -1j * tf.sin(theta),
                    -1j * tf.sin(theta),
                    tf.cos(theta),
                ),
            ),
            (2, 2),
        )

    def RY(self, theta: Tensor) -> Tensor:
        theta = tf.convert_to_tensor(theta)
        theta = tf.cast(tf.math.divide(theta, 2.0), self.dtype)
        return tf.reshape(
            tf.convert_to_tensor(
                (
                    tf.cos(theta),
                    -1 * tf.sin(theta),
                    tf.sin(theta),
                    tf.cos(theta),
                ),
            ),
            (2, 2),
        )

    def RZ(self, theta: Tensor) -> Tensor:
        theta = tf.convert_to_tensor(theta)
        theta = tf.cast(tf.math.divide(theta, 2.0), self.dtype)
        return tf.reshape(
            tf.convert_to_tensor(
                (
                    tf.exp(-1j * theta),
                    tf.cast(tf.constant(0.0), self.dtype),
                    tf.cast(tf.constant(0.0), self.dtype),
                    tf.exp(1j * theta),
                ),
            ),
            (2, 2),
        )

    def RXY(self, theta: Tensor, phi: Tensor) -> Tensor:
        theta = tf.convert_to_tensor(theta)
        phi = tf.convert_to_tensor(phi)

        theta = tf.cast(tf.math.divide(theta, 2.0), self.dtype)
        phi = tf.cast(tf.math.divide(phi, 2.0), self.dtype)

        return tf.reshape(
            tf.convert_to_tensor(
                (
                    tf.cos(theta),
                    -1j * tf.exp(-1j * phi) * tf.sin(theta),
                    -1j * tf.exp(1j * phi) * tf.sin(theta),
                    tf.cos(theta),
                ),
            ),
            (2, 2),
        )

    def get_zero_state(self, qnum: int) -> Tensor:
        state = tf.zeros(
            tf.pow(2, qnum),
            dtype=self.dtype,
        )
        state = tf.tensor_scatter_nd_update(state, indices=[[0]], updates=[1.0 + 0j])
        return state

    def reshape(self, state: Tensor, shape: Sequence) -> Tensor:
        return tf.reshape(state, shape)

    def ravel(self, state: Tensor) -> Tensor:
        return tf.experimental.numpy.ravel(state)

    def stack(self, states: Sequence[Tensor], axis: int = 0) -> Tensor:
        return tf.stack(states, axis=axis)

    def real(self, state: Tensor) -> Tensor:
        return tf.math.real(state)

    def sum(self, state: Tensor, axis: int | None = None) -> Tensor:
        return tf.math.reduce_sum(state, axis=axis)

    def conj(self, state: Tensor) -> Tensor:
        return tf.math.conj(state)

    def sqrt(self, state: Tensor) -> Tensor:
        return tf.sqrt(state)

    def copy(self, state: Tensor) -> Tensor:
        return tf.identity(state)

    def dot(self, state1: Tensor, state2: Tensor) -> Tensor:
        state1 = self.as_tensor(state1)
        state2 = self.as_tensor(state2)
        return tf.tensordot(state1, state2, [[0], [0]])
