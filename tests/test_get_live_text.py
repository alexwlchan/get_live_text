#!/usr/bin/env python3

import os
from pathlib import Path
import re
import subprocess

import pytest


def test_gets_empty_result_if_no_text(bin_path: Path) -> None:
    """
    If you pass an image without any text, you get empty output.
    """
    proc = subprocess.Popen(
        [bin_path, "tests/fixtures/checkerboard.png"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()

    assert proc.returncode == 0
    assert stdout == b"\n"
    
    if os.environ.get("GITHUB_ACTIONS") != "true":
        assert stderr == b""


def test_gets_text_from_image(bin_path: Path) -> None:
    """
    If you pass an image that contains text, it gets printed to stdout.
    """
    proc = subprocess.Popen(
        [bin_path, "tests/fixtures/with_text.png"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()

    assert proc.returncode == 0
    assert stdout == b"This is an image with more than one block of text\n"
    
    if os.environ.get("GITHUB_ACTIONS") != "true":
        assert stderr == b""


def test_gives_useful_error_if_no_such_file(bin_path: Path) -> None:
    """
    If you pass a path that doesn't exist, you get a useful error.
    """
    proc = subprocess.Popen(
        [bin_path, "tests/fixtures/doesnotexist.gif"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()

    assert proc.returncode == 1
    assert stdout == b""
    assert stderr == b"Cannot find file at path: tests/fixtures/doesnotexist.gif\n"


def test_gives_useful_error_if_cannot_recognize_image(bin_path: Path) -> None:
    """
    If you pass a path that doesn't look like an image, you get a useful error.
    """
    proc = subprocess.Popen(
        [bin_path, "README.md"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()

    assert proc.returncode == 1
    assert stdout == b""
    assert stderr.startswith(b"Unable to recognise text:")


@pytest.mark.parametrize(
    "argv",
    [
        pytest.param([], id="no_arguments"),
        pytest.param(
            ["example.png", "example.gif", "--debug"], id="too_many_arguments"
        ),
    ],
)
def test_it_fails_if_you_supply_the_wrong_arguments(
    bin_path: Path, argv: list[str]
) -> None:
    """
    If you pass the wrong arguments, you get an error explaining how to use it.
    """
    proc = subprocess.Popen(
        [bin_path] + argv,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()

    assert proc.returncode == 1
    assert stdout == b""
    assert stderr.startswith(b"Usage:")


def test_prints_the_version(bin_path: Path) -> None:
    """
    If you run it with the --version flag, it prints the version number.
    """
    proc = subprocess.Popen(
        [bin_path, "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()

    assert proc.returncode == 0
    assert re.match(r"get_live_text [0-9]+\.[0-9]+\.[0-9]+\n$", stdout.decode("utf8"))
    assert stderr == b""
