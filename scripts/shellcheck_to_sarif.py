#!/usr/bin/env python3
"""Convert shellcheck JSON output to SARIF 2.1.0 format for SonarQube."""
import json
import sys

SEVERITY_MAP = {
    "error": "error",
    "warning": "warning",
    "info": "note",
    "style": "note",
}


def convert(findings: list) -> dict:
    rules: dict[str, dict] = {}
    results = []

    for f in findings:
        rule_id = f"SC{f['code']}"
        if rule_id not in rules:
            rules[rule_id] = {
                "id": rule_id,
                "name": rule_id,
                "shortDescription": {"text": f["message"]},
                "helpUri": f"https://www.shellcheck.net/wiki/SC{f['code']}",
                "defaultConfiguration": {
                    "level": SEVERITY_MAP.get(f.get("level", "warning"), "warning")
                },
            }
        results.append(
            {
                "ruleId": rule_id,
                "level": SEVERITY_MAP.get(f.get("level", "warning"), "warning"),
                "message": {"text": f["message"]},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {
                                "uri": f["file"].lstrip("./"),
                                "uriBaseId": "%SRCROOT%",
                            },
                            "region": {
                                "startLine": f["line"],
                                "startColumn": f["column"],
                                "endLine": f.get("endLine", f["line"]),
                                "endColumn": f.get("endColumn", f["column"] + 1),
                            },
                        }
                    }
                ],
            }
        )

    return {
        "version": "2.1.0",
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "shellcheck",
                        "informationUri": "https://www.shellcheck.net",
                        "rules": list(rules.values()),
                    }
                },
                "results": results,
            }
        ],
    }


if __name__ == "__main__":
    data = json.load(sys.stdin)
    print(json.dumps(convert(data), indent=2))
