-- =====================================================================
-- SCENARIO 1: Overall Monthly National Consumption Trends (2019-2020)
-- PURPOSE: Tracks month-over-month national demand fluctuations
-- =====================================================================
CREATE VIEW v_scenario1_overall_trends AS
SELECT 
    EXTRACT(YEAR FROM reading_date) AS trend_year,
    EXTRACT(MONTH FROM reading_date) AS trend_month,
    SUM(usage_mwh) AS total_national_usage,
    ROUND(AVG(usage_mwh), 2) AS daily_average_usage,
    COUNT(DISTINCT state_name) AS active_reporting_states
FROM 
    state_electricity_consumption
GROUP BY 1, 2;


-- =====================================================================
-- SCENARIO 2: Regional Variations in Demand
-- PURPOSE: Highlights demand disparities across the 5 major Indian regions
-- =====================================================================
CREATE VIEW v_scenario2_regional_demand AS
SELECT 
    region,
    EXTRACT(YEAR FROM reading_date) AS trend_year,
    EXTRACT(MONTH FROM reading_date) AS trend_month,
    SUM(usage_mwh) AS total_regional_usage,
    ROUND(AVG(usage_mwh), 2) AS avg_state_usage,
    AVG(latitude) AS center_lat,  -- Averages the coordinates to place regional bubbles on maps
    AVG(longitude) AS center_lon
FROM 
    state_electricity_consumption
GROUP BY 1, 2, 3;


-- =====================================================================
-- SCENARIO 3: Post-Lockdown Economic Recovery Timeline
-- PURPOSE: Analyzes the pre-lockdown, lockdown, and recovery phases
-- =====================================================================
CREATE VIEW v_scenario3_lockdown_recovery AS
SELECT 
    state_name,
    region,
    CASE 
        -- Pre-lockdown operational baseline (Jan 2019 to March 24, 2020)
        WHEN reading_date < '2020-03-25' THEN '1 - Pre-Lockdown Baseline'
        -- Hard nationwide lockdown window (March 25 - June 30, 2020)
        WHEN reading_date BETWEEN '2020-03-25' AND '2020-06-30' THEN '2 - Lockdown Period'
        -- Unlocking & recovery economic phases (July 2020 onwards)
        ELSE '3 - Post-Lockdown Recovery'
    END AS economic_phase,
    SUM(usage_mwh) AS total_phase_usage,
    ROUND(AVG(usage_mwh), 2) AS daily_avg_consumption,
    MIN(reading_date) AS phase_start,
    MAX(reading_date) AS phase_end
FROM 
    state_electricity_consumption
WHERE 
    reading_date >= '2019-01-01'
GROUP BY 1, 2, 3;
