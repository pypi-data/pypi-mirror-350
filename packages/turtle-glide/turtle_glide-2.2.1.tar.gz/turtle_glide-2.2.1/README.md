# turtle_glide

## Introducción

turtle_glide es una herramienta diseñada para simplificar y mejorar algunas tareas tediosas para los desarrolladores de Django.

## Instalación del Paquete

### Instalación en tu Proyecto Django

Para instalar turtle_glide en tu proyecto Django, sigue los siguientes pasos:

1. Instala el paquete mediante pip:

   ```bash
   pip install turtle_glide
   ```

2. Agrega TurtleGlide como una app de Django en `INSTALLED_APPS`:
   ```python
   INSTALLED_APPS = [
       'turtle_glide',
   ]
   ```

## Contenido

1. [Comandos](#comandos)
   1. [create_archive](#create_archive)
   2. [create_app](#create_app)
2. [Desarrolladores](#uso-para-desarrolladores)
3. [Notas](#notas)
4. [Cosas ha mejorar](#cosas-por-mejorar)

## Comandos Disponibles

turtle_glide ofrece dos comandos principales:

### [create_archive](#create_archive)

Crea múltiples archivos en las carpetas `static` y `templates` de una app de Django.

#### Parámetros Obligatorios

- `app_name`: Nombre de la app
- `--template`: para archivos en la carpeta `templates`
- `--static`: para archivos en la carpeta `static`

#### Ejemplo de Uso
```bash
python manage.py create_archive home --static css/app.css js/app.js --template layouts/main.html
```

### [create_app](#create_app)

Crea la carpeta home con todo lo necesario para la autenticación de usuarios, incluyendo el envío de correos electrónicos.

#### Ejemplo de Uso
```bash
python3 manage.py create_app
```

## [Uso para Desarrolladores](#uso-para-desarrolladores)

Después de clonar el repositorio, debes ejecutar el script `setup.sh` para instalar todas las dependencias necesarias. Luego, activa el entorno virtual con el comando `source venv/bin/activate`.

## [NOTAS](#notas)

1. [se ha agregado la traducción para la carpeta `home` y agregado el selector para el idioma](#traduccion)

## [Traducción](#traduccion)

Ya que la carpeta `home` ya tiene todas las traducciones, debes hacer lo siguiente para recoger todas las traducciones :

Primero, debes crear la carpeta `locale` dentro de la carpeta `home`.
despues corre estos comandos

```bash
    python manage.py makemessages -l es
```

```bash
    python manage.py compilemessages
```

Luego, debes estar en la carpeta raíz de tu proyecto y ejecutar el siguiente comando para recoger las traducciones:

## [Cosas por mejorar](#cosas-por-mejorar)

1. intentar mejorar el codigo utilizando DRY y KISS 
2. mejorar la UI
3. añadir peticiones AJAX
4. mejorar la UI para moviles

