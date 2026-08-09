class Localidad:
    def __init__(self, nombre: str, latitud: float = None, longitud: float = None):
        self.nombre=nombre
        self.latitud=latitud
        self.longitud=longitud
    def tiene_coordenadas(self) -> bool:
        if self.latitud is not None and self.longitud is not None:
            return True
        else:
            return False
    def show(self):
        if self.tiene_coordenadas():
            coord_str = f"{self.latitud}, {self.longitud}"
        else:
            coord_str = "Sin Coordenadas"
        print(
            f"\tLocalidad: {self.nombre}\n"
            f"\tCoordenadas: {coord_str}"
        )

class Municipio:
    def __init__(self, nombre: str):
        self.nombre=nombre
        self.localidades = []
    def agregar_localidades(self, localidad: Localidad):
        self.localidades.append(localidad)
    def total_localidades(self) -> int:
        return len(self.localidades)
    def obtener_localidades_con_coordenadas(self) -> list:
        con_coordenadas= []
        for loc in self.localidades:
            if loc.tiene_coordenadas():
                con_coordenadas.append(loc)
        return con_coordenadas
    def obtener_localidades_sin_coordenadas(self) -> list:
        sin_coordenadas = []
        for loc in self.localidades:
            if not loc.tiene_coordenadas():
                sin_coordenadas.append(loc)
        return sin_coordenadas
    def porcentaje_con_coordenadas(self) -> float:
        total = self.total_localidades()
        if total == 0:
            return 0.0
        con_coord = len(self.obtener_localidades_con_coordenadas())
        return (con_coord / total) * 100
    def show(self):
        print(
            f"Municipio: {self.nombre}\n"
            f"\tTotal localidades: {self.total_localidades()}\n"
            f"\tCon coordenadas: {len(self.obtener_localidades_con_coordenadas())}\n"
            f"\tSin coordenadas: {len(self.obtener_localidades_sin_coordenadas())}\n"
            f"\tPorcentaje con coordenadas: {self.porcentaje_con_coordenadas(): .2f}%"
        )

class ClimaActual:
    def __init__(self, localidad: Localidad, temperatura: float, humedad: float, viento:float, codigo_clima: int):
        self.localidad=localidad
        self.temperatura=temperatura
        self.humedad=humedad
        self.viento=viento
        self.codigo_clima=codigo_clima
    def show(self):
        print(
            f" Clima Actual en {self.localidad.nombre}\n"
            f"\tTemperatura: {self.temperatura} °C\n"
            f"\tHumedad relativa: {self.humedad} %\n"
            f"\tVelocidad del viento: {self.viento} km/h\n"
            f"\tCodigo de Clima: {self.codigo_clima}"
        )

class ServicioClima:
    def __init__(self):
        self.url_base="https://api.open-meteo.com/v1/forecast"
    def obtener_clima(self, localidad: Localidad) -> ClimaActual:
        if not localidad.tiene_coordenadas():
            print(f"\tError: La localidad '{localidad.nombre}' no posee coordenadas.")
            return None
        parametros = {
            "latitude": localidad.latitud,
            "longitude": localidad.longitud,
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "weather_code"]
        }
        try:
            respuesta=request.get(self.url_base, params=parametros)
            if respuesta.status_code == 200:
                datos=respuesta.json()
                actual=datos["current"]
                return ClimaActual(
                    localidad=localidad,
                    temperatura=actual["temperatura_2m"],
                    humedad=actual["relative_humidity_2m"],
                    viento= actual["wind_speed_10m"],
                    codigo_clima=actual["weather_code"]
                )
            else:
                print("\tError al conectar con el servicio de clima.")
                return None
        except Exception as e:
            print(f"\tOcurrio un fallo en la red: {e}")
            return None
    