from excepciones.exceptions import *
from model.producto import Productos as prod
from model.producto import columnas as columnas_producto



class ControlProductos:
    __productos = prod()

    def __init__(self) -> None:
        return None

    def obtener_productos(self, datos_producto={}) -> list:
        self.verificar_datos(datos_producto=datos_producto)
        return self.__productos.consultar_producto(datos_producto=datos_producto)

    def actualizar_producto(self, producto, codigo_producto):
        self.verificar_datos(datos_producto=producto)
        self.__productos.actualizar_producto(producto=producto, codigo_producto=codigo_producto)

    def registrar_producto(self, producto):
        self.verificar_datos(producto)
        self.__productos.registrar_producto(producto=producto)

    def eliminar_producto(self, codigo_producto):
        self.verificar_datos(datos_producto={"codigo_producto":f"{codigo_producto}"})

        self.__productos.eliminar_producto(codigo_producto=codigo_producto)

    def verificar_datos(self, datos_producto):
        lista_comprobacion = list()

        try:
            lista_comprobacion = list(map(lambda dato: dato.strip(), datos_producto.values()))
        except AttributeError:
            raise DatosIncorrectos
        
        lista_comprobacion = list( filter(lambda dato: len(dato) != 0, lista_comprobacion) )

        if len(datos_producto) != len(lista_comprobacion):
            raise CamposVacios
        
        for columna, valor in datos_producto.items():
            try:
                if columna == "codigo_producto":
                    int( valor )
                
                if columna == "precio":
                    float( valor )
                
                if columna == "cantidad_stock":
                    int( valor )

                if columna == "duracion_producto":
                    int( valor )

            except ValueError:
                raise DatosIncorrectos