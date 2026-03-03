import pandas as pd
import os
from sqlalchemy import create_engine
from db_config import DB_CONFIG


# copy from clean.py

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")

drivers      = pd.read_csv(f"{DATA_PATH}/drivers.csv",      na_values="\\N")
constructors = pd.read_csv(f"{DATA_PATH}/constructors.csv", na_values="\\N")
races        = pd.read_csv(f"{DATA_PATH}/races.csv",        na_values="\\N")
results      = pd.read_csv(f"{DATA_PATH}/results.csv",      na_values="\\N")
lap_times    = pd.read_csv(f"{DATA_PATH}/lap_times.csv",    na_values="\\N")

# drivers
drivers = drivers.drop(columns=["url", "number", "dob"]) if "url" in drivers.columns else drivers
drivers = drivers.rename(columns={
    "driverId":  "driver_id",
    "driverRef": "driver_ref",
    "forename":  "first_name",
    "surname":   "last_name",
})

# constructors
constructors = constructors.drop(columns=["url", "constructorRef"]) if "url" in constructors.columns else constructors
constructors = constructors.rename(columns={
    "constructorId": "constructor_id",
    "name":          "team_name",
})

# races
races = races[["raceId", "year", "round", "circuitId", "name", "date"]]
races = races.rename(columns={
    "raceId":    "race_id",
    "circuitId": "circuit_id",
    "name":      "race_name",
    "date":      "race_date",
    "year":      "season",
})

# results
results = results[[
    "resultId", "raceId", "driverId", "constructorId",
    "grid", "position", "points", "laps",
    "milliseconds", "fastestLap", "fastestLapTime",
    "fastestLapSpeed", "rank", "statusId"
]]
results = results.rename(columns={
    "resultId":        "result_id",
    "raceId":          "race_id",
    "driverId":        "driver_id",
    "constructorId":   "constructor_id",
    "fastestLap":      "fastest_lap",
    "fastestLapTime":  "fastest_lap_time",
    "fastestLapSpeed": "fastest_lap_speed",
    "statusId":        "status_id"
})
results["position"] = results["position"].fillna(0).astype(int)

# lap_times
lap_times = lap_times.rename(columns={
    "raceId":       "race_id",
    "driverId":     "driver_id",
    "position":     "position",
    "time":         "lap_time",
    "milliseconds": "lap_ms"
})


# Connect to PostgreSQL

cfg = DB_CONFIG
engine = create_engine(
    f"postgresql+psycopg2://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"
)


# Load tables — if_exists="replace" means it'll
# recreate the table fresh each time you run this

print("Loading drivers...")
drivers.to_sql("drivers", engine, if_exists="replace", index=False)

print("Loading constructors...")
constructors.to_sql("constructors", engine, if_exists="replace", index=False)

print("Loading races...")
races.to_sql("races", engine, if_exists="replace", index=False)

print("Loading results...")
results.to_sql("results", engine, if_exists="replace", index=False)

print("Loading lap_times... (big)")
lap_times.to_sql("lap_times", engine, if_exists="replace", index=False)

print("\n All tables loaded into PostgreSQL successfully!")