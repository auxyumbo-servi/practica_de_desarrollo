from data.clientes import obtener_clientes
from data.subtotales import suma_cliente

user = "ALCALDIA DE YUMBO (CENTRO)"


def main():

    df_clientes = obtener_clientes()

    resultado = suma_cliente(df_clientes)

    print(resultado)


if __name__ == "__main__":
    main()