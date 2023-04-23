import sqlite3

plantilla_promocion = {"codigo_producto": "", "fecha_inicio": "", "fecha_fin": "", "duracion_promocion": "", "porcentaje_descuento": "", "tipo_promocion": ""}
codigo_producto = "codigo_producto"


class Promocion:
    def __init__(self):
        return None

    def registrar_promocion(self, promocion):
        if promocion.keys() != plantilla_promocion.keys():
            raise Exception("Error registrar_promocion(): los campos no coinciden!")

        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            datos = (
                promocion.get("codigo_producto"), 
                promocion.get("fecha_inicio"), 
                promocion.get("fecha_fin"),
                promocion.get("duracion_promocion"), 
                promocion.get("porcentaje_descuento"), 
                promocion.get("tipo_promocion"),
            )
            instruccion = "INSERT INTO promociones(codigo_producto, fecha_inicio, fecha_fin, duracion_promocion, porcentaje_descuento, tipo_promocion) VALUES (?, ?, ?, ?, ?, ?);"
            cursor.execute(instruccion, datos)
            conexion.commit()

    def consultar_promocion(self, dato="", columna="") -> list:
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            instruccion = f"SELECT * FROM promociones" if (len(dato) == 0 and len(columna) == 0) else f"SELECT * FROM promociones WHERE {columna} LIKE ?"
            cursor.execute(instruccion) if len(dato) == 0 else cursor.execute(instruccion, (f"%{dato}%",))
            resultados = cursor.fetchall()
            return resultados

    def eliminar_promocion(self, id_promocion, codigo_producto):
        if len(id_promocion) == 0 and len(codigo_producto) == 0:
            raise Exception("Error eliminar_promocion(): el id y el código de producto están vacíos!")

        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            instruccion = "DELETE FROM promociones WHERE id_promocion = ? AND codigo_producto = ?;"
            cursor.execute(instruccion, (id_promocion, codigo_producto,))

    def actualizar_promocion(self, promocion, id_promocion):
        if promocion.keys() != plantilla_promocion.keys():
            raise Exception("Error actualizar_promocion(): los campos no coinciden!")

        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            instruccion = "UPDATE promociones SET codigo_producto = ?, fecha_inicio = ?, fecha_fin = ?, duracion_promocion = ?, porcentaje_descuento = ?, tipo_promocion = ? WHERE id_promocion = ?;"
            datos = (
                promocion.get("codigo_producto"), 
                promocion.get("fecha_inicio"), 
                promocion.get("fecha_fin"),
                promocion.get("duracion_promocion"), 
                promocion.get("porcentaje_descuento"), 
                promocion.get("tipo_promocion"), 
                id_promocion
            )
            cursor.execute(instruccion, datos)

    def existe_promocion(self, dato, columna) -> bool:
        if len(dato) == 0 and len(columna) == 0:
            raise Exception("Error existe_promocion(): dato y columna estan vacios")
        
        resultado = self.consultar_promocion(dato=dato, columna=columna)

        return len(resultado) != 0

