import os
import socket
import pytest

TUI = os.getenv("BBTUI", "./bin/bbtui-linux-amd64")
HOST = os.getenv("BEAGLE_HOST", "192.168.7.2")


def pytest_collection_modifyitems(config, items):
    if not os.path.isfile(TUI):
        skip = pytest.mark.skip(
            reason=f"TUI-Binary nicht gefunden ({TUI}) — zuerst 'make cli' ausführen"
        )
        for item in items:
            parts = item.path.parts if hasattr(item, "path") else []
            if "tui" in parts:
                item.add_marker(skip)
