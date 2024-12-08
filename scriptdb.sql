-- Creación de la base de datos
CREATE DATABASE pandemiaDB;
USE PandemiaDB;

-- Tabla Departamento
CREATE TABLE Departamento (
    codigo_departamento INT PRIMARY KEY,
    nombre_departamento VARCHAR(100) NOT NULL
);

-- Tabla Municipio
CREATE TABLE Municipio (
    codigo_municipio INT PRIMARY KEY,
    nombre_municipio VARCHAR(100) NOT NULL,
    poblacion INT NOT NULL,
    codigo_departamento INT NOT NULL,
    FOREIGN KEY (codigo_departamento) REFERENCES Departamento(codigo_departamento)
);

-- Tabla Fallecidos_Municipio
CREATE TABLE Fallecidos_Municipio (
    id_fallecidos_municipio INT PRIMARY KEY AUTO_INCREMENT,
    codigo_municipio INT NOT NULL,
    fecha DATE NOT NULL,
    fallecidos INT NOT NULL,
    FOREIGN KEY (codigo_municipio) REFERENCES Municipio(codigo_municipio)
);

-- Tabla Pais
CREATE TABLE Pais (
    codigo_pais CHAR(3) PRIMARY KEY,
    nombre_pais VARCHAR(100) NOT NULL,
    region_oms VARCHAR(100) NOT NULL
);

-- Tabla Covid_Reporte
CREATE TABLE Covid_Reporte (
    id_reporte INT PRIMARY KEY AUTO_INCREMENT,
    codigo_pais CHAR(3) NOT NULL,
    fecha_reporte DATE NOT NULL,
    nuevos_casos INT NOT NULL,
    casos_acumulados INT NOT NULL,
    nuevos_fallecimientos INT NOT NULL,
    fallecimientos_acumulados INT NOT NULL,
    FOREIGN KEY (codigo_pais) REFERENCES Pais(codigo_pais)
);

-- Tabla Integracion_Datos
CREATE TABLE Integracion_Datos (
    id_integracion INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATE NOT NULL,
    codigo_municipio INT NOT NULL,
    codigo_pais CHAR(3) NOT NULL,
    fallecidos_municipio INT NOT NULL,
    fallecidos_mundiales INT NOT NULL,
    FOREIGN KEY (codigo_municipio) REFERENCES Municipio(codigo_municipio),
    FOREIGN KEY (codigo_pais) REFERENCES Pais(codigo_pais)
);
