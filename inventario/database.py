import sqlite3

def conectar():
    conn = sqlite3.connect("data/inventario.db", check_same_thread=False)
    return conn

def crear_tablas():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS categorias(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS productos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        categoria_id INTEGER,
        stock INTEGER DEFAULT 0,
        empresa TEXT,
        FOREIGN KEY(categoria_id)
        REFERENCES categorias(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS movimientos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER,
        tipo TEXT,
        cantidad INTEGER,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(producto_id)
        REFERENCES productos(id)
    )
    """)

    conn.commit()
    conn.close()