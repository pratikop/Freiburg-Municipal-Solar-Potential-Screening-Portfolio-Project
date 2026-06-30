# Data Sources

## PVGIS

European Commission Joint Research Centre (JRC), Photovoltaic Geographical Information System (PVGIS).

The project uses the PVGIS 5.3 non-interactive API endpoint:

```text
https://re.jrc.ec.europa.eu
```

The API is called from `src/fetch_pvgis_freiburg.py`.

PVGIS provides solar radiation and photovoltaic system performance information for most global locations and supports non-interactive API calls for tools including `seriescalc`.

## Important note

Raw PVGIS JSON and processed CSV outputs are generated locally when the scripts are run. They are intentionally excluded from Git by `.gitignore`.
