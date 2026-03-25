"""Tests für c_coverage.sh (TOOL-COV-001)"""
import os
import shutil
import subprocess
import stat

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "c_coverage.sh")
BASH = shutil.which("bash") or "/bin/bash"


def test_script_exists():
    """c_coverage.sh ist vorhanden."""
    if not os.path.isfile(SCRIPT):
        raise FileNotFoundError(f"Script not found: {SCRIPT}")


def test_script_is_executable():
    """c_coverage.sh hat ausführbare Rechte."""
    mode = os.stat(SCRIPT).st_mode
    if not (mode & stat.S_IXUSR):
        raise AssertionError("Script ist nicht executable (u+x)")


def test_no_args_prints_usage():
    """Ohne Argumente: Exit 1 und Verwendungshinweis."""
    result = subprocess.run(  # nosec B603 — BASH and SCRIPT are module-level constants, no user input
        [BASH, SCRIPT],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 1:
        raise AssertionError(f"Expected exit code 1, got {result.returncode}")
    if "Verwendung" not in result.stderr:
        raise AssertionError(f"Expected 'Verwendung' in stderr, got: {result.stderr!r}")


def test_missing_source_dir_exits_nonzero(tmp_path):
    """Nicht existierendes Quell-Verzeichnis → Exit != 0."""
    result = subprocess.run(  # nosec B603 — BASH and SCRIPT are module-level constants, no user input
        [BASH, SCRIPT, str(tmp_path / "nonexistent"), str(tmp_path / "out.info")],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        raise AssertionError("Expected non-zero exit code for missing source directory")


def test_bash_syntax():
    """Bash-Syntax des Scripts ist fehlerfrei (bash -n)."""
    result = subprocess.run(  # nosec B603 — BASH and SCRIPT are module-level constants, no user input
        [BASH, "-n", SCRIPT],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        raise AssertionError(f"Syntax-Fehler: {result.stderr}")
