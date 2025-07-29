import tempfile
from pathlib import Path

import pytest

from isqtools.utils import CompileTarget, IsqcError, isqc_compile

TEST_FILE_CONTENT = """
import std;

qbit q[2];

procedure main() {
    H(q[0]);
    H(q[1]);
    M(q[0]);
    M(q[1]);
}
"""


@pytest.mark.parametrize("target", [CompileTarget.QIR, "qir"])
def test_compile_qir(target):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file_path = temp_dir_path / "temp_file.isq"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(TEST_FILE_CONTENT)
        isqc_compile(file=str(temp_file_path), target=target)
        output_file = temp_file_path.with_suffix(".so")
        assert output_file.exists()


@pytest.mark.parametrize("target", [CompileTarget.QCIS, "qcis"])
def test_compile_qcis(target):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file_path = temp_dir_path / "temp_file.isq"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(TEST_FILE_CONTENT)
        isqc_compile(file=str(temp_file_path), target=target)
        output_file_so = temp_file_path.with_suffix(".so")
        output_file_qcis = temp_file_path.with_suffix(".qcis")
        assert output_file_so.exists() and output_file_qcis


@pytest.mark.parametrize("target", [CompileTarget.OPEN_QASM3, "open-qasm3"])
def test_compile_openqasm3(target):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file_path = temp_dir_path / "temp_file.isq"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(TEST_FILE_CONTENT)
        with pytest.raises(IsqcError, match="open-qasm3 is broken"):
            isqc_compile(file=str(temp_file_path), target=target)


def test_compile_with_invalid_file():
    """Test the compile function with an invalid file path."""
    invalid_file_path = "/invalid/path/to/file.isq"

    with pytest.raises(IsqcError):
        isqc_compile(file=invalid_file_path)


def test_compile_with_empty_file():
    """Test the compile function with an empty file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file_path = temp_dir_path / "temp_file.isq"
        with open(temp_file_path, "w"):
            pass
        with pytest.raises(IsqcError):
            isqc_compile(file=str(temp_file_path))
