"""Tests für c_coverage.sh (TOOL-COV-001)"""
import os
import subprocess
import stat

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "c_coverage.sh")


def test_script_exists():
    """c_coverage.sh ist vorhanden."""
    assert os.path.isfile(SCRIPT)


def test_script_is_executable():
    """c_coverage.sh hat ausführbare Rechte."""
    mode = os.stat(SCRIPT).st_mode
    assert mode & stat.S_IXUSR, "Script ist nicht executable (u+x)"


def test_no_args_prints_usage():
    """Ohne Argumente: Exit 1 und Verwendungshinweis."""
    result = subprocess.run(
        ["bash", SCRIPT],
        capture_output=True, text=True
    )
    assert result.returncode == 1
    assert "Verwendung" in result.stderr


def test_missing_source_dir_exits_nonzero(tmp_path):
    """Nicht existierendes Quell-Verzeichnis → Exit != 0."""
    result = subprocess.run(
        ["bash", SCRIPT, str(tmp_path / "nonexistent"), str(tmp_path / "out.info")],
        capture_output=True, text=True
    )
    assert result.returncode != 0


def test_bash_syntax():
    """Bash-Syntax des Scripts ist fehlerfrei (bash -n)."""
    result = subprocess.run(
        ["bash", "-n", SCRIPT],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Syntax-Fehler: {result.stderr}"
