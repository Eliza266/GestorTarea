# Gestor de Tareas

## Descripción

Esta aplicación es un gestor de tareas desarrollado en Python utilizando `tkinter` para la interfaz gráfica y `SQLAlchemy` para la gestión de la base de datos. Permite a los usuarios:

- Añadir tareas con un título y descripción.
- Marcar tareas como completadas.
- Eliminar tareas.
- Exportar las tareas a un archivo JSON.
- Importar tareas desde un archivo JSON.

## Requisitos

- Python 3.8 o superior.
- Bibliotecas de Python:
  - `sqlalchemy`
  - `tkinter` (incluido por defecto en Python en la mayoría de los sistemas operativos)

## Instalación

1. Clona este repositorio o descarga el código fuente.
2. Instala las dependencias necesarias ejecutando:

   ```bash
   pip install sqlalchemy
   ```

3. Ejecuta el archivo principal:

   ```bash
   python main.py
   ```

## Uso

1. **Añadir Tarea**:
   - Introduce un título y descripción en los campos correspondientes.
   - Haz clic en el botón "Añadir Tarea".

2. **Completar Tarea**:
   - Selecciona una tarea de la lista.
   - Haz clic en el botón "Completar" para marcarla como completada.

3. **Eliminar Tarea**:
   - Selecciona una tarea de la lista.
   - Haz clic en el botón "Eliminar" para eliminarla de la base de datos.

4. **Exportar JSON**:
   - Haz clic en el botón "Exportar JSON" para guardar todas las tareas en un archivo llamado `tareas_exportadas.json`.

5. **Importar JSON**:
   - Haz clic en el botón "Importar JSON" para cargar tareas desde el archivo `tareas_exportadas.json`.

## Estructura de la Base de Datos

La base de datos SQLite se crea automáticamente al iniciar la aplicación. Contiene una tabla llamada `tareas` con las siguientes columnas:

- `id`: Identificador único de la tarea.
- `titulo`: Título de la tarea.
- `descripcion`: Descripción de la tarea.
- `completada`: Estado de la tarea (True para completada, False para pendiente).

## Archivos JSON

Los archivos JSON exportados tienen el siguiente formato:

```json
[
  {
    "titulo": "Título de la tarea",
    "descripcion": "Descripción de la tarea",
    "completada": false
  }
]
```

Al importar, las tareas con títulos y descripciones idénticas a las ya existentes no se duplicarán.

## Capturas de Pantalla
![Imagen del gestor en funcionamiento](/imagen.png)


