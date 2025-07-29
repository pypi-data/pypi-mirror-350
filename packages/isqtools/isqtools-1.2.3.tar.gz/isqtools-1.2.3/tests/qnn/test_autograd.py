import pytest

autograd = pytest.importorskip("autograd")


import tempfile
from pathlib import Path

import numpy as np
from autograd import grad

from isqtools import IsqCircuit
from isqtools.backend import AutogradBackend

GRAD_ISQ = """
import std;


param params[];
qbit q[1];

procedure main() {
    Ry(params[0], q[0]);
    Rx(params[1], q[0]);
    M(q[0]);
}
"""


def test_autograd():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file_path = temp_dir_path / "temp_file.isq"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(GRAD_ISQ)

        autograd_backend = AutogradBackend()
        params = np.array([0.9, 1.2])
        qc = IsqCircuit(
            file=str(temp_file_path),
            backend=autograd_backend,
            sample=False,
        )

        def circuit(params):
            results = qc.measure(params=params)
            return results[0]

        assert circuit(params) == pytest.approx(0.6126225961314372)
        grad_circuit1 = grad(circuit, [0])
        np.testing.assert_allclose(
            grad_circuit1(params)[0], np.array([-0.14192229, -0.28968239])
        )
