


class Localidad:

#representa una localidad geografica en un municipio

    def__init__(self, nombre, latitud= None, longitud=None):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud

    def tiene_coordenandas(self):
    
#devuelve True si la localidad tiene ubicacion geografica
    
        return self.latitud is not None and self.longitud is not None

class Municipio:

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


class climaActual:

#guarda los datos del clima de un momento especifico

    def__init__(self, temperatura, humedad, viento, codigo_clima)
        self.temperatura = temperatura 
        self.humedad = humedad
        self.viento = viento
        self.estado_tiempo = self.traducir_codigo_clima(codigo_clima)
    
    @staticmethod
    def traducir_codigo_clima(codigo):
    
    #convierte los codigos numericos de open-meteo a español

        codigos = {
             0: "despejado",
            1: "Casi despejado", 2: "Parcialmente nublado", 3: "Nublado",
            45: "Niebla", 48: "Niebla con escarcha",
            51: "Llovizna ligera", 53: "Llovizna moderada", 55: "Llovizna fuerte",
            61: "Lluvia ligera", 63: "Lluvia moderada", 65: "Lluvia fuerte",
            80: "Chubascos ligeros", 81: "Chubascos moderados", 82: "Chubascos muy fuertes",
            95: "Tormenta eléctrica"
        }
       
        return codigos.get(codigo, "desconocido")

class consultarealizada:

#Guarda las consultas hechas durante la sesión para sacar las estadísticas.

    def __init__(self, municipio, localidad, clima):
        self.municipio = municipio
        self.localidad = localidad
        self.clima = clima


class Lectorjson:

    @staticmethod
    def cargar_municipios(ruta_archivo):
        municipios =[]
        with open (ruta_archivo, 'r', encoding = 'utf-8') as archivo:
            datos = json.load(archivo)
            elementos = datos if isinstance(datos, list) else datos.get("municipios", [])

            for item_m in elementos:
                muni = Municipio(item_m["municipio"])
                for item_l in item_m.get("localidades", [])
                    lat = item_l.get("latitud")
                    lon =item_l.get("longitud")
                    loc = Localidad(
                        nombre =item_l["nombre"]
                        latitud=float(lat) if lat is not None else None,
                        longitud=float(lon) if lon is not None else None
                    )
                    muni.agregar_localidad(loc)
                municipios.append(muni)
        return municipios

classservicioclima:

#conecta con el servidor de open-meteo para buscar el clima

    @staticmethod
    def obtener_clima_actual(latitud, longitud)
        url =  "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitud,
            "longitude": longitud,
            "start_date": fecha_inicio,
            "end_date": fecha_fin,
            "daily": ["temperature_2m_mean", "relative_humidity_2m_mean", "precipitation_sum", "wind_speed_10m_max"]
            "timezone": "America/Caracas"
        }
        resp = request.get(url,params=params, timeout=15)

class procesadorhistorico: