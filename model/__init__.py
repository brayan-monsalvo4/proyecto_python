import sqlite3

# Conectando a la base de datos (si no existe, la crea en este momento)
conn = sqlite3.connect('negocio.db')

# Creando una tabla 'productos'
conn.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        codigo_producto INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        descripcion TEXT,
        precio REAL NOT NULL,
        cantidad_stock INTEGER NOT NULL,
        duracion_producto INTEGER
    );
''')
             
conn.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT,
                correo TEXT NOT NULL,
                telefono TEXT NOT NULL,
                fecha_cumpleanos TEXT NOT NULL,
                hobbies TEXT,
                ocupacion TEXT
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
