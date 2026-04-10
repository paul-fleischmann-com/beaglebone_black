"""
Shared fixtures for the Unity C-test wrapper.
Builds the test binary once per session, runs it, and parses the output.
"""
import os
import re
import subprocess

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
C_LIB_DIR = os.path.join(REPO_ROOT, 'c-lib')
TEST_BIN   = os.path.join(REPO_ROOT, 'project', 'c', 'test', 'test_runner')

RESULT_RE = re.compile(
    r'^(?P<file>[^:]+):(?P<line>\d+):(?P<name>[^:]+)'
    r':(?P<status>PASS|FAIL|IGNORE)(?::(?P<msg>.*))?$'
)


class UnityResult:
    def __init__(self, file, line, name, status, msg):
        self.file   = file
        self.line   = int(line)
        self.name   = name
        self.status = status          # 'PASS' | 'FAIL' | 'IGNORE'
        self.msg    = (msg or '').strip()

    @property
    def passed(self):  return self.status == 'PASS'

    @property
    def failed(self):  return self.status == 'FAIL'

    @property
    def ignored(self): return self.status == 'IGNORE'

    def __repr__(self):
        return f'<UnityResult {self.name} {self.status}>'


def parse_unity_output(text: str) -> list:
    results = []
    for line in text.splitlines():
        m = RESULT_RE.match(line.strip())
        if m:
            results.append(UnityResult(**m.groupdict()))
    return results


# ── Session-scoped fixtures ───────────────────────────────────────────────────

@pytest.fixture(scope='session')
def unity_binary():
    """Build the Unity test binary once per test session."""
    proc = subprocess.run(
        ['make', '-C', C_LIB_DIR, 'test-bin'],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        pytest.skip(f'Could not build Unity test binary:\n{proc.stderr}')
    return TEST_BIN


@pytest.fixture(scope='session')
def unity_raw_output(unity_binary):
    """Run the binary and return the raw stdout+stderr."""
    proc = subprocess.run(
        [unity_binary],
        capture_output=True,
        text=True,
    )
    return proc.stdout + proc.stderr


@pytest.fixture(scope='session')
def unity_results(unity_raw_output) -> list:
    """Parsed list of UnityResult objects."""
    return parse_unity_output(unity_raw_output)
