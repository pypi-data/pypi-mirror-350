import tempfile
from pathlib import Path

import numpy as np

from isqtools import IsqCircuit
from isqtools.backend import NumpyBackend

SIMPLE_ISQ = """
import std;

qbit q[2];

procedure main() {
    H(q[0]);
    H(q[1]);
    M(q[0]);
    M(q[1]);
}
"""


def test_numpy_measure():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file_path = temp_dir_path / "temp_file.isq"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(SIMPLE_ISQ)
        backend = NumpyBackend()
        qc = IsqCircuit(
            file=str(temp_file_path),
            backend=backend,
            sample=False,
        )
        results = np.array([0.25, 0.25, 0.25, 0.25])
        np.testing.assert_allclose(qc.measure(), results)


def test_numpy_sample():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file_path = temp_dir_path / "temp_file.isq"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(SIMPLE_ISQ)
        backend = NumpyBackend()
        qc = IsqCircuit(
            file=str(temp_file_path),
            backend=backend,
            sample=True,
            shots=1024,
        )
        assert qc.measure(rng_seed=10) == {"11": 260, "00": 266, "10": 248, "01": 250}
