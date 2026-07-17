from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent

DB = BASE_DIR / "aforos" / "data" / "aforos.db"
SCHEMA = BASE_DIR / "AFOROS" / "sql" / "schema.sql"


def crear_base():
    DB.parent.mkdir(exist_ok=True)

    with sqlite3.connect(DB) as conn:
        with open(SCHEMA, encoding="utf-8") as f:
            conn.executescript(f.read())

    print("Base de datos creada correctamente.")


if __name__ == "__main__":
    crear_base()