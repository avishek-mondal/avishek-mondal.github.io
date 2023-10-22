"""Custom module calling tesseract binary

Heavily inspired by pytesseract. Main difference -
doesn't save arrays to temp files
"""

import os
import shlex
import subprocess
from functools import partial
from typing import Callable, Dict, cast

import cv2
import numpy as np

DEFAULT_ENCODING = "utf-8"


class CustomTesseractError(Exception):
    ...


def get_tesseract_res_from_cv2_img(
    cv2_img: np.ndarray,
    lang,
    config="",
    timeout=None,
) -> Dict:
    config = f"-c tessedit_create_tsv=1 {config.strip()}"
    command = f"tesseract stdin stdout -l {lang} {config}"
    command_args = shlex.split(command)
    proc = subprocess.Popen(
        command_args,
        **subprocess_args(),
    )
    fn: Callable = cast(
        Callable,
        (
            proc.communicate
            if timeout is None
            else partial(proc.communicate, timeout=timeout)
        ),
    )
    stdout, std_err = fn(input=cv2.imencode(".tif", cv2_img)[1].tobytes())

    if proc.returncode:
        error_str = " ".join(
            line for line in std_err.decode(DEFAULT_ENCODING).splitlines()
        ).strip()
        raise CustomTesseractError(error_str)
    return file_to_dict(stdout.decode(DEFAULT_ENCODING), "\t", -1)


def file_to_dict(tsv, cell_delimiter, str_col_idx):
    result = {}  # type: ignore
    rows = [row.split(cell_delimiter) for row in tsv.strip().split("\n")]
    if len(rows) < 2:
        return result

    header = rows.pop(0)
    length = len(header)
    if len(rows[-1]) < length:
        # Fixes bug that occurs when last text string in TSV is null, and
        # last row is missing a final cell in TSV file
        rows[-1].append("")

    if str_col_idx < 0:
        str_col_idx += length

    for i, head in enumerate(header):
        result[head] = list()
        for row in rows:
            if len(row) <= i:
                continue

            if i != str_col_idx:
                try:
                    val = int(float(row[i]))
                except ValueError:
                    val = row[i]
            else:
                val = row[i]

            result[head].append(val)

    return result


def subprocess_args(include_stdout=True):
    # See https://github.com/pyinstaller/pyinstaller/wiki/Recipe-subprocess
    # for reference and comments.

    kwargs = {
        "stdin": subprocess.PIPE,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "startupinfo": None,
        "env": os.environ,
    }

    if hasattr(subprocess, "STARTUPINFO"):
        kwargs["startupinfo"] = subprocess.STARTUPINFO()  # type: ignore
        kwargs["startupinfo"].dwFlags |= subprocess.STARTF_USESHOWWINDOW  # type: ignore
        kwargs["startupinfo"].wShowWindow = subprocess.SW_HIDE  # type: ignore

    return kwargs