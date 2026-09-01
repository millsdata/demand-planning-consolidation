"""
Consolidates N inconsistent regional demand-planner submissions into a
single clean dataset: the same core pattern behind a 40+ hour/quarter
manual-entry reduction on a real seasonal planning cycle, rebuilt here
against synthetic data.

Handles:
    - inconsistent column order across files
    - inconsistent date formats across files
    - missing forecast values
    - duplicate submission rows

Usage:
    python generate_sample_data.py   # creates ./raw_submissions/
    python consolidate.py            # writes ./consolidated_forecast.csv
"""

import glob
import os

import pandas as pd

INPUT_DIR = "raw_submissions"
OUTPUT_PATH = "consolidated_forecast.csv"
EXPECTED_COLUMNS = ["planner_id", "region", "product_line", "forecast_units", "submit_date"]


def load_and_standardize(path):
    df = pd.read_csv(path)

    # Column order varies by planner; this just enforces the schema,
    # it doesn't care what order the source file was in.
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"{path} is missing expected columns: {missing}")
    df = df[EXPECTED_COLUMNS]

    # Dates arrive in at least 3 different formats across planners.
    # pandas' mixed-format inference handles the common cases; anything
    # it can't parse becomes NaT and gets flagged in the summary below
    # rather than silently dropped.
    df["submit_date"] = pd.to_datetime(df["submit_date"], format="mixed", errors="coerce")

    df["source_file"] = os.path.basename(path)
    return df


def main():
    files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.csv")))
    if not files:
        raise SystemExit(f"No files found in {INPUT_DIR}/. Run generate_sample_data.py first.")

    frames = [load_and_standardize(f) for f in files]
    combined = pd.concat(frames, ignore_index=True)

    before = len(combined)
    combined = combined.drop_duplicates(
        subset=["planner_id", "region", "product_line", "submit_date"]
    )
    duplicates_removed = before - len(combined)

    missing_forecast = combined["forecast_units"].isna().sum()
    unparseable_dates = combined["submit_date"].isna().sum()

    combined = combined.sort_values(["region", "product_line", "submit_date"])
    combined.to_csv(OUTPUT_PATH, index=False)

    print(f"Consolidated {len(files)} planner submissions -> {OUTPUT_PATH}")
    print(f"  Rows in:              {before}")
    print(f"  Duplicate rows dropped: {duplicates_removed}")
    print(f"  Rows with missing forecast_units: {missing_forecast}")
    print(f"  Rows with unparseable submit_date: {unparseable_dates}")
    print(f"  Final row count:      {len(combined)}")


if __name__ == "__main__":
    main()
