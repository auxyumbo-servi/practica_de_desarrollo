CREATE TABLE IF NOT EXISTS clientes(
    id_usuario INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    municipio INTEGER,
    activo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS aforos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    fecha TEXT,
    estado TEXT DEFAULT 'PENDIENTE',
    datos TEXT,
    FOREIGN KEY(id_usuario) REFERENCES clientes(id_usuario)
);

CREATE TABLE IF NOT EXISTS ejecuciones(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inicio TEXT,
    fin TEXT,
    procesados INTEGER,
    errores INTEGER
);

CREATE TABLE IF NOT EXISTS registros(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER,
    empresa_excel TEXT,
    fecha TEXT,
    estado TEXT DEFAULT 'PENDIENTE',
    datos TEXT,
    error TEXT,
    FOREIGN KEY(id_usuario) REFERENCES clientes(id_usuario)
);