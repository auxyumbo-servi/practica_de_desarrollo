
def transformar(df):
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()

    required = ["CLIENTES", "OBSERVACION"]

    for c in required:
        if c not in df.columns:
            raise ValueError(f"Falta columna {c}")

    df["CLIENTES"] = df["CLIENTES"].astype(str).str.strip()
    df["OBSERVACION"] = df["OBSERVACION"].astype(str).str.lower()

    # SOLO CLASIFICACIÓN (NO SUMAS)
    df["Nombre_final"] = df["CLIENTES"]

    df["ES_LODO"] = df["OBSERVACION"].str.contains("lodo", na=False)

    return df