from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Sécurité
SECRET_KEY = os.environ.get("SECRET_KEY", "insecure-local-key")
DEBUG = False

# Hôtes autorisés
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "boutique-store.onrender.com",
]

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'boutique',

    # Cloudinary
    'cloudinary',
    'cloudinary_storage',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise pour Render (static files)
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'monsite.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'boutique' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'monsite.wsgi.application'


# -------------------------------
# 🎯 RENDER DATABASE (PostgreSQL)
# -------------------------------
DATABASES = {
    'default': dj_database_url.parse(
        "postgresql://boutique_user:XVdPV95VO2JAoc5nHAhLzZyN9k0TM0rQ@dpg-d4crunk9c44c7390nk1g-a.frankfurt-postgres.render.com/boutique_db_jlmp",
        conn_max_age=600,
        ssl_require=True
    )
}


# -------------------------------
# 🎯 STATIC (Render)
# -------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'boutique' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# -------------------------------
# 🎯 CLOUDINARY CONFIG
# -------------------------------
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dtxziqbxs',
    'API_KEY': '945514746192597',
    'API_SECRET': 'WOvy4a9ftuE0ulqUUhyCZEwboZA',
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# URL MEDIA Cloudinary – Obligation ! 
MEDIA_URL = f'https://res.cloudinary.com/dtxziqbxs/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Panier
CART_SESSION_ID = 'cart'
