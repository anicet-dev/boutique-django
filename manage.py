#!/usr/bin/env python
import os
import sys

def main():
    """Point d’entrée principal du projet Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monsite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django n’est pas installé. Installe-le avec : pip install django"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
