import pandas as pd
import os

# Clase encargada de la carga del archivo principal para luego ser procesado y utilizado posteriormente

class CargadorDatos:

    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo
        self.df = None

    # Aquí nos encargamos de la carga inicial del archivo a trabajar desde donde se encuentra
    def cargar_datos(self):
        if not os.path.exists(self.ruta_archivo):
            raise FileNotFoundError(f"No se encontró el archivo en: {self.ruta_archivo}")

        self.df = pd.read_csv(self.ruta_archivo)

        filas, columnas = self.df.shape

        print(f"Archivo cargado correctamente: {os.path.basename(self.ruta_archivo)}")
        print(f"Filas: {filas}, Columnas: {columnas}")
        return self.df

    # Aquí mostramos la información general de lo que tiene el dataset y la comprobación de la información contenida
    def info_datos(self):
        if self.df is None:
            raise ValueError("No se ha cargado ningún dataset. Usa cargar_datos() primero.")

        print("\nInformación general del dataset:")
        print(self.df.info())
        print("\nPrimeras filas:")
        print(self.df.head())

    # Aquí vemos la cantidad de valores nulos que posee el dataset
    def resumen_nulos(self):
        if self.df is None:
            raise ValueError("No se ha cargado ningún dataset. Usa cargar_datos() primero.")

        nulos = self.df.isnull().sum()
        porcentaje = (nulos / len(self.df)) * 100
        resumen_nulos = pd.DataFrame({
            "Valores nulos": nulos,
            "Porcentaje (%)": porcentaje.round(2)
        })
        # Nos muestra la ubicación de los valores nulos directamente
        print("\nResumen de valores nulos:")
        print(resumen_nulos[resumen_nulos["Valores nulos"] > 0])
        return resumen_nulos
