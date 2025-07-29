# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Quantum hardware operations are performed by submitting the
QCIS instruction set. This file is the basis for hardware.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import NoReturn

from .abstract_backend import AbstractBackend


class HardwareBackendError(Exception):
    """Error for hardware running."""


class HardwareBackend(AbstractBackend):
    """Hardware running base."""

    def probs(self) -> NoReturn:
        """Running a circuit on hardware is different from a simulator,
        and it is impossible to obtain an accurate probability distribution.

        Raises:
            HardwareBackendError: ``probs`` cannot run on the hardware,
            please use the ``sample``.

        """
        raise HardwareBackendError(
            "To run on hardware, "
            "you must use the `sample` method and specify `shots`. "
            "`probs` is not supported."
        )

    def sample(
        self,
        data: str,
        shots: int = 100,
        **kwargs,
    ) -> dict[str, int]:
        """Sampling quantum circuits using hardware. This is an abstraction
        over the concrete method.

        Args:
            data: QCIS strings, This represents the information of the
                  quantum circuit.
            shots: Shots numbers.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            This method returns a dictionary, the key in the dictionary is
            the quantum state, and the value is the shots of the quantum state.

        """
        raise NotImplementedError


class TaskType:
    """Type of hardware."""

    QCIS = "QCIS"
    QCIS2 = "QCIS2"
    ARCLIGHT = "ARCLIGHT"
    # AWS = "AWS"
    # SCQ = "SCQ"


class TaskState:
    """Types of hardware tasks."""

    WAIT = "WAITING"
    COMPLETE = "COMPLETED"
    FAIL = "FAILED"
    CANCEL = "CANCELLED"


class ISQTask:
    """isq hardware task interface, used to execute hardware tasks."""

    NO_RESULT_TERMINAL_STATES = {TaskState.FAIL, TaskState.CANCEL}

    def __init__(
        self,
        task_id: int | str,
        task_type: str,
        state: str,
        device: HardwareBackend,
        shots: int,
        **kwargs,
    ) -> None:
        self._id = task_id
        self._type = task_type
        self._state = state
        self._res = {}
        self._device = device
        self.logger = logging.getLogger(__name__)
        if "logger" in kwargs:
            self.logger = kwargs["logger"]
        self.shots = shots

    @property
    def state(self) -> str:
        """Get the status of the task.

        Returns:
            Returns four different states:
            1) WAITING.
            2) COMPLETED.
            3) FAILED.
            4) CANCELLED.

        """
        return self._state

    def result(self) -> dict:
        """Query the result of the task according to the id
        of the task.

        Returns:
            This method returns a dictionary, which is the same fotmat
            as ``sample``.

        """
        if self._state in self.NO_RESULT_TERMINAL_STATES:
            return {}

        elif self._state == TaskState.COMPLETE:
            return self._res

        if self._type == TaskType.QCIS:
            # When using qcis hardware, the id of the task is used to
            # get the result of the task.
            measure_result = self._device._account.query_experiment(
                self._id,
                max_wait_time=self._device._max_wait_time,
            )
            if measure_result:
                # measure_result example (shots = 10):
                # [{'resultStatus': [[14, 9, 15], [1, 1, 1], [1, 0, 0],
                # [1, 1, 0], [1, 1, 1], [1, 0, 0], [0, 1, 1], [1, 1, 0],
                # [0, 0, 1], [0, 0, 1], [1, 0, 0]], 'probability': {'000':
                # 0.0, '011': 0.2062521227977389, '110': 0.09061964381995466,
                # '001': 0.2800637719904287, '100': 0.18968664161204915, '111':
                # 0.23337781977982858, '101': 0.0, '010': 0.0},
                # 'experimentTaskId': '1717068093878177792'}]
                self.logger.info("Task executed successfully!")
                self._state = TaskState.COMPLETE
                if self._device.is_prob == "0":
                    self._res = {
                        k: v * self.shots
                        for k, v in measure_result[0]["probability"].items()
                    }
                elif self._device.is_prob == "1":
                    answer = defaultdict(int)
                    # defaultdict is used for data processing.
                    for t in measure_result[0]["resultStatus"][1:]:
                        x = "".join([str(v) for v in t])
                        answer[x] += 1
                    self._res = dict(answer)
                elif self._device.is_prob == "2":
                    self._res = measure_result[0]["resultStatus"][1:]
            else:
                self.logger.info("Task execution, please wait.")

        if self._type == TaskType.QCIS2:
            # When using qcis hardware, the id of the task is used to
            # get the result of the task.
            measure_result = self._device._account.query_experiment(
                self._id,
                max_wait_time=self._device._max_wait_time,
            )
            if measure_result:
                # measure_result example (shots = 10):
                # [{'probability': {'0': 0.7002964101438138,
                # '1': 0.2997035898561862}, # 'experimentTaskId':
                # '3822987317073968ustc00000829969',
                # 'results': [[27], [0], [0], [1], [0], [1], [1], [0], [0],
                # [0], [0]]}]
                self.logger.info("Task executed successfully!")
                self._state = TaskState.COMPLETE
                if self._device.is_prob:
                    self._res = {
                        k: v * self.shots
                        for k, v in measure_result[0]["probability"].items()
                    }
                else:
                    answer = defaultdict(int)
                    # defaultdict is used for data processing.
                    for t in measure_result[0]["results"][1:]:
                        x = "".join([str(v) for v in t])
                        answer[x] += 1
                    self._res = dict(answer)
            else:
                self.logger.info("Task execution, please wait.")

        if self._type == TaskType.ARCLIGHT:
            measure_result = self._device._get_result(self._id)
            if measure_result:
                self._state = TaskState.COMPLETE
                self._res = measure_result.get("data")

        return self._res
