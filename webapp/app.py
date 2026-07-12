"""
app.py
------
Flask web layer for "Plugging into the Future: India's Electricity
Consumption Patterns (2019-2020)".

This reads live from the exported electricity_consumption.csv (rather than
connecting to MySQL directly) -- MySQL is still where the data lives and
gets transformed (see sql_scripts/), but the web app itself only needs the
CSV export, so it has no database dependency at runtime. That means you
can demo/submit this without MySQL running at all.
"""

import os
import csv
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "electricity_consumption.csv")


def get_csv_statistics():
    """Reads electricity_consumption.csv and computes summary stats for
    the landing page's stat strip."""
    fallback = {
        "records": "\u2014",
        "states": "\u2014",
        "total_load": "\u2014",
        "status": "CSV not found",
    }
    try:
        with open(CSV_PATH, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            total_records = 0
            unique_states = set()
            total_usage_mu = 0.0

            for row in reader:
                total_records += 1
                if row.get("state"):
                    unique_states.add(row["state"].strip())
                if row.get("usage_mwh"):
                    try:
                        total_usage_mu += float(row["usage_mwh"])
                    except ValueError:
                        continue

            if total_records == 0:
                return fallback

            # NOTE: usage_mwh already holds the source data's Million Units
            # (MU) figures unconverted (see sql_scripts/schema.sql) -- so
            # the sum below IS the MU total already. Do not divide by 1000
            # here; that would be converting an MU figure as if it were a
            # true MWh figure, which understates the total by 1000x.
            return {
                "records": f"{total_records:,}",
                "states": len(unique_states),
                "total_load": f"{total_usage_mu:,.2f} MU",
                "status": "100% CSV Extract Coverage",
            }
    except FileNotFoundError:
        print(f"[warning] CSV not found at {CSV_PATH}")
        return fallback
    except Exception as e:
        print(f"[warning] Error reading CSV file: {e}")
        return fallback


@app.route("/")
def index():
    raw_stats = get_csv_statistics()

    stats = {
        "total_records": raw_stats["records"],
        "total_states": raw_stats["states"],
        "total_load": raw_stats["total_load"],
        "status": raw_stats["status"],
    }

    tableau_url = os.getenv("TABLEAU_EMBED_URL", "")

    return render_template("index.html", stats=stats, tableau_url=tableau_url)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
