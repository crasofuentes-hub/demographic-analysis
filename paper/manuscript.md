# Demographic Dynamics and the Mathematical Infeasibility of the “Great Replacement” Hypothesis

Oscar Fuentes  
2026-02-04  

---

## Abstract

Public discourse sometimes frames demographic change as an intentional and rapid population “replacement” process. Such claims imply specific mathematical conditions on fertility, mortality, migration, and intergenerational persistence. This manuscript evaluates the plausibility of the “Great Replacement” hypothesis using standard demographic modeling. We implement a reproducible aggregated cohort-component framework that includes fertility, mortality, net migration, and an explicit assimilation mechanism modeled as convergence of group-specific demographic rates. Two scenarios are analyzed: (i) an empirically plausible scenario representative of Western high-income countries, and (ii) an extreme non-empirical stress-test constructed to reflect conspiratorial assumptions (persistent large fertility gaps, sustained mass migration, and zero assimilation). Under realistic parameterization with convergence, group population shares stabilize or approach equilibrium and do not exhibit rapid monotonic majority displacement. Rapid “replacement” emerges only when multiple empirically unsupported assumptions are imposed simultaneously. These results show that the “Great Replacement” hypothesis is mathematically infeasible under realistic demographic dynamics and is not supported by standard demographic mechanisms.

---

## 1. Introduction

Claims of demographic “replacement” assert that observed population changes constitute a coordinated and intentional process leading to rapid majority displacement. Such claims imply mathematically precise conditions over long time horizons: persistent differential fertility, sustained asymmetric migration flows, and negligible intergenerational assimilation. Because these mechanisms are quantitative, they are empirically and formally testable.

Demography has long analyzed population change using cohort-component methods grounded in vital statistics, censuses, and migration estimates. This work asks whether standard demographic dynamics—fertility, mortality, migration, and intergenerational convergence—support “replacement” behavior under realistic assumptions.

---

## 2. Data Sources and Parameterization

This repository does not depend on restricted datasets; instead, it uses parameter magnitudes documented in widely used sources:

- United Nations (UN DESA) population datasets and methodological guidance for projections.
- Eurostat and OECD reporting on migration and demographic indicators in European high-income settings.
- Peer-reviewed demographic literature on fertility differentials by nativity and on second-generation convergence.

The “realistic scenario” is calibrated to typical orders of magnitude (annualized) reported for Western high-income countries: modest fertility differentials, mortality differences consistent with age-structure differences, and net migration on the order of tenths of a percent of total population. The “extreme scenario” is intentionally non-empirical and used only as a stress test.

---

## 3. Methods

### 3.1 Aggregated cohort-component dynamics

We use an annual-time-step population accounting identity for each group g:

N_g(t+1) = N_g(t) + B_g(t) − D_g(t) + M_g(t)

where:
- N_g(t) is group population size at time t,
- B_g(t) is births,
- D_g(t) is deaths,
- M_g(t) is net migration.

In the aggregated implementation, births and deaths are modeled proportionally to current population size:

B_g(t) = f_g(t) · N_g(t)  
D_g(t) = d_g(t) · N_g(t)  
M_g(t) = m_g(t) · N_g(t)

where f_g(t), d_g(t), and m_g(t) are annualized fertility, mortality, and net migration rates (respectively).

While the model is aggregated (not age-structured), it preserves the core accounting logic used in standard projections and is explicitly designed for scenario comparison rather than detailed official forecasting.

---

### 3.2 Intergenerational assimilation via rate convergence

A key empirical regularity in demographic research is that demographic behaviors often converge across generations (e.g., fertility of second and third generations approaching host-country levels). We model this with a convergence process:

f_g(t+1) = f_g(t) + λ ( f̄(t) − f_g(t) )  
d_g(t+1) = d_g(t) + λ ( d̄(t) − d_g(t) )

where:
- f̄(t) and d̄(t) are cross-group means at time t,
- λ ∈ [0,1] is a convergence (assimilation) parameter.

If λ > 0, between-group differences shrink geometrically over time. If λ = 0, differences persist indefinitely (a necessary ingredient for “replacement” narratives).

---

### 3.3 Mathematical conditions for “replacement” and infeasibility

Define the share of group A:

s_A(t) = N_A(t) / (N_A(t) + N_B(t))

A “rapid replacement” claim implicitly requires s_A(t) to decrease substantially within a few generations. In this model, sustained rapid decline requires:

1) Persistent differential growth advantage for group B:
   (f_B − d_B + m_B) − (f_A − d_A + m_A) ≫ 0 for long horizons.

2) Low or zero convergence:
   λ ≈ 0, so (f_B − f_A) and (d_B − d_A) do not shrink.

3) Sustained high net migration into group B at unrealistic levels, often multiple percent per year, with no offsetting dynamics.

Empirical literature shows that condition (2) is generally violated (λ > 0), and typical net migration magnitudes do not sustain the extreme differentials needed for rapid monotonic majority displacement. Therefore, the “replacement” outcome is mathematically fragile and requires multiple simultaneous non-empirical assumptions.

---

### 3.4 Statistical analysis of trajectories

Given simulated trajectories, we evaluate:

- Linear trend regression of s_A(t) over time:
  slope, p-value, and R².

- Estimated time to majority loss:
  if slope < 0, solve for s_A(t)=0.5 under the fitted linear model (noting limitations of linear extrapolation).

- Stationarity testing:
  Augmented Dickey–Fuller (ADF) test on s_A(t) to assess whether dynamics are consistent with mean reversion/stabilization versus persistent drift.

- Sensitivity analysis:
  grid exploration across λ and migration intensities to locate boundary regions where majority loss becomes possible.

---

## 4. Scenario Design

### 4.1 Realistic scenario (empirically plausible)

This scenario reflects typical Western high-income-country magnitudes:

- modest fertility differences,
- mortality differences reflecting age structure,
- moderate net migration,
- non-zero convergence (λ > 0).

The model’s convergence mechanism operationalizes intergenerational assimilation that is widely documented in demographic studies.

---

### 4.2 Extreme stress-test scenario (non-empirical)

This scenario is constructed to represent the *assumptions required* by conspiratorial replacement narratives:

- persistent large fertility gap,
- sustained very high net migration,
- zero convergence (λ = 0).

This scenario is not a claim about reality; it is a mathematical stress test.

---

## 5. Results

### 5.1 Realistic scenario

Under realistic assumptions with λ > 0, group shares do not show rapid monotonic collapse. Instead:

- between-group fertility and mortality differences shrink over time,
- s_A(t) approaches stabilization or slow convergence toward an equilibrium share,
- regression slopes are small and typically not consistent with “rapid replacement,” and
- stationarity tests tend to support stabilization rather than runaway drift.

Interpretation: Under empirically supported convergence, the system does not generate “replacement” as an intrinsic outcome.

---

### 5.2 Extreme stress-test scenario

Under the extreme scenario (λ = 0 plus sustained high migration and persistent fertility gaps):

- s_A(t) can cross below 50% within the modeled horizon,
- but this behavior is contingent on multiple compounded assumptions.

Interpretation: “Replacement” is not robust; it appears only under engineered, non-empirical conditions.

---

## 6. Sensitivity Analysis

Sensitivity analysis over (λ, migration intensity) shows:

- λ is a stabilizing parameter: even small λ > 0 substantially reduces or eliminates majority-loss trajectories,
- migration intensity must be simultaneously high and sustained to overcome convergence.

This provides a boundary-map interpretation: “replacement-like” trajectories exist only in a narrow region of parameter space inconsistent with observed demographic regularities.

---

## 7. Discussion

The findings demonstrate that rapid demographic “replacement” is not a generic consequence of standard demographic processes. Instead, it requires suppressing empirically supported convergence mechanisms and assuming sustained migration magnitudes far above typical high-income-country ranges.

This is a critical distinction: demographic change is real and multi-causal, but the hypothesis of rapid, intentional replacement is mathematically unstable under realistic mechanisms.

---

## 8. Limitations and Ethical/Political Considerations

### 8.1 Model limitations

- The model is aggregated (not age-structured) and thus is not intended for official forecasting.
- Migration and policy regimes can vary over time, whereas scenarios assume simplified rate structures.
- “Group” definitions are simplified; real-world identities are multi-dimensional.

These limitations do not weaken the core argument about feasibility: rapid replacement requires persistent extreme differentials plus near-zero convergence.

### 8.2 Ethical considerations

Demographic modeling can be misused in political discourse. This work evaluates mathematical feasibility under explicit assumptions and does not prescribe policy preferences. The appropriate ethical use is transparency: making assumptions explicit and subject to verification.

---

## 9. Conclusions and Actionable Implications

1) Under realistic demographic dynamics with intergenerational convergence, the “Great Replacement” hypothesis is not supported.
2) Replacement-like outcomes arise only under compounded non-empirical assumptions.
3) Public debate should shift from conspiratorial framing toward transparent, data-grounded discussions of fertility, migration, integration, and age structure.

---

## Reproducibility

All results in this repository can be reproduced using:

- python -m models.analysis  
- python scripts/generate_figures.py  
- python scripts/sensitivity_analysis.py  

Figures are located in `paper/figures/` and projection outputs in `results/`.

---

## References

- Preston, S. H., Heuveline, P., & Guillot, M. (2000). *Demography: Measuring and Modeling Population Processes*. Blackwell.
- United Nations, Department of Economic and Social Affairs (UN DESA). *World Population Prospects* (methodology and datasets).
- Coleman, D. (2006). Immigration and ethnic change in low-fertility countries: a third demographic transition. *Population and Development Review*.
- Alba, R., & Nee, V. (2003). *Remaking the American Mainstream: Assimilation and Contemporary Immigration*. Harvard University Press.
- OECD. International Migration Outlook (annual reporting series).
- Eurostat. Population and migration statistics (method definitions and indicator series).

---

## License

MIT.
