# [SDOC_LINK: SWR-013]
# [SDOC_LINK: SWR-014]
import subprocess, os, pytest

CLI  = os.getenv("BBCLI","./bin/bbcli-linux-amd64")
HOST = os.getenv("BEAGLE_HOST","192.168.7.2")

def run(args, expect_ok=True):
    r = subprocess.run(  # nosec B603 — CLI/HOST are env-var constants; args are hardcoded in each test
        [CLI,"--host",HOST]+args,
        capture_output=True, text=True, timeout=10)
    if expect_ok: assert r.returncode==0, r.stderr
    return r.stdout

def test_help():     assert "BeagleBone" in run(["--help"])
def test_version():  run(["--version"])
def test_status():   assert "Status" in run(["system","status"])
def test_bme280():   assert "Temperatur" in run(["bme280","read"])
def test_backend_get(): run(["backend","get"])
def test_backend_set(): run(["backend","set","auto"])
def test_backend_invalid():
    r = subprocess.run(  # nosec B603 — CLI is an env-var constant; args are hardcoded literals
        [CLI,"backend","set","invalid"],
        capture_output=True, text=True, timeout=10)
    assert r.returncode != 0
