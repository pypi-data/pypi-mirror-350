import tempfile
from pathlib import Path

import pytest

from isqtools.utils import CompileTarget, IsqcError, isqc_compile, isqc_simulate

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


@pytest.fixture
def so_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_file_path = temp_dir_path / "temp_file.isq"
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(TEST_FILE_CONTENT)
        isqc_compile(file=str(temp_file_path), target=CompileTarget.QIR)
        output_file = temp_file_path.with_suffix(".so")
        yield output_file


def test_simulate_success(so_file):
    result, err, code = isqc_simulate(so_file)
    # print(result)
    assert isinstance(result, dict)
    assert code == 0
    assert err == ""


def test_simulate_invalid_file_format():
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as temp_file:
        temp_file.write("Invalid content")
        temp_file_path = temp_file.name

    with pytest.raises(IsqcError, match="format is not supported"):
        isqc_simulate(temp_file_path)

    Path(temp_file_path).unlink()


def test_simulate_missing_file():
    non_existent_file = Path("non_existent_file.so")
    with pytest.raises(IsqcError, match="does not exist"):
        isqc_simulate(non_existent_file)


def test_simulate_with_int_param(so_file):
    result, err, code = isqc_simulate(so_file, int_param=42)
    assert isinstance(result, dict)
    assert code == 0
    assert err == ""


def test_simulate_with_double_param(so_file):
    result, err, code = isqc_simulate(so_file, double_param=3.14)
    assert isinstance(result, dict)
    assert code == 0
    assert err == ""


def test_simulate_with_debug(so_file):
    result, err, code = isqc_simulate(so_file, debug=True)
    assert isinstance(result, dict)
    assert code == 0
