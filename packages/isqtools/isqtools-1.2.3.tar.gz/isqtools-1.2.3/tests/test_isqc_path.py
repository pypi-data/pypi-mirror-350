import os

import pytest

from isqtools.isqc_path import _IsqcPath, get_isqc_path, set_isqc_path


def test_initialization():
    """Test that the _IsqcPath instance initializes with an empty path."""
    isqc_path_instance = _IsqcPath()
    assert isqc_path_instance.get_path() == ""


def test_set_and_get_path():
    """Test setting and getting the path."""
    isqc_path_instance = _IsqcPath()
    test_path = "~/test_path"
    expanded_path = os.path.expanduser(test_path)

    # Set the path
    isqc_path_instance.set_path(test_path)
    assert isqc_path_instance.get_path() == expanded_path

    # Test with a different path
    another_path = "/another/path"
    isqc_path_instance.set_path(another_path)
    assert isqc_path_instance.get_path() == another_path


def test_path_expansion():
    """Test that paths are expanded correctly using os.path.expanduser."""
    test_path = "~/expanded_path"
    expanded_path = os.path.expanduser(test_path)

    # Set the path
    set_isqc_path(test_path)

    # Verify the path is expanded
    assert get_isqc_path() == expanded_path


def test_empty_path():
    """Test setting and getting an empty path."""
    set_isqc_path("")
    assert get_isqc_path() == ""


def test_non_string_path():
    """Test that setting a non-string path raises an error."""
    with pytest.raises(TypeError):
        set_isqc_path(123)  # Non-string input should raise an error
