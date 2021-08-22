# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Importamos las clases que necesitan todos los controladores
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

#   Flask               Que es el framework
#   flask_sqlalchemy    ORM para SQL
#   render_template     Permite utilizar archivos HTML
#   request             Para obtener los datos de la petición de un form
#   redirect            Para hacer redirecciones
#   url_for             Para hacer redirecciones
#   flash               Manda mensajes entre vistas
#   sys                 Para obtener el tipo de excepción

from app import app  # El 1er app es el nombre del archivo app.py. El 2do "app" es la instancia de Flask() declarada en app.py
from config import *
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime
import bcrypt
import sys

# MySQL
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASS
app.config['MYSQL_DB'] = MYSQL_DB
mysql = MySQL(app)



# Semilla para encriptamiento de contraseña
semilla = bcrypt.gensalt()

# Sesión
app.secret_key = 'mysecretkey'
