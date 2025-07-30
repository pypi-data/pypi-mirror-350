import os
import sys
import subprocess

# no tocar 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#   ---------------------------------------------------------------------------

import utils.variable_globals as va
import utils.helpers_command_global as helper
import utils.styles_variables as st

class DjangoFuncionApp:
    def __init__(self, project_root, project_name):
        self.project_root = project_root
        self.project_name = project_name
        self.home = "home"

    async def create_apps(self):
        app_path = os.path.join(self.project_root, self.home)
        print(f"🚀 Creando app '{self.home}' en {app_path}")

        try:
            subprocess.run(
                ["python", "manage.py", "startapp", self.home],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al crear la app con manage.py: {e}")
            return
        
        steps = [
            ("Instalando URLs y vistas de perfil", self.install_url_and_views_perfil),
            ("Instalando templates y archivos estáticos", self.install_templates_and_static_files),
            ("Creando carpeta services y archivos", self.create_carpet_services_and_files),
            ("Creando carpeta utils y archivos", self.carpet_utils_and_files),
            ("Creando carpeta test y archivos", self.create_carpet_test_and_files),
            ("Creando carpeta templatetags y archivos", self.create_templatetags),
            ("Configurando installed_apps", self.installed_apps),
            ("Configurando urls del proyecto", self.installed_url_in_project),
        ]

        for description, coroutine in steps:
            try:
                print(f"🔧 {description}...")
                await coroutine()
                print(f"✅ {description} completado")
            except Exception as e:
                print(f"⚠️ Error durante '{description}': {e}")
        print(f"✅ App '{self.home}' creada exitosamente en {app_path}")

    async def installed_apps(self):
        settings_path = os.path.join(self.project_name, "settings.py")
        if not os.path.exists(settings_path):
            print(f"No se encontró el archivo settings.py en {settings_path}")
            return
        
        with open(settings_path, 'r') as f:
            lines = f.readlines()

        app_already_installed = any(f"'{self.home}'" in line for line in lines)
        if app_already_installed:
            print(f"La app '{self.home}' ya está instalada en INSTALLED_APPS.")
            return

        new_lines = []
        inside_installed_apps = False
        for line in lines:
            new_lines.append(line)
            if "INSTALLED_APPS" in line and '=' in line:
                inside_installed_apps = True
            elif inside_installed_apps and line.strip().startswith(']'):
                new_lines.insert(-1, f"    '{self.home}',\n")
                inside_installed_apps = False

        with open(settings_path, 'w') as f:
            f.writelines(new_lines)

        print(f"✅ App '{self.home}' agregada a INSTALLED_APPS en settings.py.")
        await self.write_variables()

    async def write_variables(self):
        settings_path = os.path.join(self.project_name, "settings.py")
        if not os.path.exists(settings_path):     
            print(f"No se encontró el archivo settings.py en {settings_path}")
            return

        with open(settings_path, 'a') as f:
            f.write(va.config_variables.strip())
        await self.add_locale_middleware()
        await self.insert_i18n_settings()
        print("✅ Variables globales y de configuración de email agregadas a settings.py.")

    async def add_locale_middleware(self):
        settings_path = os.path.join(self.project_name, "settings.py")
        if not os.path.exists(settings_path):
            print(f"No se encontró el archivo settings.py en {settings_path}")
            return

        with open(settings_path, 'r') as f:
            lines = f.readlines()

        middleware_start = None
        middleware_end = None

        for i, line in enumerate(lines):
            if 'MIDDLEWARE' in line and '=' in line:
                middleware_start = i
            if middleware_start is not None and line.strip() == ']':
                middleware_end = i
                break

        if middleware_start is None or middleware_end is None:
            print("No se encontró la definición de MIDDLEWARE.")
            return

        # Verificar si ya está presente
        for line in lines[middleware_start:middleware_end]:
            if 'django.middleware.locale.LocaleMiddleware' in line:
                print("✅ LocaleMiddleware ya está presente en MIDDLEWARE.")
                return

        # Insertar justo después de CommonMiddleware si está
        insert_index = middleware_end
        for i in range(middleware_start, middleware_end):
            if 'django.middleware.common.CommonMiddleware' in lines[i]:
                insert_index = i + 1
                break

        lines.insert(insert_index, "    'django.middleware.locale.LocaleMiddleware',\n")

        with open(settings_path, 'w') as f:
            f.writelines(lines)

        print("✅ LocaleMiddleware agregado correctamente a MIDDLEWARE.")

    async def insert_i18n_settings(self):
        settings_path = os.path.join(self.project_name, "settings.py")
        if not os.path.exists(settings_path):
            print(f"No se encontró el archivo settings.py en {settings_path}")
            return

        with open(settings_path, 'r') as f:
            lines = f.readlines()

        insert_index = None
        for i, line in enumerate(lines):
            if line.strip().startswith("TIME_ZONE"):
                insert_index = i + 1
                break

        if insert_index is None:
            print("No se encontró la configuración TIME_ZONE en settings.py.")
            return

        lines.insert(insert_index, va.i18n_settings)

        with open(settings_path, 'w') as f:
            f.writelines(lines)

        print("✅ Configuración de internacionalización añadida después de TIME_ZONE.")

    async def installed_url_in_project(self):
        urls_path = os.path.join(self.project_name, "urls.py")

        if not os.path.exists(urls_path):
            print(f"No se encontró el archivo urls.py en {urls_path}")
            return

        with open(urls_path, 'r') as f:
            lines = f.readlines()

        # Verificar si ya existen
        has_include_import = any("include" in line and "django.urls" in line for line in lines)
        has_home_url = any("include('perfil.urls')" in line for line in lines)
        has_accounts_url = any("include('django.contrib.auth.urls')" in line for line in lines)
        has_i18n_url = any("include('django.conf.urls.i18n')" in line for line in lines)

        new_lines = []
        for line in lines:
            # Si encontramos el import sin include, lo corregimos
            if "from django.urls import path" in line and "include" not in line:
                line = line.strip().replace("path", "path, include") + "\n"
            new_lines.append(line)

        # Si falta el import, lo agregamos
        if not has_include_import:
            for i, line in enumerate(new_lines):
                if "from django.urls" in line:
                    new_lines.insert(i + 1, "from django.urls import include\n")
                    break
            else:
                new_lines.insert(0, "from django.urls import path, include\n")

        # Agregar las rutas dentro de urlpatterns
        for i, line in enumerate(new_lines):
            if "urlpatterns" in line and "=" in line:
                # Buscamos donde empieza la lista [
                for j in range(i, len(new_lines)):
                    if "[" in new_lines[j]:
                        insert_index = j + 1
                        break
                else:
                    insert_index = i + 1  # Por si no encuentra
                if not has_home_url:
                    new_lines.insert(insert_index, f"    path('', include('{self.home}.urls')),\n")
                    insert_index += 1
                if not has_accounts_url:
                    new_lines.insert(insert_index, "    path('accounts/', include('django.contrib.auth.urls')),\n")
                if not has_i18n_url:
                    new_lines.insert(insert_index, "    path('i18n/', include('django.conf.urls.i18n')),\n")
                break

        with open(urls_path, 'w') as f:
            f.writelines(new_lines)

        print("✅ URLs de 'perfil' y 'accounts' agregadas exitosamente a urls.py.")

    async def install_url_and_views_perfil(self):
        file_archive_urls =  os.path.join(self.home, 'urls.py')
        file_archive_views = os.path.join(self.home, 'views.py')
        file_archive_forms = os.path.join(self.home, 'forms.py')

        with open(file_archive_urls, 'w') as f:
            f.write(va.urls_home.strip())

        with open(file_archive_views, 'w') as f:
            f.write(va.views.strip())

        with open(file_archive_forms, 'w') as f:
            f.write(va.forms_home.strip())
        
        print(f"✅  configuracion de views y urls de {self.home}, terminada")

    async def install_templates_and_static_files(self):
        
        #rutas de destino
        dest_templates = os.path.join(self.home, 'templates')
        dest_static = os.path.join(self.home, 'static')

        #rutas de subcarpetas static
        dest_css = os.path.join(dest_static, 'css')
        dest_js = os.path.join(dest_static, 'js')

        #rutas de subcarpetas templates
        dest_components = os.path.join(dest_templates, 'components')
        dest_email = os.path.join(dest_templates, 'emails')
        dest_layout = os.path.join(dest_templates, 'layouts')
        dest_profile = os.path.join(dest_templates, 'profile')
        dest_profile_password = os.path.join(dest_profile, 'password')
        dest_registration = os.path.join(dest_templates, 'registration')

        if not os.path.exists(dest_static):
            print("📁 creando la carpeta static y sub carpetas css y js")
            os.makedirs(dest_static, exist_ok=True)
            os.makedirs(dest_css, exist_ok=True)
            os.makedirs(dest_js, exist_ok=True)
        else:
            print("⚠️ la carpeta ya existe")

        if not os.path.exists(dest_templates):
            print("📁 creando la carpeta templates y sub carpetas components, emails, layouts, profile, password")  
            os.makedirs(dest_templates, exist_ok=True)
            os.makedirs(dest_components, exist_ok=True)
            os.makedirs(dest_email, exist_ok=True)
            os.makedirs(dest_layout, exist_ok=True)
            os.makedirs(dest_profile, exist_ok=True)
            os.makedirs(dest_profile_password, exist_ok=True)
            os.makedirs(dest_registration, exist_ok=True)
        
        #static
        file_css_base_app = os.path.join(dest_css, 'base_app.css')
        file_css_basic_styles = os.path.join(dest_css, 'basic_styles.css')
        file_js_message = os.path.join(dest_js, 'message.js')

        #templates
        templates_index = os.path.join(dest_templates, 'index.html')
        templates_profile = os.path.join(dest_templates, 'profile.html')
        components_button = os.path.join(dest_components, 'button.html')
        components_card = os.path.join(dest_components, 'card.html')
        components_form = os.path.join(dest_components, 'form.html')
        email_password = os.path.join(dest_email, 'email_password.html')
        layouts_app = os.path.join(dest_layout, 'app.html')
        password_change_password = os.path.join(dest_profile_password, 'change_password.html')
        password_reset_email = os.path.join(dest_profile_password, 'reset_email.html')
        password_reset_confirm = os.path.join(dest_profile_password, 'reset_confirm.html')
        password_reset_password_complete = os.path.join(dest_profile_password, 'reset_password_complete.html')
        profile_edit = os.path.join(dest_profile, 'profile_edit.html')
        profile_delete = os.path.join(dest_profile, 'profile_delete.html')
        registration_login = os.path.join(dest_registration, 'login.html')
        registration_register = os.path.join(dest_registration, 'register.html')
        
        helper.copy_content(file_css_base_app, st.css_base_app, 'base_app.css')
        helper.copy_content(file_css_basic_styles, st.css_basic_styles, 'basic_styles.css')
        helper.copy_content(file_js_message, st.js_message, 'message.js')
        # -----------------------------------------------------------------
        helper.copy_content(templates_index, st.templates_index, 'index.html')
        helper.copy_content(templates_profile, st.templates_profile, 'profile.html')
        helper.copy_content(components_button, st.components_button, 'button.html')
        helper.copy_content(components_card, st.components_card, 'card.html')
        helper.copy_content(components_form, st.components_form, 'form.html')
        helper.copy_content(email_password, st.email_password, 'email_password.html')
        helper.copy_content(layouts_app, st.layouts_app, 'app.html')
        helper.copy_content(password_change_password, st.password_change_password, 'change_password.html')
        helper.copy_content(password_reset_email, st.password_reset_email, 'reset_email.html')
        helper.copy_content(password_reset_confirm, st.password_reset_confirm, 'reset_confirm.html')
        helper.copy_content(password_reset_password_complete, st.password_reset_password_complete, 'reset_password_complete.html')
        helper.copy_content(profile_edit, st.templates_profile_edit, 'profile_edit.html')
        helper.copy_content(profile_delete, st.templates_profile_delete, 'profile_delete.html')
        helper.copy_content(registration_login, st.templates_registration_login, 'login.html')
        helper.copy_content(registration_register, st.templates_registration_register, 'register.html')

        print("✅ archivos de las carpetas static y templates hechos corectamente ")

    async def create_carpet_services_and_files(self):
        carpet_services = os.path.join(self.home, 'services')
        if not os.path.exists(carpet_services):
            print("📁 creando la carpeta services")
            os.makedirs(carpet_services, exist_ok=True)
        else:
            print("⚠️ la carpeta ya existe")

        file_user_password = os.path.join(carpet_services, 'user_password.py')
        file_user_profile = os.path.join(carpet_services, 'user_profile.py')

        helper.copy_content(file_user_profile, va.user_profile, 'user_profile.py')
        helper.copy_content(file_user_password, va.user_password, 'user_password.py')

        print("✅ terminado los archivos de la carpeta services")

    async def carpet_utils_and_files(self):
        carpet_utils = os.path.join(self.home, 'utils')
        if not os.path.exists(carpet_utils):
            print("📁 creando la carpeta utils")
            os.makedirs(carpet_utils, exist_ok=True)
            file_init_ = os.path.join(carpet_utils, '__init__.py')
            with open(file_init_, 'w') as f:
                f.write('')
            print("✅ Archivo '__init__.py' creado dentro de 'utils'.")
        else:
            print("⚠️ la carpeta ya existe")

        file_test_helpers = os.path.join(carpet_utils, 'test_helpers.py')
        
        helper.copy_content(file_test_helpers, va.test_helpers, 'test_helpers.py')

        print(f"✅ creada la carpeta {carpet_utils}, y sus archivos")

    async def create_carpet_test_and_files(self):
        carpet_test = os.path.join(self.home, 'test')

        if not os.path.exists(carpet_test):
            print("📁 creando la carpeta test")
            os.makedirs(carpet_test, exist_ok=True)
            file_init_ = os.path.join(carpet_test, '__init__.py')
            with open(file_init_, 'w') as f:
                f.write('')
            print("✅ Archivo '__init__.py' creado dentro de 'test'.")
        else:
            print("⚠️ la carpeta ya existe")
        
        file_test_profile = os.path.join(carpet_test, 'test_profile.py')
        file_test_password = os.path.join(carpet_test, 'test_password.py')

        helper.copy_content(file_test_profile, va.test_profile, 'test_profile.py')
        helper.copy_content(file_test_password, va.test_password, 'test_password.py')

        print("✅ creada la carpeta de test y sus archivos")

    async def create_templatetags(self):
        carpet_templatetags = os.path.join(self.home, 'templatetags')
        if not os.path.exists(carpet_templatetags):
            print("📁 creando la carpeta templatetags")
            os.makedirs(carpet_templatetags, exist_ok=True)
            file_init_ = os.path.join(carpet_templatetags, '__init__.py')
            with open(file_init_, 'w') as f:
                f.write('')
            print("✅ Archivo '__init__.py' creado dentro de 'templatetags'.")
        else:
            print("⚠️ la carpeta ya existe")

        file_templatetags = os.path.join(carpet_templatetags, 'components.py')

        helper.copy_content(file_templatetags, va.components, 'components.py')

        print("✅ creada la carpeta de los templatetags y sus archivos")

