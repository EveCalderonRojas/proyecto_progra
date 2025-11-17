import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Clase para el procesamiento del dataset a trabajar

class ProcesadorEDA:

    def __init__(self, df, ruta_salida):
        self.df = df
        self.ruta_salida = ruta_salida
        self.resumen = None
        self.corr = None

    # Aquí ya empezamos a limpiar el dataset previamente cargado en la clase anterior

    def limpieza_datos(self):
        df = self.df.copy() # Primero trabajamos sobre una copia del dataset para no alterar el original

        # Corregimos la edad, usando solo los dos primeros dígitos
        if 'Age' in df.columns:
            df['Age'] = df['Age'].astype(str).str.split('-').str[0]
            df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

        # Al haber nulos reemplazamos los valores faltantes por ceros directamente
        if 'Minutes' in df.columns:
            df['Minutes'].fillna(0, inplace=True)

        # Normalización de símbolos en las cantidades
        if 'Pass Completion %' in df.columns:
            df['Pass Completion %'] = (
                df['Pass Completion %']
                .astype(str)
                .str.replace(',', '.', regex=False)
            )
            df['Pass Completion %'] = pd.to_numeric(df['Pass Completion %'], errors='coerce')

        # Cambiamos a tipo datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # 5️⃣ Normalizar categorías
        if 'Team' in df.columns:
            df['Team'] = df['Team'].str.strip().str.title()
        if 'Position' in df.columns:
            df['Position'] = df['Position'].str.strip().str.upper()

        # Para el caso de la columna '#' esta por si sola no nos dice nada, por lo que se procede a cambiar su nombre por uno más adecuado a su contenido
        if '#' in df.columns:
            df.rename(columns={'#': 'PlayerNumber'}, inplace=True)
            print("Columna '#' renombrada a 'PlayerName'")

        # Limpiamos en general lo que no lleve formato en las columnas (vacíos, símbolos extras...)
        df.columns = (
            df.columns
            .str.strip()
            .str.replace(' ', '_')
            .str.replace('%', 'Porc')
            .str.replace('[()]', '', regex=True)
        )

        # Elimina las filas completamente vacías
        df.dropna(how='all', inplace=True)

        self.df = df
        print("Limpieza completada con éxito.")
        print(f"   Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
        return df

    # Empezamos con el resumen de estadísticas del dataset ya limpio
    def resumen_descriptivo(self):
        if self.df is None:
            raise ValueError("No se han cargado datos aún. ")

        self.resumen = self.df.describe(percentiles=[.25, .5, .75])
        print("Resumen estadístico generado: ")
        return self.resumen

    # Aquí generamos tanto la matriz de correlación y el gráfico de la misma mediante métodos separados
    def matriz_correlacion(self):
        if self.df is None:
            raise ValueError("No se han cargado datos aún.")

        self.corr = self.df.corr(numeric_only=True)
        print("Matriz de correlación: ")
        return self.corr

    def graficar_correlacion(self):
        corr = self.df.corr(numeric_only=True)

        plt.figure(figsize=(12, 8))
        sns.heatmap(corr, annot=True, cmap="coolwarm")
        plt.title("Matriz de Correlación")
        return plt

    # Aquí ya guardamos el dataset corregido y lo agregamos en la ruta deseada para trabajar con él posteriormente
    def guardar_datos_limpios(self):
        """Guarda el dataset limpio"""
        if self.df is None:
            raise ValueError("No se han cargado datos aún.")

        os.makedirs(os.path.dirname(self.ruta_salida), exist_ok=True)
        self.df.to_csv(self.ruta_salida, index=False)
        print(f"Archivo limpio guardado en: {self.ruta_salida}")


