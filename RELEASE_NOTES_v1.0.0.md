## v1.0.0 — Publication-ready release

This release provides a reproducible demographic modeling framework (aggregated cohort-component dynamics with explicit intergenerational convergence) plus an extreme stress-test scenario.

### Included
- Peer-review manuscript: paper/manuscript.md
- Supplementary materials: paper/supplementary.md
- Submission figures (300 DPI): paper/figures/*.png
- Reproducible pipeline:
  - python -m models.analysis
  - python scripts/generate_figures.py
  - (optional) python scripts/sensitivity_analysis.py

### Key artifacts
- Figures:
  - population_realistic.png
  - proportion_group_a_realistic.png
  - population_extreme.png
  - proportion_group_a_extreme.png
- Data outputs:
  - projections_*.csv, indicators_*.csv, statistical_tests.json

### Assets
- paper-package-v1.0.0.zip (paper package)
- results-v1.0.0.zip (results package)
