from flask import Flask
from config import *

# Instanciamos Flask. El primer argumento es el nombre del módulo o paquete de la aplicación: __name__ es un atajo conveniente apropiado para la mayoría de los casos. Esto es necesario para que Flask sepa dónde buscar recursos como plantillas y archivos estáticos. Con esta linea Python sabe que este archivo es el que arranca la aplicación.
app = Flask(__name__)

# Importamos el controlador después de declarar la variable "app", ya que el controlador lo usa para las rutas
from controladores.controlador import *

# Si éste es el archivo que arranca a la app, entonces la ejecutamos
#   1. Declaramos el puerto a usars
#   2. Debug true para que se actualice el front ante cualquier cambio
if __name__ == '__main__':
    # Base.metadata.drop_all(engine) Se eliminan las tablas de la BD
    # Base.metadata.create_all(engine) Se generans las tablas de la BD
    app.run(port=PUERTO, debug=DEBUG)
