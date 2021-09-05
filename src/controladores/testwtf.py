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
    # try:

        formulario = FormularioTestwtf()

        usuarios = sessionDB.query(Testwtf).all()
        return render_template('testwtfs/index.html', testwtfs=usuarios, formulario=formulario)

    # except exc.SQLAlchemyError as e:
    #     error = "Excepción SQLAlchemyError: " + str(e)
    #     return render_template('error.html', error="SQLAlchemyError: "+error)
    # except TypeError as e:
    #     error = "Excepción TypeError: " + str(e)
    #     return render_template('error.html', error="TypeError: "+error)
    # except ValueError as e:
    #     error = "Excepción ValueError: " + str(e)
    #     return render_template('error.html', error="ValueError: "+error)
    # except Exception as e:
    #     error = "Excepción general: " + str(e.__class__)
    #     return render_template('error.html', error=error)



@app.route('/testwtf_post', methods=['POST'])
def testwtf_post():
    try:
        if request.method == 'POST':
            now = datetime.now()
            ahora = now.strftime("%Y-%m-%d %H:%M:%S")

            nombre = request.form['nombre']
            email = request.form['email']
            contrasena = request.form['contrasena']
            contrasena_encode = contrasena.encode('utf-8')
            contrasena_crypt = bcrypt.hashpw(contrasena_encode, semilla)

            testwtfExistente = Testwtf.getByEmail(email)

            if testwtfExistente:
                flash('Imposible crear usuario, pues '+email+' ya existe como usuario en base de datos', 'danger')
                return redirect(url_for('testwtfs'))
            else :
                usuario = Testwtf(nombre=nombre, email=email, contrasena=contrasena_crypt)
                usuario.post()

                flash('Usuario agregado', 'success')
                return redirect(url_for('testwtfs'))

    except exc.SQLAlchemyError as e:
        error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('error.html', error="SQLAlchemyError: "+error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)



@app.route('/testwtf_update/<id>', methods=['GET', 'POST'])
def testwtf_update(id):
    try:
        if (request.method == 'GET'):
            testwtf = Testwtf.getById(id)

            if testwtf:
                return render_template('testwtfs/update.html', testwtf=testwtf)
            else :
                flash('Imposible encontrar al usuario', 'danger')
                return redirect(url_for('testwtfs'))
        elif (request.method == 'POST'):
            nombre = request.form['nombre']
            email = request.form['email']
            contrasena = request.form['contrasena']

            testwtfExistente = Testwtf.getById(id)

            if not testwtfExistente:
                flash('Imposible actualizar testwtf, pues el ID '+id+' no existe más en base de datos', 'danger')
                return redirect(url_for('testwtfs'))
            else :
                if(len(contrasena) > 0):
                    contrasena_encode = contrasena.encode('utf-8')
                    contrasena_crypt = bcrypt.hashpw(contrasena_encode, semilla)
                    dataToSave = {"nombre": nombre, "email": email, "contrasena": contrasena_crypt}
                    Testwtf.put(id, dataToSave)
                else:
                    dataToSave = {"nombre": nombre, "email": email, "contrasena": testwtfExistente.contrasena}
                    Testwtf.put(id, dataToSave)

            flash('Usuario actualizado', 'success')
            return redirect(url_for('testwtfs'))

    except exc.SQLAlchemyError as e:
        error = "Excepción SQLAlchemyError: " + str(e)
        return render_template('error.html', error="SQLAlchemyError: "+error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)



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
        return render_template('error.html', error="SQLAlchemyError: "+error)
    except TypeError as e:
        error = "Excepción TypeError: " + str(e)
        return render_template('error.html', error="TypeError: "+error)
    except ValueError as e:
        error = "Excepción ValueError: " + str(e)
        return render_template('error.html', error="ValueError: "+error)
    except Exception as e:
        error = "Excepción general: " + str(e.__class__)
        return render_template('error.html', error=error)
