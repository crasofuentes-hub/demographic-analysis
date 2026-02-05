from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class CohortComponentModel:
    """Modelo simplificado tipo cohorte-componente (agregado por grupo).

    Nota metodológica:
    - Este modelo trabaja con tasas anuales efectivas per cápita por grupo.
    - No modela estructura por edad explícita (agregado). Es adecuado para
      experimentos reproducibles y comparación de escenarios bajo supuestos controlados.
    """

    initial_population: dict[str, float]
    fertility_rates: dict[str, float]  # tasa anual efectiva per cápita (aprox)
    mortality_rates: dict[str, float]  # tasa anual de mortalidad
    migration_rates: dict[str, float]  # tasa anual neta (puede ser negativa)

    def project(
        self, years: int, start_year: int = 2023, convergence_rate: float = 0.02
    ) -> pd.DataFrame:
        results = []
        current = self.initial_population.copy()
        fert = self.fertility_rates.copy()
        mort = self.mortality_rates.copy()

        groups = list(current.keys())

        for t in range(years + 1):
            total = float(sum(current.values()))
            row = {
                "year": start_year + t,
                **{g: float(current[g]) for g in groups},
                "total_population": total,
            }
            results.append(row)

            births = {g: current[g] * fert[g] for g in groups}
            deaths = {g: current[g] * mort[g] for g in groups}
            mig = {g: current[g] * self.migration_rates[g] for g in groups}

            nxt = {}
            for g in groups:
                nxt[g] = current[g] + births[g] - deaths[g] + mig[g]

            # Convergencia (asimilación): fecundidad y mortalidad convergen hacia la media entre grupos
            if t > 0 and convergence_rate > 0:
                fert_mean = float(np.mean([fert[g] for g in groups]))
                mort_mean = float(np.mean([mort[g] for g in groups]))
                for g in groups:
                    fert[g] -= (fert[g] - fert_mean) * convergence_rate
                    mort[g] -= (mort[g] - mort_mean) * convergence_rate

            current = nxt

        return pd.DataFrame(results)
