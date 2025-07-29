# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Isq quantum circuit.
Use ``isqc`` to generate qcis files, and generate quantum circuits by reading
qcis files. IsqCircuit is our recommended way to build quantum circuits.
"""

from __future__ import annotations

import os
from collections.abc import Sequence
from typing import Any

from isqtools.backend import AbstractBackend, NumpyBackend
from isqtools.utils import gen_qcis_from_so, isqc_compile

from .abstract_circuit import AbstractCircuit

Tensor = Any


class IsqCircuitError(Exception):
    """IsQ quantum circuits error."""


class IsqCircuit(AbstractCircuit):
    """IsQ quantum circuit class.

    Attributes:
        backend: The backend on which the task runs, such as a simulator or hardware.
        sample: Whether to enable sampling mode. For simulators, supports
            ``sample`` or ``probs`` modes. For hardware, only sampling mode
            is supported.
        shots: Specifies the number of shots when sampling mode is enabled.
        qcis: Qcis instruction set for quantum circuits.

    """

    def __init__(
        self,
        file: str | None = None,
        backend: AbstractBackend | None = None,
        sample: bool = False,
        shots: int = 100,
        int_param: Sequence[int] | int | None = None,
        double_param: Sequence[float] | float | None = None,
        **kw,
    ) -> None:
        """Initialization of isq quantum circuits.

        Args:
            file: The file path. It is recommended to use full paths, be
                  careful when using relative paths.
                  1) When the file extension is ``.isq``, the isq file will be
                     compiled into qcis.
                  2) When the extension of the file is ``qcis``, read the file
                     directly.
                  3) When the extension of the file is ``so``, it will be
                     called ``gen_qcis_from_so`` to process the ``so`` file
                     to generate qcis.
            backend: The backend on which the task runs can be a simulator or
                     hardware.
            sample: Whether to enable sampling mode. When the backend is a
                    simulator, you can ``sample`` or ``probs``. If the backend
                    is hardware, you can only enable the sampling mode.
            shots: When the sampling mode is enabled, this parameter can
                   specify the shots number.
            int_param: Int data when compiling qcis.
            double_param: Double data when compiling qcis.
            **kw: Optional parameters.

        Raises:
            IsqCircuitError: Check the extension of the ``file``.

        """

        if file is not None:
            if file.endswith(".isq"):
                # compile every time you build the class
                isqc_compile(
                    file=file,
                    target="qcis",
                    int_param=int_param,
                    double_param=double_param,
                )
                qcis_path = os.path.splitext(file)[0] + ".qcis"

            elif file.endswith(".qcis"):
                qcis_path = file

            elif file.endswith(".so"):
                # compile once
                # this is an advanced, not recommended
                gen_qcis_from_so(
                    file=file,
                    int_param=int_param,
                    double_param=double_param,
                )
                qcis_path = os.path.splitext(file)[0] + ".qcis"

            else:
                raise IsqCircuitError(
                    f"`{file}`'s format is not supported"
                    "Please use `.isq` or `.qcis` format of circuits."
                    "Both absolute `/home/username/file.isq` and"
                    "relative paths `file.isq` are supported,"
                    "but this kind of path `./file.isq` is not supported"
                )

            with open(qcis_path, "r") as qcis:
                lines = (line.rstrip() for line in qcis)
                lines = (line for line in lines if line)
                self.qcis = "\n".join(lines)
        else:
            self.qcis = kw["qcis"]

        if backend is None:
            backend = NumpyBackend()

        super().__init__(
            backend=backend,
            sample=sample,
            shots=shots,
        )

    def measure(self, **kw) -> dict[str, int] | Tensor:
        """Taking measurements on quantum circuits.

        Args:
            **kw: Corresponding to the parameters in qcis and the ``param`` in
                  isq file.

        Returns:
            Depending on whether to sample or not, the measurement result
            is obtained.

        """
        if not self.sample:
            measure_result = self.backend.probs(self.qcis, **kw)
        else:
            measure_result = self.backend.sample(self.qcis, self.shots, **kw)
        return measure_result

    def pauli_measure(self, **kw) -> Tensor:
        """Taking Pauli measurements on quantum circuits.

        Args:
            **kw: Corresponding to the parameters in qcis and the ``param`` in
                  isq file.

        Returns:
            Depending on whether to sample or not, the measurement result
            is obtained. The measurement result will get the final result
            according to the rules of Pauli operation. This measurement method
            needs to implement the corresponding Pauli measurement in the isq
            file.

        """
        if self.sample:
            measure_result_dict = self.measure(**kw)
            result = 0
            for res_index, frequency in measure_result_dict.items():
                parity = (-1) ** (res_index.count("1") % 2)
                # e.g. {"011": 222}, to count "1"
                result += parity * frequency / self.shots
            return result
        else:
            measure_result_array = self.measure(**kw)
            parity = [
                (-1) ** (str(bin(int(index))).count("1") % 2)
                for index in range(len(measure_result_array))
            ]
            return self.backend.dot(
                measure_result_array,
                self.backend.as_tensor(parity),
            )

    def state(self, **kw) -> Tensor:
        """Get the simulated quantum state.

        Args:
            **kw: Corresponding to the parameters in qcis and the ``param`` in
                  isq file.

        Returns:
            State vector.

        Raises:
            IsqCircuitError: This method can only be used in non-sample.

        """
        if not self.sample:
            return self.backend.state(self.qcis, **kw)
        else:
            raise IsqCircuitError(
                "The quantum state cannot be obtained during the sample."
            )
