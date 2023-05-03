import sqlite3


plantilla_cliente = {"nombre":"", "direccion": "", "correo": "", "telefono":"", "fecha_cumpleanos": "", "hobbies": "", "ocupacion": "", "info_primer_interaccion":"", "molestias":""}

columnas = ("nombre", "direccion", "correo", "telefono", "fecha_cumpleanos", "hobbies", "ocupacion", "info_primer_interaccion", "molestias")


class Clientes:
    def __init__ (self):
        return None
    
    def registrar_cliente(self, cliente):
        if(cliente.keys() != plantilla_cliente.keys()):
            raise Exception("Error registrar_cliente(): los campos no coinciden!")
        
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            datos = (
                cliente.get("nombre"), 
                cliente.get("direccion"), 
                cliente.get("correo"),
                cliente.get("telefono"), 
                cliente.get("fecha_cumpleanos"), 
                cliente.get("hobbies"), 
                cliente.get("ocupacion"),
                cliente.get("info_primer_interaccion"),
                cliente.get("molestias")
            )
            
            instruccion = "insert into clientes(nombre, direccion, correo, telefono, fecha_cumpleanos, hobbies, ocupacion, info_primer_interaccion, molestias) values(?,?,?,?,?,?,?,?,?);"
            cursor.execute(instruccion, datos)
            conexion.commit()

    def consultar_cliente(self, dato="", columna="") -> list:
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()
            
            instruccion = f"select * from clientes" if (len(dato) == 0 and len(columna) == 0) else f"select * from clientes where {columna} like %?%"
            
            cursor.execute(instruccion) if len(dato) == 0 else cursor.execute(instruccion, (f"%{dato}%",))
            resultados = cursor.fetchall()

            return resultados
        
    def eliminar_cliente(self, id_cliente, nombre_cliente):
        if len(id_cliente) == 0 and len(nombre_cliente) == 0:
            raise Exception("Error eliminar_cliente(): el id y el nombre estan vacios!")
        
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()

            instruccion = "delete from clientes where id_cliente = ? and nombre = ?"

            cursor.execute(instruccion, (id_cliente, nombre_cliente,))

    def actualizar_cliente(self, cliente, id_cliente) :
        if cliente.keys() != plantilla_cliente.keys():
            raise Exception("Error actualizar_cliente(): los campos no coinciden!")
        
        with sqlite3.connect("negocio.db") as conexion:
            cursor = conexion.cursor()

            instruccion = "update clientes set nombre = ?, direccion = ?, correo = ?, telefono = ?, fecha_cumpleanos = ?, hobbies = ?, ocupacion = ?, info_primer_interaccion = ?, molestias = ? where id_cliente = ?"
            datos = (cliente.get("nombre"), cliente.get("direccion"), cliente.get("correo"),cliente.get("telefono"), cliente.get("fecha_cumpleanos"), cliente.get("hobbies"), cliente.get("ocupacion"), cliente.get("info_primer_interaccion"), cliente.get("molestias"), id_cliente)

            cursor.execute(instruccion, datos)

    def existe_cliente(self, dato, columna) -> bool :
        if len(dato) == 0 and len(columna) == 0:
            raise Exception("Error existe_cliente(): id_cliente y nombre vacios!")
        
        resultados = self.consultar_cliente(dato=dato, columna=columna)

        return len(resultados) != 0
