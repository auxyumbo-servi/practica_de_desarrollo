PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    clave TEXT NOT NULL UNIQUE,
    codigo_origen TEXT,
    activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1))
);

CREATE TABLE IF NOT EXISTS empresas (
    id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    clave TEXT NOT NULL UNIQUE,
    activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1))
);

CREATE TABLE IF NOT EXISTS placas (
    id_placa INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT NOT NULL,
    clave TEXT NOT NULL UNIQUE,
    tipo TEXT,
    alquiler TEXT,
    activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1))
);

CREATE TABLE IF NOT EXISTS etiquetas (
    id_etiqueta INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_entidad TEXT NOT NULL
        CHECK (tipo_entidad IN ('usuario', 'placa', 'empresa')),
    nombre TEXT NOT NULL,
    clave TEXT NOT NULL,
    activo INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0, 1)),
    UNIQUE (tipo_entidad, clave),
    UNIQUE (id_etiqueta, tipo_entidad)
);

CREATE TABLE IF NOT EXISTS usuario_etiquetas (
    id_usuario INTEGER NOT NULL,
    id_etiqueta INTEGER NOT NULL,
    tipo_entidad TEXT NOT NULL DEFAULT 'usuario'
        CHECK (tipo_entidad = 'usuario'),
    PRIMARY KEY (id_usuario, id_etiqueta),
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
    FOREIGN KEY (id_etiqueta, tipo_entidad)
        REFERENCES etiquetas (id_etiqueta, tipo_entidad)
);

CREATE TABLE IF NOT EXISTS placa_etiquetas (
    id_placa INTEGER NOT NULL,
    id_etiqueta INTEGER NOT NULL,
    tipo_entidad TEXT NOT NULL DEFAULT 'placa'
        CHECK (tipo_entidad = 'placa'),
    PRIMARY KEY (id_placa, id_etiqueta),
    FOREIGN KEY (id_placa) REFERENCES placas (id_placa),
    FOREIGN KEY (id_etiqueta, tipo_entidad)
        REFERENCES etiquetas (id_etiqueta, tipo_entidad)
);

CREATE TABLE IF NOT EXISTS empresa_etiquetas (
    id_empresa INTEGER NOT NULL,
    id_etiqueta INTEGER NOT NULL,
    tipo_entidad TEXT NOT NULL DEFAULT 'empresa'
        CHECK (tipo_entidad = 'empresa'),
    PRIMARY KEY (id_empresa, id_etiqueta),
    FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa),
    FOREIGN KEY (id_etiqueta, tipo_entidad)
        REFERENCES etiquetas (id_etiqueta, tipo_entidad)
);

CREATE TABLE IF NOT EXISTS usuario_empresas (
    id_usuario INTEGER NOT NULL,
    id_empresa INTEGER NOT NULL,
    PRIMARY KEY (id_usuario, id_empresa),
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
    FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa)
);

CREATE TABLE IF NOT EXISTS historico (
    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
    fila_origen INTEGER NOT NULL UNIQUE,
    id_usuario INTEGER,
    id_placa INTEGER,
    id_empresa INTEGER,
    fecha TEXT,
    aforo NUMERIC,
    recipiente TEXT,
    cantidad NUMERIC,
    subtotal NUMERIC,
    tipo_servicio TEXT,
    valor NUMERIC,
    facturable TEXT,
    minicargador TEXT,
    observacion TEXT,
    mes TEXT,
    anio NUMERIC,
    estado TEXT,
    tarifa NUMERIC,
    horas_alquiler NUMERIC,
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario),
    FOREIGN KEY (id_placa) REFERENCES placas (id_placa),
    FOREIGN KEY (id_empresa) REFERENCES empresas (id_empresa)
);

CREATE INDEX IF NOT EXISTS idx_historico_fecha ON historico (fecha);
CREATE INDEX IF NOT EXISTS idx_historico_usuario ON historico (id_usuario);
CREATE INDEX IF NOT EXISTS idx_historico_empresa ON historico (id_empresa);
CREATE INDEX IF NOT EXISTS idx_historico_placa ON historico (id_placa);

CREATE TABLE IF NOT EXISTS historico_tipo_servicio (
    id_registro INTEGER PRIMARY KEY,
    fila_origen INTEGER NOT NULL UNIQUE,
    id_usuario INTEGER,
    id_placa INTEGER NOT NULL,
    id_empresa INTEGER,
    fecha TEXT,
    aforo NUMERIC,
    recipiente TEXT,
    cantidad NUMERIC,
    subtotal NUMERIC,
    tipo_servicio TEXT NOT NULL,
    valor NUMERIC,
    facturable TEXT,
    minicargador TEXT,
    observacion TEXT,
    mes TEXT,
    anio NUMERIC,
    estado TEXT,
    tarifa NUMERIC,
    horas_alquiler NUMERIC,
    FOREIGN KEY (id_registro) REFERENCES historico (id_registro) ON DELETE CASCADE,
    FOREIGN KEY (id_placa) REFERENCES placas (id_placa)
);

CREATE INDEX IF NOT EXISTS idx_historico_tipo_servicio_fecha
    ON historico_tipo_servicio (tipo_servicio, fecha);
CREATE INDEX IF NOT EXISTS idx_historico_tipo_servicio_usuario
    ON historico_tipo_servicio (id_usuario);
CREATE INDEX IF NOT EXISTS idx_historico_tipo_servicio_empresa
    ON historico_tipo_servicio (id_empresa);
CREATE INDEX IF NOT EXISTS idx_historico_tipo_servicio_placa
    ON historico_tipo_servicio (id_placa);
