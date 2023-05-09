from excepciones.exceptions import *
from model.cliente import Clientes as cl
from model.cliente import columnas as columnas_cliente
import re


class ControlClientes:
    __clientes = cl()

    def __init__(self) -> None:
        return None

    def obtener_clientes(self, datos_cliente={}) -> list:
        self.verificar_datos(datos_cliente=datos_cliente)
        return self.__clientes.consultar_cliente(datos_cliente=datos_cliente)

    def actualizar_cliente(self, cliente, id_cliente):
        self.verificar_datos(datos_cliente=cliente)
        self.__clientes.actualizar_cliente(cliente=cliente, id_cliente=id_cliente)

    def registrar_cliente(self, cliente):
        self.verificar_datos(datos_cliente=cliente)
        self.__clientes.registrar_cliente(cliente=cliente)

    def eliminar_cliente(self, id_cliente):
        self.verificar_datos(datos_cliente={"id_cliente": f"{id_cliente}"})

        self.__clientes.eliminar_cliente(id_cliente=id_cliente)

    def verificar_datos(self, datos_cliente):
        lista_comprobacion = list()

        try:
            lista_comprobacion = list(map(lambda dato: dato.strip(), datos_cliente.values()))
        except AttributeError:
            raise DatosIncorrectos
        
        lista_comprobacion = list( filter(lambda dato: len(dato) != 0, lista_comprobacion) )

        if len(datos_cliente) != len(lista_comprobacion):
            raise CamposVacios
        
        for columna, valor in datos_cliente.items():
            try:
                if columna == "telefono":
                    grupos = re.split(r"-| ", valor)

                    for grupo in grupos:
                        int ( grupo )

                if columna == "fecha_cumpleanos":
                    dia, mes, anio = valor.split("-")

                    int( dia )
                    int( mes )
                    int( anio )
                
            except ValueError:
                raise DatosIncorrectos