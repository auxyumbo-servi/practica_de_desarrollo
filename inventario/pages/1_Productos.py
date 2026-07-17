import streamlit as st
import pandas as pd
from database import *

conn = conectar()

st.title("Productos")

nombre = st.text_input("Nombre")

empresa=st.text_input("Empresa")

stock = st.number_input(
    "Stock Inicial",
    min_value=0
)

if st.button("Guardar"):

    conn.execute(
        """
        INSERT INTO productos
        (nombre,stock,empresa)
        VALUES(?,?,?)
        """,
        (nombre, stock, empresa)
    )

    conn.commit()
    st.success("Guardado")
    st.rerun()

df = pd.read_sql(
    "SELECT * FROM productos",
    conn
)

st.dataframe(
    df,
    use_container_width=True
)

if not df.empty:

    eliminar = st.selectbox(
        "Eliminar producto",
        df["id"]
    )

    if st.button("Eliminar"):
        conn.execute(
            "DELETE FROM productos WHERE id=?",
            (int(eliminar),)
        )
        conn.commit()
        st.rerun()