import pandas as pd
from mapeo import normalizar_cliente


def aplicar_reglas_clientes(df):
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()

    # ==========================
    # VALIDACIÓN
    # ==========================
    if "CLIENTES" not in df.columns:
        raise ValueError("Falta columna CLIENTES")

    if "OBSERVACION" not in df.columns:
        raise ValueError("Falta columna OBSERVACION")

    meses = ["ABRIL", "MARZO", "FEBRERO", "ENERO"]

    for m in meses:
        if m not in df.columns:
            df[m] = 0

        df[m] = pd.to_numeric(df[m], errors="coerce").fillna(0)

    # ==========================
    # NORMALIZACIÓN
    # ==========================
    df["CLIENTE_STD"] = df["CLIENTES"].apply(normalizar_cliente)
    df["OBSERVACION"] = df["OBSERVACION"].astype(str).str.upper()

    df["ES_LODO"] = df["OBSERVACION"].str.contains("LODO", na=False)

    # ==========================
    # RESULTADO FINAL
    # ==========================
    resultado = []

    # ==========================
    # CLIENTE X (TU REGLA)
    # ==========================
    cx = df[df["CLIENTE_STD"] == "CARTONES AMERICA S.A"]

    if not cx.empty:

        lodo = cx[cx["ES_LODO"] == True][meses].sum()
        otros = cx[cx["ES_LODO"] == False][meses].sum()

        resultado.append({
            "CLIENTES": "CCARTONES AMERICA S.A - LODO)",
            **lodo.to_dict()
        })

        resultado.append({
            "CLIENTES": "CARTEONES AMERICA S.A",
            **otros.to_dict()
        })

    # ==========================
    # OTROS CLIENTES (SIN REGLAS ESPECIALES)
    # ==========================
    otros_df = df[df["CLIENTE_STD"] != "CLIENTE X"]

    if not otros_df.empty:
        agrupado = otros_df.groupby("CLIENTE_STD")[meses].sum().reset_index()
        agrupado = agrupado.rename(columns={"CLIENTE_STD": "CLIENTES"})

        resultado.append(agrupado)

    # ==========================
    # UNIR TODO
    # ==========================
    final = pd.concat(
        [r if isinstance(r, pd.DataFrame) else pd.DataFrame([r]) for r in resultado],
        ignore_index=True
    )

    return final.fillna(0)