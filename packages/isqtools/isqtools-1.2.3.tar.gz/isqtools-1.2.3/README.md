# isqtools

<!-- home start -->

The **isqtools** is the Python interface for [**isQ**](https://www.arclightquantum.com/isq-docs/latest/) – a high-level quantum programming language developed by [**Arclight Quantum**](https://www.arclightquantum.com/). The isqtools library facilitates interaction with [**isQ**](https://www.arclightquantum.com/isq-docs/latest/), enabling users to construct, analyze, and execute quantum programs seamlessly within Python.

## Features

- Integration with [**isQ**](https://www.arclightquantum.com/isq-docs/latest/)
- Quantum Circuit Construction and Simulation
- Support for Quantum Machine Learning

<!-- home end -->

<!-- get started start -->

## Prerequisites

Before using isqtools, ensure the following requirements are met:

### Requirements:

- [Python 3.9](https://www.python.org/) or higher version
- [NumPy](https://numpy.org/)
- [isQ Compiler](https://www.arclightquantum.com/isq-docs/latest/install/) (isqc) version 0.2.5

### Additional Requirements:

- For quantum machine learning:

  - [autograd](https://github.com/HIPS/autograd)
  - [torch](https://pytorch.org/)

- For quantum chemistry simulations:

  - [openfermion](https://quantumai.google/openfermion)
  - [pyscf](https://pyscf.org/)

- For accessing [QuantumCtek](https://quantumctek-cloud.com/) quantum hardware:

  - [requests](https://requests.readthedocs.io/en/latest/)
  - [ezQgd](https://pypi.org/project/ezQgd/)

## Installation

To get started with isqtools, we recommend downloading the source code and installing it using `pip`. Follow these steps:

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Run the following command to install:

```bash
pip install .
```

## Usage

Here is an example workflow for using **isqtools**:

### Step 1: Create an isQ File

First, create an isQ file (e.g., `example.isq`) with the following content:

```cpp
import std;

qbit q[2];

procedure main() {
    H(q[0]);
    H(q[1]);
    M(q[0]);
    M(q[1]);
}
```

This file defines a simple quantum circuit using the isQ language. For more details, please refer to [isQ Programming Language](https://www.arclightquantum.com/isq-docs/latest/grammar/).

### Step 2: Compile and Simulate Using Python

Run the following Python code to compile the isQ file and simulate its execution:

```python
from pathlib import Path

from isqtools import isqc_compile, isqc_simulate
from isqtools.utils import CompileTarget, IsqcError

# Define the path to your isQ file
temp_file_path = Path("example.isq")

# Compile the isQ file to QIR (or other supported targets)
try:
    isqc_compile(file=str(temp_file_path), target=CompileTarget.QIR)
except IsqcError as e:
    print(f"Compilation failed: {e}")
    exit(1)

# Simulate the compiled QIR
output_file = temp_file_path.with_suffix(".so")
result, err, code = isqc_simulate(output_file)

if code == 0:
    print("Simulation Result:", result)
else:
    print("Simulation Error:", err)

```

**Notes:**

- Replace `example.isq` with the path to your actual isQ file.
- Ensure that all required dependencies are installed and that the isqtools environment is properly set up.

<!-- get started end -->

## License

[MIT License](https://opensource.org/license/MIT)
