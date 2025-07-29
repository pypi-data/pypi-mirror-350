# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Abstract backend."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

Tensor = Any


class AbstractBackend(ABC):
    """Abstract backend to run quantum circuits. This is the basis for
    all simulation and hardware methods.
    """

    @abstractmethod
    def probs(self) -> Tensor:
        """This method can get all the probability distributions
        after the measurement of the specified qubit. The probability
        distribution obtained by this method is the theoretical value
        after the state vector simulation, and shots are not considered.
        Therefore, this method can only be used for circuit simulation
        and cannot be used for hardware backends.

        Returns:
            Tensor(array) distribution. Sort by the size of the binary
            representation of the quantum state.

        """

    @abstractmethod
    def sample(self) -> dict[str, int]:
        """This method can get the sampling result of the specified qubit
        measurement. Unlike the ``probs`` method, this method obtains the
        measurement results of the quantum circuit by sampling, and the
        results are related to shots. This method can be implemented using
        a simulator or the specific hardware.

        Returns:
            This method returns a dictionary, the key in the dictionary is
            the quantum state, and the value is the shots of the quantum state.

        """
