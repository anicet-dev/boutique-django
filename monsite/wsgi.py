"""
WSGI config pour le projet monsite.
Ce fichier expose l’application WSGI comme variable de module nommée ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monsite.settings')

application = get_wsgi_application()
