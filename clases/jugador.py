class JugadorPremier:
    def __init__(self, nombre, equipo, nacionalidad, posicion, edad, goles, asistencias, minutos):
        self.__nombre = nombre
        self.__equipo = equipo
        self.__nacionalidad = nacionalidad
        self.__posicion = posicion
        self.__edad = edad
        self.__goles = goles
        self.__asistencias = asistencias
        self.__minutos = minutos

    # nombre
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

    # equipo
    @property
    def equipo(self):
        return self.__equipo

    @equipo.setter
    def equipo(self, valor):
        self.__equipo = valor

    # nacionalidad
    @property
    def nacionalidad(self):
        return self.__nacionalidad

    @nacionalidad.setter
    def nacionalidad(self, valor):
        self.__nacionalidad = valor

    # posicion
    @property
    def posicion(self):
        return self.__posicion

    @posicion.setter
    def posicion(self, valor):
        self.__posicion = valor

    # edad
    @property
    def edad(self):
        return self.__edad

    @edad.setter
    def edad(self, valor):
        self.__edad = valor

    # goles
    @property
    def goles(self):
        return self.__goles

    @goles.setter
    def goles(self, valor):
        self.__goles = valor

    # asistencias
    @property
    def asistencias(self):
        return self.__asistencias

    @asistencias.setter
    def asistencias(self, valor):
        self.__asistencias = valor

    # minutos
    @property
    def minutos(self):
        return self.__minutos

    @minutos.setter
    def minutos(self, valor):
        self.__minutos = valor

