"""Which files in data/ are due for their yearly refresh.

`python3 scripts/fetch_data.py status` prints every data file with its README "Refresh the data" step, the period it
covers, when it was last refreshed and whether it's due; the build prints one line when something is. A file is due
once the month its source usually publishes (`month`) has come round since it was last refreshed, or, for a source
without a fixed month, a year after. Last refreshed: the file's own "fetched" date when it has one, else the date of
the last commit that changed it (a shallow clone has no older dates, and says so).

Add a new data file to DATASETS: the report flags any it doesn't know.
"""
import datetime
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# (README step, files, when the source publishes, month it's usually out (1-12) or None: a year after the last
# refresh, or "rarely": never due). Keep in step with README "Refresh the data".
DATASETS = [
    ("1 Zones", ("elem_zones.json", "ms_zones.json", "hs_zones.json"), "each fall, when Find a School updates", 10),
    ("2 MySchools", ("hs_directory.json", "ms_directory.json", "accessibility.json"), "October, when applications open", 10),
    ("2 MySchools", ("nonzoned_k.json", "citywide_gt_k.json", "k_priority.json"), "December, kindergarten applications", 12),
    ("2b PSAL campuses and teams", ("psal_campuses.json", "psal_teams.json"), "each fall, after MySchools", 11),
    ("3 Snapshot", ("snapshot_ratings.json", "snapshot_extra.json", "snapshot_tests.json", "hs_outcomes.json",
                    "nonzoned_snapshot.json", "ms_snapshot.json", "hs_snapshot.json", "charter_snapshot.json",
                    "snapshot_counts.json", "colocation.json"), "when a new year appears", None),
    ("3b State tests", ("state_tests.json",), "late summer", 9),
    ("3c State improvement lists", ("state_status.json",), "August, when NYSED posts its report card database", 9),
    ("4 Admissions", ("k_admissions.json", "ms_admissions.json", "hs_admissions.json", "prek.json"),
     "fall or winter, for the previous fall", None),
    ("5 Class size", ("class_size.json",), "spring", 4),
    ("6 Charter schools", ("charters.json", "zips.json"), "each fall", 10),
    ("6b Demographics", ("demographics.json",), "fall, when a new Demographic Snapshot is posted", None),
    ("7 Building use", ("utilization.json",), "once a year", None),
    ("8 Hand-checked", ("citywide_ms.json", "school_fixes.json", "charter_fixes.json"), "each fall", 10),
    ("8 Hand-checked", ("shsat_cutoffs.json",), "late winter, after offers", 3),
    ("9 Rarely", ("districts.json", "streets.json", "local_streets.json", "parks.json", "neighborhoods.json"),
     "rarely", "rarely"),
]


def _shallow():
    try:
        return subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT, capture_output=True,
                              text=True).stdout.strip() == "true"
    except OSError:
        return False


def _git_date(name):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", f"data/{name}"], cwd=ROOT,
                             capture_output=True, text=True).stdout.strip()
        return datetime.date.fromisoformat(out) if out else None
    except (OSError, ValueError):
        return None


def _own_date(path):
    """A "fetched 2026-11-10" or "fetched": "2026-10-21" the file records itself, read from its first few KB."""
    try:
        with open(path, encoding="utf-8") as f:
            head = f.read(4000)
    except OSError:
        return None
    m = re.search(r'fetched"?\s*:?\s*"?\s*(\d{4}-\d{2}-\d{2})', head)
    return datetime.date.fromisoformat(m.group(1)) if m else None


def _due(last, month, today):
    """Whether a source due in `month` (or a year after `last`, month None) has come round since `last`."""
    if month == "rarely" or last is None:
        return month != "rarely" and last is None
    if month is None:
        return (today - last).days > 365
    nxt = datetime.date(last.year + (last.month >= month), month, 1)
    return today >= nxt


def report(today=None, periods=None):
    """[(step, file, covers, last refreshed or None, due, when)], then data files DATASETS doesn't list. periods:
    {file: period} (fetch_data.py history_period) for the "covers" column."""
    today = today or datetime.date.today()
    periods = periods or {}
    rows, known = [], set()
    for step, files, when, month in DATASETS:
        for name in files:
            known.add(name)
            path = os.path.join(DATA, name)
            if not os.path.exists(path):
                continue
            last = _own_date(path) or _git_date(name)
            rows.append((step, name, periods.get(name) or "", last, _due(last, month, today), when))
    unknown = sorted(n for n in os.listdir(DATA) if n.endswith(".json") and n not in known
                     and not n.endswith("_raw.json"))
    return rows, unknown


def summary(today=None):
    """The build's line: "" when nothing is due."""
    rows, unknown = report(today)
    due = sorted({r[0] for r in rows if r[4]}, key=lambda s: (int(re.match(r"\d+", s).group()), s))
    bits = []
    if due:
        bits.append("refresh due: " + ", ".join(due))
    if unknown:
        bits.append("not in scripts/data_status.py: " + ", ".join(unknown))
    return ("data: " + "; ".join(bits) + " (python3 scripts/fetch_data.py status)") if bits else ""


def print_report(periods=None):
    rows, unknown = report(periods=periods)
    w = max(len(r[1]) for r in rows)
    step = None
    for r in rows:
        if (r[0], r[5]) != step:
            step = (r[0], r[5])
            print(f"\n{r[0]}  ({r[5]})")
        last = r[3].isoformat() if r[3] else "unknown"
        print(f"  {'DUE ' if r[4] else '    '}{r[1]:<{w}}  last refreshed {last}" + (f"  covers {r[2]}" if r[2] else ""))
    if unknown:
        print("\nNot in scripts/data_status.py (add them to DATASETS and to README \"Refresh the data\"):")
        for n in unknown:
            print("  " + n)
    if _shallow():
        print("\nThis is a shallow clone: files no commit here changed show the oldest commit's date. "
              "`git fetch --unshallow` gives the real dates.")
    n = sum(1 for r in rows if r[4])
    print(f"\n{n} file{'s' if n != 1 else ''} due. Steps are in README.md, \"Refresh the data\".")
