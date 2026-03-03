import pandas as pd
import os


# Raw csv file

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")

drivers      = pd.read_csv(f"{DATA_PATH}/drivers.csv",      na_values="\\N")
constructors = pd.read_csv(f"{DATA_PATH}/constructors.csv", na_values="\\N")
races        = pd.read_csv(f"{DATA_PATH}/races.csv",        na_values="\\N")
results      = pd.read_csv(f"{DATA_PATH}/results.csv",      na_values="\\N")
lap_times    = pd.read_csv(f"{DATA_PATH}/lap_times.csv",    na_values="\\N")


# Clean drivers

drivers = drivers.drop(columns=["url", "number", "dob"])
drivers = drivers.rename(columns={
    "driverId":   "driver_id",
    "driverRef":  "driver_ref",
    "forename":   "first_name",
    "surname":    "last_name",
})


# Clean constructors

constructors = constructors.drop(columns=["url", "constructorRef"])
constructors = constructors.rename(columns={
    "constructorId": "constructor_id",
    "name":          "team_name",
    "nationality":   "nationality"
})


# Clean races

races = races[[
    "raceId", "year", "round", "circuitId", "name", "date"
]]
races = races.rename(columns={
    "raceId":    "race_id",
    "circuitId": "circuit_id",
    "name":      "race_name",
    "date":      "race_date",
    "year":      "season",
    "round":     "round"
})


# Clean results 

results = results[[
    "resultId", "raceId", "driverId", "constructorId",
    "grid", "position", "points", "laps",
    "milliseconds", "fastestLap", "fastestLapTime",
    "fastestLapSpeed", "rank", "statusId"
]]
results = results.rename(columns={
    "resultId":       "result_id",
    "raceId":         "race_id",
    "driverId":       "driver_id",
    "constructorId":  "constructor_id",
    "fastestLap":     "fastest_lap",
    "fastestLapTime": "fastest_lap_time",
    "fastestLapSpeed":"fastest_lap_speed",
    "statusId":       "status_id"
})

# position has DNFs stored as \N — fill with 0 to mean "did not finish"
results["position"] = results["position"].fillna(0).astype(int)


# Clean lap_times

lap_times = lap_times.rename(columns={
    "raceId":       "race_id",
    "driverId":     "driver_id",
    "position":     "position",
    "time":         "lap_time",
    "milliseconds": "lap_ms"
})


# Preview cleaned tables

print("=== DRIVERS ===");        print(drivers.head());      print(drivers.shape)
print("\n=== CONSTRUCTORS ==="); print(constructors.head()); print(constructors.shape)
print("\n=== RACES ===");        print(races.head());        print(races.shape)
print("\n=== RESULTS ===");      print(results.head());      print(results.shape)
print("\n=== LAP TIMES ===");    print(lap_times.head());    print(lap_times.shape)

print("\n All tables cleaned successfully")