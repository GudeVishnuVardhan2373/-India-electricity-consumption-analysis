# India Electricity Consumption Analysis — Project Documentation

## Problem Statement
Electricity is a vital driver of economic activity, reflecting both industrial
productivity and household energy access. This project analyzes state-wise
electricity consumption across India from January 2019 to December 5, 2020 —
a period spanning the COVID-19 pandemic and nationwide lockdown (March–June
2020) — to understand regional and national energy demand patterns and how
they shifted during and after the lockdown.

## Scenarios Covered
1. **Change in Overall Consumption Trends** — how national electricity usage
   shifted month-by-month across 2019–2020, including the lockdown dip.
2. **Regional Variations in Demand** — how Northern, Southern, Eastern,
   Western, and North-Eastern regions differed in consumption levels.
3. **Recovery After Lockdown** — how quickly different states returned to
   (or exceeded) pre-lockdown consumption levels between mid- and late 2020.

---

## Step 1: Data Collection & Extraction from Database

- **Dataset**: `data/Consumption.csv` — 16,599 rows, daily electricity usage
  (in Million Units) for 33 Indian states/UTs, tagged with region and
  lat/long, from 2 Jan 2019 to 5 Dec 2020.
- **Database schema**: `database/schema.sql` normalizes the raw CSV into
  three tables:
  - `regions` (region_code, region_name)
  - `states` (state_id, state_name, region_code FK, latitude, longitude)
  - `consumption` (consumption_id, state_id FK, usage_date, usage_mu)
  - plus a flat `vw_consumption_full` view joining all three, for easy
    Tableau connection.
- **Loading**: `database/load_data.py` reads the CSV, cleans it (parses
  dates, coerces numeric usage, drops bad rows), and populates all tables.
  Defaults to a local SQLite file (`consumption.db`); swap the `ENGINE_URL`
  to point at MySQL or PostgreSQL for a shared/server database.
- **SQL operations**: `database/scenario_queries.sql` contains the queries
  used to answer each scenario (monthly trend, regional totals, lockdown
  recovery %).
- **Connect DB to Tableau**:
  - SQLite: install the SQLite ODBC driver and use Tableau's "Other
    Databases (ODBC)" connector, OR
  - MySQL/PostgreSQL: use Tableau's native connector (Connect > MySQL /
    PostgreSQL, enter host/port/user/password).
  - In both cases, connect to `vw_consumption_full` — it's already flat, so
    Tableau doesn't need to redo the joins.

## Step 2: Data Preparation

- Set `usage_date` as a Date field in Tableau; confirm `usage_mu` is a
  numeric measure.
- Suggested calculated fields:
  - `Lockdown Period` (boolean): `[usage_date] >= #2020-03-25# AND [usage_date] <= #2020-06-30#`
  - `% of Pre-Lockdown Usage`: usage_mu / pre-lockdown average, by state
  - `YoY Change`: current month total vs. same month prior year
- `analysis/eda.py` runs the same logic in Python first (matplotlib charts +
  CSVs in `analysis/output/`) as a fast sanity check before building the
  same views in Tableau.

## Step 3: Data Visualization

Recommended unique visualizations (one per scenario minimum, mix of types):
- Line chart: national monthly usage, 2019 vs 2020 (Scenario 1)
- Bar chart / filled map: total usage by region (Scenario 2)
- Multi-line chart: regional usage trend over time (Scenario 2)
- Horizontal bar chart: % of pre-lockdown usage recovered, by state
  (Scenario 3)
- Heatmap: state x month usage intensity (bonus, ties scenarios together)

## Step 4: Dashboard

- Combine the Scenario 1–3 visualizations into one dashboard (or one per
  scenario, linked via a navigation dashboard).
- Add filters: Region, State, Date Range.
- Use Tableau's Device Designer to create phone/tablet/desktop layouts for
  responsiveness.

## Step 5: Story

- Use Tableau's Story feature to sequence the 3 scenarios as scenes:
  1. Overall trend (with a caption calling out the lockdown dip)
  2. Regional comparison (caption on which region held up best/worst)
  3. Recovery (caption on fastest/slowest recovering states)
- Aim for at least 3–5 scenes so the narrative has room to build.

## Step 6: Performance Testing

- **Amount of data rendered**: ~16.6K rows total; using an extract (rather
  than a live DB connection) in Tableau keeps dashboard load fast for a
  static historical dataset like this.
- **Filters**: confirm filters are context filters where appropriate, so
  they reduce the underlying query rather than just hiding marks.
- **Calculated fields**: document how many you created (see Step 2).
- **Visualizations/graphs**: document the total count across dashboard +
  story (see Step 3 list — track this number for your submission).

## Step 7: Web Integration

- Publish the finished dashboard and story to Tableau Public
  (or Tableau Server, if available).
- `webapp/app.py` is a minimal Flask app that embeds both via iframe:
  - `/` — project overview
  - `/dashboard` — embedded Tableau dashboard
  - `/story` — embedded Tableau story
- After publishing, copy each view's Tableau Public URL into
  `DASHBOARD_URL` / `STORY_URL` in `app.py`.
- Run with `python app.py` and visit `http://localhost:5000`.

## Step 8: Project Demonstration & Documentation

- **Video**: record a screen-share walking through: problem statement →
  DB/ETL → Tableau dashboard → story → Flask site, in that order.
- **Documentation**: this file. Update it with final screenshots, the exact
  count of calculated fields/visualizations you ended up with, and any
  deviations from this plan once the Tableau build is done.

---

## Folder Structure
```
project/
├── data/
│   └── Consumption.csv          # raw dataset
├── database/
│   ├── schema.sql                # table + view definitions
│   ├── load_data.py               # ETL script (CSV -> DB)
│   ├── scenario_queries.sql       # SQL for all 3 scenarios
│   └── consumption.db             # generated SQLite DB (after running load_data.py)
├── analysis/
│   ├── eda.py                     # Python sanity-check charts
│   └── output/                    # generated PNGs + CSVs
├── webapp/
│   ├── app.py                     # Flask app
│   └── templates/                 # base.html, index.html, dashboard.html, story.html
└── docs/
    └── documentation.md           # this file
```

## How to Run End-to-End
```bash
# 1. Load the database
cd database
pip install pandas sqlalchemy --break-system-packages
python load_data.py

# 2. (Optional) run the Python sanity-check analysis
cd ../analysis
pip install pandas matplotlib --break-system-packages
python eda.py

# 3. Build dashboard + story in Tableau, connected to database/consumption.db
#    (via vw_consumption_full), then publish to Tableau Public.

# 4. Update webapp/app.py with your published embed URLs, then:
cd ../webapp
pip install flask --break-system-packages
python app.py
# visit http://localhost:5000
```
