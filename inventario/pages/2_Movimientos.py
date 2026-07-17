import streamlit as st
import pandas as pd
from database import *

conn = conectar()

st.title("Movimientos")

productos = pd.read_sql(
    "SELECT * FROM productos",
    conn
)

if not productos.empty:

    producto = st.selectbox(
        "Producto",
        productos["nombre"]
    )

    tipo = st.selectbox(
        "Tipo",
        ["ENTRADA", "SALIDA"]
    )

    cantidad = st.number_input(
        "Cantidad",
        min_value=1
    )

    if st.button("Registrar"):

        fila = productos[
            productos["nombre"] == producto
        ].iloc[0]

        nuevo_stock = fila["stock"]

        if tipo == "ENTRADA":
            nuevo_stock += cantidad
        else:
            nuevo_stock -= cantidad

        conn.execute(
            """
            UPDATE productos
            SET stock=?
            WHERE id=?
            """,
            (nuevo_stock, fila["id"])
        )

        conn.execute(
            """
            INSERT INTO movimientos
            (producto_id,tipo,cantidad)
            VALUES(?,?,?)
            """,
            (fila["id"], tipo, cantidad)
        )

        conn.commit()

        st.success("Movimiento registrado")
        st.rerun()

movs = pd.read_sql(
    "SELECT * FROM movimientos",
    conn
)

st.dataframe(
    movs,
    use_container_width=True
)