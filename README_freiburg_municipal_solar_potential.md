# Freiburg Municipal Solar Potential Screening

A compact, reproducible energy data project that estimates photovoltaic (PV) generation potential for Freiburg im Breisgau, Germany using real public solar data from the European Commission Joint Research Centre PVGIS API.

The project converts location-based PV production data into monthly generation results, simple rooftop deployment scenarios, estimated CO₂ savings, and a client-style summary suitable for municipal energy planning discussions.
 
## Project Question

How much electricity could a municipal rooftop PV program in Freiburg generate, and what approximate CO₂ savings could it deliver under different deployment scenarios?

## Project Overview

This project demonstrates a small end-to-end energy planning workflow:

1. Fetch real PV production data for Freiburg using the PVGIS API.
2. Process monthly PV yield data for a 1 kWp reference system.
3. Scale the reference production to multiple municipal deployment scenarios.
4. Estimate annual electricity generation and CO₂ savings.
5. Generate charts and summary outputs for communication with non-technical stakeholders.

## Data Source

Primary data source:

- European Commission Joint Research Centre (JRC), PVGIS API
- Dataset/service: PVGIS photovoltaic performance calculation
- Location: Freiburg im Breisgau, Germany
- Default coordinates:
  - Latitude: `47.9990`
  - Longitude: `7.8421`
- PV technology assumption: crystalline silicon
- Reference system size: `1 kWp`
- Tilt angle: `35°`
- Azimuth: `0°` south-facing
- System losses: `14%`

The scripts download the data directly from PVGIS when run. Raw data can be regenerated, so it does not need to be manually collected.

## Methodology

The workflow uses a 1 kWp PV reference system from PVGIS and scales the output to larger rooftop deployment scenarios.

The analysis uses the following simplified steps:

1. Retrieve monthly PV electricity production for a 1 kWp system.
2. Calculate annual specific yield in kWh/kWp.
3. Define example municipal rooftop PV deployment scenarios.
4. Estimate annual generation for each scenario.
5. Estimate CO₂ savings using an emissions factor assumption.
6. Export processed data, figures, and a short planning summary.

This is a screening-level analysis, not a detailed engineering design. The purpose is to show how open energy data can support early-stage municipal energy transition planning.

## Example Scenarios

The project includes simple PV deployment scenarios such as:

| Scenario | Installed PV Capacity |
|---|---:|
| Small municipal pilot | 250 kWp |
| Medium rooftop program | 1,000 kWp |
| Large municipal rollout | 5,000 kWp |

The exact scenario values can be changed in the configuration file.

## Repository Structure

```text
.
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── src/
│   ├── config.py
│   ├── fetch_pvgis_freiburg.py
│   ├── analyze_solar_scenarios.py
│   └── make_client_report.py
├── data/
│   ├── raw/
│   └── processed/
├── outputs/
│   └── figures/
└── reports/
    └── client_summary.md
```

## Outputs

After running the scripts, the project generates:

- Raw PVGIS data file
- Processed monthly PV production data
- Scenario comparison table
- Monthly PV generation chart
- Scenario-level annual generation chart
- Estimated CO₂ savings chart
- Short planning summary in Markdown format

Typical output folders:

```text
data/raw/
data/processed/
outputs/figures/
reports/
```

## Requirements

Install Python 3.10 or newer.

Python packages used:

- pandas
- requests
- matplotlib

All required packages are listed in `requirements.txt`.

## Setup

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/freiburg-municipal-solar-potential.git
cd freiburg-municipal-solar-potential
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment on macOS/Linux:

```bash
source .venv/bin/activate
```

Activate the virtual environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

Run the scripts in this order:

```bash
python src/fetch_pvgis_freiburg.py
python src/analyze_solar_scenarios.py
python src/make_client_report.py
```

Then check the generated files:

```bash
ls data/raw
ls data/processed
ls outputs/figures
ls reports
```

## Configuration

Key assumptions can be adjusted in:

```text
src/config.py
```

Examples of configurable values:

- Location coordinates
- PV system size
- Tilt and azimuth
- System losses
- Scenario capacities
- CO₂ emissions factor

## Skills Demonstrated

This project demonstrates:

- Energy data analysis
- Renewable energy scenario modelling
- PV yield interpretation
- Python data processing
- API-based data collection
- Data visualization
- Technical communication
- Municipal energy transition planning support
- Reproducible project structure

## Limitations

This is a simplified screening analysis. It does not include:

- Individual rooftop geometry
- Shading analysis
- Grid connection constraints
- Hourly load matching
- Building ownership restrictions
- Detailed CAPEX/OPEX modelling
- Detailed financial feasibility analysis

For a full planning study, the analysis should be expanded with building-level rooftop data, local load profiles, grid constraints, investment costs, and stakeholder-specific planning requirements.

## Possible Extensions

Future improvements could include:

- Adding building-level rooftop datasets
- Comparing PV generation with municipal electricity demand
- Adding battery storage scenarios
- Adding economic KPIs such as CAPEX, payback period, and LCOE
- Creating a Power BI or Excel dashboard
- Adding sensitivity analysis for PV losses and emissions factors
- Extending the workflow to multiple cities

## License

This project is released under the MIT License. See `LICENSE` for details.

## Author

Pratik Prabhakar Shinde

M.Sc. Sustainable Electrical Energy Systems  
TU Dortmund University
