#!/usr/bin/env python3
"""Inline data/constituencies.json into index.html.

Replaces the contents of <script id="bootstrap-data">…</script> with the
current JSON, so the page works when opened directly via file://.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
DATA = ROOT / "data" / "constituencies.json"

PATTERN = re.compile(
    r'(<script id="bootstrap-data" type="application/json">)(.*?)(</script>)',
    re.S,
)


def main():
    rows = json.loads(DATA.read_text())
    payload = json.dumps(rows, separators=(",", ":"), ensure_ascii=False)
    src = HTML.read_text()
    new = PATTERN.sub(lambda m: m.group(1) + payload + m.group(3), src, count=1)
    if new == src:
        raise SystemExit("bootstrap-data block not found in index.html")
    HTML.write_text(new)
    print(f"inlined {len(rows)} rows ({len(payload)} bytes) into {HTML.name}")


if __name__ == "__main__":
    main()
