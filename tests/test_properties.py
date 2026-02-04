from __future__ import annotations

from hypothesis import given, settings, strategies as st
import math

# Property-based tests target model invariants at the "scenario parameter" layer
# without assuming any specific country.

@st.composite
def rates(draw):
    # Keep rates in reasonable ranges to avoid trivial blowups:
    # fertility (annualized) ~ [0, 0.05], mortality [0, 0.03], migration [-0.02, 0.05]
    fA = draw(st.floats(min_value=0.0, max_value=0.05, allow_nan=False, allow_infinity=False))
    fB = draw(st.floats(min_value=0.0, max_value=0.05, allow_nan=False, allow_infinity=False))
    dA = draw(st.floats(min_value=0.0, max_value=0.03, allow_nan=False, allow_infinity=False))
    dB = draw(st.floats(min_value=0.0, max_value=0.03, allow_nan=False, allow_infinity=False))
    mA = draw(st.floats(min_value=-0.02, max_value=0.05, allow_nan=False, allow_infinity=False))
    mB = draw(st.floats(min_value=-0.02, max_value=0.05, allow_nan=False, allow_infinity=False))
    lam = draw(st.floats(min_value=0.0, max_value=0.2, allow_nan=False, allow_infinity=False))
    return fA, fB, dA, dB, mA, mB, lam

def step(N, f, d, m):
    return N + (N * f) - (N * d) + (N * m)

@settings(max_examples=200, deadline=None)
@given(
    NA=st.floats(min_value=1.0, max_value=1e8, allow_nan=False, allow_infinity=False),
    NB=st.floats(min_value=1.0, max_value=1e8, allow_nan=False, allow_infinity=False),
    r=rates()
)
def test_population_non_negative_under_reasonable_rates(NA, NB, r):
    fA, fB, dA, dB, mA, mB, lam = r
    # One-step update should remain non-negative given moderate rates
    NA2 = step(NA, fA, dA, mA)
    NB2 = step(NB, fB, dB, mB)
    assert NA2 > 0.0
    assert NB2 > 0.0

@settings(max_examples=200, deadline=None)
@given(r=rates())
def test_convergence_shrinks_rate_gap(r):
    fA, fB, dA, dB, mA, mB, lam = r
    # Convergence should reduce absolute gap unless already equal or lam=0
    fbar = (fA + fB) / 2.0
    dbar = (dA + dB) / 2.0

    fA2 = fA + lam * (fbar - fA)
    fB2 = fB + lam * (fbar - fB)
    dA2 = dA + lam * (dbar - dA)
    dB2 = dB + lam * (dbar - dB)

    if lam > 0 and (fA != fB):
        assert abs(fA2 - fB2) < abs(fA - fB) + 1e-15
    if lam > 0 and (dA != dB):
        assert abs(dA2 - dB2) < abs(dA - dB) + 1e-15
