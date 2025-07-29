# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Arclight quantum cloud backend.
For more information, check out: http://qcloud.arclightquantum.com/#/home
"""

from __future__ import annotations

import json
import os
import time

from .hardware_backend import HardwareBackend, ISQTask, TaskState, TaskType
from .qcis_backend import get_rand_str, load_params, split_rotation_gates

try:
    import requests
except ModuleNotFoundError:
    pass


class ArclightBackend(HardwareBackend):
    """The backend of arclighth quantum cloud."""

    def __init__(
        self,
        token: str | None = None,
        version: str | None = None,
        # max_wait_time: int = 60,
        sleep_time: int = 3,
        run_time: int | None = None,
        mapping: bool = False,
    ) -> None:
        if token is None:
            token_path = os.path.expanduser("~/.isq/token")
            with open(token_path, "r") as token_file:
                token = token_file.read()
        self.headers = {"Authorization": token}
        self.host = "https://qcloud.arclightquantum.com"

        if version is None:
            self.version = ""
        else:
            self.version = str(version)

        # self._max_wait_time = max_wait_time
        self.sleep_time = sleep_time
        self.run_time = run_time
        self.mapping = mapping
        if self.mapping:
            print("Mapping is not implemented yet.")
        # TODO: Implement mapping

    def _post_circuit(
        self,
        circuit: str,
        shots: int,
    ) -> dict:
        if self.version:
            version_posted = f"{self.version}_{get_rand_str()}"
        else:
            version_posted = get_rand_str()

        post_url = f"{self.host}/qcloud/task/submit/job"
        param = {
            "circuit": circuit,
            "shots": shots,
            "version": version_posted,
        }

        post_response = requests.post(
            post_url,
            json=param,
            headers=self.headers,
        )

        return self._response_process(post_response)

    def _get_result(self, id: str) -> dict:
        get_url = f"{self.host}/qcloud/task/info/{id}"
        get_response = requests.get(get_url, headers=self.headers)
        return self._response_process(get_response)

    @staticmethod
    def _response_process(
        response: requests.models.Response,
    ) -> dict:
        status_code = response.status_code
        if status_code == 200:
            response_dict = json.loads(response.text)
            if response_dict.get("code") == 0:
                return response_dict
            elif response_dict.get("code") == -1:
                print(response_dict.get("msg"))
                return {}
        # FIX: not print every `Error code`
        else:
            print(f"Error code: {status_code}.")
            return {}

    def sample(
        self,
        data: str,
        shots: int = 100,
        **kwargs,
    ) -> dict[str, int]:
        """Call quantum hardware for sampling.

        Args:
            data: QCIS strings, This represents the information of the quantum
                  circuit.
            shots: Shots numbers.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            This method returns a dictionary, the key in the dictionary is
            the quantum state, and the value is the shots of the quantum state.

        """

        qcis_split_rotation_gates = split_rotation_gates(
            load_params(data, **kwargs),
        )

        post_dict = self._post_circuit(
            circuit=qcis_split_rotation_gates,
            shots=shots,
        )

        if post_dict:
            task = ISQTask(
                post_dict.get("data"),
                TaskType.ARCLIGHT,
                TaskState.WAIT,
                self,
            )
        else:
            task = ISQTask(
                0,
                TaskType.ARCLIGHT,
                TaskState.FAIL,
                self,
            )

        if self.run_time is not None:
            start_time = time.time()

        while task.state == TaskState.WAIT:
            print("request_test")
            task.result()
            time.sleep(self.sleep_time)
            # Wait for a period of time before doing an http request
            if self.run_time is not None:
                if time.time() > start_time + self.run_time:
                    break
        return task.result()
