import json
from servicios import Localidad, Municipio, ServicioClima, AnalizadorHistorico

class App:

    def __init__(self):
        self.municipios=[]
        self.servicio_clima= ServicioClima()
        self.analizador_historico = AnalizadorHistorico()
        self.consultas_sesion = []
        self.cargar_datos()

    def buscar_municipio(self, nombre_municipio: str) -> Municipio:
        for mun in self.municipios:
            if mun.nombre.lower() == nombre_municipio.lower():
                return mun
        return None
    
    def cargar_datos(self):
        try:
            with open("zonas_caracas.json", "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            for nombre_mun, localidades in datos.items():
                municipio_obj = self.buscar_municipio(nombre_mun)
                if municipio_obj is None:
                    municipio_obj = Municipio(nombre=nombre_mun)
                    self.municipios.append(municipio_obj)
                for item in localidades:
                    lat = item.get("latitud", None)
                    lng = item.get("longitud", None)

                    localidad_obj = Localidad(
                        nombre=item["localidad"],
                        latitud=lat,
                        longitud=lng
                )
                    municipio_obj.agregar_localidad(localidad_obj)
            print("Datos cargados con exito en la aplicacion!")
            self.mostrar_reporte_general()

        except FileNotFoundError:
            print("\nError: No se encontro el archivo 'zonas_caracas.json'.")
        except Exception as e:
            print(f"\nOcurrio un error al cargar los datos: {e}")
        
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

                            self.consultas_sesion.append(clima_obj)
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
            for idx, (mun, loc) in enumerate(coincidencias, 1):
                estado = "Con Coordenadas" if loc.tiene_coordenadas() else "Sin Coordenadas"
                print(f"{idx}. {loc.nombre} ({mun.nombre}) - [{estado}]")

            try:
                sel = int(input("\nSeleccione la localidad deseada: ")) - 1
                if 0 <= sel < len(coincidencias):
                    mun_sel, loc_sel = coincidencias[sel]
                    if not loc_sel.tiene_coordenadas():
                        print(f"\nError: '{loc_sel.nombre}' no tiene coordenadas para consulta en tiempo real.")
                        return
                    clima_obj = self.servicio_clima.obtener_clima(mun_sel.nombre, loc_sel)
                    if clima_obj:
                        clima_obj.show()
                        # === NUEVO: Guarda la consulta en la sesión ===
                        self.consultas_sesion.append(clima_obj)
                else:
                    print("\nSelección inválida.")
            except ValueError:
                print("\nError: Debe ingresar un número entero.")


    def mostrar_reporte_estadisticas(self):
        print("\n" + "="*50)
        print(" MÓDULO DE REPORTES Y ESTADÍSTICAS")
        print("="*50)


        if self.consultas_sesion:
            mas_calida = max(self.consultas_sesion, key=lambda c: c.temperatura)
            mas_fria = min(self.consultas_sesion, key=lambda c: c.temperatura)
            print("\n3.a. RANKING DE TEMPERATURA EN LA SESIÓN:")
            print(f" -> MÁS CÁLIDA: {mas_calida.localidad.nombre} ({mas_calida.municipio_nombre}) con {mas_calida.temperatura} °C")
            print(f" -> MÁS FRÍA:   {mas_fria.localidad.nombre} ({mas_fria.municipio_nombre}) con {mas_fria.temperatura} °C")


            prom = sum(c.temperatura for c in self.consultas_sesion) / len(self.consultas_sesion)
            print(f"\n3.c. PROMEDIO GENERAL DE LA SESIÓN: {prom:.2f} °C ({len(self.consultas_sesion)} consultas)")
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
        for idx, (mun, loc) in enumerate(locs_validas, 1):
            print(f"{idx}. {loc.nombre} ({mun.nombre})")

        try:
            sel = int(input("\nSeleccione el número de la localidad: ")) - 1
            if 0 <= sel < len(locs_validas):
                mun_sel, loc_sel = locs_validas[sel]
                fecha_inicio = input("Ingrese fecha de inicio (AAAA-MM-DD, ej: 2022-01-01): ").strip()
                fecha_fin = input("Ingrese fecha de fin (AAAA-MM-DD, ej: 2023-12-31): ").strip()

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
                break # CORRECCIÓN DE ERROR: detiene la ejecución del menú
            else:
                print("\nOpción invalida. Intente de nuevo.")

if __name__ == "__main__":
    app = App()
    app.start()
