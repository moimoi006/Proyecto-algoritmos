import requests
import matplotlib.pyplot as plt
from datetime import datetime

def formatear_valor(valor, sufijo: str = "") -> str:
    if valor is None:
        return "N/A"
    return f"{valor:.2f}{sufijo}"

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
    def agregar_localidad(self, localidad):
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
    def __init__(self, municipio_nombre: str, localidad: Localidad, temperatura: float, humedad: float, viento: float, codigo_clima: int):
        self.municipio_nombre = municipio_nombre
        self.localidad = localidad
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.codigo_clima = codigo_clima

    def obtener_descripcion_clima(self) -> str:
        code = self.codigo_clima
        if code == 0:
            return "Despejado"
        elif code == 1:
            return "Mayormente despejado"
        elif code == 2:
            return "Parcialmente nublado"
        elif code == 3:
            return "Nublado"
        elif code == 45:
            return "Niebla"
        elif code == 48:
            return "Niebla con escarcha"
        elif code == 51:
            return "Llovizna ligera"
        elif code == 53:
            return "Llovizna moderada"
        elif code == 55:
            return "Llovizna densa"
        elif code == 61:
            return "Lluvia ligera"
        elif code == 63:
            return "Lluvia moderada"
        elif code == 65:
            return "Lluvia fuerte"
        elif code == 80:
            return "Chubascos ligeros"
        elif code == 81:
            return "Chubascos moderados"
        elif code == 82:
            return "Chubascos violentos"
        elif code == 95:
            return "Tormenta eléctrica"
        elif code == 96:
            return "Tormenta eléctrica con granizo ligero"
        elif code == 99:
            return "Tormenta eléctrica con granizo fuerte"
        else:
            return f"Código {code}"
    def show(self):
        print("\n" + "="*50)
        print(" DETALLES METEOROLÓGICOS EN TIEMPO REAL")
        print("="*50)
        print(f"i.   Municipio: {self.municipio_nombre} | Localidad: {self.localidad.nombre}")
        print(f"ii.  Coordenadas: ({self.localidad.latitud}, {self.localidad.longitud})")
        print(f"iii. Temperatura actual: {self.temperatura} °C")
        print(f"iv.  Humedad relativa: {self.humedad} %")
        print(f"v.   Velocidad del viento: {self.viento} km/h")
        print(f"vi.  Estado del tiempo: {self.obtener_descripcion_clima()}")
        print("="*50)

class ServicioClima:
    def __init__(self, tiempo_espera: int = 15):
        self.url_base="https://api.open-meteo.com/v1/forecast"
        self.url_archive = "https://archive-api.open-meteo.com/v1/archive"
        self.tiempo_espera = tiempo_espera
    def motivo_error(self, respuesta) -> str:
        try:
            return respuesta.json().get("reason", respuesta.text)
        except ValueError:
            return respuesta.text
    def obtener_clima(self, municipio_nombre: str, localidad: Localidad) -> ClimaActual:
        if not localidad.tiene_coordenadas():
            print(f"\tError: La localidad '{localidad.nombre}' no posee coordenadas.")
            return None

        
        parametros = {
            "latitude": localidad.latitud,
            "longitude": localidad.longitud,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        }

        try:
            respuesta = requests.get(self.url_base, params=parametros, timeout=self.tiempo_espera)
        except requests.exceptions.Timeout:
            print(f"\tEl servicio de clima no respondió en {self.tiempo_espera} segundos.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"\tOcurrió un fallo en la red: {e}")
            return None

        if respuesta.status_code != 200:
            print(f"\tError al conectar con el servicio de clima (Status {respuesta.status_code}): {self.motivo_error(respuesta)}")
            return None

        try:
            datos = respuesta.json()
        except ValueError:
            print("\tEl servicio de clima devolvió una respuesta que no es JSON válido.")
            return None

        actual = datos.get("current", {})
        return ClimaActual(
            municipio_nombre=municipio_nombre,
            localidad=localidad,
            temperatura=actual.get("temperature_2m"),
            humedad=actual.get("relative_humidity_2m"),
            viento=actual.get("wind_speed_10m"),
            codigo_clima=actual.get("weather_code")
        )

    
    def obtener_historico(self, localidad: Localidad, fecha_inicio: str, fecha_fin: str) -> dict:
        if not localidad.tiene_coordenadas():
            print(f"\tError: La localidad '{localidad.nombre}' no posee coordenadas.")
            return None

        parametros = {
            "latitude": localidad.latitud,
            "longitude": localidad.longitud,
            "start_date": fecha_inicio,
            "end_date": fecha_fin,
            "daily": "temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_max",
            "timezone": "auto"
        }

        try:
            respuesta = requests.get(self.url_archive, params=parametros, timeout=self.tiempo_espera)
        except requests.exceptions.Timeout:
            print(f"\tEl servicio histórico no respondió en {self.tiempo_espera} segundos.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"\tOcurrió un fallo en la red: {e}")
            return None

        if respuesta.status_code != 200:
            print(f"\tError al conectar con el servicio histórico (Status {respuesta.status_code}): {self.motivo_error(respuesta)}")
            return None

        try:
            return respuesta.json()
        except ValueError:
            print("\tEl servicio histórico devolvió una respuesta que no es JSON válido.")
            return None

class RegistroDiario:
    def __init__(self, fecha: str, temperatura: float = None, humedad: float = None, precipitacion: float = None, viento: float = None):
        self.fecha = datetime.strptime(fecha, "%Y-%m-%d")
        self.temperatura = temperatura
        self.humedad = humedad
        self.precipitacion = precipitacion
        self.viento = viento
    def clave_mes(self) -> str:
        return self.fecha.strftime("%Y-%m")
    def clave_anio(self) -> str:
        return self.fecha.strftime("%Y")

class ResumenPeriodo:
    def __init__(self, clave: str):
        self.clave = clave
        self.registros = []
    def agregar_registro(self, registro: RegistroDiario):
        self.registros.append(registro)
    def valores(self, magnitud: str) -> list:
        resultado = []
        for r in self.registros:
            val = getattr(r,magnitud)
            if val is not None:
                resultado.append(val)
        return resultado
    def promedio(self, magnitud: str):
        valores = self.valores(magnitud)
        if not valores:
            return None
    
        suma = 0.0
        for v in valores:
            suma += v
        return suma / len(valores)
    def temperatura_promedio(self):
        return self.promedio("temperatura")
    def humedad_promedio(self):
        return self.promedio("humedad")
    def viento_promedio(self):
        return self.promedio("viento")
    def precipitacion_acumulada(self):
        valores = self.valores("precipitacion")
        if not valores:
            return None
    
        suma = 0.0
        for v in valores:
            suma += v
        return suma
    def show(self):
        print(
            f" - {self.clave} -> "
            f"Temp: {formatear_valor(self.temperatura_promedio(), '°C')} | "
            f"Humedad: {formatear_valor(self.humedad_promedio(), '%')} | "
            f"Precip. Acum: {formatear_valor(self.precipitacion_acumulada(), 'mm')} | "
            f"Viento: {formatear_valor(self.viento_promedio(), 'km/h')}"
        )

class HistorialLocalidad:
    def __init__(self, localidad: Localidad):
        self.localidad = localidad
        self.registros = []
    def valor_en(self, lista: list, indice: int):
        if indice < len(lista):
            return lista[indice]
        return None
    def cargar_desde_api(self, datos_historicos: dict) -> bool:
        daily = datos_historicos.get("daily", {})
        fechas = daily.get("time", [])
        if not fechas:
            return False
        temperaturas = daily.get("temperature_2m_mean", [])
        humedades = daily.get("relative_humidity_2m_mean", [])
        precipitaciones = daily.get("precipitation_sum", [])
        vientos = daily.get("wind_speed_10m_max", [])
        for i in range(len(fechas)):
            registro = RegistroDiario(
                fecha=fechas[i],
                temperatura=self.valor_en(temperaturas, i),
                humedad=self.valor_en(humedades, i),
                precipitacion=self.valor_en(precipitaciones, i),
                viento=self.valor_en(vientos, i)
            )
            self.registros.append(registro)
        return True
    def agrupar(self, por_anio: bool) -> list:
        resumenes = [] 
        for registro in self.registros:
            clave = registro.clave_anio() if por_anio else registro.clave_mes()
            resumen_encontrado = None
            for r in resumenes:
                if r.clave == clave:
                    resumen_encontrado = r
            if resumen_encontrado is None:
                resumen_encontrado = ResumenPeriodo(clave)
                resumenes.append(resumen_encontrado)
            resumen_encontrado.agregar_registro(registro)
        for i in range(len(resumenes)):
            for j in range(0, len(resumenes) - i - 1):
                if resumenes[j].clave > resumenes[j + 1].clave:
                    resumenes[j], resumenes[j + 1] = resumenes[j + 1], resumenes[j]
        return resumenes
        resultado = []
        for clave in sorted(resumenes):
            resultado.append(resumenes[clave])
        return resultado
    def resumenes_mensuales(self) -> list:
        return self.agrupar(False)
    def resumenes_anuales(self) -> list:
        return self.agrupar(True)
    def resumen_total(self) -> ResumenPeriodo:
        total = ResumenPeriodo("Período completo")
        for registro in self.registros:
            total.agregar_registro(registro)
        return total

class AnalizadorHistorico:
    @staticmethod
    def procesar_y_mostrar(localidad: Localidad, datos_historicos: dict):
        historial = HistorialLocalidad(localidad)
        if not historial.cargar_desde_api(datos_historicos):
            print("\nNo se encontraron datos en ese rango de fechas.")
            return

        print(f"\n================ ANÁLISIS HISTÓRICO: {localidad.nombre.upper()} ================")
        print("\n4.a. PROMEDIOS MENSUALES:")
        for resumen in historial.resumenes_mensuales():
            resumen.show()

        total = historial.resumen_total()
        print("\n4.b. PROMEDIOS GENERALES EN EL PERÍODO:")
        print(f" - Temperatura Promedio: {formatear_valor(total.temperatura_promedio(), ' °C')}")
        print(f" - Humedad Relativa Promedio: {formatear_valor(total.humedad_promedio(), ' %')}")
        print(f" - Precipitación Total Acumulada: {formatear_valor(total.precipitacion_acumulada(), ' mm')}")
        print(f" - Viento Promedio: {formatear_valor(total.viento_promedio(), ' km/h')}")

        anuales = historial.resumenes_anuales()
        print("\n4.c. REGISTROS POR AÑO:")
        AnalizadorHistorico.mostrar_extremo(anuales, "temperatura_promedio", "Año más caluroso", " °C", True)
        AnalizadorHistorico.mostrar_extremo(anuales, "temperatura_promedio", "Año más fresco", " °C", False)
        AnalizadorHistorico.mostrar_extremo(anuales, "precipitacion_acumulada", "Año con mayor precipitación", " mm", True)
        AnalizadorHistorico.mostrar_extremo(anuales, "humedad_promedio", "Año con mayor humedad", " %", True)

        AnalizadorHistorico.generar_grafico(anuales, localidad.nombre)

    @staticmethod
    def mostrar_extremo(resumenes: list, magnitud: str, etiqueta: str, sufijo: str, buscar_maximo: bool):
        validos = []
        for r in resumenes:
            if getattr(r, magnitud)() is not None:
                validos.append(r)
        if not validos:
            print(f" - {etiqueta}: N/A")
            return
        elegido = validos[0]
        for r in validos:
            val_actual = getattr(r, magnitud)()
            val_elegido = getattr(elegido, magnitud)()
    
            if buscar_maximo:
                if val_actual > val_elegido:
                    elegido = r
            else:
                if val_actual < val_elegido:
                    elegido = r
        valor_extremo = getattr(elegido, magnitud)()
        print(f" - {etiqueta}: {elegido.clave} ({formatear_valor(valor_extremo, sufijo)})")

    @staticmethod
    def valor_grafico(valor):
        if valor is None:
            return float("nan")
        return valor

    @staticmethod
    def generar_grafico(resumenes_anuales: list, nombre_localidad: str):
        anios = []
        temps=[]
        hums=[]
        precips=[]
        vientos=[]

        for r in resumenes_anuales:
            anios.append(r.clave)
            temps.append(AnalizadorHistorico.valor_grafico(r.temperatura_promedio()))
            hums.append(AnalizadorHistorico.valor_grafico(r.humedad_promedio()))
            precips.append(AnalizadorHistorico.valor_grafico(r.precipitacion_acumulada()))
            vientos.append(AnalizadorHistorico.valor_grafico(r.viento_promedio()))

        fig, axs = plt.subplots(2, 2, figsize=(10, 6))
        fig.suptitle(f"Evolución Anual del Clima - Localidad: {nombre_localidad}")

        axs[0, 0].plot(anios, temps, marker='o', color='r')
        axs[0, 0].set_title("Temperatura Promedio (°C)")
        axs[0, 0].grid(True)

        axs[0, 1].plot(anios, hums, marker='o', color='b')
        axs[0, 1].set_title("Humedad Relativa Promedio (%)")
        axs[0, 1].grid(True)

        axs[1, 0].bar(anios, precips, color='g')
        axs[1, 0].set_title("Precipitación Acumulada (mm)")
        axs[1, 0].grid(True)

        axs[1, 1].plot(anios, vientos, marker='o', color='orange')
        axs[1, 1].set_title("Velocidad del Viento Promedio (km/h)")
        axs[1, 1].grid(True)

        plt.tight_layout()
        plt.show()
