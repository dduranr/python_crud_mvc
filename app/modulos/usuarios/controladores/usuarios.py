# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Descripción de las clases importadas en este controlador
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

#   render_template     Permite utilizar archivos HTML
#   request             Para obtener los datos de la petición de un form
#   redirect            Para hacer redirecciones
#   url_for             Para hacer redirecciones
#   flash               Manda mensajes entre vistas
#   datetime            Para manejar fechas y horas
#   bcrypt              Para encriptar/desemcriptar contrasaeñas
#   sys                 Para obtener el tipo de excepción



from app import app
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from formularios.users import *
import bcrypt
import sys


# Semilla para encriptamiento de contraseña
semilla = bcrypt.gensalt()

# Importamos los modelos a usar
from modelos.user import *



@app.route('/users')
def users():
    try:
        formulario = UserFormPost()
        usuarios = sessionDB.query(User).all()
        return render_template('back/users/index.html', users=usuarios, formulario=formulario)

    except exc.SQLAlchemyError as e:
        error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('back/errores/error.html', error="SQLAlchemyError: "+error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('back/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('back/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('back/errores/error.html', error=error)



@app.route('/user_post', methods=['POST'])
def user_post():
    try:
        if request.method == 'POST':
            usuarios = sessionDB.query(User).all()
            formulario = UserFormPost()
            if formulario.validate_on_submit():
                now = datetime.now()
                ahora = now.strftime("%Y-%m-%d %H:%M:%S")

                nombre = request.form['nombre']
                email = request.form['email']
                contrasena = request.form['contrasena']
                contrasena_encode = contrasena.encode('utf-8')
                contrasena_crypt = bcrypt.hashpw(contrasena_encode, semilla)

                userExistente = User.getByEmail(email)

                if userExistente:
                    flash('Imposible crear usuario, pues '+email+' ya existe como usuario en base de datos', 'danger')
                    return redirect(url_for('users'))
                else :
                    usuario = User(nombre=nombre, email=email, contrasena=contrasena_crypt)
                    usuario.post()
                    flash('Usuario agregado', 'success')
                    return redirect(url_for('users'))
            else:
                flash('Imposible crear usuario. Algún dato es incorrecto', 'danger')
                return render_template('back/users/index.html', users=usuarios, formulario=formulario)

    except exc.SQLAlchemyError as e:
        error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('back/errores/error.html', error="SQLAlchemyError: "+error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('back/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('back/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('back/errores/error.html', error=error)



@app.route('/user_update/<id>', methods=['GET', 'POST'])
def user_update(id):
    try:
        user = User.getById(id)
        if (request.method == 'GET'):
            # Generamos el form y le pasamos los values de cada campo
            formulario = UserFormUpdate(request.form, nombre=user.nombre, email=user.email)

            if user:
                return render_template('back/users/update.html', user=user, formulario=formulario)
            else :
                flash('Imposible encontrar al usuario', 'danger')
                return redirect(url_for('users'))
        elif (request.method == 'POST'):
            formulario = UserFormUpdate()
            if formulario.validate_on_submit():
                nombre = request.form['nombre']
                email = request.form['email']
                contrasena = request.form['contrasena']

                userExistente = User.getById(id)

                if not userExistente:
                    flash('Imposible actualizar user, pues el ID '+id+' no existe más en base de datos', 'danger')
                    return redirect(url_for('users'))
                else :
                    if(len(contrasena) > 0):
                        contrasena_encode = contrasena.encode('utf-8')
                        contrasena_crypt = bcrypt.hashpw(contrasena_encode, semilla)
                        dataToSave = {"nombre": nombre, "email": email, "contrasena": contrasena_crypt}
                        User.put(id, dataToSave)
                    else:
                        dataToSave = {"nombre": nombre, "email": email, "contrasena": userExistente.contrasena}
                        User.put(id, dataToSave)
                        flash('Usuario actualizado', 'success')
                        return redirect(url_for('users'))
            else:
                flash('Imposible actualizar usuario. Algún dato es incorrecto', 'danger')
                return render_template('back/users/update.html', user=user, formulario=formulario)

    except exc.SQLAlchemyError as e:
        error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('back/errores/error.html', error="SQLAlchemyError: "+error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('back/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('back/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('back/errores/error.html', error=error)



@app.route('/user_delete/<id>')
def user_delete(id):
    try:
        userExistente = User.getById(id)

        if not userExistente:
            flash('Imposible eliminar user, pues el ID ('+id+') no coincide con ningún user en base de datos', 'danger')
            return redirect(url_for('users'))
        else :
            User.delete(id)

        flash('Usuario eliminado', 'success')
        return redirect(url_for('users'))

    except exc.SQLAlchemyError as e:
        error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('back/errores/error.html', error="SQLAlchemyError: "+error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('back/errores/error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('back/errores/error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('back/errores/error.html', error=error)
