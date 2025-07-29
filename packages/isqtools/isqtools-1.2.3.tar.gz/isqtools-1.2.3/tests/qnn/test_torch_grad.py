import pytest

torch = pytest.importorskip("torch")


import tempfile
from pathlib import Path

import numpy as np
import torch

from isqtools import IsqCircuit
from isqtools.backend import TorchBackend

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


def test_torch_grad():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file_path = temp_dir_path / "temp_file.isq"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(GRAD_ISQ)

        torch_backend = TorchBackend()
        params = torch.tensor([0.9, 1.2], requires_grad=True)
        qc = IsqCircuit(
            file=str(temp_file_path),
            backend=torch_backend,
            sample=False,
        )

        def circuit(params):
            results = qc.measure(params=params)
            return results[0]

        result = circuit(params)

        assert result.item() == pytest.approx(0.6126225961314372)
        result.backward()
        np.testing.assert_allclose(
            params.grad.detach().cpu().numpy(),
            np.array([-0.14192229, -0.28968239], dtype=np.float32),
            atol=1e-7,
        )
