# **Proyecto: Análisis de Datos Pandemia 2020**

## **Descripción General**

Este proyecto realiza un **Análisis Exploratorio de Datos (EDA)** utilizando información recopilada durante la pandemia del 2020\. El análisis incluye la exploración de datos cuantitativos y cualitativos, identificación de valores atípicos, correlaciones y multicolinealidad, utilizando **Python** y librerías de análisis de datos.

---

## **Objetivos del Proyecto**

1. Conectar a una base de datos SQL y obtener datos relevantes.  
2. Realizar un **EDA monovariable** para entender la distribución de cada variable.  
3. Identificar y tratar **outliers** mediante el uso de estadística descriptiva.  
4. Realizar un **EDA multivariable** para analizar relaciones entre variables.  
5. Calcular **correlaciones** y evaluar la **multicolinealidad** entre variables cuantitativas.  
6. Interpretar los resultados para obtener conclusiones relevantes.

---

## **Requerimientos Técnicos**

* **Lenguaje:** Python 3.8+  
* **Librerías Necesarias:**  
  * `pandas`  
  * `sqlalchemy`  
  * `matplotlib`  
  * `seaborn`  
  * `numpy`  
  * `scipy`  
  * `statsmodels`

### **Instalación de Librerías**

Utiliza el siguiente comando para instalar todas las dependencias:

pip install pandas sqlalchemy matplotlib seaborn numpy scipy statsmodels pymysql

---

## **Flujo del Análisis de Datos**

### **1\. Conexión a la Base de Datos**

* Se utiliza **SQLAlchemy** para conectarse a la base de datos SQL.  
* Se ejecuta una consulta que obtiene las columnas:  
  * Nuevas muertes  
  * Muertes acumuladas  
  * Población  
  * Nombre del municipio  
  * Nombre del departamento

---

### **2\. Exploración de Datos Monovariable**

#### **Datos Cuantitativos**

* Variables analizadas:  
  1. `nuevas_muertes`  
  2. `muertes_acumuladas`  
  3. `poblacion`  
* Se realizan los siguientes pasos:  
  1. Estadísticas descriptivas: media, desviación estándar, mínimos, máximos y cuartiles.  
  2. Visualización mediante **histogramas** y **diagramas de caja**.

#### **Datos Cualitativos**

* Variables:  
  * `nombre_municipio`  
  * `nombre_departamento`  
* Se generan gráficos de barras para mostrar la frecuencia de registros.

---

### **3\. Identificación de Outliers**

* Uso del **Rango Intercuartílico (IQR)** para detectar valores atípicos en variables cuantitativas.  
* En caso de sesgo en los datos, se aplica una **transformación logarítmica** para ajustar la escala.

---

### **4\. Exploración de Datos Multivariable**

#### **Comparación entre Variables Cuantitativas**

* **Gráficas de dispersión** entre las variables:  
  * `nuevas_muertes` vs `muertes_acumuladas`  
  * `muertes_acumuladas` vs `poblacion`

#### **Comparación entre Variables Cualitativas y Cuantitativas**

* **Gráficos de barras** y **mapas de calor** para:  
  * Departamentos y municipios vs Nuevas muertes.  
  * Departamentos y municipios vs Muertes acumuladas.  
  * Departamentos y municipios vs Población.

---

### **5\. Análisis de Correlaciones**

* Cálculo de correlaciones entre variables cuantitativas utilizando:  
  * **Pearson**  
  * **Spearman**  
  * **Kendall**  
* Visualización de resultados con **mapas de calor**.

#### **Test Chi-Cuadrado**

* Evaluación de asociaciones entre variables categóricas como municipio y departamento.

---

### **6\. Análisis de Multicolinealidad**

* Se calcula el **VIF (Variance Inflation Factor)** para medir la independencia de las variables cuantitativas.

---
