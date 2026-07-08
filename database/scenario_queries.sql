-- ============================================================
-- Scenario queries — run against vw_consumption_full
-- (created by schema.sql / load_data.py)
-- ============================================================

-- ------------------------------------------------------------
-- SCENARIO 1: Change in Overall Consumption Trends (Jan 2019–Dec 2020)
-- Month-by-month national total, so trend/seasonality/lockdown dip is visible
-- ------------------------------------------------------------
SELECT
    usage_year,
    usage_month,
    ROUND(SUM(usage_mu), 1) AS total_usage_mu
FROM vw_consumption_full
GROUP BY usage_year, usage_month
ORDER BY usage_year, usage_month;

-- Year-over-year comparison for the same month (e.g. lockdown months vs 2019)
SELECT
    usage_month,
    ROUND(SUM(CASE WHEN usage_year = '2019' THEN usage_mu END), 1) AS total_2019,
    ROUND(SUM(CASE WHEN usage_year = '2020' THEN usage_mu END), 1) AS total_2020
FROM vw_consumption_full
GROUP BY usage_month
ORDER BY usage_month;


-- ------------------------------------------------------------
-- SCENARIO 2: Regional Variations in Demand
-- Total & average daily consumption by region, Jan 2019–Dec 2020
-- ------------------------------------------------------------
SELECT
    region_name,
    ROUND(SUM(usage_mu), 1)              AS total_usage_mu,
    ROUND(AVG(usage_mu), 2)              AS avg_daily_usage_mu,
    COUNT(DISTINCT state_name)           AS num_states
FROM vw_consumption_full
GROUP BY region_name
ORDER BY total_usage_mu DESC;

-- Region trend by month (for a region-over-time line chart)
SELECT
    region_name,
    usage_year,
    usage_month,
    ROUND(SUM(usage_mu), 1) AS total_usage_mu
FROM vw_consumption_full
GROUP BY region_name, usage_year, usage_month
ORDER BY region_name, usage_year, usage_month;


-- ------------------------------------------------------------
-- SCENARIO 3: Recovery After Lockdown (pre-lockdown Feb 2020 baseline
-- vs. mid-2020 -> end-2020 recovery, per state)
-- ------------------------------------------------------------
WITH baseline AS (
    SELECT state_name, AVG(usage_mu) AS pre_lockdown_avg
    FROM vw_consumption_full
    WHERE usage_date BETWEEN '2020-02-01' AND '2020-02-29'
    GROUP BY state_name
),
recovery AS (
    SELECT state_name, usage_month, AVG(usage_mu) AS avg_usage_mu
    FROM vw_consumption_full
    WHERE usage_date BETWEEN '2020-07-01' AND '2020-12-05'
    GROUP BY state_name, usage_month
)
SELECT
    r.state_name,
    r.usage_month,
    ROUND(r.avg_usage_mu, 2)                                   AS avg_usage_mu,
    ROUND(b.pre_lockdown_avg, 2)                                AS pre_lockdown_avg,
    ROUND(100.0 * r.avg_usage_mu / b.pre_lockdown_avg, 1)       AS pct_of_pre_lockdown
FROM recovery r
JOIN baseline b ON r.state_name = b.state_name
ORDER BY r.state_name, r.usage_month;

-- Simple lockdown-period dip check (Mar–Jun 2020 vs Jan–Feb 2020 baseline)
SELECT
    state_name,
    ROUND(AVG(CASE WHEN usage_date BETWEEN '2020-01-01' AND '2020-02-29' THEN usage_mu END), 2) AS pre_lockdown_avg,
    ROUND(AVG(CASE WHEN usage_date BETWEEN '2020-03-25' AND '2020-06-30' THEN usage_mu END), 2) AS lockdown_avg,
    ROUND(AVG(CASE WHEN usage_date BETWEEN '2020-07-01' AND '2020-12-05' THEN usage_mu END), 2) AS post_lockdown_avg
FROM vw_consumption_full
GROUP BY state_name
ORDER BY state_name;


-- ============================================================
-- Connecting this DB to Tableau (Step 1: "Connect DB with Tableau")
-- ============================================================
-- SQLite (from load_data.py default):
--   Tableau doesn't have a native SQLite connector. Easiest paths:
--     a) Install the free "SQLite ODBC Driver" + Tableau's "Other Databases (ODBC)" connector, or
--     b) Skip SQLite for the live project and point ENGINE_URL in load_data.py at MySQL/PostgreSQL,
--        which Tableau connects to natively (Connect > MySQL / PostgreSQL, host/port/user/pass).
--   Either way, connect to the `vw_consumption_full` view — it's already a flat,
--   denormalized table so Tableau doesn't need to do the joins itself.
