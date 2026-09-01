# Demand Planning Consolidation

A recreation of a real problem I solved during a supply chain analytics role: each season, roughly 20 regional demand planners submitted forecast data independently, in whatever format and layout they happened to export, and someone had to turn that into one clean, usable dataset before planning could move forward.

The original version of this ran in Alteryx against real company data, so it isn't something I can publish. This version rebuilds the same logic in Python against synthetic data, so the approach is visible and the code can actually be reviewed.

## The problem

20 planners, 20 spreadsheets, only partially shared format:

- Column order differs from file to file
- Dates show up in at least three different formats
- Some rows are missing forecast values
- A handful of duplicate submissions show up every cycle
- Spelling errors / mismatches (Brazil - Brasil etc)

Manually reconciling this by hand was the previous process. Automating it saved an estimated 40+ hours of manual data entry per quarter.

## What's here

- `generate_sample_data.py` — generates 20 intentionally messy CSVs that mimic the real submission problem (synthetic data only)
- `consolidate.py` — standardizes columns, parses mixed date formats, flags missing values, drops duplicates, and writes one clean dataset

## Running it

```bash
pip install pandas
python generate_sample_data.py   # writes ./raw_submissions/
python consolidate.py            # writes ./consolidated_forecast.csv
```

Example output:

```
Consolidated 20 planner submissions -> consolidated_forecast.csv
  Rows in:              485
  Duplicate rows dropped: 11
  Rows with missing forecast_units: 50
  Rows with unparseable submit_date: 0
  Final row count:      474
```

## Tools

Python, pandas
