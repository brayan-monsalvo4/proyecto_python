import sqlite3

plantilla_registro_ventas = {"id_cliente":"", "codigo_producto" : "", "fecha_compra":"", "cantidad_productos":"", "costo_total":""}

class RegistroVentas:
    def __init__(self):
        pass
    
    def registrar_venta(self, venta):
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            instruccion = "INSERT INTO registro_ventas(id_cliente, codigo_producto, fecha_compra, cantidad_productos, costo_total) VALUES(?,?,?,?,?);"
            datos = (venta.get("id_cliente"), venta.get("codigo_producto"), venta.get("fecha_compra"), venta.get("cantidad_productos"), venta.get("costo_total"))
            cursor.execute(instruccion, datos)
            conexion.commit()

    def consultar_ventas(self, dato="", columna=""):
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            instruccion = f"SELECT * FROM registro_ventas" if (len(dato) == 0 and len(columna) == 0) else f"SELECT * FROM registro_ventas WHERE {columna} LIKE ?"
            cursor.execute(instruccion) if len(dato) == 0 else cursor.execute(instruccion, (f"%{dato}%",))
            resultados = cursor.fetchall()
            return resultados

    def eliminar_venta(self, id_venta):
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            instruccion = "DELETE FROM registro_ventas WHERE id_venta = ?"
            cursor.execute(instruccion, (id_venta,))

    def actualizar_venta(self, venta, id_venta):
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            instruccion = "UPDATE registro_ventas SET id_cliente = ?, codigo_producto = ?, fecha_compra = ?, cantidad_productos = ?, costo_total = ? WHERE id_venta = ?"
            datos = (venta.get("id_cliente"), venta.get("codigo_producto"), venta.get("fecha_compra"), venta.get("cantidad_productos"), venta.get("costo_total"), id_venta)
            cursor.execute(instruccion, datos)

    def existe_venta(self, id_venta):
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            instruccion = "SELECT * FROM registro_ventas WHERE id_venta = ?"
            cursor.execute(instruccion, (id_venta,))
            resultado = cursor.fetchall()
            return len(resultado) != 0
