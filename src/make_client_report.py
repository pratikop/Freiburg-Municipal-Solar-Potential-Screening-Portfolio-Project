"""Generate a client-style Markdown summary from scenario outputs.

Run:
    python src/make_client_report.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from config import LOCATION, PV_SYSTEM, SCENARIOS

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
REPORTS_DIR = ROOT / "reports"


def main() -> None:
    scenario_path = PROCESSED_DIR / "freiburg_pv_scenarios.csv"
    monthly_path = PROCESSED_DIR / "freiburg_pv_monthly.csv"

    if not scenario_path.exists() or not monthly_path.exists():
        raise FileNotFoundError(
            "Missing analysis files. Run fetch and analysis scripts first."
        )

    scenarios = pd.read_csv(scenario_path)
    monthly = pd.read_csv(monthly_path)

    best_month = monthly.loc[monthly["monthly_yield_kwh_per_kwp"].idxmax()]
    annual_yield = scenarios["annual_yield_kwh_per_kwp"].iloc[0]

    scenario_table = scenarios.to_markdown(index=False, floatfmt=".1f")

    report = f"""# Client Summary: Freiburg Municipal Solar Potential Screening

## Objective

Estimate PV generation and indicative CO₂ savings for municipal rooftop PV deployment scenarios in {LOCATION.city}, {LOCATION.country}.

## Data and assumptions

- Data source: European Commission JRC PVGIS 5.3 API.
- Reference location: {LOCATION.latitude}, {LOCATION.longitude}.
- Reference system: {PV_SYSTEM.reference_capacity_kwp:.0f} kWp crystalline silicon PV.
- Tilt/orientation: {PV_SYSTEM.tilt_degrees}° tilt, south-facing.
- System losses: {PV_SYSTEM.system_losses_percent:.0f}%.
- Analysis year: {PV_SYSTEM.start_year}.
- CO₂ factor: {SCENARIOS.grid_emission_factor_kg_co2_per_kwh:.2f} kg CO₂/kWh. This is a configurable reporting assumption.

## Key result

The PVGIS-based annual yield for the reference system is approximately **{annual_yield:.1f} kWh/kWp/year**.

The highest-yield month in the dataset is **month {int(best_month["month"])}**, with **{best_month["monthly_yield_kwh_per_kwp"]:.1f} kWh/kWp**.

## Scenario results

{scenario_table}

## Interpretation for municipal planning

A small 100 kWp pilot already creates a measurable local renewable-energy contribution and can be used to validate permitting, procurement, monitoring, and public communication workflows. A 500–1,000 kWp program can be framed as a city-district package, especially when paired with rooftop screening, school/public-building prioritization, and local grid-connection review.

## Recommended next steps

1. Add building-level rooftop/cadastre data.
2. Prioritize public buildings with high daytime consumption.
3. Compare PV production against municipal load profiles.
4. Add grid-connection constraints and transformer-level hosting capacity.
5. Turn the results into a workshop-ready dashboard for local stakeholders.
"""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORTS_DIR / "client_summary.md"
    out.write_text(report, encoding="utf-8")
    print(f"Saved report to: {out}")


if __name__ == "__main__":
    main()
