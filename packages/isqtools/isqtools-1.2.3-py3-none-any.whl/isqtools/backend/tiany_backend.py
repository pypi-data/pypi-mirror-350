from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from datetime import datetime

try:
    from cqlib import TianYanPlatform  # 导出量子计算机SDK的支持包
except:
    pass

from .hardware_backend import HardwareBackend


class TianyBackendError(Exception):
    """tianyan backend error"""


class TianyBackend(HardwareBackend):
    """The backend of Tianyan quantum hardware.

    token (str, optional): API token for authentication just passed when you are the first time use this backend or want to change your token. Defaults to None.

    machine_name (str, optional): Name of the machine. Defaults to full amplitude simulator .

    max_wait_time (int, optional): Maximum wait time in seconds. Defaults to 24*3600 (24 hours).

    lab_id (int | None, optional): Lab ID. Defaults to None.
    """

    def __init__(
        self,
        token: str | None = None,
        machine_name: str = "tianyan_sw",  # 默认是模拟器
        lab_id: int | None = None,
        max_wait_time: int = 5,
        **kw,
    ) -> None:

        self._token = token
        self._machine_name = machine_name
        self._max_wait_time = max_wait_time
        self._token_dir = os.path.join(self.get_homedir(), ".tianyan/")

        if token is None:
            self._token = self._load_account()
        else:
            self._token = token
            self._save_apitoken(self._token)
        if lab_id:
            self._lab_id = lab_id
        else:
            self._lab_id = f'lab.{datetime.now().strftime("%Y%m%d%H%M%S")}'

    def get_task_id(self, qcis, shots):
        self.platform = TianYanPlatform(
            login_key=self._token, machine_name=self._machine_name
        )
        lab_id = self.platform.create_lab(
            name=f"lab.{self._lab_id}", remark="test_collection"
        )
        self._query_id_single = self.platform.submit_job(
            circuit=qcis,
            lab_id=lab_id,
            exp_name=f'exp.{datetime.now().strftime("%Y%m%d%H%M%S")}',
            num_shots=shots,
        )

    def sample(
        self,
        qcis: str,
        shots: int = 100,
        **kwargs,
    ) -> dict[str, int]:
        """Call quantum hardware for sampling."""
        self.get_task_id(qcis, shots)
        return self.query_sample_result(self.query_id_single, self._max_wait_time)

    @property
    def query_id_single(self):
        return self._query_id_single

    def query_sample_result(self, query_id_single: list[str], max_wait_time: int = 1):
        try:
            measure_result = self.platform.query_experiment(
                query_id=query_id_single,
                max_wait_time=max_wait_time,
                sleep_time=0,
            )
        except Exception:
            print("Task is not done.")
            return []
        sample = self._stream_to_dict(measure_result)
        return sample

    def _load_account(self):
        file_dir = os.path.join(self._token_dir, "api")
        try:
            with open(file_dir, "r") as f:  # pylint: disable=unspecified-encoding
                data = json.load(f)
                token = data["token"]
        except FileNotFoundError as exc:
            raise TianyBackendError("Please provide the token.") from exc
        return token

    def _save_apitoken(self, token):
        data = {"token": token}
        file_path = os.path.join(self._token_dir, "api")
        if not os.path.exists(self._token_dir):
            os.mkdir(self._token_dir)
        with open(
            file_path, "w"
        ) as f:  # noqa:SCS109 # pylint: disable=unspecified-encoding
            json.dump(data, f)  # 保存为字典

    def _stream_to_dict(self, measure_result):
        answer = defaultdict(int)
        # defaultdict is used for data processing.
        # print(1112, measure_result[0]["probability"])
        for t in measure_result[0]["resultStatus"][1:]:
            x = "".join([str(v) for v in t])
            answer[x] += 1
        res = dict(answer)
        return res

    @staticmethod
    def get_homedir():
        if sys.platform == "win32":
            return os.environ["USERPROFILE"]
        if sys.platform in ["darwin", "linux"]:
            return os.environ["HOME"]
        raise ValueError(
            f"unsupported platform:{sys.platform}. "
            f"You may raise a request issue on github."
        )
