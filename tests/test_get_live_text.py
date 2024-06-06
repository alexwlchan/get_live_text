#!/usr/bin/env python3

import os
import pathlib
import plistlib
import re

import pytest

from utils import get_live_text


def test_gets_empty_result_if_no_text() -> None:
    result = get_live_text(["tests/fixtures/checkerboard.png"])

    assert result == {
        "returncode": 0,
        "stdout": "\n",
        "stderr": None,
    }


def test_gets_text_from_image() -> None:
    result = get_live_text(["tests/fixtures/with_text.png"])

    assert result == {
        "returncode": 0,
        "stdout": "This is an image with more than one block of text\n",
        "stderr": None,
    }


def test_gives_useful_error_if_no_such_file() -> None:
    result = get_live_text(["tests/fixtures/doesnotexist.gif"])

    assert result == {
        "returncode": 1,
        "stdout": None,
        "stderr": "Cannot find file at path: tests/fixtures/doesnotexist.gif\n",
    }


def test_gives_useful_error_if_cannot_recognize_image(tmp_path: pathlib.Path) -> None:
    with open(tmp_path / "broken.tif", "wb") as outfile:
        outfile.write(b"helloworld")

    result = get_live_text([str(tmp_path / "broken.tif")])

    assert result["returncode"] == 1
    assert result["stdout"] is None
    assert result["stderr"].startswith("Unable to recognise text:")


@pytest.mark.parametrize(
    "argv",
    [
        pytest.param([], id="no_arguments"),
        pytest.param(["example.png", "example.gif", "--debug"], id="too_many_arguments"),
    ],
)
def test_it_fails_if_you_supply_the_wrong_arguments(argv: list[str]) -> None:
    result = get_live_text(argv)

    assert result == {
        "returncode": 1,
        "stdout": None,
        "stderr": "Usage: get_live_text.swift <PATH>\n",
    }



def test_prints_the_version() -> None:
    result = get_live_text(["--version"])

    assert result["returncode"] == 0
    assert result["stderr"] is None
    assert re.match(
        r"^get_live_text.swift [0-9]+\.[0-9]+\.[0-9]+\n$", result["stdout"]
    ), result["stdout"]
