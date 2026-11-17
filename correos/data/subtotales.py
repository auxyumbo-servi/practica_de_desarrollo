import pandas as pd


def suma_cliente(df):

    resultado = df.groupby("Nombre").apply(
        lambda x: pd.Series({

            "Contrato": x["Contrato"].iloc[0],

            # Minicargador con valor
            "Subtotal_mini": x.loc[
                x["Minicargador"].notna(), "Subtotal"
            ].sum(),

            # Minicargador vacío
            "Subtotal_vacio": x.loc[
                x["Minicargador"].isna(), "Subtotal"
            ].sum()

        })
    ).reset_index()

    return resultado