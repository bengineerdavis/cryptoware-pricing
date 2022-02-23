CREATE TABLE merchant (
    id INTEGER,
    merchant VARCHAR(128),
    PRIMARY KEY(id)
); 

CREATE TABLE ram_prod (
    id SERIAL,
    manufacturer VARCHAR(128),
    ram_name VARCHAR(128),
    memory_type VARCHAR(128),
    speed DOUBLE PRECISION,
    capacity DOUBLE PRECISION,
    PRIMARY KEY(id)
); 

CREATE TABLE time (
    id DOUBLE PRECISION,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    week INTEGER,
    PRIMARY KEY(id)
); 

CREATE TABLE region (
    id INTEGER,
    code VARCHAR(128),
    currency VARCHAR(128),
    PRIMARY KEY(id)
); 

CREATE TABLE cpu_prod (
    id INTEGER,
    manufacturer VARCHAR(128),
    series VARCHAR(128),
    cpu_name VARCHAR(128),
    cores INTEGER,
    socket VARCHAR(128),
    PRIMARY KEY(id)
);

CREATE TABLE crypto_data (
    id SERIAL,
    code VARCHAR(128) UNIQUE,
    currency_name VARCHAR(128),
    is_mineable BOOLEAN NOT NULL,
    PRIMARY KEY(id)
); 

CREATE TABLE gpu_prod (
    id SERIAL,
    processor_manufacturer VARCHAR(128),
    processor VARCHAR(128),
    gpu_manufacturer VARCHAR(128),
    memory_capacity DOUBLE PRECISION,
    memory_type VARCHAR(128),
    PRIMARY KEY(id)
); 

CREATE TABLE cpu_price (
    id SERIAL,
    cpu_prod_id INTEGER REFERENCES cpu_prod(id) ON DELETE CASCADE,
    time_id INTEGER REFERENCES time(id) ON DELETE CASCADE,
    region_id INTEGER REFERENCES region(id) ON DELETE CASCADE,
    merchant_id INTEGER REFERENCES merchant(id) ON DELETE CASCADE,
    price_usd NUMERIC(20,2),
    price_original NUMERIC(20,2),
    PRIMARY KEY(id)
); 

CREATE TABLE ram_price (
    id SERIAL,
    ram_prod_id INTEGER REFERENCES ram_prod(id) ON DELETE CASCADE,
    time_id INTEGER REFERENCES time(id) ON DELETE CASCADE,
    region_id INTEGER REFERENCES region(id) ON DELETE CASCADE,
    merchant_id INTEGER REFERENCES merchant(id) ON DELETE CASCADE,
    price_usd NUMERIC(20,2),
    price_original NUMERIC(20,2),
    PRIMARY KEY(id)
); 

CREATE TABLE gpu_price (
    id SERIAL,
    gpu_prod_id INTEGER REFERENCES gpu_prod(id) ON DELETE CASCADE,
    time_id INTEGER REFERENCES time(id) ON DELETE CASCADE,
    region_id INTEGER REFERENCES region(id) ON DELETE CASCADE,
    merchant_id INTEGER REFERENCES merchant(id) ON DELETE CASCADE,
    price_usd NUMERIC(20,2),
    price_original NUMERIC(20,2),
    PRIMARY KEY(id)
); 

CREATE TABLE crypto_rate (
    id SERIAL,
    crypto_data_code_id VARCHAR(128) REFERENCES crypto_data(code) ON DELETE CASCADE,
    time_id DOUBLE PRECISION REFERENCES time(id) ON DELETE CASCADE,
    open NUMERIC(20,2),
    close NUMERIC(20,2),
    high NUMERIC(20,2),
    low NUMERIC(20,2),
    PRIMARY KEY(id)
); 

\copy merchant(id,merchant) FROM 'data/DIM_MERCHANT.csv' WITH DELIMITER ',' CSV HEADER;

\copy ram_prod(id,manufacturer,ram_name,memory_type,speed,capacity) FROM 'data/DIM_RAM_PROD.csv' WITH DELIMITER ',' CSV HEADER;

\copy time(id,year,month,day,week) FROM 'data/DIM_TIME.csv' WITH DELIMITER ',' CSV HEADER;

\copy region(id,code,currency) FROM 'data/DIM_REGION.csv' WITH DELIMITER ',' CSV HEADER;

\copy cpu_prod(id,manufacturer,series,cpu_name,cores,socket) FROM 'data/DIM_CPU_PROD.csv' WITH DELIMITER ',' CSV HEADER;

\copy gpu_prod(id,processor_manufacturer,processor,gpu_manufacturer,memory_capacity,memory_type) FROM 'data/DIM_GPU_PROD.csv' WITH DELIMITER ',' CSV HEADER;

\copy crypto_data(id,code,currency_name,is_mineable) FROM 'data/DIM_CRYPTO_DATA.csv' WITH DELIMITER ',' CSV HEADER;

\copy cpu_price(cpu_prod_id,time_id,region_id,merchant_id,price_usd,price_original) FROM 'data/FACT_CPU_PRICE.csv' WITH DELIMITER ',' CSV HEADER;

\copy ram_price(ram_prod_id,time_id,region_id,merchant_id,price_usd,price_original) FROM 'data/FACT_RAM_PRICE.csv' WITH DELIMITER ',' CSV HEADER;

\copy gpu_price(gpu_prod_id,time_id,region_id,merchant_id,price_usd,price_original) FROM 'data/FACT_GPU_PRICE.csv' WITH DELIMITER ',' CSV HEADER;

\copy crypto_rate(crypto_data_code_id,time_id,open,close,high,low) FROM 'data/FACT_CRYPTO_RATE.csv' WITH DELIMITER ',' CSV HEADER;

