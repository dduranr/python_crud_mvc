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


@app.route('/login')
def login():
    try:
        if 'user_id' in session:
            return redirect(url_for('welcome'))
        else:
            return render_template('login.html')

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)


@app.route('/acceso', methods=['POST'])
def acceso():
    try:
        email = request.form['email']
        contrasena = request.form['contrasena']
        contrasena_encode = contrasena.encode('utf-8')

        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
        user = cursor.fetchone()

        bd_contrasena = user[3]
        bd_contrasena = bd_contrasena.encode('utf-8')

        # Si en la BD se guarda un texto cualquiera y no un hash (p.e. abc), el navegador devuelve: ValueError: Invalid salt
        if(bcrypt.checkpw(contrasena_encode, bd_contrasena)):
            session['user_id'] = user[0]
            session['user_nombre'] = user[1]
            session['user_email'] = email
            return redirect(url_for('welcome'))
        else:
            flash('Usuario/contraseña incorrectos', 'danger')
            return redirect(url_for('login'))

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)


@app.route('/welcome')
def welcome():
    try:
        return render_template('welcome.html')

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)


@app.route('/logout')
def logout():
    try:
        session.clear()
        return redirect(url_for('login'))

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)
