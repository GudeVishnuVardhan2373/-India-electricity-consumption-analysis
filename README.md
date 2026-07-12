# Plugging into the Future: India's Electricity Consumption Patterns (2019–2020)

State-wise daily electricity consumption across 33 Indian states/UTs,
analyzed for national trends, regional disparities, and the 2020 COVID-19
lockdown's impact and recovery. Built on MySQL, Tableau, and Flask.

## Folder Structure
```
india-electricity-consumption/
├── data/
│   ├── state_wise_power_consumption.csv   # raw source, 16,599 rows (has duplicates)
│   ├── electricity_consumption.csv        # clean export from MySQL, 16,434 rows
│   ├── vw_monthly_national_trend.csv      # exported view, Scenario 1
│   ├── vw_regional_demand.csv             # exported view, Scenario 2
│   └── vw_lockdown_recovery.csv           # exported view, Scenario 3
├── sql_scripts/
│   ├── schema.sql                          # table + indexes + dedup transform
│   └── aggregation.sql                     # 3 views, one per scenario
├── web_app/
│   ├── app.py                              # Flask app (reads electricity_consumption.csv -> HTML)
│   ├── requirements.txt
│   ├── .env.example                        # copy to .env, fill in your embed URL
│   ├── templates/
│   │   └── index.html                      # landing page + Tableau embed
│   └── static/                             # (reserved for future assets)
├── tableau/
│   └── README.txt                          # save your .twbx workbook here
├── .gitignore
└── README.md
```

**Why the CSVs and not a live MySQL connection from Flask:** MySQL is still where
the data is transformed (staging → dedup → views, all in `sql_scripts/`), and
it's still what Tableau connects to while you're authoring. But the Flask app
itself reads `data/electricity_consumption.csv` directly rather than opening a
live DB connection — meaning you can demo or resubmit this site anytime without
MySQL running in the background. If you'd rather have Flask prove live MySQL
connectivity too (since it's in the tech stack), that's a small add-on — ask
and it can be layered back in as a MySQL-first-CSV-fallback.

## Tech Stack
MySQL &middot; Tableau Desktop/Public &middot; Python (Flask) &middot; HTML/CSS &middot; Git

## Quick Start
See the full phase-by-phase execution guide for exact clicks and commands.
Short version:
```bash
# 1. MySQL: run schema.sql, import data/state_wise_power_consumption.csv,
#    then run aggregation.sql  (see execution guide for Workbench steps)
#    (data/electricity_consumption.csv + the 3 vw_*.csv files are already
#    exported for you -- only re-export if you rebuild the database)

# 2. Tableau: connect to electricity_db (or the CSVs above, if using
#    Tableau Public Desktop Edition), build the dashboard/story,
#    publish to Tableau Public, copy the embed URL

# 3. Flask app
cd web_app
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env         # then edit .env with your embed URL (no DB password needed)
python app.py
# visit http://127.0.0.1:5000
```

> **Security note:** an earlier version of `.env.example` in this project had
> a real database password committed into it. That's fixed in this copy
> (replaced with a placeholder) — but if the old version was ever pushed to
> GitHub, that password is in your commit history and technically exposed.
> Safest move: change your actual MySQL `app_user` password in Workbench
> (Administration → Users and Privileges) so the old leaked one is useless,
> regardless of what's in git history.

## Data Notes
- Source columns: `state, region, usage_date, usage_mwh, latitude, longitude`
- `usage_mwh` carries the source data's Million Units (MU) figures unconverted
  (1 MU = 1,000 MWh) — multiply by 1000 if you need true MWh.
- The raw source CSV has 165 rows with two conflicting usage readings for
  the same state+date (5 dates in July 2019). schema.sql loads it into a
  staging table first, then de-duplicates into the final
  `electricity_consumption` table by averaging the conflicting pair. The
  final table has 16,434 rows (33 states x 498 reported dates), verified
  total usage 1,695,001.75 (MU, i.e. `usage_mwh` summed directly — don't
  divide by 1000, that column already holds MU-scale figures despite the
  name).
