# This code is part of isQ.
# (C) Copyright ArcLight Quantum 2025.
# This code is licensed under the MIT License.

"""This file provides some utility functions for calling the ``isqc`` compiler
from python."""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
from collections.abc import Sequence
from enum import Enum
from pathlib import Path

from .isqc_path import _IsqcPath, get_isqc_path, set_isqc_path

_default_isqc_path = _IsqcPath()


class IsqcError(Exception):
    """IsQ compiler Error."""


class CompileTarget(Enum):
    QIR = "qir"
    OPEN_QASM3 = "open-qasm3"
    QCIS = "qcis"

    @classmethod
    def from_string(cls, value: str) -> "CompileTarget":
        """Convert a string to the corresponding CompileTarget enum value."""
        value = value.lower()  # Case-insensitive comparison
        for target in cls:
            if target.value == value:
                return target
        raise ValueError(
            f"Invalid target: {value}. Valid options are: {[t.value for t in cls]}"
        )


def isqc_compile(
    file: str,
    target: CompileTarget | str = CompileTarget.QIR,
    int_param: Sequence[int] | int | None = None,
    double_param: Sequence[float] | float | None = None,
    additional_args: str = "",
) -> None:
    """This function encapsulates the ``compile`` of isQ compiler.

    Args:
        file: The path to the file that needs to be compiled.
        target: The compiled target output form (either a CompileTarget enum or a string).
        int_param: An integer variable (array) passed in when compiling.
        double_param: An double variable (array) passed in when compiling.
        additional_args: Other arguments passed in when compiling, see more:
                         https://www.arclightquantum.com/isq-docs/latest/

    """

    if isinstance(target, str):
        target = CompileTarget.from_string(target)
    if target == CompileTarget.OPEN_QASM3:
        raise IsqcError("open-qasm3 is broken")

    file = str(Path(file).expanduser())
    int_cmd, double_cmd = _deal_params(int_param, double_param)
    isqc_path = str(Path(_default_isqc_path.default_isqc_path) / "isqc")

    compile_cmd = [isqc_path, "compile", file, "--target", target.value]

    if int_cmd:
        compile_cmd.extend(int_cmd.split())
    if double_cmd:
        compile_cmd.extend(double_cmd.split())
    if additional_args:
        compile_cmd.extend(additional_args.split())

    out = subprocess.run(
        compile_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,  # Decode output as text
    )

    if out.returncode != 0:
        raise IsqcError(
            f"Compile Failed! "
            f"Error code: {out.returncode}. "
            f"Error message: {out.stdout} {out.stderr}"
            # isqc stdout and stderr
        )


def isqc_simulate(
    file: str | Path,
    shots: int = 100,
    int_param: Sequence[int] | int | None = None,
    double_param: Sequence[float] | float | None = None,
    debug: bool = False,
    additional_args: str = "",
) -> tuple[dict[str, int], str, int] | tuple[str, str, int]:
    """This function encapsulates the ``simulate`` of isQ compiler.

    Args:
        file: The path to the file that needs to be compiled.
        shots: Shots number of quantum simulation.
        int_param: An integer variable (array) passed in when compiling.
        double_param: An double variable (array) passed in when compiling.
        additional_args: Other arguments passed in when compiling, see more:
                         https://www.arclightquantum.com/isq-docs/latest/

    Returns:
        A dictionary with simulation results if successful, otherwise a tuple containing
        stdout, stderr, and the return code.

    Raises:
        IsqcError: If the file format is unsupported or the file does not exist.
        subprocess.CalledProcessError: If the simulation command fails.

    """

    if isinstance(file, str):
        file = Path(file).expanduser()
    if file.suffix == ".so":
        so_file = file
    elif file.suffix == ".isq":
        so_file = file.with_suffix(".so")
    else:
        raise IsqcError(
            f"`{file}`'s format is not supported. Please use `.isq` or `.so`"
        )

    if not so_file.exists():
        raise IsqcError(f"`{so_file}` does not exist. Please compile isQ file first.")

    int_cmd, double_cmd = _deal_params(int_param, double_param)
    isqc_path = os.path.join(_default_isqc_path.default_isqc_path, "isqc")
    simulate_cmd = [isqc_path, "simulate", str(so_file), "--shots", str(shots)]

    if int_cmd:
        simulate_cmd.extend(int_cmd.split())
    if double_cmd:
        simulate_cmd.extend(double_cmd.split())
    if additional_args:
        simulate_cmd.extend(additional_args.split())
    if debug:
        simulate_cmd.append("--debug")

    result = subprocess.run(
        simulate_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        text=True,
    )
    if result.returncode == 0:
        return dict(json.loads(result.stdout)), result.stderr, result.returncode
    else:
        return result.stdout, result.stderr, result.returncode


def isqc_run(
    file: str,
    target: CompileTarget = CompileTarget.QIR,
    shots: int = 100,
    int_param: Sequence[int] | int | None = None,
    double_param: Sequence[float] | float | None = None,
) -> tuple[dict[str, int], str, int] | tuple[str, str, int]:
    """This method executes ``compile`` and ``simulate`` in sequence."""

    isqc_compile(file=file, target=target)

    return isqc_simulate(
        file=file, shots=shots, int_param=int_param, double_param=double_param
    )


def _deal_params(
    int_param: Sequence[int] | int | None = None,
    double_param: Sequence[float] | float | None = None,
) -> tuple[str, str]:
    """Convert integer and double parameters into command-line arguments for the isQ compiler.

    Args:
        int_param: A single integer, a sequence of integers, or None.
        double_param: A single float, a sequence of floats, or None.

    Returns:
        A tuple containing the command-line arguments for integer parameters and double parameters.
    """

    int_cmd = _format_params(int_param, "-i")
    double_cmd = _format_params(double_param, "-d")

    return int_cmd, double_cmd


def _format_params(param, flag):
    if param is None:
        return ""
    if isinstance(param, (int, float)):
        param = [param]
    return " ".join(f"{flag} {value}" for value in param)


def gen_qcis_from_so(
    file: str | Path,
    int_param: Sequence[int] | int | None = None,
    double_param: Sequence[float] | float | None = None,
    additional_args: str = "",
) -> None:
    """According to the compilation plan of isQ compiler, this function is not
    open to users.
    """

    if isinstance(file, str):
        file = Path(file).expanduser()

    int_cmd, double_cmd = _deal_params(int_param, double_param)

    qcis_path = file.with_suffix(".qcis")

    FindSimulator.make_simulator_bin()
    simulator_exec = FindSimulator.get_simulator_bin_path()

    cmd = [
        simulator_exec,
        str(file),
        "--qcisgen",
        "-e",
        "__isq__entry",
    ]

    if int_cmd:
        cmd.extend(int_cmd.split())
    if double_cmd:
        cmd.extend(double_cmd.split())
    if additional_args:
        cmd.extend(additional_args.split())

    with open(qcis_path, "w") as output_file:
        out = subprocess.run(
            cmd,
            stdout=output_file,
            stderr=output_file,
            text=True,
        )

    if out.returncode != 0:
        raise IsqcError(
            f"Compile Failed! "
            f"Error code: {out.returncode}. "
            f"Error message: {out.stdout} {out.stderr}"
            # isqc stdout and stderr
        )


class FindSimulator:
    """To build a SIMULATOR BIN for isqc."""

    def __init__(self) -> None:
        self.make_simulator_bin()

    @staticmethod
    def set_simulator_file_name():
        return "SIMULATOR"

    @staticmethod
    def get_dir_name_of_simulator(isqcDIR):
        storeDIR = os.path.join(isqcDIR, "nix", "store")
        messList = os.listdir(storeDIR)
        for line in messList:
            if "simulator" in line:
                return line.strip()
        logging.error("cannot find simulator dir")

    @staticmethod
    def get_isQ_dir():
        if not get_isqc_path():
            isqcBIN = shutil.which("isqc")
            if isqcBIN:
                isqcDIR = os.path.abspath(os.path.dirname(isqcBIN))
                return isqcDIR
            return None
        return get_isqc_path()

    @classmethod
    def get_simulator_bin_path(cls):
        return os.path.join(cls.get_isQ_dir(), cls.set_simulator_file_name())

    @classmethod
    def make_simulator_bin(cls):
        """
        Automatically find the directory of isqc, create a SIMULATOR file
        with appropriate content, and set file permissions.
        """
        simBinFile = os.path.abspath(cls.get_simulator_bin_path())

        if os.path.exists(simBinFile):
            print(f"{simBinFile} already exists.")
            return

        isQdir = os.path.abspath(cls.get_isQ_dir())
        if not os.path.isdir(isQdir):
            print(f"Error: {isQdir} is not a valid directory.")
            return
        messName = cls.get_dir_name_of_simulator(isQdir)
        simulator_path = os.path.join("/nix/store", messName, "bin", "simulator")
        isqcFile = os.path.join(isQdir, "isqc")
        if not os.path.isfile(isqcFile):
            print(f"Error: {isqcFile} does not exist or is not a file.")
            return
        try:
            with open(isqcFile, "r") as f:
                isqcContent = f.read()
            slides = isqcContent.split(" ")
            if len(slides) < 2:
                print("Error: The isqc file format is not valid.")
                return
            slides[-2] = simulator_path  # 更新模拟器路径
            simBINcontent = " ".join(slides)
            with open(simBinFile, "w") as f:
                f.write(simBINcontent)
            os.chmod(simBinFile, 0o555)
            print(f"Simulator binary created successfully at {simBinFile}.")

        except OSError as e:
            print(f"Failed to create simulator binary: {e}")
