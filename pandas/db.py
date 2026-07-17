import sqlite3
import pandas as pd


def crear_base_datos():
    # conectar sqlite
    conn = sqlite3.connect("basedatos.db")

    # crear tabla
    conn.execute("""
    CREATE TABLE IF NOT EXISTS ventas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        fecha TEXT,
        total REAL
    )
    """)

    # insertar datos de ejemplo
    datos_ejemplo = [
        ("Cliente A", "2024-01-15", 100.0),
        ("Cliente B", "2024-02-20", 150.0),
        ("Cliente A", "2024-03-10", 200.0),
        ("Cliente C", "2024-01-25", 50.0),
        ("Cliente B", "2024-02-28", 120.0)
    ]

    conn.executemany("""
    INSERT INTO ventas (cliente, fecha, total)
    VALUES (?, ?, ?)
    """, datos_ejemplo)

    conn.commit()
    conn.close()


def obtener_datos():
    # conectar sqlite
    conn = sqlite3.connect("basedatos.db")

    query = """
    SELECT
        Nombre,
        Fecha as fecha,
        Tarifa
        Observaciones
    FROM produccion
    """

    # leer datos
    df = pd.read_sql_query(query, conn)   
    df = df.rename(columns={
        "Nombre": "CLIENTES",
        "Fecha": "ABRIL"
        })
    conn.close()

    return df