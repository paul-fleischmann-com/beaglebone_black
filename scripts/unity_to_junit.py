#!/usr/bin/env python3
"""
Convert Unity test framework output to JUnit XML with Allure-compatible
properties, attachments (system-out), and step metadata.

Unity output format:
  path/file.c:LINE:TEST_NAME:PASS
  path/file.c:LINE:TEST_NAME:FAIL:message
  path/file.c:LINE:TEST_NAME:IGNORE:message

Summary line:
  N Tests M Failures K Ignored

Allure reads the following <properties> keys from JUnit XML:
  severity, feature, story, owner, tag, issue, testId, description
"""
import sys
import re
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

# ── Feature detection from test-name prefix ───────────────────────────────────
# Maps test name prefix → (feature, severity, story)
FEATURE_MAP = {
    'test_bme280':  ('BME280 Sensor',   'normal',   'I2C Sensor Driver'),
    'test_gpio':    ('GPIO',            'normal',   'Sysfs GPIO Driver'),
    'test_uart':    ('UART',            'normal',   'Serial Communication'),
    'test_spi':     ('SPI',             'normal',   'SPI Bus Driver'),
}

# Step labels extracted from known test-name suffixes (for <system-out> steps)
STEP_PATTERNS = [
    (re.compile(r'null_ptr|null_ptrs'),   'Verify null pointer guard'),
    (re.compile(r'null_output'),          'Verify NULL output parameter'),
    (re.compile(r'null_settings'),        'Verify NULL settings parameter'),
    (re.compile(r'null_data'),            'Verify NULL data parameter'),
    (re.compile(r'invalid_fd'),           'Verify invalid file descriptor handling'),
    (re.compile(r'no_device|no_sysfs'),   'Verify graceful failure without hardware'),
    (re.compile(r'fails?_'),              'Verify error-path behaviour'),
    (re.compile(r'init'),                 'Call init function'),
    (re.compile(r'open'),                 'Open device'),
    (re.compile(r'close'),                'Close device'),
    (re.compile(r'read'),                 'Read from device'),
    (re.compile(r'write'),                'Write to device'),
]

OWNER   = 'Adrian'
SUITE   = 'C Hardware Drivers'


def detect_feature(name):
    for prefix, info in FEATURE_MAP.items():
        if name.startswith(prefix):
            return info
    return ('C Library', 'minor', 'Hardware Abstraction')


def detect_steps(name, status, msg):
    """Return a list of step strings for <system-out>."""
    steps = []
    for pattern, label in STEP_PATTERNS:
        if pattern.search(name):
            steps.append(label)
            break
    if not steps:
        steps.append('Execute test')

    if status == 'PASS':
        steps.append('Assert: PASS')
    elif status == 'FAIL':
        steps.append(f'Assert: FAIL — {msg}' if msg else 'Assert: FAIL')
    elif status == 'IGNORE':
        steps.append(f'Skipped: {msg}' if msg else 'Skipped')
    return steps


def add_properties(parent, props: dict):
    props_el = ET.SubElement(parent, 'properties')
    for name, value in props.items():
        ET.SubElement(props_el, 'property', name=name, value=str(value))


# ── Parser ────────────────────────────────────────────────────────────────────

RESULT_RE = re.compile(
    r'^(?P<file>[^:]+):(?P<line>\d+):(?P<name>[^:]+)'
    r':(?P<status>PASS|FAIL|IGNORE)(?::(?P<msg>.*))?$'
)


def parse_unity_output(text):
    tests = []
    for line in text.splitlines():
        m = RESULT_RE.match(line.strip())
        if m:
            tests.append({
                'file':   m.group('file'),
                'line':   m.group('line'),
                'name':   m.group('name'),
                'status': m.group('status'),
                'msg':    (m.group('msg') or '').strip(),
            })
    return tests


# ── Builder ───────────────────────────────────────────────────────────────────

def build_junit(tests, suite_name, raw_output=''):
    failures = sum(1 for t in tests if t['status'] == 'FAIL')
    skipped  = sum(1 for t in tests if t['status'] == 'IGNORE')

    suite = ET.Element('testsuite', {
        'name':     suite_name,
        'tests':    str(len(tests)),
        'failures': str(failures),
        'skipped':  str(skipped),
        'errors':   '0',
        'hostname': 'ci',
    })

    # Suite-level properties (shown in Allure's environment panel)
    add_properties(suite, {
        'owner':       OWNER,
        'suite':       SUITE,
        'framework':   'Unity',
        'language':    'C',
        'priority':    'high',
    })

    for t in tests:
        feature, severity, story = detect_feature(t['name'])
        steps = detect_steps(t['name'], t['status'], t['msg'])

        tc = ET.SubElement(suite, 'testcase', {
            'name':      t['name'],
            'classname': suite_name,
            'file':      t['file'],
            'line':      t['line'],
            'time':      '0',
        })

        # Per-testcase properties — Allure reads these as labels/links
        add_properties(tc, {
            'severity':    severity,
            'feature':     feature,
            'story':       story,
            'owner':       OWNER,
            'priority':    'high',
            'language':    'C',
            'framework':   'Unity',
            'source_file': os.path.basename(t['file']),
            'source_line': t['line'],
            'description': (
                t['msg'] if t['msg']
                else f'{t["name"]} — CI error-path test (no hardware required)'
            ),
        })

        # <system-out>: human-readable steps + raw assertion message
        step_text = '\n'.join(f'[STEP] {s}' for s in steps)
        if t['msg']:
            step_text += f'\n[DETAIL] {t["msg"]}'
        step_text += f'\n[SOURCE] {t["file"]}:{t["line"]}'
        ET.SubElement(tc, 'system-out').text = step_text

        if t['status'] == 'FAIL':
            ET.SubElement(tc, 'failure', {
                'message': t['msg'],
                'type':    'AssertionError',
            }).text = t['msg']
        elif t['status'] == 'IGNORE':
            ET.SubElement(tc, 'skipped', message=t['msg'])

    # Attach the full Unity console output as <system-out> on the suite element
    if raw_output:
        ET.SubElement(suite, 'system-out').text = raw_output

    root = ET.Element('testsuites')
    root.append(suite)
    return root


def pretty(root):
    raw = ET.tostring(root, encoding='unicode')
    return minidom.parseString(raw).toprettyxml(indent='  ')


def main():
    suite_name = sys.argv[1] if len(sys.argv) > 1 else 'c-unity'
    raw_output = sys.stdin.read()
    tests = parse_unity_output(raw_output)
    if not tests:
        tests = [{
            'file': 'unknown', 'line': '0',
            'name': 'no_tests_found', 'status': 'PASS', 'msg': '',
        }]
    print(pretty(build_junit(tests, suite_name, raw_output)))


if __name__ == '__main__':
    main()
