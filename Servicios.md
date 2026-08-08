


class localidad:

#representa una localidad geografica en un municipio

    def__init__(self, nombre, latitud= None, longitud=None):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud

    def tiene_coordenandas(self)
    
    #devuelve True si la localidad tiene ubicacion geografica
    return self.latitud is not None and self.longitud is not None

class municipio
