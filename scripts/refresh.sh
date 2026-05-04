#!/usr/bin/env bash
# Re-fetch ECI statewise pages, parse them, and inline into index.html.
# Used both locally and by the GitHub Actions cron.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="${ECI_SRC:-$(mktemp -d)}"
mkdir -p "$SRC_DIR"

for n in $(seq 1 12); do
  curl -fsSL -o "$SRC_DIR/statewise_${n}.md" \
    "https://r.jina.ai/https://results.eci.gov.in/ResultAcGenMay2026/statewiseS22${n}.htm"
done

python3 "$ROOT/scripts/parse_statewise.py" --src "$SRC_DIR"
python3 "$ROOT/scripts/build.py"
