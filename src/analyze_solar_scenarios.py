"""Analyze Freiburg PV production scenarios.

Run after fetching PVGIS data:
    python src/analyze_solar_scenarios.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from config import LOCATION, PV_SYSTEM, SCENARIOS

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURE_DIR = ROOT / "outputs" / "figures"


def load_hourly() -> pd.DataFrame:
    path = PROCESSED_DIR / "freiburg_pv_hourly.csv"
    if not path.exists():
        raise FileNotFoundError(
            "Missing processed PVGIS file. Run: python src/fetch_pvgis_freiburg.py"
        )
    df = pd.read_csv(path, parse_dates=["time"])
    return df


def build_monthly(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby("month", as_index=False)["pv_energy_kwh_per_kwp"]
        .sum()
        .rename(columns={"pv_energy_kwh_per_kwp": "monthly_yield_kwh_per_kwp"})
    )
    monthly["city"] = LOCATION.city
    monthly["year"] = PV_SYSTEM.start_year
    return monthly


def build_scenarios(monthly: pd.DataFrame) -> pd.DataFrame:
    annual_yield = monthly["monthly_yield_kwh_per_kwp"].sum()

    rows = []
    for capacity in SCENARIOS.capacities_kwp:
        annual_generation = annual_yield * capacity
        co2_savings_kg = (
            annual_generation * SCENARIOS.grid_emission_factor_kg_co2_per_kwh
        )
        rows.append(
            {
                "scenario_capacity_kwp": capacity,
                "annual_yield_kwh_per_kwp": annual_yield,
                "annual_generation_kwh": annual_generation,
                "annual_generation_mwh": annual_generation / 1000,
                "estimated_co2_savings_tonnes": co2_savings_kg / 1000,
            }
        )
    return pd.DataFrame(rows)


def make_figures(monthly: pd.DataFrame, scenarios: pd.DataFrame) -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(monthly["month"], monthly["monthly_yield_kwh_per_kwp"])
    ax.set_title("Freiburg PV yield by month, 1 kWp reference system")
    ax.set_xlabel("Month")
    ax.set_ylabel("PV yield (kWh/kWp)")
    ax.set_xticks(range(1, 13))
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "monthly_pv_yield.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(
        scenarios["scenario_capacity_kwp"].astype(str),
        scenarios["annual_generation_mwh"],
    )
    ax.set_title("Annual PV generation by municipal deployment scenario")
    ax.set_xlabel("Installed PV capacity (kWp)")
    ax.set_ylabel("Annual generation (MWh/year)")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "scenario_annual_generation.png", dpi=160)
    plt.close(fig)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    hourly = load_hourly()
    monthly = build_monthly(hourly)
    scenarios = build_scenarios(monthly)

    monthly.to_csv(PROCESSED_DIR / "freiburg_pv_monthly.csv", index=False)
    scenarios.to_csv(PROCESSED_DIR / "freiburg_pv_scenarios.csv", index=False)
    make_figures(monthly, scenarios)

    print("Saved monthly and scenario outputs.")
    print(scenarios.to_string(index=False))


if __name__ == "__main__":
    main()
