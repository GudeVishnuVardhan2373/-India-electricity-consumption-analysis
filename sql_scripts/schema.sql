-- =====================================================================
-- TABLE: state_electricity_consumption
-- PURPOSE: Stores the raw daily/monthly electricity usage data across Indian states
-- =====================================================================

CREATE TABLE state_electricity_consumption (
    state_name VARCHAR(100) NOT NULL,
    region VARCHAR(50),
    reading_date DATE NOT NULL,
    usage_mwh NUMERIC(12, 2), -- Electricity consumption in MegaWatt-hours
    latitude NUMERIC(9, 6),   -- For geographic mapping in Tableau
    longitude NUMERIC(9, 6)   -- For geographic mapping in Tableau
)
