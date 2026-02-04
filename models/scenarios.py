from __future__ import annotations

def realistic_scenario_model():
    """Escenario realista tipo país occidental (parametrización agregada).

    Notas:
    - Tasas expresadas como tasas anuales efectivas per cápita (aprox) para simulación.
    - La convergencia modela asimilación intergeneracional (2–3 generaciones).
    """
    return {
        "initial_population": {"group_a": 45_000_000, "group_b": 10_000_000},
        "fertility_rates":    {"group_a": 0.018, "group_b": 0.024},
        "mortality_rates":    {"group_a": 0.009, "group_b": 0.007},
        "migration_rates":    {"group_a": 0.000, "group_b": 0.005},
        "convergence_rate":   0.03,
    }

def conspiracy_scenario_model():
    """Escenario extremo (stress test) con parámetros intencionalmente no empíricos.

    Se usa para mostrar que el fenómeno tipo "reemplazo rápido" requiere supuestos
    simultáneamente irreales: fecundidad diferencial constante, migración masiva sostenida
    y ausencia total de convergencia (asimilación).
    """
    return {
        "initial_population": {"group_a": 50_000_000, "group_b": 5_000_000},
        "fertility_rates":    {"group_a": 0.010, "group_b": 0.040},
        "mortality_rates":    {"group_a": 0.012, "group_b": 0.005},
        "migration_rates":    {"group_a": -0.002, "group_b": 0.020},
        "convergence_rate":   0.00,
    }
