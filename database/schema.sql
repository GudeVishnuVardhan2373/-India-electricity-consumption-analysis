-- ============================================================
-- Electricity Consumption Project — Database Schema
-- Works on MySQL 8+ / PostgreSQL 13+ with minor tweaks noted
-- ============================================================

DROP TABLE IF EXISTS consumption;
DROP TABLE IF EXISTS states;
DROP TABLE IF EXISTS regions;

-- ------------------------------------------------------------
-- 1. Regions dimension (NR, WR, SR, ER, NER)
-- ------------------------------------------------------------
CREATE TABLE regions (
    region_code   VARCHAR(5)   PRIMARY KEY,
    region_name   VARCHAR(50)  NOT NULL
);

INSERT INTO regions (region_code, region_name) VALUES
    ('NR',  'Northern Region'),
    ('WR',  'Western Region'),
    ('SR',  'Southern Region'),
    ('ER',  'Eastern Region'),
    ('NER', 'North Eastern Region');

-- ------------------------------------------------------------
-- 2. States dimension (33 states/UTs, each mapped to a region)
-- ------------------------------------------------------------
CREATE TABLE states (
    state_id      INT AUTO_INCREMENT PRIMARY KEY,   -- Postgres: SERIAL PRIMARY KEY
    state_name    VARCHAR(50)  NOT NULL UNIQUE,
    region_code   VARCHAR(5)   NOT NULL,
    latitude      DECIMAL(10,6),
    longitude     DECIMAL(10,6),
    CONSTRAINT fk_state_region FOREIGN KEY (region_code)
        REFERENCES regions(region_code)
);

-- ------------------------------------------------------------
-- 3. Consumption fact table (one row per state per day)
-- ------------------------------------------------------------
CREATE TABLE consumption (
    consumption_id  BIGINT AUTO_INCREMENT PRIMARY KEY, -- Postgres: BIGSERIAL PRIMARY KEY
    state_id        INT          NOT NULL,
    usage_date      DATE         NOT NULL,
    usage_mu        DECIMAL(10,2) NOT NULL,             -- Million Units
    CONSTRAINT fk_consumption_state FOREIGN KEY (state_id)
        REFERENCES states(state_id),
    CONSTRAINT uq_state_date UNIQUE (state_id, usage_date)
);

-- ------------------------------------------------------------
-- 4. Indexes for dashboard/story performance (Step 6: Performance Testing)
-- ------------------------------------------------------------
CREATE INDEX idx_consumption_date        ON consumption(usage_date);
CREATE INDEX idx_consumption_state_date  ON consumption(state_id, usage_date);
CREATE INDEX idx_states_region           ON states(region_code);

-- ------------------------------------------------------------
-- 5. Convenience view Tableau can connect to directly (one flat table)
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW vw_consumption_full AS
SELECT
    c.consumption_id,
    s.state_name,
    s.region_code,
    r.region_name,
    s.latitude,
    s.longitude,
    c.usage_date,
    YEAR(c.usage_date)  AS usage_year,      -- Postgres: EXTRACT(YEAR FROM c.usage_date)
    MONTH(c.usage_date) AS usage_month,     -- Postgres: EXTRACT(MONTH FROM c.usage_date)
    c.usage_mu
FROM consumption c
JOIN states  s ON c.state_id = s.state_id
JOIN regions r ON s.region_code = r.region_code;
