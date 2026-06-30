"""Configuration for the Freiburg Municipal Solar Potential Screening project."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LocationConfig:
    city: str = "Freiburg im Breisgau"
    country: str = "Germany"
    latitude: float = 47.9990
    longitude: float = 7.8421


@dataclass(frozen=True)
class PVSystemConfig:
    reference_capacity_kwp: float = 1.0
    tilt_degrees: int = 35
    # PVGIS aspect: 0 = south-facing, -90 = east, 90 = west
    aspect_degrees: int = 0
    system_losses_percent: float = 14.0
    start_year: int = 2023
    end_year: int = 2023


@dataclass(frozen=True)
class ScenarioConfig:
    # Example municipal deployment packages.
    capacities_kwp: tuple[int, ...] = (100, 500, 1000)
    # Conservative reporting factor; adjust to match the municipality/reporting standard.
    grid_emission_factor_kg_co2_per_kwh: float = 0.38


LOCATION = LocationConfig()
PV_SYSTEM = PVSystemConfig()
SCENARIOS = ScenarioConfig()
