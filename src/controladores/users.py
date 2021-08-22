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


@app.route('/users')
def users():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        return render_template('users/index.html', users=users)

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)



@app.route('/user_post', methods=['POST'])
def user_post():
    try:
        if request.method == 'POST':
            now = datetime.now()
            ahora = now.strftime("%Y-%m-%d %H:%M:%S")

            nombre = request.form['nombre']
            email = request.form['email']
            contrasena = request.form['contrasena']

            cursor = mysql.connection.cursor()
            cursor.execute(
                f"INSERT INTO users (nombre, email, contrasena, created_at) VALUES ('{nombre}', '{email}', '{contrasena}', '{ahora}')")
            mysql.connection.commit()
            flash('Usuario agregado', 'success')
            return redirect(url_for('users'))

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)



@app.route('/user_update/<id>', methods=['GET', 'POST'])
def user_update(id):
    try:
        if (request.method == 'GET'):
            cursor = mysql.connection.cursor()
            cursor.execute(f"SELECT * FROM users WHERE id = {id}")
            user = cursor.fetchone()
            return render_template('users/update.html', user=user)
        elif (request.method == 'POST'):
            nombre = request.form['nombre']
            email = request.form['email']
            contrasena = request.form['contrasena']
            contrasena_encode = contrasena.encode('utf-8')
            contrasena_crypt = bcrypt.hashpw(contrasena_encode, semilla)

            # Los f-strings no funcionan bien al armar esta query con un hash de contraseña, así que uso el código porcentaje
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE users SET nombre = %s, email = %s, contrasena = %s WHERE id = %s',
                           (nombre, email, contrasena_crypt, id))
            mysql.connection.commit()
            flash('Usuario actualizado', 'success')
            return redirect(url_for('users'))

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)



@app.route('/user_delete/<id>')
def user_delete(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(f'DELETE FROM users WHERE id={id}')
        mysql.connection.commit()
        flash('Usuario eliminado', 'success')
        return redirect(url_for('users'))

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)
