import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "weather.py"
PY = sys.executable


def _run(
    cmd: list[str],
    stdin: str | None = None,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        input=stdin,
        text=True,
        capture_output=True,
        timeout=10,
        cwd=ROOT,
    )


def execute_script(city: str) -> subprocess.CompletedProcess:
    proc = _run([PY, str(SCRIPT), city])

    if proc.returncode != 0:
        proc = _run([PY, str(SCRIPT)], stdin=city + "\n")

    return proc


def test_happy_path_prints_city_and_temp():
    result = execute_script("Kyiv")
    assert result.returncode == 0, result.stderr
    out = result.stdout.strip()

    assert "kyiv" in out.lower(), "City name should be in the output"

    assert re.search(r"\d{2}/\d{2}/\d{4}", out), "Date format should be DD/MM/YYYY"
    assert re.search(r"\d+\s*°\s*[Cc]", out), "Temperature should be in Celsius"


def test_error_path_when_no_city():
    proc = _run([PY, str(SCRIPT)], stdin="\n")

    if proc.returncode != 0:
        assert re.search(
            r"(usage|error)", proc.stderr + proc.stdout, re.I
        ), "Usage or error message should be shown when script fails"
    else:
        assert re.search(
            r"city.*required|enter.*city", proc.stdout, re.I
        ), "Should prompt for city when none provided"
