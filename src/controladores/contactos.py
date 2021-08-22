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


@app.route('/contactos')
def contactos():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM contactos')
        contactos = cursor.fetchall()
        print(contactos)
        return render_template('contactos.html', contactos=contactos)

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)



@app.route('/contacto_post', methods=['POST'])
def contacto_post():
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            telefono = request.form['telefono']
            email = request.form['email']

            cursor = mysql.connection.cursor()
            cursor.execute(
                f"INSERT INTO contactos (nombre, telefono, email) VALUES ('{nombre}', '{telefono}', '{email}')")
            mysql.connection.commit()
            flash('Contacto agregado', 'success')
            return redirect(url_for('contactos'))

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)


@app.route('/contacto_edit/<id>', methods=['GET'])
def contacto_edit(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(f"SELECT * FROM contactos WHERE id = {id}")
        contacto = cursor.fetchall()
        return render_template('editar_contacto.html', contacto=contacto[0])

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)


@app.route('/contacto_update/<id>', methods=['POST'])
def contacto_update(id):
    try:
        if request.method == 'POST':
            nombre = request.form['nombre']
            telefono = request.form['telefono']
            email = request.form['email']
            cursor = mysql.connection.cursor()
            cursor.execute(
                f"UPDATE contactos SET nombre = '{nombre}', telefono = '{telefono}', email = '{email}' WHERE id = {id}")
            mysql.connection.commit()
            flash('Contacto actualizado', 'success')
            return redirect(url_for('contactos'))

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)


@app.route('/contacto_delete/<id>')
def contacto_delete(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(f'DELETE FROM contactos WHERE id={id}')
        mysql.connection.commit()
        flash('Contacto eliminado', 'success')
        return redirect(url_for('contactos'))

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)
