# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2023.
# This code is licensed under the MIT License.

"""
All the backends needed for quantum circuit simulation.
The quantum circuit is based on parsing the qcis file.
The backend can be a simulator or hardware.
The simulator is based on state vectors.
"""

from .abstract_backend import AbstractBackend
from .arclight_backend import ArclightBackend
from .autograd_backend import AutogradBackend
from .numpy_backend import NumpyBackend
from .qcis_backend import QcisBackend
from .qcis_backend2 import QcisBackend2
from .tensorflow_backend import TensorFlowBackend
from .tiany_backend import TianyBackend
from .torch_backend import TorchBackend
