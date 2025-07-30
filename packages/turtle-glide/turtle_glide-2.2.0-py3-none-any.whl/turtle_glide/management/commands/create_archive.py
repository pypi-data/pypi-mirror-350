import os
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

class Command(BaseCommand):
    help = 'Crea archivos dentro de la carpeta templates o static de una app'

    FILE_TEMPLATES = {
        '.html': '<div>Este es el contenido del componente.</div>',
        '.js': 'console.log("Este es el contenido del componente.");',
        '.css': '/* Este es el contenido del componente */'
    }

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='Nombre de la app')
        parser.add_argument('--template', nargs='+', default=[], help='Archivos para la carpeta templates')
        parser.add_argument('--static', nargs='+', default=[], help='Archivos para la carpeta static')

    def get_app_config_or_fail(self, app_name):
        try:
            return apps.get_app_config(app_name)
        except LookupError:
            raise CommandError(f'App "{app_name}" no encontrada.')

    def create_directories(self, file_full_path):
        dir_path = os.path.dirname(file_full_path)
        try:
            os.makedirs(dir_path, exist_ok=True)
            self.stdout.write(self.style.SUCCESS(f'Directorio {dir_path} verificado/creado.'))
        except PermissionError:
            raise CommandError(f'No se pudo crear el directorio {dir_path}. Verifica permisos.')

    def create_file(self, file_full_path, file_path, app_name, file_type):
        ext = os.path.splitext(file_path)[1]
        content = self.FILE_TEMPLATES.get(ext, '')

        if not content:
            self.stdout.write(self.style.WARNING(f'Extensión "{ext}" no tiene plantilla predeterminada. Se creará un archivo vacío.'))

        if os.path.exists(file_full_path):
            self.stdout.write(self.style.WARNING(f'El archivo "{file_path}" ya existe en {app_name}/{file_type}/.'))
        else:
            try:
                with open(file_full_path, 'w') as f:
                    f.write(content)
                self.stdout.write(self.style.SUCCESS(f'Archivo "{file_path}" creado en {app_name}/{file_type}/.'))
            except PermissionError:
                raise CommandError(f'No se pudo escribir en "{file_full_path}". Verifica permisos.')

    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']
        template_files = kwargs['template']
        static_files = kwargs['static']

        app_config = self.get_app_config_or_fail(app_name)

        for file_path in template_files:
            base_dir = os.path.join(app_config.path, 'templates')
            file_full_path = os.path.normpath(os.path.join(base_dir, file_path))
            self.create_directories(file_full_path)
            self.create_file(file_full_path, file_path, app_name, 'templates')

        for file_path in static_files:
            base_dir = os.path.join(app_config.path, 'static')
            file_full_path = os.path.normpath(os.path.join(base_dir, file_path))
            self.create_directories(file_full_path)
            self.create_file(file_full_path, file_path, app_name, 'static')
