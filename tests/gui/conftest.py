import os
import pytest

GUI = os.getenv("BBGUI", "./bin/bbgui-linux-amd64")


def pytest_collection_modifyitems(config, items):
    if not os.path.isfile(GUI):
        skip = pytest.mark.skip(
            reason=f"GUI-Binary nicht gefunden ({GUI}) — zuerst 'make cli' ausführen"
        )
        for item in items:
            parts = item.path.parts if hasattr(item, "path") else []
            if "gui" in parts:
                item.add_marker(skip)
