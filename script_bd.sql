CREATE DATABASE DatosAbiertosDB;
GO

USE DatosAbiertosDB;
GO

CREATE TABLE RegistrosAPI (
    id_api VARCHAR(100) PRIMARY KEY,
    departamento VARCHAR(100),
    municipio VARCHAR(150),
    edad INT,
    sexo VARCHAR(10),
    estado VARCHAR(50),
    recuperado VARCHAR(50),
    fecha_reporte VARCHAR(50),
    json_original VARCHAR(MAX),
    fecha_captura DATETIME DEFAULT GETDATE()
);
GO
