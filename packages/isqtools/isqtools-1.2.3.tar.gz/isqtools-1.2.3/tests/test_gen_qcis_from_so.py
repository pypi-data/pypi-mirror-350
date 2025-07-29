import tempfile
from pathlib import Path

from isqtools.utils import CompileTarget, gen_qcis_from_so, isqc_compile

TEST_FILE_CONTENT = """
import std;

qbit q[1];

procedure main(int x[], double d[]) {
    H(q[x[0]]);
    Rx(d[0], q[x[1]]);
    M(q[x[2]]);
}
"""


def test_gen_qcis_from_so():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        temp_isq_file_path = temp_dir_path / "temp_file.isq"
        with open(temp_isq_file_path, "w") as temp_file:
            temp_file.write(TEST_FILE_CONTENT)
        isqc_compile(
            file=str(temp_isq_file_path),
            target=CompileTarget.QCIS,
            int_param=[0, 0, 0],  # fake data
            double_param=[0.5],
        )
        output_so_file = temp_isq_file_path.with_suffix(".so")
        gen_qcis_from_so(
            file=str(output_so_file),
            int_param=[0, 0, 0],  # real data
            double_param=[0.8],
        )
        output_qcis_file = temp_isq_file_path.with_suffix(".qcis")
        with open(output_qcis_file, "r") as f:
            assert f.read() == """H Q0\nRX Q0 0.8\nM Q0\n"""
        assert output_qcis_file.exists()
