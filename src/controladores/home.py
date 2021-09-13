# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Descripción de las clases importadas en este controlador
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

#   render_template     Permite utilizar archivos HTML



from app import app  # El 1er app es el nombre del archivo app.py. El 2do "app" es la instancia de Flask() declarada en app.py
from flask import render_template

from datetime import datetime
import bcrypt
import sys
# Semilla para encriptamiento de contraseña
semilla = bcrypt.gensalt()

# Importamos los modelos a usar
from modelos.user import *

@app.route('/')
def index():

    # Crear usuario al acceder a esta ruta
    # contrasena = 'abc'
    # contrasena_encode = contrasena.encode('utf-8')
    # contrasena_crypt = bcrypt.hashpw(contrasena_encode, semilla)
    # usuario = User(nombre='David', email='official.dduran@gmail.com', contrasena=contrasena_crypt, created_at='2021-09-12 17:07:00', updated_at='2021-09-12 17:07:00')
    # usuario.post()


    return render_template('index.html')
