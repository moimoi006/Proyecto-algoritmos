


class localidad:

#representa una localidad geografica en un municipio

    def__init__(self, nombre, latitud= None, longitud=None):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud

    def tiene_coordenandas(self):
    
#devuelve True si la localidad tiene ubicacion geografica
    
        return self.latitud is not None and self.longitud is not None

class municipio:

#representa a un municipio que contiene varias localidades

    def__init__(self, nombre):
        self.nombre = nombre
        self.localidades = []

    def agregar_localidad(self, localidad):
        self.localidades.append(localidad)

    def total_localidades(self):
        return len(self.localidades)

    def localidades_con_coordenadas(self):
        return[loc for loc in self.localidades if loc.tiene_coordenadas()]
    
    def localidades_sin_coordenadas(self):
        return[loc for loc in self.localidades if not loc.tiene_coordenadas()]

    def porcentaje_con_coordenadas(self):
        if self.total_localidades() == 0
            return 0.0
        return (len(self.localidades_con_coordenadas())/ self.total_localidades()) * 100


class climaactual:
