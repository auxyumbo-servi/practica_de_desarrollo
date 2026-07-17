from reglas import clasificar_fila


def transformar(df):

    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()

    # ==========================
    # VALIDACIÓN
    # ==========================
    required_cols = ["CLIENTES", "Observaciones"]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Falta columna {col}. Columnas: {df.columns.tolist()}")

    # ==========================
    # LIMPIEZA
    # ==========================
    df["CLIENTES"] = df["CLIENTES"].astype(str).str.strip()
    df["Observaciones"] = (
        df["Observaciones"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # ==========================
    # APLICAR REGLAS
    # ==========================
    df["Nombre_final"] = df.apply(
        lambda row: clasificar_fila(row),
        axis=1
    )

    return df