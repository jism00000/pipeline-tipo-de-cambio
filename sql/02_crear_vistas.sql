USE pipeline_fx;
GO

CREATE VIEW vw_tipo_cambio_diario AS
SELECT
    fecha,
    tipo_cambio,
    tipo_cambio - LAG(tipo_cambio) OVER (ORDER BY fecha) AS variacion,
    ROUND(
        (tipo_cambio - LAG(tipo_cambio) OVER (ORDER BY fecha))
        / LAG(tipo_cambio) OVER (ORDER BY fecha) * 100
    , 4) AS variacion_pct,
    AVG(tipo_cambio) OVER (
        ORDER BY fecha
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS promedio_7d,
    AVG(tipo_cambio) OVER (
        ORDER BY fecha
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS promedio_30d
FROM fact_tipo_cambio;
GO

CREATE VIEW vw_tipo_cambio_mensual AS
SELECT
    YEAR(fecha) AS anio,
    MONTH(fecha) AS mes,
    MIN(tipo_cambio) AS minimo,
    MAX(tipo_cambio) AS maximo,
    AVG(tipo_cambio) AS promedio,
    COUNT(*) AS dias_habiles
FROM fact_tipo_cambio
GROUP BY YEAR(fecha), MONTH(fecha);
GO

CREATE TABLE dim_calendario (
    fecha DATE NOT NULL PRIMARY KEY,
    anio INT NOT NULL,
    mes INT NOT NULL,
    nombre_mes VARCHAR(20) NOT NULL,
    dia INT NOT NULL,
    trimestre INT NOT NULL,
    dia_semana INT NOT NULL,
    es_fin_semana BIT NOT NULL
);
GO

WITH fechas AS (
    SELECT CAST('2020-01-01' AS DATE) AS f
    UNION ALL
    SELECT DATEADD(DAY, 1, f) FROM fechas WHERE f < '2030-12-31'
)
INSERT INTO dim_calendario
SELECT
    f,
    YEAR(f),
    MONTH(f),
    DATENAME(MONTH, f),
    DAY(f),
    DATEPART(QUARTER, f),
    DATEPART(WEEKDAY, f),
    CASE WHEN DATEPART(WEEKDAY, f) IN (1, 7) THEN 1 ELSE 0 END
FROM fechas
OPTION (MAXRECURSION 0);
GO