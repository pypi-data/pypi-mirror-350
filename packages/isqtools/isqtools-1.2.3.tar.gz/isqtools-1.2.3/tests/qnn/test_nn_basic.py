import pytest

torch = pytest.importorskip("torch")


import random
import tempfile
from pathlib import Path

import numpy as np
import torch
import torch.optim as optim

from isqtools import IsqCircuit
from isqtools.backend import TorchBackend
from isqtools.neural_networks import TorchLayer


@pytest.fixture(scope="module", autouse=True)
def set_seed():
    seed = 222
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)


@pytest.fixture(scope="module")
def qc():
    with tempfile.TemporaryDirectory() as temp_dir:
        script_dir = Path(__file__).resolve().parent
        file_path = script_dir / "nn_basic.isq"
        temp_dir_path = Path(temp_dir)
        temp_file_path = temp_dir_path / "temp_file.isq"
        temp_file_path.write_text(file_path.read_text())

        if not temp_file_path.exists():
            raise FileNotFoundError(f"File not found: {temp_file_path}")

        backend = TorchBackend()
        isq_circuit = IsqCircuit(
            file=str(temp_file_path),
            backend=backend,
            sample=False,
        )
        yield isq_circuit


@pytest.fixture(scope="module")
def circuit(qc):
    def _circuit(inputs, weights):
        param = {
            "inputs": inputs,
            "weights": weights,
        }
        return qc.pauli_measure(**param)

    return _circuit


@pytest.fixture(scope="module")
def qnn(circuit):
    weights = torch.randn(24)
    return TorchLayer(
        circuit=circuit,
        is_vmap=False,
        num_weights=24,
        initial_weights=weights,
    )


def test_nn_run(circuit):
    inputs = torch.randn(4)
    weights = torch.randn(24)
    expected_result = np.array([-0.127469], dtype=np.float32)

    result = circuit(inputs, weights).detach().cpu().numpy()
    np.testing.assert_allclose(result, expected_result[0], atol=1e-6)


def test_qnn(qnn):
    inputs = torch.randn(4)
    expected_result = np.array([0.03218], dtype=np.float32)

    result = qnn(inputs).detach().cpu().numpy()
    np.testing.assert_allclose(result, expected_result[0], atol=1e-6)


def test_opt(qnn):
    inputs = torch.randn(4)
    optimizer = optim.SGD(qnn.parameters(), lr=0.05)

    for i in range(50):
        measurement = qnn(inputs)
        measurement.backward()
        optimizer.step()
        optimizer.zero_grad()
    assert measurement.item() < 0.9
