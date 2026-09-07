import sys
from pathlib import Path
from importlib import import_module
from sqlalchemy import create_engine, text

sys.path.append(str(Path(__file__).parent))

transform = import_module("02_transform")

CADENA = (
    "mssql+pyodbc://localhost\\SQLEXPRESS/pipeline_fx"
    "?driver=ODBC+Driver+18+for+SQL+Server"
    "&trusted_connection=yes"
    "&TrustServerCertificate=yes"
)


def cargar(df, motor):
    df.to_sql("stg_tipo_cambio", motor, if_exists="replace", index=False)

    with motor.begin() as conexion:
        conexion.execute(text("""
            DELETE FROM fact_tipo_cambio
            WHERE fecha IN (SELECT fecha FROM stg_tipo_cambio)
        """))

        conexion.execute(text("""
            INSERT INTO fact_tipo_cambio (fecha, tipo_cambio, fecha_carga)
            SELECT fecha, tipo_cambio, fecha_carga FROM stg_tipo_cambio
        """))


if __name__ == "__main__":
    datos = transform.cargar_json_mas_reciente()
    df = transform.limpiar(datos)

    motor = create_engine(CADENA)
    cargar(df, motor)

    with motor.connect() as conexion:
        total = conexion.execute(text("SELECT COUNT(*) FROM fact_tipo_cambio")).scalar()

    print(f"Filas en fact_tipo_cambio: {total}")