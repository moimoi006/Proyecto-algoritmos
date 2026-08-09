import json
from servicios import Localidad, Municipio, ServicioClima

class App:
    def __init__(self):
        self.municipios=[]
        self.servicio_clima