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


def _row(ac_no, name, lc, lp_full, tc, tp_full, margin, rounds, status):
    return {
        "ac_no": ac_no,
        "name": name,
        "district": AC_DISTRICT.get(ac_no, ""),
        "leading_candidate": lc,
        "leading_party": PARTY_ABBR.get(lp_full, lp_full),
        "leading_party_full": lp_full,
        "trailing_candidate": tc,
        "trailing_party": PARTY_ABBR.get(tp_full, tp_full),
        "trailing_party_full": tp_full,
        "margin": int(margin) if str(margin).isdigit() else 0,
        "round": rounds,
        "status": status,
    }


def parse_row(line: str) -> dict | None:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 9:
        return None
    name, no, lead_cand, lead_party, trail_cand, trail_party, margin, rounds, status = cells[:9]
    if not no.isdigit():
        return None
    lead_full, _ = clean_party(lead_party)
    trail_full, _ = clean_party(trail_party)
    return _row(int(no), name, lead_cand, lead_full, trail_cand, trail_full,
                margin, rounds, status)


# --- Naked-text fallback (Jina sometimes drops the Markdown table format) ---

# Sorted longest-first so longer party names win over their prefixes.
_PARTY_NAMES_SORTED = sorted(set(PARTY_ABBR.keys()), key=len, reverse=True)
_PARTY_RE = re.compile("|".join(re.escape(p) for p in _PARTY_NAMES_SORTED))
_TRENDS_SPLIT = re.compile(r"\s*i\s*###\s*Party Wise State Trends\s*")
_TRENDS_TAIL = re.compile(r"^Leading In:\d+ Won In:\d+ Trailing In:\d+\s*")
_STATUS_RE = re.compile(r"\s+(\d+)\s+(\d+/\d+)\s+(Result Declared|Result in Progress)\s*$")


def _split_cand_party(chunk: str) -> tuple[str, str] | None:
    matches = list(_PARTY_RE.finditer(chunk))
    if not matches:
        return None
    last = matches[-1]
    return chunk[: last.start()].rstrip(), last.group(0)


def parse_naked_row(line: str) -> dict | None:
    parts = _TRENDS_SPLIT.split(line)
    if len(parts) != 3:
        return None
    tail = _STATUS_RE.search(parts[2])
    if not tail:
        return None
    margin, rounds, status = tail.groups()

    m0 = re.match(r"^(.+?)\s*(\d{1,3})\s+(.*)$", parts[0])
    if not m0:
        return None
    name, ac_no, rest0 = m0.group(1).strip(), int(m0.group(2)), m0.group(3)
    cp_l = _split_cand_party(rest0)
    if not cp_l:
        return None

    rest1 = _TRENDS_TAIL.sub("", parts[1])
    cp_t = _split_cand_party(rest1)
    if not cp_t:
        return None

    return _row(ac_no, name, cp_l[0], cp_l[1], cp_t[0], cp_t[1],
                margin, rounds, status)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC,
                    help="directory holding statewise_N.md files")
    args = ap.parse_args()
    seen: set[int] = set()
    rows: list[dict] = []
    for n in range(1, 13):
        path = args.src / f"statewise_{n}.md"
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            r = None
            if line.startswith("| ") and "Const. No." not in line and "Status Known" not in line:
                r = parse_row(line)
            elif _TRENDS_SPLIT.search(line) and _STATUS_RE.search(line):
                r = parse_naked_row(line)
            if r and r["ac_no"] not in seen:
                seen.add(r["ac_no"])
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
