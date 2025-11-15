"""
ASGI config pour le projet monsite.
Expose l’application ASGI comme variable de module nommée ``application``.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monsite.settings')

application = get_asgi_application()
