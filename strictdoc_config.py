from strictdoc.core.project_config import ProjectConfig


def create_config():
    return ProjectConfig(
        project_title="BeagleBone Black Embedded SW",
        include_doc_paths=["docs/requirements", "reports"],
        # Nur Quellcode-Verzeichnisse für Source-Traceability scannen
        include_source_paths=[
            "go-api/",
            "c-lib/",
            "project/rust-lib/",
            "tests/",
            "Makefile",
        ],
        project_features=[
            "HTML2PDF",
            "TRACEABILITY_SCREEN",
            "DEEP_TRACEABILITY_SCREEN",
            "TRACEABILITY_MATRIX_SCREEN",
            "TABLE_SCREEN",
            "PROJECT_STATISTICS_SCREEN",
            "REQUIREMENT_TO_SOURCE_TRACEABILITY",
            "MERMAID",
            "DIFF",
        ],
    )
