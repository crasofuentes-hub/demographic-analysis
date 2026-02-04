from __future__ import annotations
import json

def _write_deterministic_csv(df: pd.DataFrame, path: str) -> None:
    """Write CSV deterministically across OS/Python (stable column order, floats, newlines)."""
    # Stable column order: year first if present, then sorted remainder
    cols = list(df.columns)
    if "year" in cols:
        rest = sorted([c for c in cols if c != "year"])
        cols = ["year"] + rest
        df = df[cols]
    df.to_csv(path, index=False, float_format="%.10g", lineterminator="\n")
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import adfuller

from .cohort_model import CohortComponentModel
from .scenarios import realistic_scenario_model, conspiracy_scenario_model

def test_replacement_hypothesis(df: pd.DataFrame) -> dict:
    years = df["year"].to_numpy()
    prop_a = (df["group_a"] / df["total_population"]).to_numpy()

    slope, intercept, r_value, p_value, std_err = stats.linregress(years, prop_a)

    years_to_50 = None
    if slope < 0:
        y50 = (0.5 - intercept) / slope
        if y50 > years.min():
            years_to_50 = float(y50)

    adf_stat, adf_p, *_ = adfuller(prop_a)

    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "p_value_trend": float(p_value),
        "r_squared": float(r_value**2),
        "years_to_majority_loss": years_to_50,
        "adf_statistic": float(adf_stat),
        "adf_p_value": float(adf_p),
        "is_stationary": bool(adf_p < 0.05),
    }

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = []
    for _, r in df.iterrows():
        total = r["total_population"]
        prop = np.array([r["group_a"], r["group_b"]], dtype=float)
        prop = prop / prop.sum()
        diversity = -float(np.sum([p * np.log(p) for p in prop if p > 0]))

        out.append({
            "year": int(r["year"]),
            "proportion_group_a": float(r["group_a"] / total),
            "dependency_ratio": float(r["group_b"] / r["group_a"]) if r["group_a"] > 0 else None,
            "diversity_index": diversity
        })
    return pd.DataFrame(out)

def run():
    real = realistic_scenario_model()
    m1 = CohortComponentModel(real["initial_population"], real["fertility_rates"], real["mortality_rates"], real["migration_rates"])
    df_real = m1.project(100, start_year=2023, convergence_rate=real["convergence_rate"])

    con = conspiracy_scenario_model()
    m2 = CohortComponentModel(con["initial_population"], con["fertility_rates"], con["mortality_rates"], con["migration_rates"])
    df_con = m2.project(100, start_year=2023, convergence_rate=con["convergence_rate"])

    stats_real = test_replacement_hypothesis(df_real)
    stats_con  = test_replacement_hypothesis(df_con)

    ind_real = calculate_indicators(df_real)
    ind_con  = calculate_indicators(df_con)

    _write_deterministic_csv(df_real, r"results\projections_realistic.csv")
    _write_deterministic_csv(df_con,  r"results\projections_extreme.csv")
    _write_deterministic_csv(ind_real, r"results\indicators_realistic.csv")
    _write_deterministic_csv(ind_con,  r"results\indicators_extreme.csv")

    with open(r"results\statistical_tests.json", "w", encoding="utf-8") as f:
        json.dump({"realistic": stats_real, "extreme": stats_con}, f, indent=2, sort_keys=True)if __name__ == "__main__":
    run()

