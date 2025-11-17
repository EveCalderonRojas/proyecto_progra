class Equipo:
    def __init__(self, nombre, liga, jugadores):
        self.__nombre = nombre
        self.__liga = liga
        self.__jugadores = jugadores

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

    @property
    def liga(self):
        return self.__liga

    @liga.setter
    def liga(self, valor):
        self.__liga = valor

    @property
    def jugadores(self):
        return self.__jugadores

    @jugadores.setter
    def jugadores(self, valor):
        self.__jugadores = valor


