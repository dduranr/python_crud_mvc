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
#   sys                 Para obtener el tipo de excepción



from app import app
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
import sys

# Importamos los modelos a usar
from modelos.contacto import *



@app.route('/contactos')
def contactos():
    try:
        contactos = sessionDB.query(Contacto).all()
        return render_template('contactos/index.html', contactos=contactos)

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



@app.route('/contacto_post', methods=['POST'])
def contacto_post():
    try:
        if request.method == 'POST':
            now = datetime.now()
            ahora = now.strftime("%Y-%m-%d %H:%M:%S")

            nombre = request.form['nombre']
            telefono = request.form['telefono']
            email = request.form['email']

            contactoExistente = Contacto.getByEmail(email)

            if contactoExistente:
                flash('Imposible crear contacto, pues '+email+' ya existe como contacto en base de datos', 'danger')
                return redirect(url_for('contactos'))
            else :
                contacto = Contacto(nombre=nombre, telefono=telefono, email=email)
                contacto.post()

                flash('Contacto agregado', 'success')
                return redirect(url_for('contactos'))

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



@app.route('/contacto_update/<id>', methods=['GET', 'POST'])
def contacto_update(id):
    try:
        if (request.method == 'GET'):
            contacto = Contacto.getById(id)

            if contacto:
                return render_template('contactos/update.html', contacto=contacto)
            else :
                flash('Imposible encontrar el contacto', 'danger')
                return redirect(url_for('contactos'))
        elif (request.method == 'POST'):
            nombre = request.form['nombre']
            telefono = request.form['telefono']
            email = request.form['email']

            contactoExistente = Contacto.getById(id)

            if not contactoExistente:
                flash('Imposible actualizar contacto, pues el ID '+id+' no existe más en base de datos', 'danger')
                return redirect(url_for('contactos'))
            else :
                dataToSave = {"nombre": nombre, "email": email, "telefono": telefono}
                Contacto.put(id, dataToSave)

            flash('Contacto actualizado', 'success')
            return redirect(url_for('contactos'))

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



@app.route('/contacto_delete/<id>')
def contacto_delete(id):
    try:
        contactoExistente = Contacto.getById(id)

        if not contactoExistente:
            flash('Imposible eliminar contacto, pues el ID ('+id+') no coincide con ningún contacto en base de datos', 'danger')
            return redirect(url_for('contactos'))
        else :
            Contacto.delete(id)

        flash('Contacto eliminado', 'success')
        return redirect(url_for('contactos'))

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
