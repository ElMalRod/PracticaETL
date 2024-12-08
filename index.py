import pandas as pd
from sqlalchemy import create_engine

# Configuración de archivos y base de datos
LOCAL_FILE_PATH = 'municipio.csv'
WEB_FILE_PATH = 'https://storage.googleapis.com/ss2practica1/global_calificacion.csv'
DB_CONNECTION = 'mysql+pymysql://root:@localhost/pandemiaDB'  
TABLE_NAME = 'Integracion_Datos'

# 1. Cargar los datos
print("Cargando los archivos CSV...")
municipios_df = pd.read_csv(LOCAL_FILE_PATH)
global_df = pd.read_csv(WEB_FILE_PATH)

# 2. Limpieza y transformación de los datos de municipios
print("Transformando datos de municipios a formato largo...")
municipios_df_melted = municipios_df.melt(
    id_vars=["departamento", "codigo_departamento", "municipio", "codigo_municipio", "poblacion"],
    var_name="fecha",
    value_name="fallecidos"
)
municipios_df_melted["fecha"] = pd.to_datetime(municipios_df_melted["fecha"], errors="coerce")
municipios_df_melted["fallecidos"] = pd.to_numeric(municipios_df_melted["fallecidos"], errors="coerce").fillna(0)

# 3. Limpieza y filtrado de datos globales
print("Filtrando datos globales para Guatemala y año 2020...")
global_df["Date_reported"] = pd.to_datetime(global_df["Date_reported"], errors="coerce")
global_df = global_df[(global_df["Country_code"] == "GT") & (global_df["Date_reported"].dt.year == 2020)]

# 4. Combinar datasets
print("Combinando datasets...")
combined_df = municipios_df_melted.merge(
    global_df,
    left_on="fecha",
    right_on="Date_reported",
    how="inner"
)[["fecha", "codigo_municipio", "fallecidos", "Country_code", "Cumulative_deaths"]]

combined_df = combined_df.rename(columns={
    "fecha": "fecha",
    "fallecidos": "fallecidos_municipio",
    "Country_code": "codigo_pais",
    "Cumulative_deaths": "fallecidos_mundiales"
})

# 5. Conexión a la base de datos
print("Conectando a la base de datos...")
engine = create_engine(DB_CONNECTION)

# Función para cargar datos por bloques con manejo de errores
def cargar_datos_por_bloques(df, table_name, engine, chunk_size=50):
    exitosos = 0
    fallidos = 0
    fallos = []
    
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size]
        try:
            with engine.begin() as connection:
                chunk.to_sql(name=table_name, con=connection, if_exists='append', index=False)
            print(f"Bloque {i // chunk_size + 1} insertado con éxito.")
            exitosos += 1
        except SQLAlchemyError as e:
            print(f"Error al insertar bloque {i // chunk_size + 1}: {e}")
            fallos.append(chunk)
            fallidos += 1

    # Reintentar los fallos al final
    if fallos:
        print("Reintentando bloques fallidos...")
        for chunk in fallos:
            try:
                with engine.begin() as connection:
                    chunk.to_sql(name=table_name, con=connection, if_exists='append', index=False)
                print("Bloque fallido insertado con éxito.")
                fallidos -= 1
                exitosos += 1
            except SQLAlchemyError as e:
                print(f"Error al reintentar insertar bloque: {e}")

    print(f"Reporte final: {exitosos} bloques insertados con éxito, {fallidos} bloques fallidos.")

# 6. Insertar datos combinados
print("Insertando datos integrados...")
cargar_datos_por_bloques(combined_df, TABLE_NAME, engine)

print("Proceso ETL completado.")