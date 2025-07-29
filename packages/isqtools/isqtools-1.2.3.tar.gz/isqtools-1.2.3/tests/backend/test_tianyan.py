import tempfile
from pathlib import Path

import pytest

from isqtools import IsqCircuit
from isqtools.backend import TianyBackend

TEST_FILE_CONTENT = """
import std;
procedure main(int seq[], double double_[]) {
    int qbit_topo[]=[0,1,2,3,4,5,6];
    qbit q[seq[0]];
    X(q[qbit_topo[0]]);
    M(q[qbit_topo[0]]);
}
"""


def test_tianyan_simulator(request):
    if not request.config.getoption("--run-tianyan"):
        pytest.skip("Skipping TianyBackend test since --run-tianyan is not set")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file_path = temp_dir_path / "temp_file.isq"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(TEST_FILE_CONTENT)

        backend = TianyBackend(
            token="Ev5Ex6zUru41Grtoixg68ac2fCPW5cBrWxLVyPkavG0=",
            machine_name="tianyan_sw",
            max_wait_time=1,
        )

        qc = IsqCircuit(
            file=str(temp_file_path),
            sample=True,
            shots=100,
            backend=backend,
            int_param=[1],
        )
        result = qc.measure()

        query_id_single = backend.query_id_single
        while not result:
            result = backend.query_sample_result(
                query_id_single=query_id_single, max_wait_time=1
            )
