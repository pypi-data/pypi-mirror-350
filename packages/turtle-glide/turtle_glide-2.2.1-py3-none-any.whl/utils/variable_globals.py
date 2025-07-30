# variables

urls_home = """from django.urls import path
from .views import app
from home.services.user_profile import ProfileCreateView, Profile, ProfileUpdateView, ProfileDeleteView
from home.services.user_password import UserPasswordChange, UserPasswordReset, UserPasswordConfirm, UserPasswordComplete

urlpatterns = [
    path('', app, name="app"),
    path('logout', Profile.exit, name="exit"),
    # CRUD Profile
    path('register/', ProfileCreateView.as_view(), name='register'),
    path('profile/', Profile.index ,name="profile"),
    path('profile/edit/<int:pk>', ProfileUpdateView.as_view() , name="profile_edit"),
    path('profile/delete/<int:pk>', ProfileDeleteView.as_view() , name="profile_delete"),
    # Password
    path('profile/change-password/', UserPasswordChange.as_view(), name="change-password"),
    path('profile/reset-password/', UserPasswordReset.as_view(), name="reset-password"),
    path('profile/<uidb64>/<token>/', UserPasswordConfirm.as_view(), name="reset-password-confirm"),
    path('profile/reset/complete', UserPasswordComplete.as_view(), name="reset-password-done"),
]
"""

config_variables = """\n# Variables Globales
LOGIN_REDIRECT_URL = "app"
LOGOUT_REDIRECT_URL = "app"
\n# Envío de emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'turtle@misitio.com'
"""

views = """from django.shortcuts import render
from django.utils.translation import gettext as _

# Create your views here.
def app(request):
    button = _("Go")
    return render(request, 'index.html', {'button': button})
"""

forms_home = """from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password1', 'password2'
        ]

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email'
        ]
"""

user_password = """from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib import messages

template_general = "profile/password/"

class UserPasswordChange(PasswordChangeView):
        form_class = SetPasswordForm
        template_name = f"{template_general}change_password.html"
        success_url = reverse_lazy('profile')

        def form_valid(self, form):
            messages.success(self.request, _("The password has been changed successfully."))
            return super().form_valid(form)
        
        def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                context['title'] = _('Change Password')
                context['contents'] = ['new_password1', 'new_password2']
                context['content_button'] = _('Change')
                context['href'] = 'reset-password'
                context['href_text'] = _("Do you want to change your password?")
                return context

class UserPasswordReset(PasswordResetView):
        template_name = "emails/email_password.html"
        success_url = reverse_lazy('profile')
        email_template_name = f"{template_general}reset_email.html"

        def form_valid(self, form):
            messages.success(self.request, _("An email has been sent to your inbox."))
            return super().form_valid(form)

class UserPasswordConfirm(PasswordResetConfirmView):
        template_name = f"{template_general}reset_confirm.html"
        success_url = reverse_lazy('reset-password-done')

class UserPasswordComplete(PasswordResetCompleteView):
        template_name = f"{template_general}reset_password_complete.html"
"""

user_profile = """from home.forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create perfil
class ProfileCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('app')

    def form_valid(self, form):
        self.object = form.save()
        success_url = reverse_lazy('app')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            
        return redirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Register')
        context['contents'] = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        context['content_button'] = _('Sing Up')
        return context

# Read perfil
class Profile():
    def exit(request):
        logout(request)
        return redirect('app')

    @login_required
    def index(request):

        context = {
            'label_username': _('username'),
            'label_first_name': _('First name'),
            'label_last_name': _('Last name'),
            'label_email': _('Email'),
        }

        return render(request, 'profile.html', context)
    
# Update perfil
class ProfileUpdateView(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'profile/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        user_id = int(self.kwargs.get('pk'))
        if self.request.user.id == user_id:
            return self.request.user
        raise Http404("No puedes editar otro usuario.")

    def form_valid(self, form):
        messages.success(self.request, 'Tu perfil se ha actualizado correctamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit User')
        context['contents'] = ['username', 'first_name', 'last_name', 'email']
        context['content_button'] = _('Edit')
        return context
    
# Delete perfil 
class ProfileDeleteView(DeleteView):
    model = User
    template_name = 'profile/profile_delete.html'
    success_url = reverse_lazy('app')

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        logout(request)

        return response
"""

test_helpers = """from django.urls import reverse
from django.contrib.messages import get_messages

def template_use(name):
    templates = {
        'app': 'index.html',
        # CRUD profile 
        'register': 'registration/register.html',
        'profile': 'profile.html',
        'profile_edit': 'profile/profile-edit.html',
        'profile_delete': 'profile/profile-delete.html'
        # Password
    }
    return templates.get(name)

def call_status(response=None, *, client=None, url_name=None, expected_status=200, message="", expected_message=None, method="get", data=None):
    if response is None:
        if not client or not url_name:
            raise ValueError("Si no se pasa 'response', se deben pasar 'client' y 'url_name'.")
        
        url = reverse(url_name)
        method = method.lower()
        
        if method == "post":
            response = client.post(url, data or {})
        else:
            response = client.get(url)

    if expected_message:
        messages = list(get_messages(response.wsgi_request))
        if any(expected_message in str(m) for m in messages):
            print(f"✅ [{url_name.upper()}] MENSAJE OK → '{expected_message}'")
        else:
            print(f"❌ [{url_name.upper()}] MENSAJE NO ENCONTRADO → '{expected_message}'")

    if response.status_code == expected_status:
        print(f"✅ [{url_name.upper() if url_name else ''}] PASÓ ({expected_status}) → {message}")
    else:
        print(f"❌ [{url_name.upper() if url_name else ''}] FALLÓ - Esperado: {expected_status}, Recibido: {response.status_code} → {message}")

    return response
"""

test_profile = """from django.test import TestCase, Client
from django.urls import reverse
from home.utils.test_helpers import template_use, call_status
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

# Create your tests here.

class ViewTests(TestCase):
    def test_app(self):
        url_name_index = 'app'
        try: 
            response = self.client.get(reverse('app'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_use(url_name_index))
            call_status(
                client=self.client,
                url_name=url_name_index,
                expected_status=200, 
                message="vista renderizada"
            )
        except Exception as e:
            print(f"❌ [ERROR EN {url_name_index.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{url_name_index}': {e}")

class ProfileCreateTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_register_page(self):
        url_name = 'register'
        try:
            response = self.client.get(reverse(url_name))
            self.assertTemplateUsed(response, template_use(url_name))
            call_status(
                client=self.client,
                url_name=url_name,
                expected_status=200,
                message='Render de página de registro'
            )
        except Exception as e:
            print(f"❌ [ERROR EN {url_name.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{url_name}': {e}")

    def test_user_creation_and_login(self):
        url_name_index = 'app'
        url_name_register = 'register'

        user_data = {
            'username': 'nuevo_usuario',
            'password1': 'SuperSecreto123',
            'password2': 'SuperSecreto123',
        }

        try:
            response = self.client.post(reverse(url_name_register), user_data)
            call_status(
                url_name=url_name_register,
                response=response,
                expected_status=302,
                message="Usuario creado e insertado en la base de datos"
            )
            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse(url_name_index))

            self.assertTrue(User.objects.filter(username='nuevo_usuario').exists())

            response = self.client.get(reverse(url_name_index))
            self.assertTrue(response.wsgi_request.user.is_authenticated)

        except Exception as e:
            print(f"❌ [ERROR EN {url_name_register.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{url_name_register}': {e}")

class ProfileReadTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="nuevo_usuario", password="SuperSecreto123")

    def test_logout_redirects_to_app(self):
        template_exit = 'exit'
        try:
            self.client.login(username="nuevo_usuario", password="SuperSecreto123")
            response = self.client.get(reverse('exit'))

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse('app'))

            response_index = self.client.get(reverse('profile'))
            self.assertEqual(response_index.status_code, 302)
            call_status(
                url_name=template_exit,
                response=response,
                expected_status=302,
                message="logout y redireccion hecho"
            )
        except Exception as e:
            print(f"❌ [ERROR EN {template_exit.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{template_exit}': {e}")

    def test_read_profile(self):
        page_name = 'profile'

        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        try:
            self.assertTrue(response.url.startswith('/accounts/login'))

            self.client.login(username="nuevo_usuario", password="SuperSecreto123")
            response = self.client.get(reverse(page_name))

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(template_use(page_name))

            expected_keys = ['label_username', 'label_first_name', 'label_last_name', 'label_email']
            for key in expected_keys:
                self.assertIn(key, response.context)
            call_status(
                url_name=page_name,
                response=response,
                expected_status=200,
                message="Vista de perfil cargada correctamente con los datos esperados"
            )
        except Exception as e:
            print(f"❌ [ERROR EN {page_name.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{page_name}': {e}")

class ProfileUpdataTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="nuevo_usuario", password="SuperSecreto123")
        self.other_user = User.objects.create_user(username="otro_usuario", password="OtraClave123")

    def test_edit_own_profile_succesfully(self):
        template_edit = "profile"

        self.client.login(username="nuevo_usuario", password="SuperSecreto123")
        url = reverse("profile_edit", kwargs={"pk": self.user.pk})

        try:
            data = {
                "username": "usuario_actualizado",
                "first_name": "Nuevo",
                "last_name": "Nombre",
                "email": "nuevo@email.com",
            }

            response = self.client.post(url, data, follow=True)  # usamos follow=True

            self.user.refresh_from_db()

            # Comprobamos que hubo redirección en algún punto
            self.assertGreater(len(response.redirect_chain), 0)
            self.assertEqual(response.status_code, 200)

            # Comprobamos datos actualizados
            self.assertEqual(self.user.username, "usuario_actualizado")
            self.assertEqual(self.user.email, "nuevo@email.com")

            # Comprobamos que se usó la plantilla correcta
            self.assertTemplateUsed(response, template_use(template_edit))

            # Validamos mensaje de éxito
            expected_msg = "Tu perfil se ha actualizado correctamente."
            messages = list(get_messages(response.wsgi_request))
            self.assertTrue(any(expected_msg in str(m) for m in messages))

            # Llamada a call_status con mensaje esperado
            call_status(
                response=response,
                url_name=template_edit,
                expected_status=200,
                message="usuario editado exitosamente",
                expected_message=expected_msg
            )

        except Exception as e:
            print(f"❌ [ERROR EN {template_edit.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{template_edit}': {e}")
    
    def test_edit_profile_template_render(self):
        template_edit = "profile"

        self.client.login(username="nuevo_usuario", password="SuperSecreto123")
        url = reverse("profile_edit", kwargs={"pk": self.user.pk})

        try:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(template_use('profile_edit'))

            call_status(
                client=self.client,
                url_name=template_edit,
                expected_status=200,
                message="renderizado de la pagina exitoso"
            )

        except Exception as e:
            print(f"❌ [ERROR EN {template_edit.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{template_edit}': {e}")

    def test_cannot_edit_other_user(self):
        template_edit = "profile"
        self.client.login(username="nuevo_usuario", password="SuperSecreto123")
        url = reverse("profile_edit", kwargs={"pk": self.other_user.pk})                

        try:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
            call_status(
                response=response,
                url_name=template_edit,
                expected_status=404,
                message="No se puede editar otr usuario que no sea el tuyo"
            )

        except Exception as e:
            print(f"❌ [ERROR EN {template_edit.upper()}] - {str(e)}")
            self.fail(f"Falló al testear la vista '{template_edit}': {e}")

class ProfileDeleteTest(TestCase):
        def setUp(self):
            self.client = Client()
            self.user = User.objects.create_user(username="borrar_usuario", password="Clave123")

        def test_user_can_delete_own_account(self):
            template_delete =  "profile_delete"
            delete_url = reverse("profile_delete", kwargs={"pk": self.user.pk})
            success_url = reverse("app")

            self.client.login(username="borrar_usuario", password="Clave123")

            try:
                response_get = self.client.get(delete_url)
                self.assertEqual(response_get.status_code, 200)
                self.assertTemplateUsed(template_use('profile_delete'))

                response_post = self.client.post(delete_url, follow=True)

                self.assertRedirects(response_post, success_url)

                u_e = User.objects.filter(username="borrar_usuario").exists()

                self.assertFalse(u_e)

                self.assertFalse(response_post.wsgi_request.user.is_authenticated)

                call_status(
                    response=response_post,
                    url_name=template_delete,
                    expected_status=200,
                    message="usuario eliminado exitosamente"
                )                

            except Exception as e:
                print(f"❌ [ERROR EN {template_delete.upper()}] - {str(e)}")
                self.fail(f"Falló al testear la vista '{template_delete}': {e}")


"""

test_password = """from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.messages import get_messages
from home.utils.test_helpers import call_status
from django.contrib.auth.models import User

# Create your tests here.
class TestPasswordUser(TestCase):
    #variables templates
    template_password = 'profile/password/'

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="usuario_password", password="ContraseñaVieja123", email="usuario@email.com")
        self.client.login(username="usuario_password", password="ContraseñaVieja123")

    def test_user_change_password(self):
        template_password_change = f"{self.template_password}change-password.html"
        url = reverse('change-password')

        try:
            response_get = self.client.get(url)
            self.assertEqual(response_get.status_code, 200)
            self.assertTemplateUsed(response_get, template_password_change)

            data = {
                "old_password": "ContraseñaVieja123",
                "new_password1": "ContraseñaNueva456",
                "new_password2": "ContraseñaNueva456"
            }

            response_post = self.client.post(url, data, follow=True)
            self.assertRedirects(response_post, reverse('profile'))

            self.client.logout()
            login_success = self.client.login(username="usuario_password", password="ContraseñaNueva456")
            self.assertTrue(login_success)
            messages = list(get_messages(response_post.wsgi_request))   
            self.assertTrue(any("La contraseña se ha cambiado exitosamente." in str(m) for m in messages))

            call_status(
                response=response_post,
                url_name=url,
                expected_status=200,
                message="contraseña cambiada correctamente"
            )

        except Exception as e:
            print(f"❌ [ERROR EN PASSWORD_CHANGE] - {str(e)}")
            self.fail(f"Falló al testear el cambio de contraseña: {e}")

    def test_user_reset_password(self):
        template_password_reset = f"{self.template_password}reset_password_email.html"
        url = reverse('reset-password')

        try:
            response_get = self.client.get(url)
            self.assertEqual(response_get.status_code, 200)
            self.assertTemplateUsed(response_get, template_password_reset)

            data = {"email": self.user.email}
            response_post = self.client.post(url, data, follow=True)

            self.assertRedirects(response_post, reverse('profile'))
            messages = list(get_messages(response_post.wsgi_request))
            self.assertTrue(any(
                "Se ha enviado un correo electrónico a tu bandeja de entrada." in str(m)
                for m in messages
            ))

            self.assertEqual(len(mail.outbox), 1)
            self.assertIn(self.user.email, mail.outbox[0].to)

            call_status(
                response=response_post,
                url_name=url,
                expected_status=200,
                message="solicitud de restablecimiento de contraseña exitosa"
            )

        except Exception as e:
            print(f"❌ [ERROR EN PASSWORD_RESET] - {str(e)}")
            self.fail(f"Falló al testear el restablecimiento de contraseña: {e}")            

    def test_user_confirm_password(self):
        template_password_confirm = f"{self.template_password}reset_confirm.html"
        url = reverse('reset-password-done')
        try:
            # GET request
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

            call_status(
                response=response,
                url_name=url,
                expected_status=200,
                message="confirmación de restablecimiento de contraseña exitosa"
            )

        except Exception as e:
            print(f"❌ [ERROR EN PASSWORD_CONFIRM] - {str(e)}")
            self.fail(f"Falló al testear el restablecimiento de contraseña: {e}")

    def test_user_complete_change_password(self):
        try:
            template_password_complete = f"{self.template_password}reset_password_complete.html"
            
            # Obtener la URL real usando el `name` de la ruta
            url = reverse('reset-password-done')

            # Hacer GET request
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template_password_complete)

            call_status(
                response=response,
                url_name=template_password_complete,
                expected_status=200,
                message="renderización del template de finalización de cambio de contraseña"
            )

        except Exception as e:
            print(f"❌ [ERROR EN PASSWORD_COMPLETE] - {str(e)}")
            self.fail(f"Falló al testear el render del password complete: {e}")


"""

components = """from django import template
from django.template import loader, Node, Variable
from django.utils.html import mark_safe
from django.utils.translation import gettext as _

register = template.Library()

# card
@register.tag(name="card")
def do_card(parser, token):
    try:
        tag_name, title = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument for the title"
            % token.contents.split()[0]
        )

    # ¡Esto también estaba mal! Debe pasarse como tupla:
    nodelist = parser.parse(('endcard',))
    parser.delete_first_token()

    return CardNode(title, nodelist)

class CardNode(Node):  # CORRECTO
    def __init__(self, title, nodelist):
        self.title = Variable(title)
        self.nodelist = nodelist

    def render(self, context):
        title = self.title.resolve(context)
        content = self.nodelist.render(context)

        translated_title = _(title)

        tpl = loader.get_template('components/card.html')
        if hasattr(context, 'request'):
            return tpl.render({
                'title': translated_title,
                'content': mark_safe(content),
                **context.flatten(),
            }, request=context['request'])
        else:
            return tpl.render({
                'title': translated_title,
                'content': mark_safe(content),
                **context.flatten(),
            })
#------------------------------------------------------------------

@register.inclusion_tag('components/form.html')
def r_form(form, title, contents, content_button, name=None, href=None, href_text=None):
    if isinstance(contents, str):
        contents = [campo.strip() for campo in contents.split(',')]
    
    campos = {field: form[field] for field in contents}

    return {
        'form': form,
        'title': title,
        'contents': campos,
        'content_button': content_button,
        'name': name,
        'href': href,
        'href_text': href_text
    }

@register.inclusion_tag('components/button.html')
def button(title_button, href=None, parent_class=None, btn_class='', align='center', size='md', color='primary', text_color='white', name_button="name_button"):
    
    #Renderiza un botón reutilizable con varias opciones de estilo.

    #Args:
    #- title_button (str): Texto dentro del botón.
    #- name (str): es para darle un valor a la etiqueta name .
    #- href (str): Si se proporciona, se usa un <a>, si no, <button>.
    #- parent_class (str): Clase personalizada para el contenedor padre.
    #- btn_class (str): Clases extra para el botón.
    #- align (str): Alineación del botón (left, center, right). Default: center.
    #- size (str): Tamaño del botón (sm, md, lg). Default: sm.
    #- color (str): Color del fondo. Puede ser clase ('primary') o código hexadecimal ('#ff0000').
    #- text_color (str): Color del texto. Igual que color.

    return {
        'title_button': title_button,
        'name_button': name_button,
        'href': href,
        'parent_class': parent_class,
        'btn_class': btn_class,
        'align': align,
        'size': size,
        'color': color,
        'text_color': text_color,
    }
"""

i18n_settings = """\nUSE_L10N = True
\nLANGUAGES = [
    ('en', 'English'),
    ('es', 'Español'),
]
\nLOCALE_PATHS = [
    BASE_DIR / 'locale',
]
\nUSE_ACCEPT_LANGUAGE_HEADER = False
"""

