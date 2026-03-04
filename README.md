# Web Tarjetas de Crédito

Aplicación en Python para la gestión de tarjetas de crédito con interfaz web en Flask, almacenamiento en SQLite y opción de uso por consola.

## Funcionalidades

- Crear tarjetas de crédito con validaciones (NIF, PIN, límite y número de tarjeta con Luhn).
- Ver detalle de cada tarjeta y sus movimientos.
- Registrar pagos asociados a una tarjeta.
- Cambiar PIN de una tarjeta.
- Eliminar tarjetas con confirmación.
- Consultar el gasto total acumulado.
- Exportar e importar datos en formato JSON (desde la versión de consola).

## Tecnologías

- Python 3
- Flask
- SQLite3
- HTML + CSS (plantillas Jinja2)

## Estructura principal

```text
TarjetasCredito/
  app.py                         # Aplicación web Flask
  aplicacion_tarjetas_credito.py # Aplicación por consola
  bdd.py                         # Acceso y operaciones de base de datos
  tarjeta_credito.py             # Modelo de tarjeta y validaciones
  movimiento.py                  # Modelo de movimiento
  persistencia.py                # Importación/exportación JSON
  templates/                     # Vistas HTML
  static/                        # Estilos CSS
```

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/curromarin16/Web_TarjetasCredito.git
   cd Web_TarjetasCredito
   ```

2. (Opcional) Crea y activa un entorno virtual:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Instala dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

### Opción 1: Aplicación web (Flask)

Desde la carpeta `TarjetasCredito/`:

```bash
python app.py
```

Abre en el navegador:

```text
http://127.0.0.1:5000
```

### Opción 2: Aplicación por consola

Desde la carpeta `TarjetasCredito/`:

```bash
python aplicacion_tarjetas_credito.py
```

## Base de datos

La aplicación crea automáticamente la base de datos SQLite en:

```text
TarjetasCredito/tarjetas_credito.db
```

También existe el archivo `tarjetas.json` para pruebas/importación-exportación.

## Autor

Proyecto para prácticas de desarrollo con Python y Flask.
