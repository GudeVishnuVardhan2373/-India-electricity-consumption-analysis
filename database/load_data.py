"""
load_data.py
------------
Loads ../data/Consumption.csv into the normalized schema (regions / states / consumption).

Default target: SQLite file `consumption.db` in this same folder (zero setup).

To point at MySQL or PostgreSQL instead, install the driver and change
ENGINE_URL below, e.g.:
    MySQL:      mysql+pymysql://user:password@localhost:3306/consumption_db
    PostgreSQL: postgresql+psycopg2://user:password@localhost:5432/consumption_db

Usage:
    pip install pandas sqlalchemy --break-system-packages
    python load_data.py
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "..", "data", "Consumption.csv")
ENGINE_URL = "sqlite:///" + os.path.join(BASE_DIR, "consumption.db")

REGION_NAMES = {
    "NR": "Northern Region",
    "WR": "Western Region",
    "SR": "Southern Region",
    "ER": "Eastern Region",
    "NER": "North Eastern Region",
}


def main():
    engine = create_engine(ENGINE_URL)

    # ---- 1. Read & clean the raw CSV -------------------------------------
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.strip() for c in df.columns]
    df["Dates"] = pd.to_datetime(df["Dates"], format="%d/%m/%Y")
    df["Usage"] = pd.to_numeric(df["Usage"], errors="coerce")
    df = df.dropna(subset=["Usage"])

    # ---- 2. Build the regions table --------------------------------------
    regions_df = pd.DataFrame(
        [{"region_code": k, "region_name": v} for k, v in REGION_NAMES.items()]
    )
    regions_df.to_sql("regions", engine, if_exists="replace", index=False)

    # ---- 3. Build the states dimension table -------------------------------
    states_df = (
        df[["States", "Regions", "latitude", "longitude"]]
        .drop_duplicates(subset=["States"])
        .rename(columns={"States": "state_name", "Regions": "region_code"})
        .reset_index(drop=True)
    )
    states_df.insert(0, "state_id", states_df.index + 1)
    states_df.to_sql("states", engine, if_exists="replace", index=False)

    # ---- 4. Build the consumption fact table -------------------------------
    state_lookup = dict(zip(states_df["state_name"], states_df["state_id"]))
    fact_df = pd.DataFrame(
        {
            "state_id": df["States"].map(state_lookup),
            "usage_date": df["Dates"].dt.date,
            "usage_mu": df["Usage"],
        }
    )
    fact_df.insert(0, "consumption_id", range(1, len(fact_df) + 1))
    fact_df.to_sql("consumption", engine, if_exists="replace", index=False)

    # ---- 5. Add indexes + flat view for Tableau -----------------------------
    with engine.begin() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_consumption_date ON consumption(usage_date)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_consumption_state_date ON consumption(state_id, usage_date)"))
        conn.execute(text("DROP VIEW IF EXISTS vw_consumption_full"))
        conn.execute(
            text(
                """
                CREATE VIEW vw_consumption_full AS
                SELECT
                    c.consumption_id,
                    s.state_name,
                    s.region_code,
                    r.region_name,
                    s.latitude,
                    s.longitude,
                    c.usage_date,
                    strftime('%Y', c.usage_date) AS usage_year,
                    strftime('%m', c.usage_date) AS usage_month,
                    c.usage_mu
                FROM consumption c
                JOIN states s ON c.state_id = s.state_id
                JOIN regions r ON s.region_code = r.region_code
                """
            )
        )

    print(f"Loaded {len(regions_df)} regions, {len(states_df)} states, {len(fact_df)} consumption rows")
    print(f"Database written to {ENGINE_URL}")


if __name__ == "__main__":
    main()
