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
            raise RegistroExistente

        if self.existe_cliente(datos_cliente= {"correo" : cliente.get("correo")}):
            raise RegistroExistente 
        
        if self.existe_cliente(datos_cliente= {"telefono" : cliente.get("telefono")}):
            raise RegistroExistente 
        
        
        with sqlite3.connect("negocio.db") as conexion:
            datos = tuple(map(lambda dato: dato.strip(), cliente.values()))

            cursor = conexion.cursor()
            
            campos = ",".join( cliente.keys() )

            instruccion = f"insert into clientes({campos}) values(?,?,?,?,?,?,?,?,?);"
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

            respuesta = list()

            for registro in resultados:
                    respuesta.append({})

                    for columna, dato in zip( columnas, registro ):
                        respuesta[-1].update({ columna: dato })
                    
            return respuesta

    def eliminar_cliente(self, id_cliente):
        if not id_cliente:
            raise CamposVacios
            
        try:
            res = id_cliente.isdigit()
        except AttributeError as e:
            raise CodigoIncorrecto

        if not self.existe_cliente({"id_cliente":id_cliente}):
            raise RegistroNoExistente

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
            raise RegistroNoExistente

        with sqlite3.connect("negocio.db") as conexion:
            datos = list(map(lambda dato: dato.strip(), cliente.values()))
            cursor = conexion.cursor()

            #instruccion = "update clientes set nombre = ?, direccion = ?, correo = ?, telefono = ?, fecha_cumpleanos = ?, hobbies = ?, ocupacion = ?, info_primer_interaccion = ?, molestias = ? where id_cliente = ?"

            instruccion = self.__generar_update_dinamico(datos_cliente=cliente)

            print("instruccion:", instruccion)

            datos.append(id_cliente)

            cursor.execute(instruccion, datos)

    def existe_cliente(self, datos_cliente) -> bool :
        if not set(datos_cliente.keys()).issubset(columnas):
            print(datos_cliente.keys(), columnas.keys())
            raise CamposIncorrectos

        self.__verificar_datos(datos_cliente=datos_cliente)

        print(len(self.consultar_cliente(datos_cliente=datos_cliente)))

        return len(self.consultar_cliente(datos_cliente=datos_cliente)) != 0

    def __generar_select_dinamico(self, datos_cliente) -> str:
        sql = "select * from clientes"

        if datos_cliente:
            sql += " where "

            for indice, tupla in enumerate(datos_cliente.items()):
                sql += f" {tupla[0]} LIKE '%' || ? || '%' "

                if not indice == len(datos_cliente)-1:
                    sql += "and"

        sql += ";"

        return sql
    
    def __generar_update_dinamico(self, datos_cliente) -> str:
        sql = "update clientes set "

        for indice, campo in enumerate(datos_cliente.keys()):
            sql += f" {campo} = ?"

            if not indice == len(datos_cliente)-1:
                sql += ","

        sql += " where id_cliente = ?"

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