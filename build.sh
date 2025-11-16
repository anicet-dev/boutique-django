#!/usr/bin/env bash
set -o errexit

# Met à jour pip
pip install --upgrade pip

# Installe les dépendances
pip install -r requirements.txt

# Collecte les fichiers statiques Django
python manage.py collectstatic --noinput

# Applique les migrations (si Render ne le fait pas automatiquement)
python manage.py migrate --noinput
