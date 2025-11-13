
import pandas as pd

class ProcesadorEDA:
    """
    Clase para realizar el análisis exploratorio de datos (EDA)
    del dataset de la Premier League.
    """

    def __init__(self, ruta_entrada, ruta_salida):
        self.ruta_entrada = ruta_entrada
        self.ruta_salida = ruta_salida
        self.df = None

    # ------------------------------------------------------------
    def cargar_datos(self):
        """Carga el dataset original desde CSV"""
        self.df = pd.read_csv(self.ruta_entrada)
        filas, columnas = self.df.shape
        nulos = self.df.isnull().sum().sum()
        porcentaje_nulos = round((nulos / (filas * columnas)) * 100, 2)

        print(f"✅ Datos cargados correctamente.")
        print(f"   Filas: {filas}, Columnas: {columnas}")
        print(f"   Porcentaje de valores nulos: {porcentaje_nulos}%")
        return self.df

    # ------------------------------------------------------------
    def limpieza_datos(self):
        """Limpieza de nulos, tipos y normalización"""
        df = self.df.copy()

        # ---- 1. Corregir 'Age' (extraer solo la edad numérica)
        if 'Age' in df.columns:
            df['Age'] = df['Age'].astype(str).str.split('-').str[0]
            df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

        # ---- 2. Rellenar nulos de 'Minutes' con 0
        if 'Minutes' in df.columns:
            df['Minutes'].fillna(0, inplace=True)

        # ---- 3. Corregir formato de 'Pass Completion %'
        if 'Pass Completion %' in df.columns:
            df['Pass Completion %'] = (
                df['Pass Completion %']
                .astype(str)
                .str.replace(',', '.', regex=False)
            )
            df['Pass Completion %'] = pd.to_numeric(df['Pass Completion %'], errors='coerce')

        # ---- 4. Convertir columna 'Date' a tipo datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # ---- 5. Normalizar equipos (eliminar espacios, mayúsculas coherentes)
        if 'Team' in df.columns:
            df['Team'] = df['Team'].str.strip().str.title()

        # ---- 6. Eliminar filas totalmente vacías (si hubiera)
        df.dropna(how='all', inplace=True)

        # ---- 7. Renombrar columna '#' por 'NumeroJugador' (más robusto)
        df.rename(columns=lambda c: c.strip().replace('#', 'NumeroJugador') if '#' in c else c, inplace=True)
        # ---- 7. Renombrar columna '#' por 'NumeroJugador' (antes de limpiar nombres)
        if '#' in df.columns:
            df.rename(columns={'#': 'NumeroJugador'}, inplace=True)

        # ---- 8. Limpieza general de nombres de columnas
        df.columns = (
            df.columns
            .str.strip()
            .str.replace(' ', '_')
            .str.replace('%', 'Porc')
            .str.replace('[()]', '', regex=True)
        )

        # Guardar cambios
        self.df = df
        print("🧹 Limpieza completada con éxito.")
        print(f"   Dataset final: {df.shape[0]} filas, {df.shape[1]} columnas.")
        return df

    # ------------------------------------------------------------
    def resumen_descriptivo(self):
        """Muestra resumen estadístico descriptivo"""
        if self.df is None:
            raise ValueError("El dataset no ha sido cargado. Usa cargar_datos() primero.")
        resumen = self.df.describe(include='all')
        print("📈 Resumen estadístico generado.")
        return resumen

    # ------------------------------------------------------------
    def matriz_correlacion(self):
        """Genera y devuelve la matriz de correlación de variables numéricas"""
        if self.df is None:
            raise ValueError("El dataset no ha sido cargado. Usa cargar_datos() primero.")
        corr = self.df.corr(numeric_only=True)
        print("🔗 Matriz de correlación calculada.")
        return corr

    # ------------------------------------------------------------
    def guardar_datos_limpios(self):
        """Guarda el dataset limpio en la ruta especificada"""
        if self.df is None:
            raise ValueError("No hay datos para guardar. Ejecuta limpieza_datos() primero.")
        self.df.to_csv(self.ruta_salida, index=False)
        print(f"💾 Archivo limpio guardado en: {self.ruta_salida}")
