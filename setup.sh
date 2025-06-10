#!/bin/bash

# Verifica si el entorno virtual existe
if [ ! -d "venv" ]; then
  echo "Creando entorno virtual..."
  python3 -m venv venv
fi

# Activa el entorno virtual
source venv/bin/activate

# Instala dependencias
pip install --upgrade pip
pip install -r requirements.txt || pip install django joblib numpy pandas scikit-learn

# Ejecuta migraciones si es un proyecto Django
if [ -f "manage.py" ]; then
  echo "Levantando servidor de desarrollo..."
  python manage.py runserver
else
  echo "No se encontró manage.py. Proyecto Django no detectado."
fi
