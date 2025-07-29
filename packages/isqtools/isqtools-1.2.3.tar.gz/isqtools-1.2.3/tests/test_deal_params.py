import pytest

from isqtools.utils import _deal_params


@pytest.mark.parametrize(
    "int_param, double_param, expected_output",
    [
        (3, 0.5, ("-i 3", "-d 0.5")),
        ([1, 2], [0.1, 0.2], ("-i 1 -i 2", "-d 0.1 -d 0.2")),
        (None, None, ("", "")),
        ([3], None, ("-i 3", "")),
        (None, [0.1], ("", "-d 0.1")),
        ([], [], ("", "")),
        ([42], 3.14, ("-i 42", "-d 3.14")),
    ],
)
def test_deal_params(int_param, double_param, expected_output):
    assert _deal_params(int_param, double_param) == expected_output
