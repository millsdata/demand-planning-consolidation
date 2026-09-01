"""
Generates 21 messy, inconsistent CSV files, one per "demand planner," to
stand in for the kind of raw regional submissions that show up in real
seasonal planning cycles: different column orders, different date formats,
missing values, and a few duplicate rows.

This is synthetic data. It exists to demonstrate the consolidation pattern
below, not to represent any real company's actual planning data.

Usage:
    python generate_sample_data.py
"""

import os
import random
from datetime import datetime, timedelta

import pandas as pd

random.seed(42)

OUTPUT_DIR = "raw_submissions"
NUM_PLANNERS = 20
REGIONS = [
    "North", "South", "East", "West", "Central", "Pacific", "Mountain",
    "Gulf", "Great Lakes", "Northeast", "Southeast", "Southwest",
]
PRODUCT_LINES = ["Footwear", "Apparel", "Accessories", "Equipment"]
DATE_FORMATS = ["%Y-%m-%d", "%m/%d/%Y", "%d-%b-%Y"]
COLUMN_ORDERS = [
    ["planner_id", "region", "product_line", "forecast_units", "submit_date"],
    ["region", "planner_id", "submit_date", "product_line", "forecast_units"],
    ["submit_date", "planner_id", "region", "forecast_units", "product_line"],
]


def random_date():
    start = datetime(2026, 1, 1)
    return start + timedelta(days=random.randint(0, 60))


def build_planner_file(planner_id):
    rows = []
    num_rows = random.randint(15, 30)
    for _ in range(num_rows):
        rows.append({
            "planner_id": f"P{planner_id:03d}",
            "region": random.choice(REGIONS),
            "product_line": random.choice(PRODUCT_LINES),
            "forecast_units": random.randint(500, 20000) if random.random() > 0.12 else None,
            "submit_date": random_date(),
        })

    # Introduce a duplicate row here and there, same as real submissions
    if random.random() < 0.4:
        rows.append(dict(rows[random.randint(0, len(rows) - 1)]))

    df = pd.DataFrame(rows)

    # Randomize date formatting per planner, since in practice every
    # planner exports from whatever tool or locale they're used to
    fmt = random.choice(DATE_FORMATS)
    df["submit_date"] = df["submit_date"].apply(lambda d: d.strftime(fmt))

    # Randomize column order per planner
    df = df[random.choice(COLUMN_ORDERS)]

    return df


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for planner_id in range(1, NUM_PLANNERS + 1):
        df = build_planner_file(planner_id)
        path = os.path.join(OUTPUT_DIR, f"planner_{planner_id:03d}_submission.csv")
        df.to_csv(path, index=False)
    print(f"Wrote {NUM_PLANNERS} raw submission files to ./{OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
