from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"

def _run(cmd, cwd=REPO):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(map(str, cmd))}\nSTDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}"
        )
    return r

def _sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()

def _is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except Exception:
        return False

def _normalize_csv_bytes(path: Path, float_decimals: int = 12) -> bytes:
    """
    Canonical CSV:
    - UTF-8
    - newline = \n
    - stable column order (alphabetical)
    - stable row order (lexicographic over all fields)
    - float rounding to fixed decimals (stringified)
    """
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        if reader.fieldnames is None:
            return b""

    cols = sorted(reader.fieldnames)

    # Normalize values
    norm_rows = []
    for row in rows:
        nr = {}
        for c in cols:
            v = "" if row.get(c) is None else str(row.get(c))
            v = v.strip()
            if _is_float(v):
                nr[c] = f"{float(v):.{float_decimals}f}"
            else:
                nr[c] = v
        norm_rows.append(nr)

    # Stable row order
    norm_rows.sort(key=lambda r: tuple(r[c] for c in cols))

    # Write canonical bytes
    out_lines = []
    out_lines.append(",".join(cols))
    for r in norm_rows:
        out_lines.append(",".join(r[c] for c in cols))
    return ("\n".join(out_lines) + "\n").encode("utf-8")

def _normalize_json_bytes(path: Path) -> bytes:
    obj = json.loads(path.read_text(encoding="utf-8"))
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")

def _canon_hash(path: Path) -> str:
    if path.suffix.lower() == ".csv":
        return _sha256_bytes(_normalize_csv_bytes(path))
    if path.suffix.lower() == ".json":
        return _sha256_bytes(_normalize_json_bytes(path))
    return _sha256_bytes(path.read_bytes())

def test_reproducibility_outputs_match_repo(tmp_path):
    """
    Strong reproducibility (semantic): regenerate outputs in a clean temp dir and require
    canonical-hash equality for CSV/JSON vs the versioned ones in results/.
    """
    work = tmp_path / "work"
    shutil.copytree(REPO / "models", work / "models")
    shutil.copytree(REPO / "scripts", work / "scripts")
    (work / "results").mkdir(parents=True, exist_ok=True)

    # Ensure package init exists
    (work / "models" / "__init__.py").touch(exist_ok=True)

    _run([sys.executable, "-m", "models.analysis"], cwd=work)

    expected = {
        "projections_realistic.csv",
        "projections_extreme.csv",
        "indicators_realistic.csv",
        "indicators_extreme.csv",
        "statistical_tests.json",
    }

    for name in expected:
        got = (work / "results" / name)
        ref = (RESULTS / name)
        assert got.exists(), f"Missing generated output: {got}"
        assert ref.exists(), f"Missing reference output tracked in repo: {ref}"
        assert _canon_hash(got) == _canon_hash(ref), f"Non-reproducible output (canonical mismatch): {name}"