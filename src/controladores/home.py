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


@app.route('/')
def index():
    return render_template('index.html')
