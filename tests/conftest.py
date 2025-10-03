import os
import subprocess

import pytest


@pytest.fixture(scope="session")
def bin_path(tmp_path_factory: pytest.TempPathFactory) -> str:
    """
    Compiles a new `get_live_text` binary, and returns a path to the binary.
    """
    p = tmp_path_factory.mktemp("bin") / "get_live_text"
    p.parent.mkdir(exist_ok=True)

    subprocess.check_call(
        ["swiftc", os.path.abspath("get_live_text.swift")], cwd=p.parent
    )
    assert p.exists()

    return str(p)
