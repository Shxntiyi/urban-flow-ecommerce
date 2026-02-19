"""
Este módulo centraliza la inicialización de Firebase Admin SDK
y expone el cliente de Firestore para ser usado en las vistas.
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore
from django.conf import settings

# Ruta absoluta al archivo JSON
cred_path = os.path.join(settings.BASE_DIR, 'firebase-key.json')

# Aplicamos la filosofía EAFP usando un bloque Try-Except
try:
    # Intenta obtener la aplicación por defecto de Firebase
    firebase_admin.get_app()
except ValueError:
    # Si lanza ValueError es porque no se ha inicializado aún.
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# Instanciamos el cliente de la base de datos
db = firestore.client()