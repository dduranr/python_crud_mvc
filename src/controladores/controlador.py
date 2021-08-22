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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
import bcrypt
import sys

Base = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URI)




# Base.metadata.drop_all(engine) Se eliminan las tablas de la BD
# Base.metadata.create_all(engine) Se generans las tablas de la BD

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)
    created_at = Column(DateTime(255), default=datetime.now())
    updated_at = Column(DateTime(255), default=datetime.now())

    def __str__(self):
        return self.email


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



# HOME
# ------------------------------------------------------------
@app.route('/')
def index():

    # Para establecer conexión entre "sqlalchemy import create_engine" y los modelos se hace mediante sesiones. A través de esta sesión se va a gestionar las BD
    Session = sessionmaker(engine)
    session = Session()

    user1 = User(nombre='Tolomeo', email='tolomeo@gmail.com', contrasena='abcdef', created_at='2021-08-21 00:00:01', updated_at='2021-08-21 00:00:01')

    session.add(user1)
    session.commit()

    return render_template('index.html')



# AUTH
# ------------------------------------------------------------
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



# USERS
# ------------------------------------------------------------
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
            contrasena_encode = contrasena.encode('utf-8')
            contrasena_crypt = bcrypt.hashpw(contrasena_encode, semilla)
            contrasena_crypt_encode = contrasena_crypt.encode('utf-8')

            print("XXXXXXXXXXXXXXXXXXX HASH: ", contrasena_crypt_encode)

            cursor = mysql.connection.cursor()
            cursor.execute(
                f"INSERT INTO users (nombre, email, contrasena, created_at) VALUES ('{nombre}', '{email}', '{contrasena_crypt_encode}', '{ahora}')")
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



# CONTACTOS
# ------------------------------------------------------------
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
