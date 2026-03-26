#!/usr/bin/env python3
"""
Requirements coverage gate for StrictDoc-based projects.

Reads all .sdoc files and checks:
  1. Every Active requirement has at least one test file relation
  2. If a JUnit XML is provided, linked test files are cross-referenced
     against actual test pass/fail results

Exit 0 if coverage >= threshold, exit 1 otherwise.

Usage:
    python3 scripts/check_req_coverage.py \
        --sdoc-dir docs/requirements \
        --junit-xml reports/go-tests-junit.xml \
        --min-coverage 70
"""
import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from xml.dom import minidom


TEST_FILE_RE = re.compile(
    r'(test_.*\.py|.*_test\.go|.*_test\.py|.*_test\.c|test.*\.rs)',
    re.IGNORECASE,
)

REQ_BLOCK_TYPES = {'SYS_REQUIREMENT', 'SW_REQUIREMENT', 'HW_REQUIREMENT', 'TEST_CASE'}


@dataclass
class Requirement:
    uid: str
    title: str
    status: str
    doc_type: str
    file_relations: list = field(default_factory=list)


def parse_sdoc_file(path: Path) -> list:
    content = path.read_text(encoding='utf-8')

    # Split on requirement block markers
    pattern = r'\n(?=\[(?:SYS_REQUIREMENT|SW_REQUIREMENT|HW_REQUIREMENT|TEST_CASE)\])'
    blocks = re.split(pattern, content)

    requirements = []
    for block in blocks:
        type_match = re.match(r'\[(\w+)\]', block.strip())
        if not type_match or type_match.group(1) not in REQ_BLOCK_TYPES:
            continue
        doc_type = type_match.group(1)

        uid_m = re.search(r'^UID:\s*(.+)$', block, re.MULTILINE)
        if not uid_m:
            continue

        title_m = re.search(r'^TITLE:\s*(.+)$', block, re.MULTILINE)
        status_m = re.search(r'^STATUS:\s*(.+)$', block, re.MULTILINE)

        # Collect TYPE: File relations
        file_relations = []
        rel_block = re.search(r'RELATIONS:(.*?)(?=\n\[|\Z)', block, re.DOTALL)
        if rel_block:
            file_relations = re.findall(
                r'-\s*TYPE:\s*File\s*\n\s*VALUE:\s*(.+)', rel_block.group(1)
            )
            file_relations = [v.strip() for v in file_relations]

        requirements.append(Requirement(
            uid=uid_m.group(1).strip(),
            title=title_m.group(1).strip() if title_m else '',
            status=status_m.group(1).strip() if status_m else 'Draft',
            doc_type=doc_type,
            file_relations=file_relations,
        ))

    return requirements


def is_test_file(path: str) -> bool:
    return bool(TEST_FILE_RE.match(os.path.basename(path)))


def load_junit_results(junit_path: Path) -> dict:
    """Returns {qualified_name: 'pass'|'fail'|'skip'}."""
    if not junit_path.exists():
        return {}
    try:
        root = ET.parse(junit_path).getroot()
        results = {}
        for tc in root.iter('testcase'):
            name = '/'.join(filter(None, [tc.get('classname'), tc.get('name')]))
            if tc.find('failure') is not None or tc.find('error') is not None:
                results[name] = 'fail'
            elif tc.find('skipped') is not None:
                results[name] = 'skip'
            else:
                results[name] = 'pass'
        return results
    except ET.ParseError as exc:
        print(f'WARNING: Cannot parse JUnit XML: {exc}', file=sys.stderr)
        return {}


def junit_status_for(test_files: list, junit_results: dict) -> str:
    """Return aggregate JUnit status for a requirement's test files."""
    if not junit_results or not test_files:
        return '-'
    any_pass = False
    any_fail = False
    for tf in test_files:
        stem = Path(tf).stem.lower()  # e.g. 'hal_test'
        for name, result in junit_results.items():
            if stem in name.lower():
                if result == 'fail':
                    any_fail = True
                elif result == 'pass':
                    any_pass = True
    if any_fail:
        return 'FAIL'
    if any_pass:
        return 'PASS'
    return '?'


def write_junit_xml(active: list, covered_set: set, junit_failures_set: set, output_path: Path) -> None:
    """Write requirements coverage results as JUnit XML for Drone plugin cards."""
    testsuites = ET.Element('testsuites')
    testsuite = ET.SubElement(testsuites, 'testsuite')
    testsuite.set('name', 'Requirements Coverage')
    testsuite.set('tests', str(len(active)))

    failures = 0
    for req in active:
        tc = ET.SubElement(testsuite, 'testcase')
        # classname = requirement type prefix (SYS, SWR, HW-DRV, …)
        prefix = req.uid.split('-')[0]
        tc.set('classname', prefix)
        tc.set('name', f'{req.uid}: {req.title}')

        if req.uid in junit_failures_set:
            failures += 1
            f = ET.SubElement(tc, 'failure')
            f.set('message', 'Linked test(s) are FAILING')
            f.text = f'Requirement {req.uid} has failing tests in JUnit results'
        elif req.uid not in covered_set:
            failures += 1
            f = ET.SubElement(tc, 'failure')
            f.set('message', 'No test file relation')
            f.text = f'Requirement {req.uid} has no linked test file (TYPE: File → *_test.*)'

    testsuite.set('failures', str(failures))
    testsuite.set('errors', '0')
    testsuite.set('skipped', '0')

    output_path.parent.mkdir(parents=True, exist_ok=True)
    xml_str = minidom.parseString(ET.tostring(testsuites, encoding='unicode')).toprettyxml(indent='  ')
    # minidom adds an XML declaration — keep it
    output_path.write_text(xml_str, encoding='utf-8')
    print(f'JUnit XML written to {output_path}')


def main() -> None:
    parser = argparse.ArgumentParser(description='Requirements coverage gate')
    parser.add_argument('--sdoc-dir', default='docs/requirements')
    parser.add_argument('--junit-xml', default='reports/go-tests-junit.xml')
    parser.add_argument('--output-junit', default='reports/req-coverage-junit.xml',
                        help='Output JUnit XML for Drone plugin cards')
    parser.add_argument('--min-coverage', type=int, default=70,
                        help='Minimum test-file coverage %% (default: 70)')
    args = parser.parse_args()

    sdoc_dir = Path(args.sdoc_dir)
    junit_path = Path(args.junit_xml)

    # ── Parse .sdoc files ────────────────────────────────────────────────────
    all_reqs: list = []
    for sdoc_file in sorted(sdoc_dir.rglob('*.sdoc')):
        reqs = parse_sdoc_file(sdoc_file)
        all_reqs.extend(reqs)
        print(f'  {sdoc_file.name}: {len(reqs)} requirement(s)')

    if not all_reqs:
        print('WARNING: No requirements found — nothing to check')
        sys.exit(0)

    # Only gate on Active non-TEST_CASE items
    active = [r for r in all_reqs if r.status == 'Active' and r.doc_type != 'TEST_CASE']
    print(f'\n{len(active)} active requirement(s) found (of {len(all_reqs)} total)\n')

    # ── JUnit cross-reference ────────────────────────────────────────────────
    junit_results = load_junit_results(junit_path)
    if junit_results:
        passed = sum(1 for v in junit_results.values() if v == 'pass')
        failed = sum(1 for v in junit_results.values() if v == 'fail')
        print(f'JUnit XML ({junit_path}): {passed} passed, {failed} failed\n')
    else:
        print(f'JUnit XML: not found at {junit_path} — pass/fail check skipped\n')

    # ── Coverage table ───────────────────────────────────────────────────────
    header = f"{'UID':<16} {'Cov':<5} {'JUnit':<6}  Title"
    print(header)
    print('─' * 72)

    covered = 0
    covered_set = set()
    uncovered_reqs = []
    junit_failures = []
    junit_failures_set = set()

    for req in active:
        test_files = [f for f in req.file_relations if is_test_file(f)]
        has_test = bool(test_files)
        cov_icon = '✓' if has_test else '✗'
        j_status = junit_status_for(test_files, junit_results)
        title_short = req.title[:44] + '…' if len(req.title) > 45 else req.title

        print(f'{req.uid:<16} {cov_icon:<5} {j_status:<6}  {title_short}')

        if has_test:
            covered += 1
            covered_set.add(req.uid)
        else:
            uncovered_reqs.append(req)

        if j_status == 'FAIL':
            junit_failures.append(req)
            junit_failures_set.add(req.uid)

    # ── JUnit XML output for Drone plugin cards ───────────────────────────────
    write_junit_xml(active, covered_set, junit_failures_set, Path(args.output_junit))

    # ── Summary ──────────────────────────────────────────────────────────────
    coverage_pct = int(covered / len(active) * 100) if active else 0
    print(f'\nCoverage: {covered}/{len(active)} ({coverage_pct}%)')

    exit_code = 0

    if uncovered_reqs:
        print(f'\nRequirements without test file relation ({len(uncovered_reqs)}):')
        for r in uncovered_reqs:
            print(f'  [{r.uid}] {r.title}')

    if junit_failures:
        print(f'\nRequirements with FAILING tests ({len(junit_failures)}):')
        for r in junit_failures:
            print(f'  [{r.uid}] {r.title}')
        exit_code = 1

    if coverage_pct < args.min_coverage:
        print(f'\n❌ Coverage gate FAILED: {coverage_pct}% < {args.min_coverage}% minimum')
        exit_code = 1
    elif exit_code == 0:
        print(f'\n✅ Coverage gate PASSED: {coverage_pct}% >= {args.min_coverage}%')

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
