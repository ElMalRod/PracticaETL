import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Configuración de archivos y base de datos
LOCAL_FILE_PATH = 'municipio.csv'
WEB_FILE_PATH = 'https://storage.googleapis.com/ss2practica1/global_calificacion.csv'
DB_CONNECTION = 'mysql+pymysql://root:@localhost/pandemiaDB'

# Cargar los datos
municipios_df = pd.read_csv(LOCAL_FILE_PATH)
global_df = pd.read_csv(WEB_FILE_PATH)

# Transformar los datos de municipios a formato largo
municipios_df_melted = municipios_df.melt(
    id_vars=["departamento", "codigo_departamento", "municipio", "codigo_municipio", "poblacion"],
    var_name="fecha",
    value_name="fallecidos"
)
municipios_df_melted["fecha"] = pd.to_datetime(municipios_df_melted["fecha"], errors="coerce")
municipios_df_melted["fallecidos"] = pd.to_numeric(municipios_df_melted["fallecidos"], errors="coerce").fillna(0)

# Filtrar y limpiar datos globales
global_df["Date_reported"] = pd.to_datetime(global_df["Date_reported"], errors="coerce")
global_df = global_df[(global_df["Country_code"] == "GT") & (global_df["Date_reported"].dt.year == 2020)]

# Combinar datasets
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

# Eliminar duplicados
combined_df = combined_df.drop_duplicates()

# Extraer municipios únicos y departamentos únicos
municipios_unique = municipios_df[["codigo_municipio", "municipio", "poblacion", "codigo_departamento"]].drop_duplicates()
departamentos_unique = municipios_df[["codigo_departamento", "departamento"]].drop_duplicates()

# Resolver conflictos de duplicados en departamentos
departamentos_unique = departamentos_unique.drop_duplicates(subset=["codigo_departamento"], keep="first")
departamentos_unique = departamentos_unique.rename(columns={"departamento": "nombre_departamento"})
municipios_unique = municipios_unique.rename(columns={"municipio": "nombre_municipio"})

# Validar datos (quitar valores nulos)
departamentos_unique = departamentos_unique.dropna()
municipios_unique = municipios_unique.dropna()

# Conexión a la base de datos
engine = create_engine(DB_CONNECTION)

# Función para cargar datos por bloques
def cargar_datos_por_bloques(df, table_name, engine, chunk_size=50):
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size]
        try:
            chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            print(f"Bloque {i // chunk_size + 1} insertado con éxito.")
        except SQLAlchemyError as e:
            print(f"Error al insertar bloque {i // chunk_size + 1}: {e}")

# Insertar departamentos
print("Insertando departamentos...")
cargar_datos_por_bloques(departamentos_unique, "Departamento", engine)

# Insertar municipios
print("Insertando municipios...")
cargar_datos_por_bloques(municipios_unique, "Municipio", engine)

# Insertar datos integrados
print("Insertando datos integrados...")
cargar_datos_por_bloques(combined_df, "Integracion_Datos", engine)

print("Datos procesados e insertados correctamente.")
