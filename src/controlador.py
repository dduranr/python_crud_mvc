# Importamos las clases que necesitamos
#   Flask               Que es el framework
#   flask_sqlalchemy    ORM para SQL
#   render_template     Permite utilizar archivos HTML
#   request             Para obtener los datos de la petición de un form
#   redirect            Para hacer redirecciones
#   url_for             Para hacer redirecciones
#   flash               Manda mensajes entre vistas
#   sys                 Para obtener el tipo de excepción
from app import app  # El 2do "app" es la instancia de Flask() declarada en app.py (el 1ro creo que es el nombre del archivo app.py)
from config import *
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime
import bcrypt
import sys

from modelos import *

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# Semilla para encriptamiento de contraseña
semilla = bcrypt.gensalt()

# Sesión
app.secret_key = 'mysecretkey'


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# AUTH
# AUTH
# AUTH
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
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
        # contrasena_crypt = bcrypt.hashpw(contrasena_encode, semilla)

        cursor = mysql.connection.cursor()
        # cursor.execute(f"SELECT * FROM users WHERE email = '{email}' AND contrasena = '{contrasena_crypt}'")
        cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
        user = cursor.fetchone()

        bd_contrasena = user[3]
        bd_contrasena = bd_contrasena.encode('utf-8')

        # Si en la BD se guarda un texto cualquier y no un hash (p.e. abc), el navegador devuelve: ValueError: Invalid salt
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


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# USERS
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users')
def users():
    try:
        users = Users.query.all()
        usersArray = []
        for user in users:
            usersArray += [[user.id, user.nombre, user.email]]
        return render_template('users/index.html', users=usersArray)

    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
    except TypeError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción general: " + str(e)
        return render_template('error.html', error="ValueError: "+error)


@app.route('/contactos')
def contactos():
    try:
        contactos = Contactos.query.all()
        contactosArray = []
        for contactos in contactos:
            contactosArray += [[contactos.id, contactos.nombre, contactos.telefono, contactos.email]]
        return render_template('contactos/index.html', contactos=contactosArray)

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


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# CONTACTOS
# CONTACTOS
# CONTACTOS
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
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
