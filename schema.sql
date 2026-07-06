 CREATE TABLE state_electricity_consumption (
    state_name VARCHAR(100) NOT NULL,
    region VARCHAR(50),
    reading_date DATE NOT NULL,
    usage_mwh NUMERIC(12, 2), 
    latitude NUMERIC(9, 6),   
    longitude NUMERIC(9, 6)   
);
