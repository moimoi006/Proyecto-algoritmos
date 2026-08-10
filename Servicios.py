import requests 
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
2
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
    
    CODIGOS_WMO = {
        0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado", 3: "Nublado",
        45: "Niebla", 48: "Niebla con escarcha", 51: "Llovizna ligera", 53: "Llovizna moderada",
        55: "Llovizna densa", 61: "Lluvia ligera", 63: "Lluvia moderada", 65: "Lluvia fuerte",
        80: "Chubascos ligeros", 81: "Chubascos moderados", 82: "Chubascos violentos",
        95: "Tormenta eléctrica", 96: "Tormenta eléctrica con granizo ligero", 99: "Tormenta eléctrica con granizo fuerte"
        }

def __init__(self, municipio_nombre: str, localidad: Localidad, temperatura: float, humedad: float, viento: float, codigo_clima: int):
        self.municipio_nombre = municipio_nombre
        self.localidad = localidad
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.codigo_clima = codigo_clima

def obtener_descripcion_clima(self) -> str:
        return self.CODIGOS_WMO.get(self.codigo_clima, f"Código {self.codigo_clima}")

    
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
    def __init__(self):
        self.url_base="https://api.open-meteo.com/v1/forecast"
        self.url_archive = "https://archive-api.open-meteo.com/v1/archive"
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
            respuesta = requests.get(self.url_base, params=parametros)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                actual = datos.get("current", {})
                return ClimaActual(
                    municipio_nombre=municipio_nombre,
                    localidad=localidad,
                    temperatura=actual.get("temperature_2m"),
                    humedad=actual.get("relative_humidity_2m"),
                    viento=actual.get("wind_speed_10m"),
                    codigo_clima=actual.get("weather_code")
                )
            else:
                print(f"\tError al conectar con el servicio de clima (Status {respuesta.status_code}).")
                return None
        except Exception as e:
            print(f"\tOcurrió un fallo en la red: {e}")
            return None

    
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
            respuesta = requests.get(self.url_archive, params=parametros)
            if respuesta.status_code == 200:
                return respuesta.json()
            else:
                print(f"\tError al conectar con el servicio histórico (Status {respuesta.status_code}).")
                return None
        except Exception as e:
            print(f"\tOcurrió un fallo en la red: {e}")
            return None

class AnalizadorHistorico:
    @staticmethod
    def procesar_y_mostrar(localidad: Localidad, datos_historicos: dict):
        daily = datos_historicos.get("daily", {})
        fechas = daily.get("time", [])
        temperaturas = daily.get("temperature_2m_mean", [])
        humedades = daily.get("relative_humidity_2m_mean", [])
        precipitaciones = daily.get("precipitation_sum", [])
        vientos = daily.get("wind_speed_10m_max", [])

        if not fechas:
            print("\nNo se encontraron datos en ese rango de fechas.")
            return

        datos_mes = defaultdict(lambda: {"temp": [], "hum": [], "precip": [], "viento": []})
        datos_anio = defaultdict(lambda: {"temp": [], "hum": [], "precip": [], "viento": []})

        for i in range(len(fechas)):
            dt = datetime.strptime(fechas[i], "%Y-%m-%d")
            clave_mes = dt.strftime("%Y-%m")
            clave_anio = dt.strftime("%Y")
            
            t = temperaturas[i] if temperaturas[i] is not None else 0
            h = humedades[i] if humedades[i] is not None else 0
            p = precipitaciones[i] if precipitaciones[i] is not None else 0
            v = vientos[i] if vientos[i] is not None else 0

            datos_mes[clave_mes]["temp"].append(t)
            datos_mes[clave_mes]["hum"].append(h)
            datos_mes[clave_mes]["precip"].append(p)
            datos_mes[clave_mes]["viento"].append(v)

            datos_anio[clave_anio]["temp"].append(t)
            datos_anio[clave_anio]["hum"].append(h)
            datos_anio[clave_anio]["precip"].append(p)
            datos_anio[clave_anio]["viento"].append(v)

        print(f"\n================ ANÁLISIS HISTÓRICO: {localidad.nombre.upper()} ================")
        print("\n4.a. PROMEDIOS MENSUALES:")
        for mes, vals in sorted(datos_mes.items()):
            t_p = sum(vals["temp"]) / len(vals["temp"]) if vals["temp"] else 0
            h_p = sum(vals["hum"]) / len(vals["hum"]) if vals["hum"] else 0
            p_a = sum(vals["precip"])
            v_p = sum(vals["viento"]) / len(vals["viento"]) if vals["viento"] else 0
            print(f" - {mes} -> Temp: {t_p:.2f}°C | Humedad: {h_p:.2f}% | Precip. Acum: {p_a:.2f}mm | Viento: {v_p:.2f}km/h")

        all_t = [t for t in temperaturas if t is not None]
        all_h = [h for h in humedades if h is not None]
        all_p = [p for p in precipitaciones if p is not None]
        all_v = [v for v in vientos if v is not None]

        print("\n4.b. PROMEDIOS GENERALES EN EL PERÍODO:")
        print(f" - Temperatura Promedio: {sum(all_t)/len(all_t):.2f} °C" if all_t else " - Temp: N/A")
        print(f" - Humedad Relativa Promedio: {sum(all_h)/len(all_h):.2f} %" if all_h else " - Humedad: N/A")
        print(f" - Precipitación Total Acumulada: {sum(all_p):.2f} mm" if all_p else " - Precipitación: N/A")
        print(f" - Viento Promedio: {sum(all_v)/len(all_v):.2f} km/h" if all_v else " - Viento: N/A")

        resumen_anios = {}
        for anio, vals in datos_anio.items():
            resumen_anios[anio] = {
                "temp_prom": sum(vals["temp"]) / len(vals["temp"]) if vals["temp"] else 0,
                "hum_prom": sum(vals["hum"]) / len(vals["hum"]) if vals["hum"] else 0,
                "precip_acum": sum(vals["precip"]),
                "viento_prom": sum(vals["viento"]) / len(vals["viento"]) if vals["viento"] else 0
            }

        c_caluroso = max(resumen_anios.items(), key=lambda x: x[1]["temp_prom"])[0]
        c_fresco = min(resumen_anios.items(), key=lambda x: x[1]["temp_prom"])[0]
        c_precip = max(resumen_anios.items(), key=lambda x: x[1]["precip_acum"])[0]
        c_humedo = max(resumen_anios.items(), key=lambda x: x[1]["hum_prom"])[0]

        print("\n4.c. REGISTROS POR AÑO:")
        print(f" - Año más caluroso: {c_caluroso} ({resumen_anios[c_caluroso]['temp_prom']:.2f} °C)")
        print(f" - Año más fresco: {c_fresco} ({resumen_anios[c_fresco]['temp_prom']:.2f} °C)")
        print(f" - Año con mayor precipitación: {c_precip} ({resumen_anios[c_precip]['precip_acum']:.2f} mm)")
        print(f" - Año con mayor humedad: {c_humedo} ({resumen_anios[c_humedo]['hum_prom']:.2f} %)")

        AnalizadorHistorico.generar_grafico(resumen_anios, localidad.nombre)

    @staticmethod
    def generar_grafico(resumen_anios: dict, nombre_localidad: str):
        anios = sorted(resumen_anios.keys())
        temps = [resumen_anios[a]["temp_prom"] for a in anios]
        hums = [resumen_anios[a]["hum_prom"] for a in anios]
        precips = [resumen_anios[a]["precip_acum"] for a in anios]
        vientos = [resumen_anios[a]["viento_prom"] for a in anios]

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
