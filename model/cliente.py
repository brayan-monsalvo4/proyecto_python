import sqlite3
from excepciones.exceptions import *

plantilla_cliente = {"nombre":"", "direccion": "", "correo": "", "telefono":"", "fecha_cumpleanos": "", "hobbies": "", "ocupacion": "", "info_primer_interaccion":"", "molestias":""}

columnas = ("id_cliente" ,"nombre", "direccion", "correo", "telefono", "fecha_cumpleanos", "hobbies", "ocupacion", "info_primer_interaccion", "molestias")


class Clientes:
    def __init__ (self):
        return None
    
    def registrar_cliente(self, cliente):
        if set(cliente.keys()) != set(plantilla_cliente.keys()):
            raise CamposIncorrectos
        
        self.__verificar_datos(datos_cliente=cliente)

        if self.existe_cliente(datos_cliente=cliente):
            raise ProductoExistente
        
        with sqlite3.connect("negocio.db") as conexion:
            datos = tuple(map(lambda dato: dato.strip(), cliente.values()))

            cursor = conexion.cursor()
            
            instruccion = "insert into clientes(nombre, direccion, correo, telefono, fecha_cumpleanos, hobbies, ocupacion, info_primer_interaccion, molestias) values(?,?,?,?,?,?,?,?,?);"
            cursor.execute(instruccion, datos)
            conexion.commit()

    def consultar_cliente(self, datos_cliente={}) -> list:
        if len(datos_cliente) != 0 and not set(datos_cliente.keys()).issubset(columnas):
            raise CamposIncorrectos

        self.__verificar_datos(datos_cliente=datos_cliente)


        with sqlite3.connect("negocio.db") as conexion:
            datos = tuple(map(lambda dato: dato.strip(), datos_cliente.values()))

            cursor = conexion.cursor()
            
            instruccion = self.__generar_select_dinamico(datos_cliente=datos_cliente)

            cursor.execute(instruccion, datos)

            resultados = cursor.fetchall()

            return resultados
        
    def eliminar_cliente(self, id_cliente):
        if not id_cliente:
            raise CamposVacios
            
        try:
            res = id_cliente.isdigit()
        except AttributeError as e:
            raise CodigoIncorrecto

        if not self.existe_cliente({"id_cliente":id_cliente}):
            raise ProductoExistente

        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()

            instruccion = "delete from clientes where id_cliente = ?"

            cursor.execute(instruccion, (id_cliente,))

    def actualizar_cliente(self, cliente, id_cliente) :
        if set(cliente.keys()) != set(plantilla_cliente.keys()):
            raise CamposIncorrectos

        try:
            res = id_cliente.isdigit()
        except AttributeError as e:
            raise CodigoIncorrecto   

        self.__verificar_datos(datos_cliente=cliente)

        if not self.existe_cliente({"id_cliente":id_cliente}):
            raise ProductoNoExistente

        with sqlite3.connect("negocio.db") as conexion:
            datos = list(map(lambda dato: dato.strip(), cliente.values()))
            cursor = conexion.cursor()

            instruccion = "update clientes set nombre = ?, direccion = ?, correo = ?, telefono = ?, fecha_cumpleanos = ?, hobbies = ?, ocupacion = ?, info_primer_interaccion = ?, molestias = ? where id_cliente = ?"

            datos.append(id_cliente)

            cursor.execute(instruccion, datos)

    def existe_cliente(self, datos_cliente) -> bool :
        if not set(datos_cliente.keys()).issubset(columnas):
            print(datos_cliente.keys(), columnas.keys())
            raise CamposIncorrectos

        self.__verificar_datos(datos_cliente=datos_cliente)

        return len(self.consultar_cliente(datos_cliente=datos_cliente)) != 0

    def __generar_select_dinamico(self, datos_cliente):
        sql = "select * from clientes"

        if datos_cliente:
            sql += " where"

            for indice, tupla in enumerate(datos_cliente.items()):
                sql += f" {tupla[0]} = ? "

                if not indice == len(datos_cliente)-1:
                    sql += "and"

        sql += ";"

        return sql

    def __verificar_datos(self, datos_cliente):
        lista_comprobacion = list()

        try:
            lista_comprobacion = list(map(lambda dato: dato.strip(), datos_cliente.values()))
        except AttributeError:
            raise DatosIncorrectos
        
        lista_comprobacion = list(filter(lambda dato: len(dato) != 0, lista_comprobacion))

        if len(datos_cliente) != len(lista_comprobacion):
            raise CamposVacios