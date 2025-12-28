"""
Django settings for core project.
Optimized for Local Development and Azure Deployment.
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# [NUEVO] Cargar variables de entorno desde el archivo .env (si existe)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# [NUEVO] Seguridad: Leemos la clave del entorno, si no existe (en producción sin configurar), falla.
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-clave-temporal-por-si-acaso')

# [NUEVO] DEBUG: Será True solo si en el .env dice "True". En Azure será False por defecto.
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# [NUEVO] Permitimos localhost y cualquier dominio de Azure (.azurewebsites.net)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.azurewebsites.net', '*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # [NUEVO] Librería para guardar fotos en Azure
    'storages', 
    'hoja_vida',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # [NUEVO] WhiteNoise va justo después de SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # Puedes agregar [BASE_DIR / 'templates'] si creas una carpeta global
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# [NUEVO] Base de Datos Inteligente
# 1. Intenta buscar una base de datos en la nube (DATABASE_URL)
# 2. Si no la encuentra, usa la configuración local del archivo .env
DATABASES = {
    'default': dj_database_url.config(
        default=f"postgres://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
        conn_max_age=600
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'es-ec' # [OPCIONAL] Lo puse en Español Ecuador, puedes dejarlo en en-us
TIME_ZONE = 'America/Guayaquil' # [OPCIONAL] Zona horaria
USE_I18N = True
USE_TZ = True


# =========================================================
# [NUEVO] ARCHIVOS ESTÁTICOS Y MEDIA (CSS e Imágenes)
# =========================================================

STATIC_URL = 'static/'
# Carpeta donde se recolectarán los estilos para producción
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
# Motor de almacenamiento para CSS (WhiteNoise con compresión)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# [NUEVO] Lógica Híbrida para Archivos Media (Fotos)
# Si configuramos las claves de Azure, usamos la nube. Si no, usamos carpeta local.

AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')
AZURE_CONTAINER = os.getenv('AZURE_CONTAINER')

if AZURE_ACCOUNT_NAME and AZURE_ACCOUNT_KEY:
    # --- CONFIGURACIÓN PARA AZURE (PRODUCCIÓN) ---
    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    MEDIA_URL = f'https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/'
else:
    # --- CONFIGURACIÓN LOCAL (DESARROLLO) ---
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración básica para el ID automático
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'