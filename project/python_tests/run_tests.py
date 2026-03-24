# file: run_tests.py
import subprocess
import sys
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--bin-dir", default="/output")
parser.add_argument("--log-dir", default="/logs")
parser.add_argument("--cov-dir", default=None)
args = parser.parse_args()

BIN = args.bin_dir
LOG = args.log_dir
COV = args.cov_dir

C_TESTS = ["test_bme280_init_no_hardware"]

BINARIES = [
    {"name": "bme280_main", "path": f"{BIN}/bme280_main", "log": f"{LOG}/c.log"},
    {"name": "rust_app",    "path": f"{BIN}/rust_app",    "log": f"{LOG}/rust.log"},
    {"name": "go_app",      "path": f"{BIN}/go_app",      "log": f"{LOG}/go.log"},
]


def _run(cmd, log, extra_env=None):
    """Führt einen Befehl aus, schreibt stdout in log, gibt True/False zurück."""
    env = {**os.environ, **(extra_env or {})}
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, check=True, env=env)
        os.makedirs(os.path.dirname(log), exist_ok=True)
        with open(log, "w") as f:
            f.write(result.stdout)
        print(result.stdout.strip())
        if result.stderr.strip():
            print("=== STDERR ===")
            print(result.stderr.strip())
        return True
    except subprocess.CalledProcessError as e:
        os.makedirs(os.path.dirname(log), exist_ok=True)
        with open(log, "w") as f:
            f.write(e.stdout)
        print(f"[FAIL] exit code {e.returncode}")
        print(e.stdout.strip())
        print(e.stderr.strip())
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def run_binary(binary):
    """Führt ein Binary aus — bei bme280_main per C-Test mit Coverage."""
    path = binary["path"]
    name = binary["name"]
    log  = binary["log"]

    if not os.path.isfile(path):
        print(f"[ERROR] Binary '{name}' nicht gefunden unter {path}")
        return False

    lib_dir = os.path.dirname(path)

    if name == "bme280_main" and COV:
        passed = True
        for test in C_TESTS:
            cov_dir = os.path.join(COV, test)
            os.makedirs(cov_dir, exist_ok=True)
            print(f"  [{test}]", end=" ", flush=True)
            ok = _run(
                [path, "--test", test],
                log=os.path.join(os.path.dirname(log), f"{test}.log"),
                extra_env={
                    "LD_LIBRARY_PATH": lib_dir,
                    "GCOV_PREFIX":     cov_dir,
                    "GCOV_PREFIX_STRIP": "100",
                },
            )
            if not ok:
                passed = False
        return passed

    return _run([path], log=log,
                extra_env={"LD_LIBRARY_PATH": lib_dir})

def main():
    all_passed = True
    for binary in BINARIES:
        print(f"\n--- Testing {binary['name']} ---")
        passed = run_binary(binary)
        if not passed:
            print(f"\n--- Testing {binary['name']} failed ---")
            all_passed = False

    if all_passed:
        print("\n=== Alle Tests bestanden ✅ ===")
        sys.exit(0)
    else:
        print("\n=== Einige Tests fehlgeschlagen ❌ ===")
        sys.exit(1)

if __name__ == "__main__":
    main()