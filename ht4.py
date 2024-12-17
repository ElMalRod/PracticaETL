import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Configuración de conexión a la base de datos
DB_CONNECTION = 'mysql+pymysql://root:@localhost/pandemiaDB'
engine = create_engine(DB_CONNECTION)

# Consulta para obtener los datos agrupados por municipio (top 10)
query_municipios = """
SELECT m.nombre_municipio, COUNT(i.id_integracion) AS total_registros
FROM Integracion_Datos i
JOIN Municipio m ON i.codigo_municipio = m.codigo_municipio
GROUP BY m.nombre_municipio
ORDER BY total_registros DESC
LIMIT 10
"""

# Consulta para obtener los datos agrupados por departamento (top 10)
query_departamentos = """
SELECT d.nombre_departamento, COUNT(i.id_integracion) AS total_registros
FROM Integracion_Datos i
JOIN Municipio m ON i.codigo_municipio = m.codigo_municipio
JOIN Departamento d ON m.codigo_departamento = d.codigo_departamento
GROUP BY d.nombre_departamento
ORDER BY total_registros DESC
LIMIT 10
"""

# Obtener los datos de la base de datos
print("Ejecutando consulta para municipios...")
municipios_top10 = pd.read_sql_query(query_municipios, engine)
print("Datos obtenidos para municipios (Top 10):")
print(municipios_top10)

print("\nEjecutando consulta para departamentos...")
departamentos_top10 = pd.read_sql_query(query_departamentos, engine)
print("Datos obtenidos para departamentos (Top 10):")
print(departamentos_top10)

# Graficar los datos: Top 10 Municipios
if not municipios_top10.empty:
    plt.figure(figsize=(10, 6))
    plt.bar(municipios_top10['nombre_municipio'], municipios_top10['total_registros'], color='blue')
    plt.title('Top 10 Municipios por Total de Registros', fontsize=16)
    plt.xlabel('Municipios', fontsize=12)
    plt.ylabel('Total de Registros', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    for i, valor in enumerate(municipios_top10['total_registros']):
        plt.text(i, valor + 5, str(valor), ha='center')
    plt.show()
else:
    print("No se encontraron datos para municipios.")

# Graficar los datos: Top 10 Departamentos
if not departamentos_top10.empty:
    plt.figure(figsize=(10, 6))
    plt.bar(departamentos_top10['nombre_departamento'], departamentos_top10['total_registros'], color='green')
    plt.title('Top 10 Departamentos por Total de Registros', fontsize=16)
    plt.xlabel('Departamentos', fontsize=12)
    plt.ylabel('Total de Registros', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    for i, valor in enumerate(departamentos_top10['total_registros']):
        plt.text(i, valor + 5, str(valor), ha='center')
    plt.show()
else:
    print("No se encontraron datos para departamentos.")
