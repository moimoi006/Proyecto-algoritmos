import json
from pathlib import Path
from datetime import datetime
from servicios import Localidad, Municipio, ServicioClima, AnalizadorHistorico

RUTA_DATOS = Path(__file__).resolve().parent / "zonas_caracas.json"

class App:

    def __init__(self):
        self.municipios=[]
        self.servicio_clima= ServicioClima()
        self.consultas_sesion = []
        self.cargar_datos()

    def registrar_consulta(self, clima_obj):
        for idx, consulta in enumerate(self.consultas_sesion):
            if (consulta.municipio_nombre == clima_obj.municipio_nombre and
                    consulta.localidad.nombre == clima_obj.localidad.nombre):
                self.consultas_sesion[idx] = clima_obj
                return
        self.consultas_sesion.append(clima_obj)

    def buscar_municipio(self, nombre_municipio: str) -> Municipio:
        for mun in self.municipios:
            if mun.nombre.lower() == nombre_municipio.lower():
                return mun
        return None
    
    def cargar_datos(self):
        try:
            with open(RUTA_DATOS, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except FileNotFoundError:
            print(f"\nError: No se encontro el archivo '{RUTA_DATOS}'.")
            return
        except json.JSONDecodeError as e:
            print(f"\nError: El archivo '{RUTA_DATOS}' no contiene un JSON valido: {e}")
            return
        except OSError as e:
            print(f"\nError: No se pudo leer el archivo '{RUTA_DATOS}': {e}")
            return

        if not isinstance(datos, dict):
            print(f"\nError: Se esperaba un objeto de municipios en '{RUTA_DATOS}'.")
            return

        for nombre_mun, localidades in datos.items():
            municipio_obj = self.buscar_municipio(nombre_mun)
            if municipio_obj is None:
                municipio_obj = Municipio(nombre=nombre_mun)
                self.municipios.append(municipio_obj)
            for item in localidades:
                nombre_loc = item.get("localidad", None)
                if nombre_loc is None:
                    print(f"Aviso: se omitio un registro sin nombre de localidad en '{nombre_mun}'.")
                    continue

                localidad_obj = Localidad(
                    nombre=nombre_loc,
                    latitud=item.get("latitud", None),
                    longitud=item.get("longitud", None)
                )
                municipio_obj.agregar_localidad(localidad_obj)

        print("Datos cargados con exito en la aplicacion!")
        self.mostrar_reporte_general()


    def mostrar_reporte_general(self):
        print("\n" + "=" * 50)
        print(" Reporte de Municipios y Localidades (Caracas)")
        print("=" * 50)
        for mun in self.municipios:
            mun.show()
            print("=" * 40)

    def consultar_clima_tiempo_real(self):
        print("\n--- CONSULTA DEL CLIMA EN TIEMPO REAL ---")
        print("1. Buscar por Municipio y Localidad")
        print("2. Búsqueda directa por nombre de Localidad")
        sub_op = input("Seleccione una opción: ").strip()

        if sub_op == "1":
            print("\nMunicipios disponibles:")
            for idx, mun in enumerate(self.municipios, 1):
                print(f"{idx}. {mun.nombre}")

            try:
                sel_m = int(input("\nSeleccione el número del Municipio: ")) - 1
                if 0 <= sel_m < len(self.municipios):
                    mun_sel = self.municipios[sel_m]
                    locs_validas = mun_sel.obtener_localidades_con_coordenadas()

                    if not locs_validas:
                        print(f"\nEl municipio {mun_sel.nombre} no tiene localidades con coordenadas válidas.")
                        return

                    print(f"\nLocalidades con coordenadas en {mun_sel.nombre}:")
                    for idx_l, loc in enumerate(locs_validas, 1):
                        print(f"{idx_l}. {loc.nombre}")

                    sel_l = int(input("\nSeleccione la Localidad: ")) - 1
                    if 0 <= sel_l < len(locs_validas):
                        loc_sel = locs_validas[sel_l]
                        clima_obj = self.servicio_clima.obtener_clima(mun_sel.nombre, loc_sel)
                        if clima_obj:
                            clima_obj.show()
                            self.registrar_consulta(clima_obj)
                    else:
                        print("\nSelección de localidad inválida.")
                else:
                    print("\nSelección de municipio inválida.")
            except ValueError:
                print("\nError: Debe ingresar un número entero.")

        elif sub_op == "2":
            query = input("\nIngrese el nombre de la localidad (o parte de él): ").strip().lower()
            coincidencias = []
            for mun in self.municipios:
                for loc in mun.localidades:
                    if query in loc.nombre.lower():
                        coincidencias.append((mun, loc))

            if not coincidencias:
                print("\nNo se encontraron coincidencias.")
                return

            print(f"\nCoincidencias encontradas ({len(coincidencias)}):")
            for idx in range(len(coincidencias)):
                item = coincidencias[idx]
                mun = item[0]
                loc = item[1]
                estado = "Con Coordenadas" if loc.tiene_coordenadas() else "Sin Coordenadas"
                print(f"{idx + 1}. {loc.nombre} ({mun.nombre}) - [{estado}]")

            try:
                sel = int(input("\nSeleccione la localidad deseada: ")) - 1
                if 0 <= sel < len(coincidencias):
                    item_sel = coincidencias[sel]
                    mun_sel = item_sel[0]
                    loc_sel = item_sel[1]
                    if not loc_sel.tiene_coordenadas():
                        print(f"\nError: '{loc_sel.nombre}' no tiene coordenadas para consulta en tiempo real.")
                        return
                    clima_obj = self.servicio_clima.obtener_clima(mun_sel.nombre, loc_sel)
                    if clima_obj:
                        clima_obj.show()
                        self.registrar_consulta(clima_obj)
                else:
                    print("\nSelección inválida.")
            except ValueError:
                print("\nError: Debe ingresar un número entero.")


    def mostrar_reporte_estadisticas(self):
        print("\n" + "="*50)
        print(" MÓDULO DE REPORTES Y ESTADÍSTICAS")
        print("="*50)


        consultas_validas = []
        for c in self.consultas_sesion:
            if c.temperatura is not None:
                consultas_validas.append(c)

        if consultas_validas:
            mas_calida = consultas_validas[0]
            mas_fria = consultas_validas[0]
            suma_temperaturas = 0.0
            for consulta in consultas_validas:
                suma_temperaturas += consulta.temperatura
                if consulta.temperatura > mas_calida.temperatura:
                    mas_calida = consulta
                if consulta.temperatura < mas_fria.temperatura:
                    mas_fria = consulta
            print("\n3.a. RANKING DE TEMPERATURA EN LA SESIÓN:")
            print(f" -> MÁS CÁLIDA: {mas_calida.localidad.nombre} ({mas_calida.municipio_nombre}) con {mas_calida.temperatura} °C")
            print(f" -> MÁS FRÍA:   {mas_fria.localidad.nombre} ({mas_fria.municipio_nombre}) con {mas_fria.temperatura} °C")


            prom = suma_temperaturas / len(consultas_validas)
            print(f"\n3.c. PROMEDIO GENERAL DE LA SESIÓN: {prom:.2f} °C ({len(consultas_validas)} localidades consultadas)")
        else:
            print("\n3.a y 3.c: No se han realizado consultas de clima en esta sesión aún.")


        print("\n3.b. COBERTURA GEOGRÁFICA (LOCALIDADES SIN COORDENADAS REGISTRADAS):")
        for mun in self.municipios:
            sin_coords = mun.obtener_localidades_sin_coordenadas()
            print(f"\nMunicipio {mun.nombre} ({len(sin_coords)} sin coordenadas):")
            if sin_coords:
                for loc in sin_coords:
                    print(f"  - {loc.nombre}")
            else:
                print("  (Todas las localidades tienen coordenadas)")


    def consultar_historico(self):
        print("\n--- CONSULTA HISTÓRICA ---")
        locs_validas = []
        for mun in self.municipios:
            for loc in mun.obtener_localidades_con_coordenadas():
                locs_validas.append((mun, loc))

        if not locs_validas:
            print("\nNo existen localidades con coordenadas disponibles.")
            return

        print("Localidades disponibles para consulta histórica:")
        for idx in range(len(locs_validas)):
            item = locs_validas[idx]
            mun = item[0]
            loc = item[1]
            print(f"{idx + 1}. {loc.nombre} ({mun.nombre})")

        try:
            sel = int(input("\nSeleccione el número de la localidad: ")) - 1
            if 0 <= sel < len(locs_validas):
                item_sel = locs_validas[sel]
                mun_sel = item_sel[0]
                loc_sel = item_sel[1]
                fecha_inicio = input("Ingrese fecha de inicio (AAAA-MM-DD, ej: 2022-01-01): ").strip()
                fecha_fin = input("Ingrese fecha de fin (AAAA-MM-DD, ej: 2023-12-31): ").strip()
                try:
                    f_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
                    f_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
                    
                    if f_inicio > f_fin:
                        print("\nError: La fecha de inicio no puede ser posterior a la fecha de fin.")
                        return
                except ValueError:
                    print("\nError: El formato de fecha debe ser estrictamente AAAA-MM-DD.")
                    return
                print(f"\nConsultando datos históricos para '{loc_sel.nombre}'...")
                datos = self.servicio_clima.obtener_historico(loc_sel, fecha_inicio, fecha_fin)
                if datos:
                    AnalizadorHistorico.procesar_y_mostrar(loc_sel, datos)
            else:
                print("\nSelección inválida.")
        except ValueError:
            print("\nError: Debe ingresar un número entero.")

    def start(self):
        while True:
            print("\n" + "="*40)
            print("Sistema meteorológico de Caracas")
            print("="*40)
            print("1. Ver reporte general de Municipios y Localidades")
            print("2. Consultar clima actual de una localidad")
            print("3. Módulo de Reportes y Estadísticas")
            print("4. Consulta Histórica (Rango de fechas)")
            print("0. Salir del programa")
            print("="*40)

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.mostrar_reporte_general()
            elif opcion == "2":
                self.consultar_clima_tiempo_real()
            elif opcion == "3":
                self.mostrar_reporte_estadisticas()
            elif opcion == "4":
                self.consultar_historico()
            elif opcion == "0":
                print("\nGracias por utilizar el sistema! Hasta luego.")
                break
            else:
                print("\nOpción invalida. Intente de nuevo.")

if __name__ == "__main__":
    app = App()
    app.start()
