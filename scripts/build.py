#!/usr/bin/env python3
"""Inline data/constituencies.json + a built-at timestamp into index.html.

Replaces the contents of <script id="bootstrap-data">…</script> with the
current JSON, and <script id="bootstrap-meta">…</script> with a small
metadata blob (built_at). So the page works when opened via file:// and
can also display when the bundled snapshot was last refreshed.
"""
import datetime as dt
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
DATA = ROOT / "data" / "constituencies.json"

DATA_PATTERN = re.compile(
    r'(<script id="bootstrap-data" type="application/json">)(.*?)(</script>)',
    re.S,
)
META_PATTERN = re.compile(
    r'(<script id="bootstrap-meta" type="application/json">)(.*?)(</script>)',
    re.S,
)


def main():
    rows = json.loads(DATA.read_text())
    payload = json.dumps(rows, separators=(",", ":"), ensure_ascii=False)
    meta = json.dumps(
        {"built_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
        separators=(",", ":"),
    )
    src = HTML.read_text()
    new, n1 = DATA_PATTERN.subn(lambda m: m.group(1) + payload + m.group(3), src, count=1)
    if not n1:
        raise SystemExit("bootstrap-data block not found in index.html")
    new, n2 = META_PATTERN.subn(lambda m: m.group(1) + meta + m.group(3), new, count=1)
    if not n2:
        raise SystemExit("bootstrap-meta block not found in index.html")
    HTML.write_text(new)
    print(f"inlined {len(rows)} rows ({len(payload)} bytes) + meta into {HTML.name}")


if __name__ == "__main__":
    main()
