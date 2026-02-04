from __future__ import annotations

import hashlib
import json
import runpy
import shutil
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"

EXPECTED = {
    "projections_realistic.csv",
    "projections_extreme.csv",
    "indicators_realistic.csv",
    "indicators_extreme.csv",
    "statistical_tests.json",
}

def _canon_hash(path: Path) -> str:
    """
    Canonical hash:
    - CSV: parse -> sort columns -> stable float rounding -> stable line endings
    - JSON: parse -> sort keys
    """
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
        # canonicalize: sort columns, stable rounding, stable ordering
        df = df.reindex(sorted(df.columns), axis=1)
        # round numerics aggressively enough to kill formatting noise
        for c in df.columns:
            if pd.api.types.is_numeric_dtype(df[c]):
                df[c] = df[c].round(12)
        # stable bytes
        b = df.to_csv(index=False, lineterminator="\n").encode("utf-8")
        return hashlib.sha256(b).hexdigest()

    if path.suffix.lower() == ".json":
        obj = json.loads(path.read_text(encoding="utf-8"))
        b = json.dumps(obj, sort_keys=True, indent=2).encode("utf-8")
        return hashlib.sha256(b).hexdigest()

    return hashlib.sha256(path.read_bytes()).hexdigest()

def test_reproducibility_outputs_match_repo(tmp_path, monkeypatch):
    """
    Strong reproducibility:
    - run the analysis in a CLEAN working dir (tmp)
    - require canonical match vs versioned results/
    """
    work = tmp_path / "work"
    work.mkdir(parents=True, exist_ok=True)
    (work / "results").mkdir(parents=True, exist_ok=True)

    # Run models.analysis as __main__ IN-PROCESS so coverage counts.
    monkeypatch.chdir(work)
    runpy.run_module("models.analysis", run_name="__main__")

    for name in EXPECTED:
        got = work / "results" / name
        ref = RESULTS / name
        assert got.exists(), f"Missing generated output: {got}"
        assert ref.exists(), f"Missing reference output tracked in repo: {ref}"
        assert _canon_hash(got) == _canon_hash(ref), f"Non-reproducible output (canonical mismatch): {name}"