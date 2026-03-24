# file: run_tests.py
import subprocess
import sys
import os
import argparse
import time
import xml.etree.ElementTree as ET

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
    """Führt einen Befehl aus, schreibt stdout in log, gibt (passed, output, duration) zurück."""
    env = {**os.environ, **(extra_env or {})}
    t0 = time.monotonic()
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, check=True, env=env)
        duration = time.monotonic() - t0
        os.makedirs(os.path.dirname(log), exist_ok=True)
        with open(log, "w") as f:
            f.write(result.stdout)
        print(result.stdout.strip())
        if result.stderr.strip():
            print("=== STDERR ===")
            print(result.stderr.strip())
        return True, result.stdout, duration
    except subprocess.CalledProcessError as e:
        duration = time.monotonic() - t0
        os.makedirs(os.path.dirname(log), exist_ok=True)
        with open(log, "w") as f:
            f.write(e.stdout)
        print(f"[FAIL] exit code {e.returncode}")
        print(e.stdout.strip())
        print(e.stderr.strip())
        return False, f"{e.stdout}\n{e.stderr}", duration
    except Exception as e:
        print(f"[ERROR] {e}")
        return False, str(e), 0.0


def run_binary(binary):
    """Führt ein Binary aus — bei bme280_main per C-Test mit Coverage."""
    path = binary["path"]
    name = binary["name"]
    log  = binary["log"]

    if not os.path.isfile(path):
        msg = f"Binary '{name}' nicht gefunden unter {path}"
        print(f"[ERROR] {msg}")
        return [(name, False, msg, 0.0)]

    lib_dir = os.path.dirname(path)
    results = []

    if name == "bme280_main" and COV:
        for test in C_TESTS:
            cov_dir = os.path.join(COV, test)
            os.makedirs(cov_dir, exist_ok=True)
            print(f"  [{test}]", end=" ", flush=True)
            ok, out, dur = _run(
                [path, "--test", test],
                log=os.path.join(os.path.dirname(log), f"{test}.log"),
                extra_env={
                    "LD_LIBRARY_PATH": lib_dir,
                    "GCOV_PREFIX":     cov_dir,
                    "GCOV_PREFIX_STRIP": "100",
                },
            )
            results.append((f"{name}/{test}", ok, out, dur))
        return results

    ok, out, dur = _run([path], log=log, extra_env={"LD_LIBRARY_PATH": lib_dir})
    return [(name, ok, out, dur)]


def write_junit_xml(all_results, log_dir):
    failures = sum(1 for _, ok, _, _ in all_results if not ok)
    suite = ET.Element("testsuite", name="BBB Hardware Tests",
                       tests=str(len(all_results)), failures=str(failures),
                       errors="0")
    for name, ok, output, duration in all_results:
        tc = ET.SubElement(suite, "testcase", name=name,
                           classname="hardware", time=f"{duration:.3f}")
        if not ok:
            fail = ET.SubElement(tc, "failure", message="Test failed")
            fail.text = output[:4000]  # JUnit readers truncate anyway

    tree = ET.ElementTree(ET.Element("testsuites"))
    tree.getroot().append(suite)
    ET.indent(tree, space="  ")
    os.makedirs(log_dir, exist_ok=True)
    tree.write(os.path.join(log_dir, "test-results.xml"),
               encoding="unicode", xml_declaration=True)


def main():
    all_results = []
    all_passed = True

    for binary in BINARIES:
        print(f"\n--- Testing {binary['name']} ---")
        results = run_binary(binary)
        for name, ok, out, dur in results:
            all_results.append((name, ok, out, dur))
            if not ok:
                print(f"\n--- Testing {name} failed ---")
                all_passed = False

    write_junit_xml(all_results, LOG)

    if all_passed:
        print("\n=== Alle Tests bestanden ===")
        sys.exit(0)
    else:
        print("\n=== Einige Tests fehlgeschlagen ===")
        sys.exit(1)

if __name__ == "__main__":
    main()
