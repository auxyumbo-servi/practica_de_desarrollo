import streamlit as st
import pandas as pd
from database import *

conn = conectar()

st.title("Reportes")

df = pd.read_sql(
    "SELECT * FROM productos",
    conn
)

st.dataframe(df)

excel = "inventario.xlsx"

df.to_excel(
    excel,
    index=False
)

with open(excel, "rb") as f:

    st.download_button(
        "Exportar Excel",
        f,
        file_name=excel
    )