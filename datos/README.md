# Migración de AFOROS a SQLite

## Ejecutar

Desde esta carpeta, usar el entorno virtual del proyecto:

```powershell
.\.venv\Scripts\python.exe .\bk\migrar_historico.py --dry-run
.\.venv\Scripts\python.exe .\bk\migrar_historico.py
```

La primera orden valida el Excel y muestra cantidades sin guardar cambios. La segunda crea o actualiza `historico.db` en esta carpeta. También se pueden indicar otras rutas con `--source` y `--database`. El Excel se abre en modo de solo lectura y no se modifica.

## Exportar a Excel con nombres

Para exportar todas las tablas a un libro Excel con nombres legibles en lugar de IDs internos:

```powershell
.\.venv\Scripts\python.exe .\bk\exportar_tablas.py
```

El archivo se guarda como `Exportacion_tablas.xlsx` en esta carpeta. Cada tabla tiene su propia hoja; los registros históricos muestran el nombre del usuario, la placa y la empresa. Las tablas de relaciones también se exportan usando nombres, y las claves internas no aparecen. Se puede cambiar el origen y el destino:

```powershell
.\.venv\Scripts\python.exe .\bk\exportar_tablas.py --database .\historico.db --output .\Exportacion_tablas.xlsx
```

## Tablas y relaciones

- `usuarios`: ID interno autogenerado, nombre, estado `activo` (`1`/`0`) y `codigo_origen` de `clientes.Nombre_ID` cuando existe.
- `empresas`: catálogo de empresas y estado `activo`.
- `placas`: placas, tipo, dato de alquiler y estado `activo`.
- `etiquetas`: nombres de etiquetas independientes por entidad, con estado `activo`.
- `usuario_etiquetas`, `placa_etiquetas`, `empresa_etiquetas`: relaciones entre cada catálogo y sus etiquetas; las claves foráneas impiden asignar una etiqueta al tipo incorrecto.
- `usuario_empresas`: relación muchos-a-muchos derivada del catálogo de clientes y de las empresas registradas en el histórico.
- `historico`: conserva los campos de la hoja de origen y enlaza cada registro con usuario, placa y empresa cuando esos datos están disponibles. `fila_origen` permite volver a ejecutar la carga sin duplicar registros.
- `historico_tipo_servicio`: tabla auxiliar con una copia vinculada solo de los registros cuyo `tipo_servicio` y placa no son `NULL`; se reconstruye al ejecutar la migración.

Las clasificaciones de `clientes` se cargan como etiquetas de usuario y el tipo de `vehiculos` como etiqueta de placa. El Excel no proporciona etiquetas de empresa; la tabla `empresa_etiquetas` queda lista para agregarlas después. Los estados no informados se inician como activos (`1`), según lo acordado; los estados existentes del catálogo vehicular se interpretan desde su columna `activo`.

La carga actualizó la base local con **61.447 registros históricos**. La tabla auxiliar `historico_tipo_servicio` conserva solo registros con `tipo_servicio` y placa presentes; también se importaron **1.231 usuarios**, **7 empresas** y **85 placas**. La base SQLite está excluida del control de versiones para no subir los datos operativos.

Para calcular totales por tipo de servicio, se puede consultar la tabla auxiliar:

```sql
SELECT tipo_servicio, SUM(cantidad) AS cantidad_total, SUM(subtotal) AS subtotal_total
FROM historico_tipo_servicio
GROUP BY tipo_servicio;
```
