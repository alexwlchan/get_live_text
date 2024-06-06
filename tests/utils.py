import pathlib
import subprocess
import typing


class CommandOutput(typing.TypedDict):
    returncode: int
    stdout: str | None
    stderr: str | None


def get_live_text(argv: list[str | pathlib.Path]) -> CommandOutput:
    """
    Run the ``get_live_text.swift`` script and return the result.
    """
    cmd = ["swift", "get_live_text.swift"] + [str(av) for av in argv]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = proc.communicate()

    if stdout is not None:
        stdout = stdout.decode("utf8")

    if stderr is not None:
        stderr = stderr.decode("utf8")

    return CommandOutput(
        returncode=proc.returncode,
        stdout=stdout or None,
        stderr=stderr or None,
    )
