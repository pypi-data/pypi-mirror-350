css_base_app = """* {
    padding: 0;
    margin: 0;
}

:root {
    --navbar-color: #2C514C;
    --tea-green: #C5EFCB;
    --pomp-and-power: #9F6BA0;
    --sky-blue: #82C0CC;
    --dark-purple: #2D1E2F;
    --link-hover-bg: rgba(255, 255, 255, 0.15);
}

.navbar {
    background-color: var(--navbar-color);
    padding: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
}

.navbar-header {
    display: none;
}

.menu {
    list-style: none;
    display: flex;
    gap: 1rem;
}

.menu li a {
    text-decoration: none;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}

.menu li a:hover {
    background-color: var(--link-hover-bg);
    color: black;
}

.menu-toggle {
    display: none;
    background: none;
    border: none;
    color: white;
    font-size: 2rem;
    cursor: pointer;
    padding: 0.5rem 1rem;
    border-radius: 5px;
}


@media (max-width: 800px) {
    .navbar-header {
        display: flex;
        width: 100%;
        justify-content: flex-end;
    }

    .menu-toggle {
        display: block;
    }

    .menu {
        display: none;
        width: 100%;
        flex-direction: column;
        margin-top: 1rem;
    }

    .menu.active {
        display: flex;
    }

    .menu li {
        width: 100%;
    }

    .menu li a {
        display: block;
        width: 100%;
        padding: 1rem;
        color: white;
        background-color: var(--navbar-color);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .menu li a:hover {
        background-color: var(--link-hover-bg);
    }
}
"""

css_basic_styles = """* {
    padding: 0;
    margin: 0;
}

:root {
    --navbar-color: #2C514C;
    --tea-green: #C5EFCB;
    --pomp-and-power: #9F6BA0;
    --sky-blue: #82C0CC;
    --dark-purple: #2D1E2F;
    --link-hover-bg: rgba(255, 255, 255, 0.15);
}

.content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2rem;
    margin-top: 2rem;
    margin-bottom: 3rem;
}

.card {
    padding: 2rem 4rem;
    background-color: #fff;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    border-radius: 8px;
    width: 100%;
    max-width: 700px;
}

.form-group{
    columns: 2;
}

.form-control {
    width: 100%;
}

.form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.9rem;
    margin-top: 1rem;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-label {
    font-weight: bold;
    margin-bottom: 0.3rem;
    text-wrap: pretty;
}

.form-input input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
    transition: border-color 0.2s ease-in-out;
}

.form-input input:focus {
    border-color: var(--sky-blue);
    outline: none;
}

.field-error {
    color: red;
    font-size: 0.85rem;
    margin-top: 0.25rem;
}

.form-button {
    grid-column: span 2;
    display: flex;
    justify-content: center;
    margin-top: 2rem;
}

.sub-button {
    background-color: var(--sky-blue);
    color: white;
    padding: 0.75rem 1.5rem;
    margin: 10px;
    font-size: 1rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s ease;
    text-decoration: none;
}

.sub-button:hover {
    background-color: var(--pomp-and-power);
}

.user-info-label {
    font-weight: bold;
    color: #2C514C;
    margin-bottom: 0.4rem;
    font-size: 1rem;
}
  
.user-info-value {
    background-color: #f5f5f5;
    padding: 0.6rem 1rem;
    border-radius: 6px;
    border: 1px solid #ddd;
    font-size: 1rem;
    color: #333;
}

.card-text {
    text-align: center;
    text-wrap: pretty;
}

.form-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}

.form-actions .sub-button {
    text-align: center;
    padding: 0.6rem 2rem;
    font-size: 1rem;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: white;
    text-decoration: none;
    cursor: pointer;
}

.form-actions .sub-button:hover {
    background-color: #0056b3;
}

.message-container {
    width: 90%;
    max-width: 600px;
    margin: 20px auto;
}
  
.message {
    position: relative;
    padding: 14px 24px;
    border-radius: 10px;
    margin-bottom: 15px;
    font-weight: 500;
    font-size: 1rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    animation: fadeIn 0.4s ease-in-out;
    padding-right: 40px;
}
  
/* Tipos de mensajes */
.message.success {
    background-color: #e6ffed;
    color: #1a7f37;
    border-left: 6px solid #1a7f37;
}
  
.message.error {
    background-color: #ffe6e6;
    color: #d60000;
    border-left: 6px solid #d60000;
}
  
.message.warning {
    background-color: #fffbe6;
    color: #8c6d00;
    border-left: 6px solid #8c6d00;
}
  
.message.info {
    background-color: #e6f0ff;
    color: #0052cc;
    border-left: 6px solid #0052cc;
}
  
/* Botón cerrar */
.close-btn {
    position: absolute;
    top: 10px;
    right: 14px;
    font-size: 1.2rem;
    color: #999;
    cursor: pointer;
    transition: color 0.2s ease;
}
  
.close-btn:hover {
    color: #333;
}
  
/* Animaciónes */
/* Animación de entrada */
@keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(-10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
}
  
/* Animación de salida */
.fade-out {
    animation: fadeOut 0.3s forwards;
}
  
@keyframes fadeOut {
    to {
      opacity: 0;
      transform: translateY(-10px);
    }
}

@media (max-width: 800px) {
    .card {
        padding: 1.5rem;
    }

    .form-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }

    .form-actions {
        flex-direction: column;
        gap: 1rem;
    }

    .form-actions .sub-button {
        width: 100%;
        text-align: center;
    }

    .content h2 {
        font-size: 1.5rem;
        text-align: center;
    }

    .form-input input {
        font-size: 1rem;
    }

    .message-container {
        width: 95%;
    }

    .message {
        font-size: 0.95rem;
        padding: 12px 20px;
    }

    .close-btn {
        top: 8px;
        right: 10px;
    }

    .form-actions {
        flex-direction: row;
        justify-content: center;
        gap: 1rem;
    }

    .form-actions .sub-button {
        flex: 0 0 auto;
        width: auto;
    }
}
"""

js_message = """function closeMessage(button) {
    const message = button.parentElement;
    message.classList.add('fade-out');
    setTimeout(() => {
        message.style.display = 'none';
    }, 300);
}
"""

templates_index = """{% extends 'layouts/app.html' %}
{% load static %}
{% load i18n %}

{% block static %}
    <link rel="stylesheet" href="{% static 'css/basic_styles.css' %}">
{% endblock %}

{% block content %}
{% if request.user.is_authenticated %}
<section class="content">
    <div class="card">
        <h2 class="card-text">{% blocktrans with username=request.user.username %}You are logged, {{ username }}</h2>{% endblocktrans %}
    </div>
</section>
{% else %}
    <h1>{% trans "hello welcome to turtle glade" %}</h1>
{% endif %}
{% endblock %}
"""

templates_profile = """{% extends 'layouts/app.html' %}
{% load static %}
{% load components %}
{% load i18n %}

{% block static %}
    <link rel="stylesheet" href="{% static 'css/basic_styles.css' %}">
{% endblock %}

{% block content %}
{% if messages %}
  <div class="message-container">
    {% for message in messages %}
      <div class="message {{ message.tags }}">
        <span class="close-btn" onclick="closeMessage(this)">&times;</span>
        {{ message }}
      </div>
    {% endfor %}
  </div>
{% endif %}

{% card _("profile") %}
{% if request.user.is_authenticated %}
<div class="form-grid">
  <div class="form-group">
    <div class="user-info-label">{{ label_username }}:</div>
    <div class="user-info-value">{{ request.user.username }}</div>
  </div>

  <div class="form-group">
    <div class="user-info-label">{{ label_first_name }}:</div>
    <div class="user-info-value">{{ request.user.first_name }}</div>
  </div>

  <div class="form-group">
    <div class="user-info-label">{{ label_last_name }}:</div>
    <div class="user-info-value">{{ request.user.last_name }}</div>
  </div>

  <div class="form-group">
      <div class="user-info-label">{{ label_email }}:</div>
      <div class="user-info-value">{{ request.user.email }}</div>
    </div>
  </div>

  <div class="form-button">
    {% if request.user.is_authenticated and request.user.id %}
    <a href="{% url 'profile_edit' request.user.id %}" class="sub-button">{% trans "Edit profile" %}</a>
    {% endif %}
  </div>  
</div>
{% else %}
<h2>{% trans "you aren't authenticated" %}</h2>
{% endif %}
{% endcard %}

{% card _("Change password") %}
  <p class="card-text">{% trans "You can update your password to keep your account secure." %}</p>
  <div class="form-button">
    <a href="{% url 'change-password' %}" class="sub-button">{% trans "Change password" %}</a>
  </div>
{% endcard %}

{% card _("Delete account") %}
  <p class="card-text">{% trans "This action will permanently delete your account. You won't be able to recover it afterwards." %}</p>
  <div class="form-button">
    {% if request.user.is_authenticated and request.user.id %}
      <a href="{% url 'profile_delete' request.user.id %}" class="sub-button">{% trans "Delete profile" %}</a>
    {% endif %}
  </div>
{% endcard %}
{% endblock %}

{% block script %}
<script src="{% static 'js/message.js' %}"></script>
{% endblock %}
"""

components_button = """<div class="{{ parent_class|default:'botton_ui' }}" style="justify-content: {{ align|default:'center' }};">
  {% with 
    base_classes="btn btn-"|add:color|stringformat:"s" 
    size_class=size|yesno:" btn-"|add:size if size in 'sm md lg' 
    full_class=base_classes|add:" "|add:btn_class|stringformat:"s"|add:size_class|stringformat:"s"
  %}
  
    {% with 
      custom_styles=""|add:(
        color|slice:":1" == "#" or color|slice:":4" == "rgb(" 
        and "background-color: "|add:color|add:";" or ""
      )|add:(
        text_color|slice:":1" == "#" or text_color|slice:":4" == "rgb(" 
        and " color: "|add:text_color|add:";" or ""
      )|add:(
        size not in 'sm md lg' 
        and " padding: "|add:size|add:"; font-size: calc("|add:size|add:" * 0.5);" or ""
      )|add:" display: inline-block; text-align: center;"
    %}
    
      {% if href %}
        <a href="{% url href %}"
           name="{{ name_button }}"
           class="{{ full_class }}"
           style="{{ custom_styles }}">
          {{ title_button }}
        </a>
      {% else %}
        <button name="{{ name_button }}"
                class="{{ full_class }}"
                style="{{ custom_styles }}">
          {{ title_button }}
        </button>
      {% endif %}
      
    {% endwith %}
  {% endwith %}
</div>
"""

components_card = """<section class="content">
    <h2>{{title}}</h2>
    <div class="card">
        {{ content }}
    </div>
</section>
"""

components_form = """<section class="content">
    <h2>{{title}}</h2>
    <div class="card">
        {% if form.non_field_errors %}
            <div class="form-errors">
                {% for error in form.non_field_errors %}
                <p>{{ error }}</p>
                {% endfor %}
            </div>
        {% endif %}

        <form method="post" class="form-control">
            {% csrf_token %}
            <div class="form-grid">
                {% for field_name, field in contents.items %}
                  <div class="form-group">
                      <div class="form-label">{{ field.label_tag }}</div>
                      <div class="form-input">{{ field }}</div>
                      {% if field.errors %}
                        <div class="field-error">{{ field.errors.0 }}</div>
                      {% endif %}
                  </div>
                {% endfor %}
            </div>

            <div class="form-actions">
                <button type="submit" class="sub-button">{{ content_button }}</button>
                {% if href %}
                    <a href="{% url href %}" class="sub-button">
                        {{ href_text|default:"Volver" }}
                    </a>
                {% endif %}
            </div>
        </form>
    </div>
</section>
"""

email_password = """{% extends 'layouts/app.html' %}
{% load static %}
{% load components %}
{% load i18n %}


{% block static %}
    <link rel="stylesheet" href="{% static 'css/basic_styles.css' %}">
{% endblock %}

{% block content %}
{% card _("Reset password") %}
    {% if form.non_field_errors %}
    <div class="form-errors">
        {% for error in form.non_field_errors %}
        <p>{{ error }}</p>
        {% endfor %}
    </div>
    {% endif %}

    <p>{% blocktrans %}Forgot your password? Enter your email address below and we’ll send you instructions to set a new one.{% endblocktrans %}</p>

    <form method="post" class="form-control">
        {% csrf_token %}

        <div class="form-grid">
            <div class="form-group">
                <div class="form-label">{{ form.email.label_tag }}</div>
                <div class="form-input">{{ form.email }}</div>
                {% if form.email.errors %}
                <div class="field-error">{{ form.email.errors.0 }}</div>
                {% endif %}
            </div>
            <div class="form-button">
                <button type="submit" class="sub-button">{% trans "Reset password" %}</button>
            </div>
        </div>
    </form>
{% endcard %}
{% endblock %}
"""

layouts_app = """{% load static %}
{% load i18n %}
<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pruebas para el paquete de turtle glide</title>
    <link rel="stylesheet" href="{% static 'css/base_app.css' %}">
    {% block static %}{% endblock %}
</head>
<body>
    <nav class="navbar">
        <div class="navbar-header">
            <button class="menu-toggle" onclick="toggleMenu()">☰</button>
        </div>
        <ul class="menu">
            {% if request.user.is_authenticated %}
                <li><a href="{% url 'app' %}">{% trans "Home" %}</a></li>
                <li><a href="{% url 'profile' %}">{% trans "Profile" %}</a></li>
                <li><a href="{% url 'exit' %}">{% trans "Logout" %}</a></li>
            {% else %}
                <li><a href="{% url 'app' %}">{% trans "Home" %}</a></li>
                <li><a href="{% url 'login' %}">{% trans "Login" %}</a></li>
                <li><a href="{% url 'register' %}">{% trans "register" %}</a></li>
            {% endif %}
        </ul>
        <form action="{% url 'set_language' %}" method="post">{% csrf_token %}
            <input name="next" type="hidden" value="{{ redirect_to }}">
            <select name="language">
                {% get_current_language as LANGUAGE_CODE %}
                {% get_available_languages as LANGUAGES %}
                {% get_language_info_list for LANGUAGES as languages %}
                {% for language in languages %}
                    <option value="{{ language.code }}"{% if language.code == LANGUAGE_CODE %} selected{% endif %}>
                        {{ language.name_local }} ({{ language.code }})
                    </option>
                {% endfor %}
            </select>
            <input type="submit" value="Go">
        </form>
    </nav>        
    <main>{% block content %}{% endblock %}</main>    
    {% block script %}{% endblock %}
    <script>
        function toggleMenu() {
            const menu = document.querySelector('.menu');
            menu.classList.toggle('active');
        }
    </script>
</body>
</html>
"""

password_change_password = """{% extends 'layouts/app.html' %}
{% load static %}
{% load components %}

{% block static %}
    <link rel="stylesheet" href="{% static 'css/basic_styles.css' %}">
{% endblock %}

{% block content %}
{% r_form form title contents content_button href=href href_text=href_text %}
{% endblock %}
"""

password_reset_email = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Restablecer tu contraseña</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f9f9f9;
      padding: 20px;
      color: #333;
    }
    .container {
      background-color: #fff;
      border-radius: 8px;
      padding: 30px;
      max-width: 600px;
      margin: auto;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    h2 {
      color: #1a73e8;
    }
    a.button {
      display: inline-block;
      background-color: #1a73e8;
      color: white;
      padding: 12px 20px;
      text-decoration: none;
      border-radius: 5px;
      margin-top: 20px;
    }
    .footer {
      font-size: 0.9em;
      color: #777;
      margin-top: 40px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>{% trans %}Hello {{ user.get_username }},</h2>
    <p>{% trans %}You have requested to reset your password.</p>
    <p>{% trans %}Click the button below to reset it:</p>

    <p>
      <a href="{{ protocol }}://{{ domain }}{% url 'reset-password-confirm' uidb64=uid token=token %}" class="button">
        {% trans %}Reset password
      </a>
    </p>

    <p>{% trans %}If you did not request this change, you can ignore this email.</p>

    <div class="footer">
      <p>{% trans %}Thank you for using our site.</p>
      <p>{% trans %}The {{ domain }} team</p>
    </div>
  </div>
</body>
</html>
"""

password_reset_confirm = """{% extends 'layouts/app.html' %}
{% load static %}
{% load components %}
{% load i18n %}

{% block static %}
  <link rel="stylesheet" href="{% static 'css/basic_styles.css' %}">
{% endblock %}

{% block content %}
{% card _("Set new password") %}
    {% if validlink %}
        <p>{% trans "Enter your new password below:" %}</p>
        <form method="post" class="form-control">
            {% csrf_token %}
            <div class="form-grid">
                <div class="form-group">
                    <div class="form-label">{{ form.new_password1.label_tag }}</div>
                    <div class="form-input">{{ form.new_password1 }}</div>
                    {% if form.new_password1.errors %}
                        <div class="field-error">
                            {{ form.new_password1.errors.0 }}
                        </div>
                    {% endif %}
                </div>
                <div class="form-group">
                    <div class="form-label">{{ form.new_password2.label_tag }}</div>
                    <div class="form-input">{{ form.new_password2 }}</div>
                    {% if form.new_password2.errors %}
                        <div class="field-error">
                            {{ form.new_password2.errors.0 }}
                        </div>
                    {% endif %}
                </div>
            </div>
            <div class="form-button">
                <button type="submit" class="sub-button">{% trans "Change password" %}</button>
            </div>
        </form>
    {% else %}
        <p class="text-error">
            {% trans "The password reset link is not valid. It may have already been used or expired." %}
        </p>
    {% endif %}
{% endcard %}
{% endblock %}
"""

password_reset_password_complete = """{% extends 'layouts/app.html' %}
{% load static %}
{% load components %}
{% load i18n %}

{% block static %}
  <link rel="stylesheet" href="{% static 'css/basic_styles.css' %}">
{% endblock %}

{% block content %}
{% card _("Password reset complete") %}
  <p class="card-text">{% trans "Your password has been set. You may go ahead and log in now." %}</p>

  <div class="form-button">
    <a href="{% url 'login' %}" class="sub-button">{% trans "Go to login" %}</a>
  </div>
{% endcard %}
{% endblock %}
"""

templates_profile_delete = """{% extends 'layouts/app.html' %}
{% load static %}
{% load i18n %}
{% load components %}

{% block static %}
    <link rel="stylesheet" href="{% static 'css/basic_styles.css' %}">
{% endblock %}

{% block content %}
{% card _("Delete User") %}
<form method="post">
    {% csrf_token %}
    <p class="card-text">{% trans "Are you sure you want to delete your account?" %}</p>
    <div class="form-actions">
        <button type="submit" class="sub-button">{% trans "Delete" %}</button>
            <a href="{% url 'profile' %}" class="sub-button">{% trans "Back" %}</a>
    </div>
</form>
{% endcard %}
{% endblock %}
"""

templates_profile_edit = """{% extends 'layouts/app.html' %}
{% load static %}
{% load components %}

{% block static %}
    <link rel="stylesheet" href="{% static 'css/basic_styles.css' %}">
{% endblock %}

{% block content %}
{% r_form form title contents content_button %}
{% endblock %}
"""

templates_registration_login = """{% extends 'layouts/app.html' %}
{% load static %}
{% load components %}
{% load i18n %}

{% block static %}
    <link rel="stylesheet" href="{% static 'css/basic_styles.css' %}">
{% endblock %}

{% block content %}
{% card "Login" %}
    {% if form.non_field_errors %}
    <div class="form-errors">
    {% for error in form.non_field_errors %}
    <p>{{ error }}</p>
    {% endfor %}
    </div>
    {% endif %}

    <form method="post" class="form-control">
        {% csrf_token %}

        <div class="form-grid">
            <div class="form-group">
                <div class="form-label">{{ form.username.label_tag }}</div>
                <div class="form-input">{{ form.username }}</div>
                {% if form.username.errors %}
                <div class="field-error">{{ form.username.errors.0 }}</div>
                {% endif %}
            </div>

            <div class="form-group">
                <div class="form-label">{{ form.password.label_tag }}</div>
                <div class="form-input">{{ form.password }}</div>
                {% if form.password.errors %}
                    <div class="field-error">{{ form.password.errors.0 }}</div>
                {% endif %}
            </div>
        </div>

        <div class="form-button">
            <button type="submit" class="sub-button">{% trans "Login" %}</button>
        </div>
    </form>
{% endcard %}
{% endblock %}
"""

templates_registration_register = """{% extends 'layouts/app.html' %}
{% load static %}
{% load components %}

{% block static %}
    <link rel="stylesheet" href="{% static 'css/basic_styles.css' %}">
{% endblock %}

{% block content %}
{% r_form form title contents content_button %}
{% endblock %}
"""

