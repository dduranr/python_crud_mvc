# Para que el contenido del directorio "app" sea accesible en Python, debemos usar este __init__.py, donde se define la función que utilizamos en run.py para crear el objeto app con su correspondiente configuración.
# Aquí será donde quedan registrados los Blueprints.
from flask import Flask
from config import config

def create_app(entorno):
	app = Flask(__name__)
	# Para habilitar la configuración hallada en config.py sólo se llama a from_object(). Por tanto, En la siguiente línea indicamos el environment (producción, desarrollo, etc) a usar cuando se genere la app.
	app.config.from_object(config[entorno])

	# Configuración de los BluePrints
	from app.modulos.auth import auth as auth


	app.register_blueprint(auth, url_prefix='/auth') # url_prefix sirve para ponerle un prefijo a todas las rutas del módulo en cuestión

	return app