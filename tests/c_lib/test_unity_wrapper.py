"""
allure-pytest wrapper for Unity C tests.

Each hardware component is a class with @allure.epic / @allure.feature.
Each test method runs the Unity binary, checks one named result, and
attaches stdout/stderr — exactly like a subprocess-based integration test.

Run:
    pip install pytest allure-pytest
    pytest tests/c_lib/ --alluredir=allure-results -v
    allure generate allure-results -o allure-report --clean
"""
import subprocess

import allure
import pytest

from conftest import REPO_ROOT, UnityResult, parse_unity_output
from conftest import C_LIB_DIR, TEST_BIN


# ── Session fixture: build + run once ────────────────────────────────────────

@pytest.fixture(scope='session')
def unity_run():
    """Build the binary and run it once; return (results, stdout, stderr)."""
    build = subprocess.run(
        ['make', '-C', C_LIB_DIR, 'test-bin'],
        capture_output=True, text=True,
    )
    if build.returncode != 0:
        pytest.skip(f'Unity build failed:\n{build.stderr}')

    proc = subprocess.run([TEST_BIN], capture_output=True, text=True)
    results = {r.name: r for r in parse_unity_output(proc.stdout + proc.stderr)}
    return results, proc.stdout, proc.stderr


def _run_unity_test(test_name: str, unity_run):
    """
    Core helper — mirrors the pattern:
        subprocess.run(binary, ...) → attach output → assert returncode / result
    """
    results, stdout, stderr = unity_run

    with allure.step(f'Starte Unity C-Binary: {TEST_BIN}'):
        allure.attach(
            stdout,
            name='C-Standard-Output',
            attachment_type=allure.attachment_type.TEXT,
        )
        if stderr:
            allure.attach(
                stderr,
                name='C-Fehlermeldung',
                attachment_type=allure.attachment_type.TEXT,
            )

    with allure.step(f'Suche Ergebnis für: {test_name}'):
        result: UnityResult = results.get(test_name)
        if result is None:
            pytest.fail(f'Test "{test_name}" nicht in Unity-Output gefunden')

        allure.attach(
            f'{result.file}:{result.line}  →  {result.status}'
            + (f'\n{result.msg}' if result.msg else ''),
            name='Unity Testergebnis',
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step(f'Prüfe Rückgabewert → {result.status}'):
        if result.ignored:
            pytest.skip(result.msg or 'IGNORE gesetzt')
        assert result.passed, (
            f'Unity meldet FAIL für {test_name}: {result.msg}'
        )


# ── BME280 ────────────────────────────────────────────────────────────────────

@allure.epic('C Hardware Drivers')
@allure.feature('BME280 Sensor')
class TestBME280:

    @allure.story('Null-Pointer Validierung')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_bme280_init_null_ptrs(self, unity_run):
        allure.dynamic.title('BME280 init — null function pointers')
        allure.dynamic.description(
            'Erwartet BME280_E_NULL_PTR wenn read/write/delay_us NULL sind.'
        )
        allure.dynamic.label('owner', 'Adrian')
        allure.dynamic.link('https://github.com/BoschSensortec/BME280_driver',
                            name='BME280 Treiber Dokumentation')
        _run_unity_test('test_bme280_init_null_ptrs', unity_run)

    @allure.story('Null-Pointer Validierung')
    @allure.severity(allure.severity_level.NORMAL)
    def test_bme280_get_sensor_data_null_output(self, unity_run):
        allure.dynamic.title('BME280 get_sensor_data — NULL comp_data')
        allure.dynamic.label('owner', 'Adrian')
        _run_unity_test('test_bme280_get_sensor_data_null_output', unity_run)

    @allure.story('Null-Pointer Validierung')
    @allure.severity(allure.severity_level.NORMAL)
    def test_bme280_set_sensor_settings_null_settings(self, unity_run):
        allure.dynamic.title('BME280 set_sensor_settings — NULL settings')
        allure.dynamic.label('owner', 'Adrian')
        _run_unity_test('test_bme280_set_sensor_settings_null_settings', unity_run)

    @allure.story('Kompensationsberechnung')
    @allure.severity(allure.severity_level.NORMAL)
    def test_bme280_compensate_null_data(self, unity_run):
        allure.dynamic.title('BME280 compensate_data — NULL comp und calib')
        allure.dynamic.label('owner', 'Adrian')
        _run_unity_test('test_bme280_compensate_null_data', unity_run)


# ── GPIO ──────────────────────────────────────────────────────────────────────

@allure.epic('C Hardware Drivers')
@allure.feature('GPIO')
class TestGPIO:

    @allure.story('Sysfs Fehlerbehandlung')
    @allure.severity(allure.severity_level.NORMAL)
    def test_gpio_export_fails_no_sysfs(self, unity_run):
        allure.dynamic.title('GPIO export — schlägt fehl ohne /sys/class/gpio')
        allure.dynamic.description(
            'Prüft ob gpio_export() einen Fehlercode zurückgibt '
            'wenn kein sysfs vorhanden ist (CI-Umgebung).'
        )
        allure.dynamic.label('owner', 'Adrian')
        allure.dynamic.label('tag', 'ci-compatible')
        _run_unity_test('test_gpio_export_fails_no_sysfs', unity_run)

    @allure.story('Sysfs Fehlerbehandlung')
    @allure.severity(allure.severity_level.NORMAL)
    def test_gpio_read_fails_no_sysfs(self, unity_run):
        allure.dynamic.title('GPIO read — schlägt fehl ohne /sys/class/gpio')
        allure.dynamic.label('owner', 'Adrian')
        allure.dynamic.label('tag', 'ci-compatible')
        _run_unity_test('test_gpio_read_fails_no_sysfs', unity_run)

    @allure.story('Sysfs Fehlerbehandlung')
    @allure.severity(allure.severity_level.NORMAL)
    def test_gpio_write_fails_no_sysfs(self, unity_run):
        allure.dynamic.title('GPIO write — schlägt fehl ohne /sys/class/gpio')
        allure.dynamic.label('owner', 'Adrian')
        allure.dynamic.label('tag', 'ci-compatible')
        _run_unity_test('test_gpio_write_fails_no_sysfs', unity_run)


# ── UART ──────────────────────────────────────────────────────────────────────

@allure.epic('C Hardware Drivers')
@allure.feature('UART')
class TestUART:

    @allure.story('Geräteinitialisierung')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_uart_open_fails_no_device(self, unity_run):
        allure.dynamic.title('UART open — schlägt fehl ohne /dev/ttyS1')
        allure.dynamic.description(
            'uart_open() muss einen Fehler zurückgeben wenn das Gerät '
            'nicht existiert. Relevant für CI ohne angeschlossene Hardware.'
        )
        allure.dynamic.label('owner', 'Adrian')
        allure.dynamic.label('tag', 'ci-compatible')
        _run_unity_test('test_uart_open_fails_no_device', unity_run)

    @allure.story('Ressourcenfreigabe')
    @allure.severity(allure.severity_level.NORMAL)
    def test_uart_close_invalid_fd(self, unity_run):
        allure.dynamic.title('UART close — fd=-1 darf nicht abstürzen')
        allure.dynamic.description(
            'uart_close() mit fd=-1 darf keinen Segfault oder '
            'undefined behaviour auslösen.'
        )
        allure.dynamic.label('owner', 'Adrian')
        _run_unity_test('test_uart_close_invalid_fd', unity_run)
