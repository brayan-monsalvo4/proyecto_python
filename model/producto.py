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
        
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            datos = (producto.get("nombre"), producto.get("descripcion"),producto.get("precio"), producto.get("cantidad_stock"), producto.get("duracion_producto"), producto.get("beneficios"))
            instruccion = "insert into productos(nombre, descripcion, precio, cantidad_stock, duracion_producto, beneficios) values(?,?,?,?,?,?);"
            cursor.execute(instruccion, datos)
            conexion.commit()

    def consultar_producto(self, dato="", columna="") -> list:
        if len(columna) != 0 and columna not in columnas:
            raise CamposIncorrectos

        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            
            instruccion = f"select * from productos" if (len(dato) == 0 and len(columna) == 0) else f"select * from productos where {columna} like ?"
            
            cursor.execute(instruccion) if len(dato) == 0 else cursor.execute(instruccion, (f"%{dato}%",))
            resultados = cursor.fetchall()

            return resultados
        
    def eliminar_producto(self, codigo_producto, nombre):
        if len(codigo_producto) == 0 and len(nombre) == 0:
            raise CamposVacios
        
        if not codigo_producto.isdigit():
            raise CodigoIncorrecto

        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()

            instruccion = "delete from productos where codigo_producto = ? and nombre = ?"

            cursor.execute(instruccion, (codigo_producto, nombre,))

    def actualizar_producto(self, producto, codigo_producto) :
        if not set(producto.keys()).issubset(columnas):
            raise CamposIncorrectos
        
        if not codigo_producto.isdigit():
            raise CodigoIncorrecto
        
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()

            instruccion = "update productos set nombre = ?, descripcion = ?, precio = ?, cantidad_stock = ?, duracion_producto = ?, beneficios = ? where codigo_producto = ?"
            datos = (producto.get("nombre"), producto.get("descripcion"),producto.get("precio"), producto.get("cantidad_stock"), producto.get("duracion_producto"), producto.get("beneficios"), codigo_producto)

            cursor.execute(instruccion, datos)

    def existe_producto(self, dato, columna) -> bool :
        if len(dato) == 0 and len(columna) == 0:
            raise Exception("Error existe_producto(): el dato y la columna estan vacios!")
        
        resultados = self.consultar_producto(dato=dato, columna=columna)

        return len(resultados) != 0
