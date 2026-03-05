
--Query 1: Driver Season Standings

SELECT
    r.season,
    d.first_name || ' ' || d.last_name AS driver_name,
    d.nationality,
    c.team_name,
    SUM(res.points)                    AS total_points,
    COUNT(CASE WHEN res.position = 1 
          THEN 1 END)                  AS wins,
    COUNT(CASE WHEN res.position <= 3 
          THEN 1 END)                  AS podiums,
    RANK() OVER (
        PARTITION BY r.season
        ORDER BY SUM(res.points) DESC
    )                                  AS season_rank
FROM results res
JOIN races r        ON res.race_id       = r.race_id
JOIN drivers d      ON res.driver_id     = d.driver_id
JOIN constructors c ON res.constructor_id = c.constructor_id
GROUP BY r.season, d.first_name, d.last_name, d.nationality, c.team_name
ORDER BY r.season DESC, total_points DESC;


--Query 2: Average Lap Time per Driver per Circuit

SELECT
    d.first_name || ' ' || d.last_name AS driver_name,
    r.race_name,
    r.season,
    COUNT(lt.lap)                       AS laps_completed,
    ROUND(AVG(lt.lap_ms) / 1000.0, 3)  AS avg_lap_seconds,
    ROUND(MIN(lt.lap_ms) / 1000.0, 3)  AS fastest_lap_seconds,
    ROUND(MAX(lt.lap_ms) / 1000.0, 3)  AS slowest_lap_seconds,
    RANK() OVER (
        PARTITION BY r.race_id
        ORDER BY AVG(lt.lap_ms) ASC
    )                                   AS speed_rank
FROM lap_times lt
JOIN races r    ON lt.race_id   = r.race_id
JOIN drivers d  ON lt.driver_id = d.driver_id
GROUP BY d.first_name, d.last_name, r.race_name, r.season, r.race_id
ORDER BY r.season DESC, r.race_name, avg_lap_seconds ASC;


--Query 3: Year Over Year Driver Performance

SELECT
    d.first_name || ' ' || d.last_name  AS driver_name,
    r.season,
    SUM(res.points)                      AS total_points,
    LAG(SUM(res.points)) OVER (
        PARTITION BY d.driver_id
        ORDER BY r.season
    )                                    AS prev_season_points,
    SUM(res.points) - LAG(SUM(res.points)) OVER (
        PARTITION BY d.driver_id
        ORDER BY r.season
    )                                    AS points_change,
    COUNT(CASE WHEN res.position = 1 
          THEN 1 END)                    AS wins,
    RANK() OVER (
        PARTITION BY r.season
        ORDER BY SUM(res.points) DESC
    )                                    AS season_rank
FROM results res
JOIN races r    ON res.race_id   = r.race_id
JOIN drivers d  ON res.driver_id = d.driver_id
GROUP BY d.driver_id, d.first_name, d.last_name, r.season
ORDER BY d.last_name, r.season DESC;



--Query 4: Constructor Performance Over Time

SELECT
    c.team_name,
    r.season,
    SUM(res.points)                     AS total_points,
    COUNT(CASE WHEN res.position = 1 
          THEN 1 END)                   AS wins,
    COUNT(CASE WHEN res.position <= 3 
          THEN 1 END)                   AS podiums,
    ROUND(AVG(res.points)::numeric, 2)  AS avg_points_per_race,
    LAG(SUM(res.points)) OVER (
        PARTITION BY c.constructor_id
        ORDER BY r.season
    )                                   AS prev_season_points,
    SUM(res.points) - LAG(SUM(res.points)) OVER (
        PARTITION BY c.constructor_id
        ORDER BY r.season
    )                                   AS points_change,
    RANK() OVER (
        PARTITION BY r.season
        ORDER BY SUM(res.points) DESC
    )                                   AS constructor_rank
FROM results res
JOIN races r        ON res.race_id        = r.race_id
JOIN constructors c ON res.constructor_id = c.constructor_id
GROUP BY c.constructor_id, c.team_name, r.season
ORDER BY r.season DESC, total_points DESC;


--Query 5: Fastest Lap Rankings Per Race

SELECT
    r.season,
    r.race_name,
    d.first_name || ' ' || d.last_name  AS driver_name,
    c.team_name,
    res.fastest_lap_time,
    res.fastest_lap_speed,
    RANK() OVER (
        PARTITION BY r.race_id
        ORDER BY res.fastest_lap_speed DESC
    )                                   AS speed_rank,
    RANK() OVER (
        PARTITION BY r.season
        ORDER BY res.fastest_lap_speed DESC
    )                                   AS season_speed_rank
FROM results res
JOIN races r        ON res.race_id        = r.race_id
JOIN drivers d      ON res.driver_id      = d.driver_id
JOIN constructors c ON res.constructor_id = c.constructor_id
WHERE res.fastest_lap_speed IS NOT NULL
ORDER BY r.season DESC, res.fastest_lap_speed DESC;