CREATE TABLE operator_gas_station (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE gas_station (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coords TEXT NOT NULL,
    ai92 REAL,
    ai95 REAL,
    ai98 REAL,
    ai100 REAL,
    diesel REAL,
    gas_propane REAL,
    gas_methane REAL,
    operator_gas_station_id INTEGER,
    FOREIGN KEY (operator_gas_station_id) REFERENCES operator_gas_station(id) ON DELETE SET NULL
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,  -- SQLite не поддерживает CHAR(1) явно
    avatar TEXT
);

CREATE TABLE auto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    generation TEXT NOT NULL,
    engine TEXT NOT NULL,
    engine_capacity REAL NOT NULL,
    fuel_type TEXT NOT NULL,
    fuel_consumption REAL NOT NULL,
    fuel_tank_capacity INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE TABLE favorite_route (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    point_departure TEXT NOT NULL,
    point_arrival TEXT NOT NULL,
    travel_time TEXT NOT NULL,
    route_length REAL NOT NULL,
    fuel_type TEXT NOT NULL,
    fuel_volume REAL NOT NULL,
    fuel_cost REAL NOT NULL,
    date INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    operator_gas_station_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (operator_gas_station_id) REFERENCES operator_gas_station(id) ON DELETE SET NULL
);

CREATE TABLE brand (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE model (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand_id INTEGER NOT NULL,
    FOREIGN KEY (brand_id) REFERENCES brand(id) ON DELETE CASCADE
);

CREATE TABLE generation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    model_id INTEGER NOT NULL,
    FOREIGN KEY (model_id) REFERENCES model(id) ON DELETE CASCADE
);

CREATE TABLE engine (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    engine_capacity REAL NOT NULL,
    fuel_consumption REAL NOT NULL,
    generation_id INTEGER NOT NULL,
    FOREIGN KEY (generation_id) REFERENCES generation(id) ON DELETE CASCADE
);

CREATE TABLE city (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    coords TEXT NOT NULL
);

CREATE TABLE map_route (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_city_id INTEGER NOT NULL,
    finish_sity_id INTEGER NOT NULL,
    route_data TEXT NOT NULL,
    route_length INTEGER NOT NULL,
    FOREIGN KEY (start_city_id) REFERENCES city(id) ON DELETE CASCADE,
    FOREIGN KEY (finish_sity_id) REFERENCES city(id) ON DELETE CASCADE
);
