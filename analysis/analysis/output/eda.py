"""
eda.py
------
Quick Python-side analysis for the 3 project scenarios, using the database
built by database/load_data.py. This is NOT a replacement for the Tableau
dashboard/story (Steps 3-5) -- it's a fast sanity check so you know what
the Tableau visuals SHOULD show before you build them.

Usage:
    pip install pandas matplotlib --break-system-packages
    python eda.py
Outputs PNG charts to analysis/output/
"""

import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "consumption.db")
OUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)


def get_conn():
    return sqlite3.connect(DB_PATH)


def scenario1_overall_trend(conn):
    df = pd.read_sql(
        """
        SELECT usage_year, usage_month, SUM(usage_mu) AS total_usage
        FROM vw_consumption_full
        GROUP BY usage_year, usage_month
        ORDER BY usage_year, usage_month
        """,
        conn,
    )
    df["period"] = df["usage_year"] + "-" + df["usage_month"]
    plt.figure(figsize=(11, 5))
    plt.plot(df["period"], df["total_usage"], marker="o")
    plt.xticks(rotation=75)
    plt.title("Scenario 1: National Monthly Electricity Consumption (2019-2020)")
    plt.ylabel("Total Usage (MU)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "scenario1_overall_trend.png"))
    plt.close()
    df.to_csv(os.path.join(OUT_DIR, "scenario1_overall_trend.csv"), index=False)


def scenario2_regional_variation(conn):
    df = pd.read_sql(
        """
        SELECT region_name, usage_year, usage_month, SUM(usage_mu) AS total_usage
        FROM vw_consumption_full
        GROUP BY region_name, usage_year, usage_month
        ORDER BY region_name, usage_year, usage_month
        """,
        conn,
    )
    df["period"] = df["usage_year"] + "-" + df["usage_month"]
    plt.figure(figsize=(11, 5))
    for region, sub in df.groupby("region_name"):
        plt.plot(sub["period"], sub["total_usage"], marker="o", label=region)
    plt.xticks(rotation=75)
    plt.legend()
    plt.title("Scenario 2: Regional Electricity Consumption Trend (2019-2020)")
    plt.ylabel("Total Usage (MU)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "scenario2_regional_variation.png"))
    plt.close()
    df.to_csv(os.path.join(OUT_DIR, "scenario2_regional_variation.csv"), index=False)


def scenario3_lockdown_recovery(conn):
    df = pd.read_sql(
        """
        SELECT
            state_name,
            ROUND(AVG(CASE WHEN usage_date BETWEEN '2020-01-01' AND '2020-02-29' THEN usage_mu END), 2) AS pre_lockdown_avg,
            ROUND(AVG(CASE WHEN usage_date BETWEEN '2020-03-25' AND '2020-06-30' THEN usage_mu END), 2) AS lockdown_avg,
            ROUND(AVG(CASE WHEN usage_date BETWEEN '2020-07-01' AND '2020-12-05' THEN usage_mu END), 2) AS post_lockdown_avg
        FROM vw_consumption_full
        GROUP BY state_name
        ORDER BY state_name
        """,
        conn,
    )
    df["pct_recovered"] = (100 * df["post_lockdown_avg"] / df["pre_lockdown_avg"]).round(1)
    df_sorted = df.sort_values("pct_recovered", ascending=False)

    plt.figure(figsize=(11, 9))
    plt.barh(df_sorted["state_name"], df_sorted["pct_recovered"])
    plt.axvline(100, color="red", linestyle="--", label="Pre-lockdown level")
    plt.xlabel("% of Pre-Lockdown Average Usage")
    plt.title("Scenario 3: Post-Lockdown Recovery by State (Jul-Dec 2020)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "scenario3_lockdown_recovery.png"))
    plt.close()
    df.to_csv(os.path.join(OUT_DIR, "scenario3_lockdown_recovery.csv"), index=False)


def main():
    conn = get_conn()
    scenario1_overall_trend(conn)
    scenario2_regional_variation(conn)
    scenario3_lockdown_recovery(conn)
    conn.close()
    print(f"Charts and CSVs written to {OUT_DIR}")


if __name__ == "__main__":
    main()
