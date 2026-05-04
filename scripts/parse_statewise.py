#!/usr/bin/env python3
"""Parse statewise_*.md (Jina-rendered ECI pages) into a flat JSON list."""
import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from districts import ac_to_district

DEFAULT_SRC = Path(os.environ.get("ECI_SRC", "/tmp/eci_data"))
OUT = Path(__file__).resolve().parent.parent / "data" / "constituencies.json"
AC_DISTRICT = ac_to_district()

# Strip the "i ### Party Wise State Trends Leading In:43 Won In:63 Trailing In:41"
# tail that Jina folds into the party cells.
PARTY_TAIL = re.compile(r"\s*i\s*###.*$", re.S)

PARTY_ABBR = {
    "Tamilaga Vettri Kazhagam": "TVK",
    "Dravida Munnetra Kazhagam": "DMK",
    "All India Anna Dravida Munnetra Kazhagam": "ADMK",
    "Pattali Makkal Katchi": "PMK",
    "Indian National Congress": "INC",
    "Indian Union Muslim League": "IUML",
    "Communist Party of India": "CPI",
    "Communist Party of India  (Marxist)": "CPI(M)",
    "Communist Party of India (Marxist)": "CPI(M)",
    "Viduthalai Chiruthaigal Katchi": "VCK",
    "Bharatiya Janata Party": "BJP",
    "Desiya Murpokku Dravida Kazhagam": "DMDK",
    "Amma Makkal Munnettra Kazagam": "AMMK",
    "Independent": "IND",
}


def clean_party(raw: str) -> tuple[str, str]:
    """Return (full_name, abbr) from a Jina party cell."""
    name = PARTY_TAIL.sub("", raw).strip()
    return name, PARTY_ABBR.get(name, name)


def parse_row(line: str) -> dict | None:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 9:
        return None
    name, no, lead_cand, lead_party, trail_cand, trail_party, margin, rounds, status = cells[:9]
    if not no.isdigit():
        return None
    lead_full, lead_abbr = clean_party(lead_party)
    trail_full, trail_abbr = clean_party(trail_party)
    ac_no = int(no)
    return {
        "ac_no": ac_no,
        "name": name,
        "district": AC_DISTRICT.get(ac_no, ""),
        "leading_candidate": lead_cand,
        "leading_party": lead_abbr,
        "leading_party_full": lead_full,
        "trailing_candidate": trail_cand,
        "trailing_party": trail_abbr,
        "trailing_party_full": trail_full,
        "margin": int(margin) if margin.isdigit() else 0,
        "round": rounds,
        "status": status,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC,
                    help="directory holding statewise_N.md files")
    args = ap.parse_args()
    rows = []
    for n in range(1, 13):
        path = args.src / f"statewise_{n}.md"
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            if not line.startswith("| ") or "Const. No." in line or "Status Known" in line:
                continue
            r = parse_row(line)
            if r:
                rows.append(r)
    rows.sort(key=lambda r: r["ac_no"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    print(f"wrote {len(rows)} constituencies → {OUT}")
    parties = {}
    for r in rows:
        parties[r["leading_party"]] = parties.get(r["leading_party"], 0) + 1
    print("party tallies:", dict(sorted(parties.items(), key=lambda kv: -kv[1])))


if __name__ == "__main__":
    main()
