
import logging
from config import LOGS_DIR


def configurar_logger():

    archivo_log = LOGS_DIR / "historial.log"

    logging.basicConfig(
        filename=archivo_log,
        level=logging.ERROR,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
        force=True
    )

    return logging.getLogger("Facturacion")
