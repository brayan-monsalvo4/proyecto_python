import sqlite3

plantilla_producto = {"nombre":"", "descripcion":"", "precio":"", "cantidad_stock":"", "duracion_producto":"", "beneficios":""}

class producto:
    def __init__(self):
        return None

    def registrar_producto(self, producto):
        if(producto.keys() != plantilla_producto.keys()):
            raise Exception("Error registrar_producto(): los campos no coinciden!")
    
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            datos = (producto.get("nombre"), producto.get("descripcion"),producto.get("precio"), producto.get("cantidad_stock"), producto.get("duracion_producto"))
            instruccion = "insert into productos(nombre, descripcion, precio, cantidad_stock, duracion_producto) values(?,?,?,?,?);"
            cursor.execute(instruccion, datos)
            conexion.commit()

    def consultar_producto(self, dato="", columna="") -> list:
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            
            instruccion = f"select * from productos" if (len(dato) == 0 and len(columna) == 0) else f"select * from productos where {columna} like ?"
            
            cursor.execute(instruccion) if len(dato) == 0 else cursor.execute(instruccion, (f"%{dato}%",))
            resultados = cursor.fetchall()

            return resultados
        
    def eliminar_producto(self, codigo_producto, nombre):
        if len(codigo_producto) == 0 and len(nombre) == 0:
            raise Exception("Error eliminar_producto(): el codigo y nombre estan vacios!")
        
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()

            instruccion = "delete from productos where codigo_producto = ? and nombre = ?"

            cursor.execute(instruccion, (codigo_producto, nombre,))

    def actualizar_producto(self, producto, codigo_producto) :
        if producto.keys() != plantilla_producto.keys():
            raise Exception("Error actualizar_producto(): los campos no coinciden!")
        
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()

            instruccion = "update productos set nombre = ?, descripcion = ?, precio = ?, cantidad_stock = ?, duracion_producto = ? where codigo_producto = ?"
            datos = (producto.get("nombre"), producto.get("descripcion"),producto.get("precio"), producto.get("cantidad_stock"), producto.get("duracion_producto"), codigo_producto)

            cursor.execute(instruccion, datos)

    def existe_producto(self, dato, columna) -> bool :
        if len(dato) == 0 and len(columna) == 0:
            raise Exception("Error existe_producto(): el dato y la columna estan vacios!")
        
        resultados = self.consultar_producto(dato=dato, columna=columna)

        return len(resultados) != 0
