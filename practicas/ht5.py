import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

DB_CONNECTION = 'mysql+pymysql://root:@localhost/pandemiaDB'
engine = create_engine(DB_CONNECTION)

query = "SELECT fallecidos_municipio, fallecidos_mundiales FROM Integracion_Datos"
df = pd.read_sql_query(query, engine)

quantitative_vars = ['fallecidos_municipio', 'fallecidos_mundiales']

# Procesar cada variable cuantitativa
for var in quantitative_vars:
    # Filtrar los valores distintos de cero
    filtered_data = df[var][df[var] > 0]

    if not filtered_data.empty:
        # Crear boxplot sin ceros
        plt.figure(figsize=(6, 4))
        plt.boxplot(filtered_data, vert=False)
        plt.title(f'Boxplot de {var} (sin ceros)')
        plt.xlabel(var)
        # Guardar el gráfico como archivo PNG
        plt.savefig(f'boxplot_{var}.png')
        plt.close()

        # Calcular rango intercuartílico (IQR)
        Q1 = filtered_data.quantile(0.25)
        Q3 = filtered_data.quantile(0.75)
        IQR = Q3 - Q1

        # Límites para detectar outliers
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        print(f"\nVariable: {var}")
        print(f"Q1 (25%): {Q1}")
        print(f"Q3 (75%): {Q3}")
        print(f"IQR: {IQR}")
        print(f"Límite inferior: {limite_inferior}")
        print(f"Límite superior: {limite_superior}")

        # Filtrar datos sin outliers
        sin_outliers = filtered_data[(filtered_data >= limite_inferior) & (filtered_data <= limite_superior)]
        print(f"Total de registros sin outliers en {var}: {len(sin_outliers)}")
    else:
        print(f"No hay valores distintos de cero en {var}.")
