# F1 Performance Analytics

An end-to-end data analytics project exploring Formula 1 performance trends from 2000–2024 using SQL, Python, and Tableau.

 **[View Live Tableau Dashboards](https://public.tableau.com/app/profile/david.shi3369/vizzes)**

---

## Project Overview

This project builds a full analytics pipeline on F1 race data — from raw CSVs through a structured PostgreSQL database, to interactive Tableau dashboards. The goal was to uncover performance trends across drivers, constructors, circuits, and seasons.

**Key finding:** McLaren's dramatic resurgence in 2023–2024 after nearly a decade of midfield obscurity — culminating in the 2024 Constructors' Championship — is one of the most striking stories visible in the data.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python (pandas) | Data cleaning and loading |
| PostgreSQL | Structured data storage and querying |
| SQL (window functions) | Performance analysis |
| Tableau Public | Interactive dashboards |

---

## Project Structure

```
f1-analytics/
├── data/                   # Raw CSVs (not tracked in git)
├── exports/                # Query output CSVs (not tracked in git)
├── python/
│   ├── clean.py            # Data cleaning script
│   └── load_to_db.py       # PostgreSQL loader
├── sql/
│   └── queries.sql         # All analysis queries
└── README.md
```

---

## Data Source

[Formula 1 World Championship Dataset (Kaggle)](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)

5 tables used:
- `drivers` — driver profiles and nationalities
- `constructors` — team information
- `races` — race calendar and circuit data
- `results` — finishing positions, points, fastest laps
- `lap_times` — lap-by-lap timing data (589,081 rows)

---

## SQL Analysis

5 queries written across `sql/queries.sql` using advanced PostgreSQL features:

**Query 1 — Driver Season Standings**
Ranks drivers within each season using `RANK() OVER (PARTITION BY season)`, with wins and podium counts via `COUNT(CASE WHEN)`.

**Query 2 — Average Lap Time per Driver per Circuit**
Aggregates lap-by-lap timing data to compute average, fastest and slowest lap per driver per race, with circuit-level speed rankings.

**Query 3 — Year Over Year Driver Performance**
Uses `LAG()` window function to compare each driver's points total to their previous season, surfacing improvement and decline trends.

**Query 4 — Constructor Performance Over Time**
Tracks team points, wins and podiums across seasons with year-over-year change using `LAG()`, revealing the rise and fall of constructor dominance.

**Query 5 — Fastest Lap Rankings**
Identifies the fastest lap speeds across races and seasons, ranking drivers within each race and across the full season using nested `RANK() OVER` window functions.

---

## Tableau Dashboards

**[View all dashboards here](https://public.tableau.com/app/profile/david.shi3369/vizzes)**

**Dashboard 1 — F1 Driver Championship Analysis**
- Points progression across seasons for top drivers
- Career wins leaderboard
- Hamilton vs Verstappen vs Vettel era comparison

**Dashboard 2 — F1 Constructor Championship Analysis**
- Constructor points over time (2000–2024)
- All-time wins by team
- Visualises Mercedes dominance (2014–2021) and McLaren's 2024 resurgence

**Dashboard 3 — F1 2024 Speed Analysis**
- Average fastest lap speed by team in 2024
- Circuit-by-circuit speed breakdown
- Monza (Italian GP) confirmed as the fastest circuit on the calendar

---

## Key Insights

- **McLaren's resurgence** — after finishing 5th or lower in the constructors standings from 2013–2022, McLaren climbed to win the 2024 championship with 609 points, the biggest single-season points jump of any team in the dataset
- **Verstappen's 2023 dominance** — Red Bull scored 860 points in 2023, the highest single-season constructor total in the dataset, before dropping to 537 in 2024
- **Hamilton's LAG analysis** — the year-over-year query clearly shows Hamilton's 2022 drop of -152 points when Mercedes struggled with the new car regulations
- **Monza is the fastest circuit** — Lando Norris set the fastest lap of the 2024 season at the Italian GP at 256.1 km/h

---

## How to Run Locally

1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/f1-analytics.git
cd f1-analytics
```

2. Install dependencies
```bash
pip3 install pandas psycopg2-binary sqlalchemy
```

3. Download the dataset from Kaggle and place CSVs in `data/`

4. Create a `python/db_config.py` file:
```python
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "database": "f1_analytics",
    "user": "postgres",
    "password": "your_password"
}
```

5. Run the pipeline
```bash
python3 python/clean.py
python3 python/load_to_db.py
```

6. Open `sql/queries.sql` in pgAdmin and run queries against the `f1_analytics` database