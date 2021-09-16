# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Descripción de las clases importadas en este controlador
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

#   Flask               El framework
#   config              Mi archivo que guarda las configuraciones generales del aplicativo



from flask import Flask
from config import *

# Instanciamos Flask. El primer argumento es el nombre del módulo o paquete de la aplicación: __name__ es un atajo conveniente apropiado para la mayoría de los casos. Esto es necesario para que Flask sepa dónde buscar recursos como plantillas y archivos estáticos. Con esta linea Python sabe que este archivo es el que arranca la aplicación.
app = Flask(__name__)

# Importamos los controladores después de declarar la variable "app", ya que el controlador lo usa para las rutas
# Backend
from controladores.back.auth import *
from controladores.back.users import *
from controladores.back.contactos import *
from controladores.back.testwtf import *
# Frontend
from controladores.front.home import *

# Si éste es el archivo que arranca a la app, entonces la ejecutamos
#   1. Declaramos el puerto a usar
#   2. Debug true para que se actualice el front ante cualquier cambio
if __name__ == '__main__':
    app.run(port=PUERTO, debug=DEBUG)
