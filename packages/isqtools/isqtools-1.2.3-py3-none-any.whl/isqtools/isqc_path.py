import os


class _IsqcPath:
    """Singleton class to manage the default ``isqc`` path."""

    __slots__ = ("default_isqc_path",)

    def __init__(self):
        self.default_isqc_path = ""

    def get_path(self) -> str:
        """Get the current default ``isqc`` path."""
        return self.default_isqc_path

    def set_path(self, isqc_path: str) -> None:
        """Set the default ``isqc`` path.

        Args:
            isqc_path (str): The path to set as the default ``isqc`` path.
        """
        self.default_isqc_path = os.path.expanduser(isqc_path)


_default_isqc_path = _IsqcPath()


def get_isqc_path() -> str:
    """Get the current default ``isqc`` path.

    Returns:
        str: The current default ``isqc`` path.
    """
    return _default_isqc_path.get_path()


def set_isqc_path(isqc_path: str) -> None:
    """Set the default ``isqc`` path.

    Args:
        isqc_path (str): The path to set as the default ``isqc`` path.
    """
    _default_isqc_path.set_path(isqc_path)
