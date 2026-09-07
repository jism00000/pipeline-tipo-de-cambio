CREATE DATABASE pipeline_fx;
GO

USE pipeline_fx;
GO

CREATE TABLE stg_tipo_cambio (
    fecha DATE,
    tipo_cambio DECIMAL(10, 4),
    fecha_carga DATETIME
);
GO

CREATE TABLE fact_tipo_cambio (
    fecha DATE NOT NULL PRIMARY KEY,
    tipo_cambio DECIMAL(10, 4) NOT NULL,
    fecha_carga DATETIME NOT NULL
);
GO