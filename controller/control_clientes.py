from excepciones.exceptions import *
from model.cliente import Clientes as cl
from model.cliente import columnas as columnas_cliente
import re
from datetime import datetime

class ControlClientes:
    __clientes = cl()
    plantilla_cliente = {"nombre":"", "direccion": "", "correo": "", "telefono":"", "fecha_cumpleanos": "", "hobbies": "", "ocupacion": "", "info_primer_interaccion":"", "molestias":""}
    columnas = ("id_cliente" ,"nombre", "direccion", "correo", "telefono", "fecha_cumpleanos", "hobbies", "ocupacion", "info_primer_interaccion", "molestias")  
    columnas_campos = ("nombre", "direccion", "correo", "telefono", "fecha_cumpleanos", "hobbies", "ocupacion", "info_primer_interaccion", "molestias")

    def __init__(self) -> None:
        return None

    def obtener_clientes(self, datos_cliente={}) -> list:
        self.verificar_datos(datos_cliente=datos_cliente)
        correccion = self.__corregir_datos(datos_cliente=datos_cliente)
        return self.__clientes.consultar_cliente(datos_cliente=correccion)

    def actualizar_cliente(self, cliente, id_cliente):
        self.verificar_datos(datos_cliente=cliente)
        correccion = self.__corregir_datos(datos_cliente=cliente)
        self.__clientes.actualizar_cliente(cliente=correccion, id_cliente=id_cliente)

    def registrar_cliente(self, cliente):
        self.verificar_datos(datos_cliente=cliente)
        correccion = self.__corregir_datos(datos_cliente=cliente)
        self.__clientes.registrar_cliente(cliente=correccion)

    def eliminar_cliente(self, id_cliente):
        self.verificar_datos(datos_cliente={"id_cliente": f"{id_cliente}"})

        self.__clientes.eliminar_cliente(id_cliente=id_cliente)

    def verificar_datos(self, datos_cliente):
        def validar_correo(correo):
            # Expresión regular para validar correo electrónico
            patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            # Validar correo electrónico
            if re.match(patron, correo):
                return True
            else:
                return False

        if len(datos_cliente) == 1:
            return None

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
                    int ( valor )

                if columna == "fecha_cumpleanos":
                    datetime.strptime(valor, "%d-%m-%Y")

                if columna == "codigo_postal":
                    int ( valor )
                
                if columna == "correo":

                    if not validar_correo(correo=valor):
                        raise ValueError
                
            except ValueError:
                raise DatosIncorrectos
            
    def __corregir_datos(self, datos_cliente) -> dict:
        corregido = dict()

        if len(datos_cliente) == 1:
            for clave, valor in datos_cliente.items():
                corregido.update({ clave : valor })

                return corregido

        if not datos_cliente:
            return {}

        for clave, valor in datos_cliente.items():
            if clave == "correo":
                corregido.update({ "correo" : valor})
                continue

            if clave == "fecha_cumpleanos":
                fecha = datetime.strptime(valor, "%d-%m-%Y")
                fecha = str( fecha.strftime("%d-%m-%Y") )
                corregido.update( {"fecha_cumpleanos" : fecha })
                continue

            corregido.update( { clave : valor.upper() } )

        return corregido