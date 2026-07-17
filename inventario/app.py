import streamlit as st
import pandas as pd
from database import *

crear_tablas()

st.set_page_config(
    page_title="Inventario",
    page_icon="📦",
    layout="wide"
)

conn = conectar()

st.title("📦 Sistema de Inventario")

productos = pd.read_sql(
    "SELECT * FROM productos",
    conn
)

movimientos = pd.read_sql(
    "SELECT * FROM movimientos",
    conn
)

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Productos",
        len(productos)
    )

with c2:
    st.metric(
        "Stock Total",
        productos["stock"].sum()
        if not productos.empty else 0
    )

with c3:
    st.metric(
        "Movimientos",
        len(movimientos)
    )

st.info(
    "Utiliza el menú lateral para administrar productos y movimientos."
)