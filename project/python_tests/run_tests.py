# file: run_tests.py
import subprocess
import sys
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--bin-dir", default="/output")
parser.add_argument("--log-dir", default="/logs")
args = parser.parse_args()

BIN = args.bin_dir
LOG = args.log_dir

BINARIES = [
    {"name": "bme280_main", "path": f"{BIN}/bme280_main", "log": f"{LOG}/c.log"},
    {"name": "rust_app",    "path": f"{BIN}/rust_app",    "log": f"{LOG}/rust.log"},
    {"name": "go_app",      "path": f"{BIN}/go_app",      "log": f"{LOG}/go.log"},
]


def run_binary(binary):
    """Führt ein Binary aus und prüft Ausgabe und Exitcode."""
    path = binary["path"]
    name = binary["name"]
    log  = binary["log"]

    if not os.path.isfile(path):
        print(f"[ERROR] Binary '{name}' nicht gefunden unter {path}")
        return False

    os.makedirs(os.path.dirname(log), exist_ok=True)

    try:
        result = subprocess.run(
            [path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        with open(log, "w") as f:
            f.write(result.stdout)
        print(f"[OK] {name} ausgeführt:")
        print("=== STDOUT ===")
        print(result.stdout.strip())
        if result.stderr.strip():
            print("=== STDERR ===")
            print(result.stderr.strip())
        return True

    except subprocess.CalledProcessError as e:
        with open(log, "w") as f:
            f.write(e.stdout)
        print(f"[FAIL] {name} exit code {e.returncode}")
        print("=== STDOUT ===")
        print(e.stdout.strip())
        print("=== STDERR ===")
        print(e.stderr.strip())
        return False
    except Exception as e:
        print(f"[ERROR] {name} konnte nicht ausgeführt werden: {str(e)}")
        return False

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