turtle_glide
================

**Introducción**
---------------

turtle_glide es una herramienta para crear archivos dentro de la carpeta `templates` o `static` de una app de Django.

**Instalación del paquete**
-------------------------

### Instalación en tu proyecto Django

Instalar turtle_glide en tu proyecto Django:

```bash
pip install turtle_glide
```

Luego, agregar TurtleGlide como una app de Django en `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'turtle_glide'
]
```

**Uso de turtle_glide**
---------------------

### Parámetros obligatorios

Hay tres parámetros obligatorios para el uso del comando `create_archive`:

* `app_name`: Nombre de la app
* `--template`: para archivos en la carpeta `templates`
* `--static`: para archivos en la carpeta `static`

### Comando de ejemplo
```bash
python manage.py create_archive "app_name" --static "file_path"
```

### create_archive

Crea multiples archivos en las carpetas `static` y `templates` de una app de Django.

```bash
python manage.py create_archive home --static css/app.css js/app.js --template layouts/main.html
```

**uso de turtle_glide para desarrolladores**
------------

hay tres paramentros obligatorios para el uso del comando creeate_archive:

### Paso 1: Instalar dependencias y crear entorno virtual

comandos:
-----------

#### instalacion de dependencias

```bash
./setup.sh
```

### Paso 2: Activar entorno virtual
Activar el entorno virtual:

```bash
source venv/bin/activate
```

#### variables

- app_name: Nombre de la app
- `--template`: para archivos en la carpeta `templates`
- `--static`: para archivos en la carpeta `static`

```bash
python manage.py create_archive "app_name" --static "file_path"
```

### Listo para empezar
Ya estás listo para empezar a trabajar con TurtleGlide sin problemas.