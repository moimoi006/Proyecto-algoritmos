import json
from servicios import Localidad, Municipio, ServicioClima

class App:
    def __init__(self):
        self.municipios=[]
        self.servicio_clima= ServicioClima()
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
        except FileNotFoundError:
            print("Error: No se encontro el archivo 'zonas_caracas.json'.")
        except Exception as e:
            print(f"Ocurrio un error al cargar los datos: {e}")
    def monstrar_reporte_general(self):
        print("\n" + "=" * 50)
        print(" Reporte de Municipios y Localidades (Caracas)")
        print("=" * 50)
        for mun in self.municipios:
            mun.show()
            print("=" * 40)
    def consultar_clima_localidad(self):
        print("\n Consulta de clima en tiempo real")
        nombre_loc = input("Ingrese el nombre de la localidad a consultar: ").strip()
        localidad_encontrada= None
        for mun in self.municipios:
            for loc in mun.localidades:
                if loc.nombre.strip().lower() == nombre_loc.lower():
                    localidad_encontrada = loc
                    break
            if localidad_encontrada:
                break
        if localidad_encontrada:
            if not localidad_encontrada.tiene_coordenadas():
                print(f"\n\tLa localidad '{localidad_encontrada.nombre}' existe pero no posee coordenadas.")
            else:
                clima_obj= self.servicio_clima.obtener_clima(localidad_encontrada)
                if clima_obj:
                    print()
                    clima_obj.show()
        else:
            print(f"\n\tNo se encontro la localidad '{nombre_loc}' en el sistema")

    def start(self):
        while True:
            print("\n" + "=" *40)
            print("Sistema meteorologico de caracas")
            print("=" * 40)
            print("1. Ver reporte general de Municipios y Localidades")
            print("2. Consultar clima actual de una localidad")
            print("0. Salir del programa")
            print("=" * 40)

            opcion = input("Seleccione una opcion: ").strip()

            if opcion == "1":
                self.monstrar_reporte_general()
            elif opcion == "2":
                self.consultar_clima_localidad()
            elif opcion == "0":
                print("\nGracias por utilizar el sistema! Hasta luego.")
            else:
                print("\n Opcion invalida. Intente de nuevo.")

if __name__ == "__main__":
    app = App()
    app.start()