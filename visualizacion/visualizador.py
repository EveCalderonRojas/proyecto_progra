import matplotlib.pyplot as plt
import pandas as pd

# Clase para la visualización de los resultados encontrados en el dataset

class Visualizador:

    def __init__(self, dataframe):
        self._dataframe = None
        self.__dataframe = dataframe

    @property
    def dataframe(self):
        return self.__dataframe

    @dataframe.setter
    def dataframe(self, valor):
        if isinstance(valor, pd.DataFrame):
            self.__dataframe = valor



    # 1) TOP 10 GOLEADORES

    def top_goleadores(self):
        datos = self.__dataframe.nlargest(10, "Goals")

        plt.figure(figsize=(10, 6))
        plt.barh(datos["Player"], datos["Goals"])
        plt.title("Top 10 Goleadores")
        plt.xlabel("Goles")
        plt.gca().invert_yaxis()
        plt.show()


    # 3) TOP ASISTIDORES 

    def top_asistidores(self):
        datos = self.__dataframe.nlargest(10, "Assists")

        plt.figure(figsize=(10, 6))
        plt.plot(datos["Player"], datos["Assists"], marker="o")
        plt.xticks(rotation=45, ha="right")
        plt.title("Top 10 Asistidores")
        plt.ylabel("Asistencias")
        plt.tight_layout()
        plt.show()


    # 4) GOLES POR PAÍS EN UN EQUIPO

    def goles_por_pais_en_equipos(self, equipo):
        datos = self.__dataframe[self.__dataframe["Team"] == equipo]

        if datos.empty:
            print(f"No se encontraron datos del equipo '{equipo}'.")
            return

        goles_por_pais = datos.groupby("Nation")["Goals"].sum()

        plt.figure(figsize=(8, 8))
        plt.pie(goles_por_pais, labels=goles_por_pais.index, autopct="%1.1f%%")
        plt.title(f"Goles por Nacionalidad en {equipo}")
        plt.show()



    # 5) Distribución de edades

    def distribucion_edades(self):
        plt.figure(figsize=(10, 6))
        plt.hist(self.__dataframe["Age"], bins=15)
        plt.title("Distribución de Edades en la Premier League")
        plt.xlabel("Edad")
        plt.ylabel("Cantidad de jugadores")
        plt.show()




    # 7) Tarjetas amarillas por equipo

    def amarillas_por_equipo(self):
        datos = self.__dataframe.groupby("Team")["Yellow_Cards"].sum().sort_values()

        plt.figure(figsize=(12, 6))
        plt.barh(datos.index, datos.values)
        plt.title("Tarjetas Amarillas por Equipo")
        plt.xlabel("Total de Tarjetas Amarillas")
        plt.tight_layout()
        plt.show()


    # 4) Goles por posición — TOP 10

    def goles_por_posicion(self):
        datos = (
            self.__dataframe.groupby("Position")["Goals"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        datos.plot(kind="bar")
        plt.title("Top 10 Posiciones con Más Goles")
        plt.ylabel("Goles Totales")
        plt.xticks(rotation=45)
        plt.show()



df = pd.read_csv("../src/data/processed/premier_clean.csv")

print(df.head(10))
