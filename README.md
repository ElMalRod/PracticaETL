# Proyecto de ETL para el Análisis de Datos de la Pandemia

## Descripción del Proyecto
Este proyecto implementa un proceso de Extracción, Transformación y Carga (ETL) para analizar datos recopilados durante la pandemia de COVID-19 en el año 2020. Se utilizaron diferentes fuentes de datos para obtener información sobre fallecimientos por municipio en Guatemala y estadísticas globales sobre casos y muertes por COVID-19.

El objetivo es centralizar, limpiar y transformar estos datos en un formato integrado y almacenarlos en una base de datos SQL para su posterior análisis.

---

## Objetivos
- Comprender el proceso de ETL para la gestión de datos.
- Trabajar con diferentes formatos de datos y fuentes.
- Familiarizarse con Python y Pandas para el procesamiento de datos.
- Diseñar un modelo relacional de datos optimizado para el análisis.

---

## Fuentes de Datos
### 1. Fallecidos por Municipio
- **Formato**: CSV (cargado localmente).
- **Campos**:
  - `departamento`: Nombre del departamento en Guatemala.
  - `codigo_departamento`: Identificador único de cada departamento.
  - `municipio`: Nombre del municipio.
  - `codigo_municipio`: Identificador único de cada municipio.
  - `poblacion`: Cantidad de habitantes en cada municipio.
  - **Fechas**: Columna para cada día que reporta la cantidad de fallecimientos.

### 2. Conteo Mundial de Fallecidos y Casos
- **Formato**: CSV (descargado programáticamente desde la web).
- **Campos**:
  - `Date_reported`: Fecha del reporte.
  - `Country_code`: Código del país.
  - `Country`: Nombre del país.
  - `WHO_region`: Región del mundo.
  - `New_cases`: Nuevos casos reportados.
  - `Cumulative_cases`: Casos acumulados.
  - `New_deaths`: Nuevas muertes reportadas.
  - `Cumulative_deaths`: Muertes acumuladas.

---

## Proceso de Limpieza y Transformación de Datos
### 1. Limpieza de Datos
- **Remoción de duplicados**: Se eliminaron registros duplicados en ambas fuentes de datos.
- **Estandarización**:
  - Se corrigieron columnas con valores incoherentes o faltantes.
  - Las fechas fueron convertidas al formato `datetime`.
- **Manejo de valores faltantes**:
  - En datos de municipios, los valores nulos se llenaron con 0.
  - En datos globales, se eliminaron filas con fechas o países faltantes.
- **Filtrado**:
  - Solo se conservaron los datos de Guatemala (`Country_code = 'GT'`) y del año 2020.

### 2. Transformación de Datos
- **Formato largo**:
  - Los datos de municipios se transformaron de un formato horizontal (fechas como columnas) a un formato largo con columnas `fecha` y `fallecidos`.
- **Combinación de Datos**:
  - Se unieron los datos de fallecimientos por municipio con los datos globales utilizando la columna `fecha`.

---

## Modelo Relacional de la Base de Datos
Se diseñó una base de datos SQL relacional con las siguientes tablas:

### 1. `Departamento`
- **Campos**:
  - `codigo_departamento` (PK): Identificador único.
  - `nombre_departamento`: Nombre del departamento.

### 2. `Municipio`
- **Campos**:
  - `codigo_municipio` (PK): Identificador único.
  - `nombre_municipio`: Nombre del municipio.
  - `poblacion`: Población del municipio.
  - `codigo_departamento` (FK): Referencia al departamento.

### 3. `Fallecidos_Municipio`
- **Campos**:
  - `id_fallecidos_municipio` (PK): Identificador único.
  - `codigo_municipio` (FK): Referencia al municipio.
  - `fecha`: Fecha del reporte.
  - `fallecidos`: Número de fallecidos en esa fecha.

### 4. `Pais`
- **Campos**:
  - `codigo_pais` (PK): Código del país.
  - `nombre_pais`: Nombre del país.
  - `region_oms`: Región según la OMS.

### 5. `Covid_Reporte`
- **Campos**:
  - `id_reporte` (PK): Identificador único.
  - `codigo_pais` (FK): Referencia al país.
  - `fecha_reporte`: Fecha del reporte.
  - `nuevos_casos`: Nuevos casos reportados.
  - `casos_acumulados`: Casos acumulados.
  - `nuevos_fallecimientos`: Nuevos fallecimientos reportados.
  - `fallecimientos_acumulados`: Fallecimientos acumulados.

### 6. `Integracion_Datos`
- **Campos**:
  - `id_integracion` (PK): Identificador único.
  - `fecha`: Fecha del reporte.
  - `codigo_municipio` (FK): Referencia al municipio.
  - `codigo_pais` (FK): Referencia al país.
  - `fallecidos_municipio`: Fallecimientos en el municipio.
  - `fallecidos_mundiales`: Fallecimientos acumulados globalmente.

---

## Análisis del Modelo de Datos
- Las tablas `Departamento`, `Municipio`, y `Pais` permiten estructurar los datos geográficamente.
- La tabla `Fallecidos_Municipio` almacena los datos locales transformados.
- La tabla `Covid_Reporte` consolida los datos globales descargados.
- La tabla `Integracion_Datos` centraliza la información combinada para análisis.

---

## Razón para No Usar Otras Tablas
Las tablas individuales de datos de fallecidos y reportes globales ya no son necesarias después de la creación de `Integracion_Datos`, que contiene toda la información combinada y estandarizada. Este enfoque optimiza el acceso a los datos y simplifica los análisis futuros.

---

## Proceso de Carga
- **Bloques de 50 registros**:
  - La inserción de datos se realiza en bloques para optimizar el rendimiento.
- **Transacciones**:
  - Cada bloque se inserta como una transacción con manejo de commit y rollback en caso de error.
- **Reintentos**:
  - Los bloques fallidos se reintentan al final del proceso.
- **Reporte**:
  - Al final, se genera un reporte de la cantidad de bloques insertados exitosamente y los fallidos.

---

## Instrucciones de Ejecución
1. Configurar la base de datos usando el script SQL proporcionado.
2. Instalar dependencias:
   ```bash
   pip install pandas sqlalchemy pymysql

