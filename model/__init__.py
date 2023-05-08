import sqlite3

# Conectando a la base de datos (si no existe, la crea en este momento)
conn = sqlite3.connect('negocio.db')

# Creando una tabla 'productos'
conn.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        codigo_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        precio REAL NOT NULL,
        cantidad_stock INTEGER NOT NULL,
        duracion_producto INTEGER NOT NULL,
        beneficios TEXT NOT NULL
    );
''')
             
conn.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT NOT NULL,
                correo TEXT NOT NULL,
                telefono TEXT NOT NULL,
                fecha_cumpleanos TEXT NOT NULL,
                hobbies TEXT NOT NULL,
                ocupacion TEXT NOT NULL,
                info_primer_interaccion TEXT NOT NULL,
                molestias TEXT NOT NULL
            );
''')
             

# Creando una tabla 'promociones'
conn.execute('''
    CREATE TABLE IF NOT EXISTS promociones (
        id_promocion INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_producto INTEGER NOT NULL,
        fecha_inicio text NOT NULL,
        fecha_fin text NOT NULL,
        duracion_promocion INTEGER NOT NULL,
        porcentaje_descuento INTEGER NOT NULL,
        tipo_promocion TEXT CHECK(tipo_promocion IN ('mensual', 'semanal')) NOT NULL,
        FOREIGN KEY(codigo_producto) REFERENCES productos(codigo_producto)
    );
''')
             
conn.execute('''
    CREATE TABLE IF NOT EXISTS registro_ventas (
        id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        codigo_producto INTEGER NOT NULL,
        fecha_compra text NOT NULL,
        cantidad_productos INTEGER NOT NULL,
        costo_total REAL NOT NULL,
        FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente),
        FOREIGN KEY(codigo_producto) REFERENCES productos(codigo_producto)
    );
''')


# Cerrando la conexión
conn.close()
