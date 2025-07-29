# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""Qcis2 hardware backend.
For more information, check out: https://quantumcomputer.ac.cn/
"""

from __future__ import annotations

import logging
import secrets
import string
import time

from numpy import pi

from .hardware_backend import HardwareBackend, ISQTask, TaskState, TaskType

try:
    from pyezQ import Account

    # pyezQ is necessary for the execution of the hardware.
except ImportError as e:
    logging.info(f"Failed to import pyezQ module: {e}")


def load_params(qcis: str, **kw) -> str:
    """Use the periodicity to convert the angles in all rotation operations to
    the range of -2pi to 2pi.

    Args:
        qcis: qcis for quantum circuits.

    Returns:
        qcis being converted.

    """
    line_data = qcis.split("\n")
    new_qcis = []
    for line in line_data:
        line = line.strip()
        if not line:
            continue
        str_arr = line.split(" ")
        if str_arr[0] in ["RX", "RY", "RZ", "RXY"]:
            theta_arr = []
            for v in str_arr[2:]:
                theta = float(eval(v, kw))
                theta %= 4 * pi
                if theta > 2 * pi:
                    theta -= 4 * pi
                theta_arr.append(str(theta))
            new_line = str_arr[:2] + theta_arr
            new_qcis.append(" ".join(new_line))
        else:
            new_qcis.append(line)
    return "\n".join(new_qcis)


def split_rotation_gates(qcis: str) -> str:
    """The qcis hardware currently has certain limitations. For the rotation
    operation, when the angle is in the range of -2pi to -pi and pi to 2pi, it
    is necessary to divide the angle into two and convert it into two rotation
    operations.

    Args:
        qcis: qcis for quantum circuits.

    Returns:
        qcis being converted.

    """
    ir_list = qcis.split("\n")
    ir_list_copy = ir_list.copy()
    for i, ir in enumerate(ir_list):
        if ir.startswith("RXY"):
            ir_list_copy_list = ir_list_copy[i].split()
            if float(ir_list_copy_list[3]) > pi or float(ir_list_copy_list[3]) < -pi:
                q, phi, theta = (
                    ir_list_copy_list[1],
                    float(ir_list_copy_list[2]),
                    float(ir_list_copy_list[3]),
                )
                decompose = []
                phi1 = pi / 2 - phi
                if abs(phi1) > pi:
                    decompose.append(f"RZ {q} {phi1/2}")
                    decompose.append(f"RZ {q} {phi1/2}")
                else:
                    decompose.append(f"RZ {q} {phi1}")
                decompose.append(f"X2P {q}")
                decompose.append(f"RZ {q} {theta / 2}")
                decompose.append(f"RZ {q} {theta / 2}")
                decompose.append(f"X2M {q}")
                phi2 = phi - pi / 2
                if abs(phi2) > pi:
                    decompose.append(f"RZ {q} {phi2/2}")
                    decompose.append(f"RZ {q} {phi2/2}")
                else:
                    decompose.append(f"RZ {q} {phi2}")
                ir_list_copy[i] = "\n".join(decompose)
        elif any([ir.startswith("RX"), ir.startswith("RY"), ir.startswith("RZ")]):
            ir_list_copy_list = ir_list_copy[i].split()
            if float(ir_list_copy_list[2]) > pi or float(ir_list_copy_list[2]) < -pi:
                ir_list_copy_list_new = ir_list_copy_list.copy()
                ir_list_copy_list_new[2] = str(float(ir_list_copy_list[2]) / 2)
                ir_list_copy_new = " ".join(ir_list_copy_list_new)
                new_str = ir_list_copy_new + "\n" + ir_list_copy_new
                ir_list_copy[i] = new_str

    return "\n".join(ir_list_copy)


def get_rand_str() -> str:
    """Generate a cryptographically secure random string."""
    rand_str = "".join(secrets.choice(string.ascii_lowercase) for _ in range(10))
    return rand_str


class QcisBackend2Error(Exception):
    """Qcis backend error"""


class QcisBackend2(HardwareBackend):
    """the backend of qcis quantum hardware"""

    def __init__(
        self,
        login_key: str,
        machine_name: str,
        lab_id: str | None = None,
        exp_name: str | None = None,
        # remark: str = "arclight",
        max_wait_time: int = 60,
        sleep_time: int = 3,
        run_time: int | None = None,
        mapping: bool = False,
        is_prob: bool = False,
        logger=None,
    ) -> None:
        if logger is None:
            logger = logging.getLogger(__name__)

        self.sleep_time = sleep_time
        self.run_time = run_time
        self.mapping = mapping
        self.is_prob = is_prob
        self.logger = logger

        self._account = Account(login_key=login_key, machine_name=machine_name)

        if lab_id:
            self.lab_id = lab_id
        else:
            if exp_name is None:
                time_now = time.strftime(
                    "%Y_%m_%d_%H_%M_%S", time.localtime(time.time())
                )
                exp_name = f"arclight_{time_now}"
            create_res = self._account.create_experiment(
                exp_name,
                # remark=remark,
                # NOTE: different from ezQgd
            )
            if create_res == 0:
                print("新建实验合集失败")
            else:
                print("新建实验合辑成功，ID=", create_res)
                self.lab_id = create_res

        self._qid = 0
        self._max_wait_time = max_wait_time

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
        if self.mapping:
            qcis_split_rotation_gates = self._account.qcis_mapping_isq(
                qcis_split_rotation_gates
            )
        time_now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
        query_id = self._account.submit_job(
            circuit=qcis_split_rotation_gates,
            lab_id=self.lab_id,
            version=f"{self._qid}_{time_now}",
            num_shots=shots,
        )
        self._qid += 1
        if query_id:
            self.logger.info("Qcis hardware: submitted the task successfully.")
            task = ISQTask(query_id, TaskType.QCIS2, TaskState.WAIT, self, shots)
        else:
            self.logger.error(
                "Qcis submission failed, please confirm whether the hardware"
                "is normal, or try again later."
            )
            task = ISQTask(0, TaskType.QCIS2, TaskState.FAIL, self, shots)

        if self.run_time is not None:
            start_time = time.time()

        while task.state == TaskState.WAIT:
            try:
                task.result()
                time.sleep(self.sleep_time)
            except Exception as e:
                continue

            # Wait for a period of time before doing an http request
            if self.run_time is not None:
                if time.time() > start_time + self.run_time:
                    break
        return task.result()
