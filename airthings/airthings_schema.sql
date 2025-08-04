-- Airthings sensor data table
CREATE TABLE airthings_readings (
    id SERIAL PRIMARY KEY,
    time BIGINT NOT NULL,  -- Unix timestamp
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- When record was inserted
    battery INTEGER,
    co2 DECIMAL(8,2),
    humidity DECIMAL(5,2),
    pm1 DECIMAL(8,2),
    pm25 DECIMAL(8,2),
    pressure DECIMAL(8,2),
    radon_short_term_avg DECIMAL(8,2),
    relay_device_type VARCHAR(50),
    rssi INTEGER,
    temp DECIMAL(5,2),
    voc DECIMAL(8,2)
);

-- Create an index on the time column for efficient time-based queries
CREATE INDEX idx_airthings_time ON airthings_readings(time);

-- Create an index on recorded_at for efficient recent data queries
CREATE INDEX idx_airthings_recorded_at ON airthings_readings(recorded_at);

-- Example INSERT statement
-- INSERT INTO airthings_readings (
--     time, battery, co2, humidity, pm1, pm25, pressure, 
--     radon_short_term_avg, relay_device_type, rssi, temp, voc
-- ) VALUES (
--     1754252821, 100, 929.0, 50.0, 5.0, 5.0, 1013.0, 
--     14.0, 'hub', 0, 23.9, 145.0
-- );
