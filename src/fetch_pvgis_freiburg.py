"""Download hourly PVGIS data for Freiburg.

This script calls the European Commission JRC PVGIS 5.3 API and stores both
the raw JSON response and a tidy hourly CSV for analysis.

Run:
    python src/fetch_pvgis_freiburg.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from config import LOCATION, PV_SYSTEM

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

PVGIS_URL = "https://re.jrc.ec.europa.eu/api/v5_3/seriescalc"


def build_params() -> dict[str, Any]:
    return {
        "lat": LOCATION.latitude,
        "lon": LOCATION.longitude,
        "startyear": PV_SYSTEM.start_year,
        "endyear": PV_SYSTEM.end_year,
        "pvcalculation": 1,
        "peakpower": PV_SYSTEM.reference_capacity_kwp,
        "loss": PV_SYSTEM.system_losses_percent,
        "angle": PV_SYSTEM.tilt_degrees,
        "aspect": PV_SYSTEM.aspect_degrees,
        "outputformat": "json",
    }


def download_pvgis() -> dict[str, Any]:
    response = requests.get(PVGIS_URL, params=build_params(), timeout=60)
    response.raise_for_status()
    return response.json()


def parse_hourly(data: dict[str, Any]) -> pd.DataFrame:
    hourly = data["outputs"]["hourly"]
    df = pd.DataFrame(hourly)

    # PVGIS time format commonly appears as YYYYMMDD:HHMM.
    df["time"] = pd.to_datetime(df["time"], format="%Y%m%d:%H%M", errors="coerce")

    # P is PV system power in W for the configured peakpower.
    # For a 1 kWp reference system, hourly Wh ~= W averaged over one hour.
    df = df.rename(
        columns={
            "P": "pv_power_w",
            "G(i)": "plane_of_array_irradiance_w_m2",
            "H_sun": "solar_elevation_deg",
            "T2m": "temperature_c",
            "WS10m": "wind_speed_m_s",
        }
    )

    keep = [
        "time",
        "pv_power_w",
        "plane_of_array_irradiance_w_m2",
        "solar_elevation_deg",
        "temperature_c",
        "wind_speed_m_s",
    ]
    existing = [col for col in keep if col in df.columns]
    df = df[existing].copy()

    df["pv_energy_kwh_per_kwp"] = df["pv_power_w"] / 1000.0
    df["month"] = df["time"].dt.month
    return df


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    data = download_pvgis()

    raw_path = RAW_DIR / "pvgis_freiburg_hourly.json"
    raw_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    df = parse_hourly(data)
    processed_path = PROCESSED_DIR / "freiburg_pv_hourly.csv"
    df.to_csv(processed_path, index=False)

    print(f"Saved raw PVGIS response to: {raw_path}")
    print(f"Saved tidy hourly data to: {processed_path}")
    print(f"Rows: {len(df):,}")


if __name__ == "__main__":
    main()
