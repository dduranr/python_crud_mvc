# from flask import Flask, render_template, url_for
# from app.modulos.auth import auth

# @auth.route('/') # Tengo que sacar la home de aquí, ya que no tiene nada que ver con el módulo de auth
# def index():
# 	return render_template('auth/blueprint.html')

# @auth.route('/')
# def auth2():
# 	return render_template('auth/blueprint.html')

# @auth.route('/saludo')
# def saludo():
# 	return render_template('auth/saludo.html')

# @auth.route('/user/<username>')
# def user(username):
# 	return render_template('auth/user.html', username=username)


# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Descripción de las clases importadas en este controlador
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

#   flask_sqlalchemy    ORM para SQL
#   render_template     Permite utilizar archivos HTML
#   request             Para obtener los datos de la petición de un form
#   redirect            Para hacer redirecciones
#   url_for             Para hacer redirecciones
#   flash               Manda mensajes entre vistas
#   session             Para gestionar sesiones
#   bcrypt              Para encriptar/desemcriptar contrasaeñas
#   sys                 Para obtener el tipo de excepción



from run import app
from flask import render_template, request, redirect, url_for, flash, session
from app.modulos.auth import auth
from app.modulos.auth.formularios.auth import AuthFormLogin
# from app.modulos.auth.modelos.user import *
import config
import bcrypt
import sys


# Para que la sesiones funcionen (la sesión del aplicativo, no de la BD), se debe establecer el "secret key"
# app.secret_key = 'mysecretkey'
print('SE LEE ESTO DESDE /app/modulos/auth/routes.py: ' + app.config.get('SECRET_KEY'))




@auth.route('/login')
def login():
    try:
        if 'user_id' in session:
            return redirect(url_for('welcome'))
        else:
            formulario = AuthFormLogin()
            return render_template('auth/login.html', formulario=formulario)

    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('errores/error.html', error=error)



@auth.route('/acceso', methods=['POST'])
def acceso():
    try:
        formulario = AuthFormLogin()
        if formulario.validate_on_submit():
            email = request.form['email']
            contrasena = request.form['contrasena']
            contrasena_encode = contrasena.encode('utf-8')

            usuario = User.getByEmail(email)

            if usuario:
                bd_contrasena = usuario.contrasena
                bd_contrasena = bd_contrasena.encode('utf-8')

                # Si en la BD se guarda un texto cualquiera y no un hash (p.e. abc), el navegador devuelve: ValueError: Invalid salt
                if(bcrypt.checkpw(contrasena_encode, bd_contrasena)):
                    session['user_id'] = usuario.id
                    session['user_nombre'] = usuario.nombre
                    session['user_email'] = usuario.email
                    return redirect(url_for('welcome'))
                else:
                    flash('Usuario/contraseña incorrectos', 'danger')
                    return redirect(url_for('login'))
            else :
                flash('Usuario/contraseña incorrectos', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Imposible crear sesión. Algún dato es incorrecto', 'danger')
            return render_template('auth/login.html', formulario=formulario)

    except exc.SQLAlchemyError as e:
        error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('errores/error.html', error="SQLAlchemyError: "+error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('errores/error.html', error=error)



@auth.route('/welcome')
def welcome():
    try:
        return render_template('auth/welcome.html')

    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('errores/error.html', error=error)



@auth.route('/logout')
def logout():
    try:
        session.clear()
        return redirect(url_for('login'))

    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('errores/error.html', error=error)
