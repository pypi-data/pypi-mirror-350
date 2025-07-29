# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Abstract quantum circuit.
The core of current quantum circuits is the Qcis instruction set. The qcis file
compiled by the isq compiler (icqc) is the main quantum circuit construction
method, and other methods are not recommended.
"""

from abc import ABC, abstractmethod

import numpy as np

from isqtools.backend import AbstractBackend


class AbstractCircuit(ABC):
    """Abstract quantum circuit.

    Attributes:
        backend: The backend on which the task runs can be a simulator or
                 hardware.
        sample: Whether to enable sampling mode. When the backend is a
                simulator, you can ``sample`` or ``probs``. If the backend is
                hardware, you can only enable the sampling mode.
        shots: When the sampling mode is enabled, this parameter can specify
               the shots number.

    """

    def __init__(
        self,
        backend: AbstractBackend,
        sample: bool,
        shots: int = 100,
    ) -> None:
        self.backend = backend
        self.sample = sample
        self.shots = shots

    @abstractmethod
    def measure(self, **kw):
        """Taking measurements on quantum circuits."""

    @abstractmethod
    def pauli_measure(self, **kw):
        """Taking Pauli measurements on quantum circuits."""

    def __repr__(self) -> str:
        """Returns the Qcis instruction set for a quantum circuit."""
        return self.qcis

    __str__ = __repr__

    def dict2array(
        self,
        result_dicts: dict,
    ) -> np.ndarray:
        """Transfer measurement results from Dict to Array.

        Args:
            result_dicts: Use a dict to represent measurements, for example:
                          ``{"00": 10, "01": 25, "10": 30, "11": 35}``.

        Returns:
            Use array to represent the measurement results, arranged in binary
            order, for example: ``[0.1, 0.25, 0.3, 0.35]``.

        """
        shots = self.shots
        len_array = len(list(result_dicts.keys())[0])
        results_arrays = np.zeros(2**len_array)

        for bin_idx, freq in result_dicts.items():
            results_arrays[int(bin_idx, 2)] = float(freq / shots)
        return results_arrays

    def sort_dict(
        self,
        result_dicts: dict,
    ) -> dict:
        """After the python >= 3.6, the dict will save the order. Use this
        method to sort the measurement results dictionary in binary.
        """
        return dict(
            sorted(
                result_dicts.items(),
                key=lambda item: int(item[0], 2),
            )
        )
