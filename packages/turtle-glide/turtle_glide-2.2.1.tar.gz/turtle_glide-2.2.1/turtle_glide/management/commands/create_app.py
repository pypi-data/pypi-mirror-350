from django.core.management.base import BaseCommand
from services.configuration_app import DjangoFuncionApp
import asyncio

class Command(BaseCommand):
    help = "Crea una nueva aplicación dentro del proyecto Django"

    def handle(self, *args, **options):
        project_root = input("Introduce el nombre de la carpeta root del proyecto: ")
        project_name = input("Introduce el nombre del proyecto: ")

        create = DjangoFuncionApp(project_root=project_root, project_name=project_name)

        asyncio.run(create.create_apps())