import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RESULTS = REPO / "results"

def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _run(cmd, cwd=REPO):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\nSTDOUT:\n{r.stdout}\nSTDERR:\n{r.stderr}"
        )
    return r

def test_reproducibility_outputs_match_repo(tmp_path):
    """
    Strong reproducibility: regenerate outputs in a clean temp dir and require byte-identical
    CSV/JSON vs the versioned ones in results/.
    """
    # Copy repo minimal structure into temp (models, scripts, pyproject/requirements, etc.)
    work = tmp_path / "work"
    shutil.copytree(REPO / "models", work / "models")
    shutil.copytree(REPO / "scripts", work / "scripts")
    (work / "results").mkdir(parents=True, exist_ok=True)

    # Ensure package init exists
    (work / "models" / "__init__.py").touch(exist_ok=True)

    # Run analysis (writes into work/results)
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
        assert _sha256(got) == _sha256(ref), f"Non-reproducible output: {name}"

def test_statistical_tests_json_is_stable_schema():
    """
    Basic schema sanity for results/statistical_tests.json
    """
    p = RESULTS / "statistical_tests.json"
    assert p.exists(), "results/statistical_tests.json missing"
    data = json.loads(p.read_text(encoding="utf-8"))
    for k in ("realistic", "extreme"):
        assert k in data
        for field in ("slope", "p_value_trend", "r_squared", "adf_statistic", "adf_p_value", "is_stationary"):
            assert field in data[k]
