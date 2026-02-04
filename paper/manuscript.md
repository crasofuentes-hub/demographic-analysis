---
title: "Demographic Dynamics and the Mathematical Infeasibility of the “Great Replacement” Hypothesis"
author: "Oscar Fuentes"
date: "2026-02-04"
---

## Abstract
Public discourse sometimes frames demographic change as an intentional “replacement” process. This manuscript evaluates that claim using standard demographic modeling. We implement a reproducible aggregated cohort-component simulation with explicit modeling of intergenerational assimilation via convergence of demographic rates. Two scenarios are analyzed: (i) an empirically plausible scenario representative of Western high-income countries and (ii) an extreme non-empirical stress-test constructed to reflect conspiratorial assumptions. Results show that under realistic parameterization with convergence, population shares stabilize and do not exhibit rapid majority displacement. Rapid “replacement” emerges only when multiple unrealistic assumptions are simultaneously imposed. All results are fully reproducible.

## 1. Introduction
Claims of demographic “replacement” assert that observed population changes constitute a coordinated and intentional process leading to rapid majority displacement. Such claims imply specific mathematical conditions over long time horizons and are therefore empirically and formally testable.

This work asks whether standard demographic dynamics—fertility, mortality, migration, and intergenerational assimilation—support such a hypothesis under realistic assumptions.

## 2. Methods
### 2.1 Population dynamics model
We use an aggregated cohort-component–style model with annual time steps. For each group g:

N_g(t+1) = N_g(t) + B_g(t) − D_g(t) + M_g(t)

where births, deaths, and net migration are modeled as proportional to current population size.

### 2.2 Assimilation via rate convergence
Intergenerational assimilation is modeled through convergence of group-specific fertility and mortality rates toward the cross-group mean, governed by a convergence parameter λ.

This reflects well-documented empirical regularities in demographic research on second- and third-generation populations.

### 2.3 Statistical analysis
We analyze group-share trajectories using:
- Linear trend regression (slope, p-value, R²)
- Estimated time to majority loss (if applicable)
- Augmented Dickey–Fuller test to distinguish persistent trends from mean-reverting dynamics

## 3. Scenario design
### 3.1 Realistic scenario
Parameters are chosen to reflect typical orders of magnitude observed in Western high-income countries: modest fertility differentials, moderate net migration, and non-zero convergence.

### 3.2 Extreme stress-test scenario
A deliberately non-empirical scenario imposes persistent large fertility gaps, sustained mass migration, and zero convergence. This scenario serves only as a stress test to identify conditions required for rapid majority displacement.

## 4. Results
Under realistic assumptions with convergence, group proportions do not exhibit rapid monotonic collapse. In contrast, the extreme stress-test produces majority loss only under compounded unrealistic assumptions.

## 5. Sensitivity analysis
A grid-based sensitivity analysis over convergence rate and migration intensity identifies boundary conditions under which majority loss can occur, demonstrating that convergence strongly stabilizes demographic trajectories.

## 6. Discussion
Rapid demographic “replacement” requires the simultaneous failure of multiple empirically supported mechanisms, most critically intergenerational convergence. Observed demographic systems do not satisfy these conditions.

## 7. Conclusion
Standard demographic modeling does not support the “Great Replacement” hypothesis under realistic assumptions. Apparent replacement dynamics arise only under non-empirical parameter combinations.

## Reproducibility
All results can be reproduced using:
- python -m models.analysis
- python scripts/generate_figures.py
- python scripts/sensitivity_analysis.py

## License
MIT.
