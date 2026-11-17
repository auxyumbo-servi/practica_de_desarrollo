
import os
import win32com.client as win32

from config import (
    CUENTA_REMITENTE,
    DESTINATARIOS_FIJOS,
    COPIAS_FIJAS,
    USAR_CORREO_EXCEL,
    USAR_COPIA_EXCEL
)


class OutlookSender:

    def __init__(self):

        self.outlook = win32.Dispatch(
            "Outlook.Application"
        )

        self.namespace = self.outlook.GetNamespace("MAPI")

        self.cuenta = self._buscar_cuenta()

    def _buscar_cuenta(self):

        for cuenta in self.namespace.Accounts:

            if cuenta.SmtpAddress.lower() == CUENTA_REMITENTE.lower():
                return cuenta

        raise ValueError(
            f"No se encontró la cuenta: {CUENTA_REMITENTE}"
        )

    def enviar(self, datos, mensaje):

        correo = self.outlook.CreateItem(0)

        correo.SendUsingAccount = self.cuenta

        # Destinatarios
        destinatarios = list(DESTINATARIOS_FIJOS)

        if USAR_CORREO_EXCEL and datos["correo"]:
            destinatarios.append(datos["correo"])

        correo.To = "; ".join(
            dict.fromkeys(destinatarios)
        )

        # Copias
        copias = list(COPIAS_FIJAS)

        if USAR_COPIA_EXCEL and datos["copia"]:
            copias.append(datos["copia"])

        correo.CC = "; ".join(
            dict.fromkeys(copias)
        )

        correo.Subject = datos["asunto"]
        correo.HTMLBody = mensaje

        # Adjuntar PDF
        archivo = datos["archivo"]

        if archivo:

            if not os.path.isfile(archivo):
                raise FileNotFoundError(
                    f"No se encontró el PDF: {archivo}"
                )

            correo.Attachments.Add(
                os.path.abspath(archivo)
            )

        return correo

    def gestionar(self, correo, modo):

        if modo == "ENVIAR":
            correo.Send()
            return "ENVIADO"

        elif modo == "BORRADOR":
            correo.Save()
            return "BORRADOR"

        raise ValueError(f"Modo desconocido: {modo}")
