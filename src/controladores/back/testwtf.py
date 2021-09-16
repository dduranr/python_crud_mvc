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
from formularios.testwtf import FormularioTestwtf
import bcrypt
import sys


# Semilla para encriptamiento de contraseña
semilla = bcrypt.gensalt()

# Importamos los modelos a usar
from modelos.testwtf import *



@app.route('/testwtfs')
def testwtfs():
    try:
        formulario = FormularioTestwtf()
        usuarios = sessionDB.query(Testwtf).all()
        return render_template('back/testwtfs/index.html', testwtfs=usuarios, formulario=formulario)

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



@app.route('/testwtf_post', methods=['POST'])
def testwtf_post():
    try:
        if request.method == 'POST':
            formulario = FormularioTestwtf()
            if formulario.validate_on_submit():
                nombre = request.form['nombre']
                email = request.form['email']

                testwtfExistente = Testwtf.getByEmail(email)

                if testwtfExistente:
                    flash('Imposible crear usuario, pues '+email+' ya existe como usuario en base de datos', 'danger')
                    return redirect(url_for('testwtfs'))
                else :
                    usuario = Testwtf(nombre=nombre, email=email)
                    usuario.post()
                    flash('Usuario agregado', 'success')
                    return redirect(url_for('testwtfs'))
            else:
                flash('Imposible crear testwtf. Algún dato es incorrecto', 'danger')
                return redirect(url_for('testwtfs'))

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



@app.route('/testwtf_update/<id>', methods=['GET', 'POST'])
def testwtf_update(id):
    try:
        testwtf = Testwtf.getById(id)
        if (request.method == 'GET'):
            # Generamos el form y le pasamos los values de cada campo
            formulario = FormularioTestwtf(request.form, nombre=testwtf.nombre, email=testwtf.email)

            if testwtf:
                return render_template('back/testwtfs/update.html', testwtf=testwtf, formulario=formulario)
            else :
                flash('Imposible encontrar al usuario', 'danger')
                return redirect(url_for('testwtfs'))
        elif (request.method == 'POST'):
            formulario = FormularioTestwtf()
            if formulario.validate_on_submit():

                nombre = request.form['nombre']
                email = request.form['email']
                testwtfExistente = Testwtf.getById(id)

                if not testwtfExistente:
                    flash('Imposible actualizar testwtf, pues el ID '+id+' no existe más en base de datos', 'danger')
                    return redirect(url_for('testwtfs'))
                else :
                    dataToSave = {"nombre": nombre, "email": email}
                    Testwtf.put(id, dataToSave)
                    flash('Usuario actualizado', 'success')
                    return redirect(url_for('testwtfs'))
            else:
                flash('Imposible actualizar testwtf. Algún dato es incorrecto', 'danger')
                return render_template('back/testwtfs/update.html', testwtf=testwtf, formulario=formulario)

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



@app.route('/testwtf_delete/<id>')
def testwtf_delete(id):
    try:
        testwtfExistente = Testwtf.getById(id)

        if not testwtfExistente:
            flash('Imposible eliminar testwtf, pues el ID ('+id+') no coincide con ningún testwtf en base de datos', 'danger')
            return redirect(url_for('testwtfs'))
        else :
            Testwtf.delete(id)

        flash('Usuario eliminado', 'success')
        return redirect(url_for('testwtfs'))

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
