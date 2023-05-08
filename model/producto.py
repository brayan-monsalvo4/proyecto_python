import sqlite3
from excepciones.exceptions import *

plantilla_producto = {"nombre":"", "descripcion":"", "precio":"", "cantidad_stock":"", "duracion_producto":"", "beneficios":""}

columnas = ("codigo_producto", "nombre", "descripcion", "precio", "cantidad_stock", "duracion_producto", "beneficios")

class Productos:
    def __init__(self):
        return None

    def registrar_producto(self, producto):
        if set(producto.keys()) != set(plantilla_producto.keys()):
            raise CamposIncorrectos

        self.__comprobar_datos_vacios(datos_producto=producto)

        if self.existe_producto(datos_producto=producto):
            raise ProductoExistente

        with sqlite3.connect("negocio.db") as conexion:
            datos = tuple(map(lambda dato: dato.strip(), producto.values()))

            cursor = conexion.cursor()
            instruccion = "insert into productos(nombre, descripcion, precio, cantidad_stock, duracion_producto, beneficios) values(?,?,?,?,?,?);"
            cursor.execute(instruccion, datos)
            conexion.commit()
    
    def consultar_producto(self, datos_producto={}) -> list:
        if len(datos_producto) != 0 and not set(datos_producto.keys()).issubset(columnas):
            raise CamposIncorrectos
        
        self.__comprobar_datos_vacios(datos_producto=datos_producto)
        
        with sqlite3.connect("negocio.db") as conexion:
            datos = tuple(map(lambda dato: dato.strip(), datos_producto.values()))

            cursor = conexion.cursor()

            instruccion = self.__generar_select_dinamico(datos_producto=datos_producto)

            cursor.execute(instruccion, datos)

            resultados = cursor.fetchall()

            return resultados

    def eliminar_producto(self, codigo_producto):
        if not codigo_producto:
            raise CamposVacios
        
        if not codigo_producto.isdigit():
            raise CodigoIncorrecto
        
        if not self.existe_producto({"codigo_producto":codigo_producto}):\
            raise ProductoNoExistente

        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()

            instruccion = "delete from productos where codigo_producto = ?"

            cursor.execute(instruccion, (codigo_producto,))

    def actualizar_producto(self, producto, codigo_producto) :
        if set(producto.keys()) != set(plantilla_producto.keys()):
            raise CamposIncorrectos
        
        if not codigo_producto.isdigit():
            raise CodigoIncorrecto
        
        self.__comprobar_datos_vacios(datos_producto=producto)

        if not self.existe_producto({"codigo_producto":codigo_producto}):
            raise ProductoNoExistente
        
        with sqlite3.connect("negocio.db") as conexion:
            datos = list(map(lambda dato: dato.strip(), producto.values()))
            cursor = conexion.cursor()

            instruccion = "update productos set nombre = ?, descripcion = ?, precio = ?, cantidad_stock = ?, duracion_producto = ?, beneficios = ? where codigo_producto = ?"

            datos.append(codigo_producto)

            cursor.execute(instruccion, datos)
        
    def existe_producto(self, datos_producto) -> bool:
        if not set(datos_producto.keys()).issubset(columnas):
            raise CamposIncorrectos

        self.__comprobar_datos_vacios(datos_producto=datos_producto)
        
        return len( self.consultar_producto(datos_producto=datos_producto)) != 0

    def __generar_select_dinamico(self, datos_producto):
        sql = "select * from productos"

        if datos_producto:
            sql +=" where"

            for indice, tupla in enumerate(datos_producto.items()):
                sql += f" {tupla[0]} = ?  "

                if not indice == len(datos_producto)-1:
                    sql += "and"

        sql += ";"

        return sql

    def __comprobar_datos_vacios(self, datos_producto):
        lista_comprobacion = list(map(lambda dato: dato.strip(), datos_producto.values()))
        lista_comprobacion = list( filter(lambda dato: len(dato) != 0, lista_comprobacion) )

        if len(datos_producto) != len(lista_comprobacion):
            raise CamposVacios