# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# Descripción de las clases importadas en este controlador
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

#   os                 Permite acceder a funcionalidades dependientes del Sistema Operativo. Sobre todo
# 					   aquellas que nos refieren información sobre el entorno del mismo y nos permiten
# 					   manipular la estructura de directorios, para leer y escribir archivos. Gracias al
# 					   paquete "os" podemos acceder a las variables de entorno de nuestro sistema operativo.
# 					   Más abajo se ve cómo obtener la variable de entorno SECRET_KEY a través del módulo os
# 					   (puede llevar un 2do parámetro el GET, con el fin de que si no se encuentra disponible
# 					   SECRET_KEY se asigna como default cualquiera que sea el valor que se ponga como 2do parámetro).
# 					   Si una variable de entorno buscada no ha sido definida, get() devuelve None.

# IMPORTANTE. Se recomienda utilizar las variables de entorno. Si bien es posible configurar ENV y DEBUG en su configuración o código, esto se desaconseja enfáticamente. El comando flask no puede leerlos con anticipación y es posible que algunos sistemas o extensiones ya se hayan configurado en función de un valor anterior.


import os

# DEBUG = True
# secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

class Config:
	# Aquí se obtienen las variables de entorno del SO. Como no las declaro, se usa en sul ugar el valor por defecto.
	SECRET_KEY = os.environ.get('SECRET_KEY', 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT')

class Development(Config):
	DEBUG = True	# Se detecta el debug justo así (no hay necesidad de hacer después app.run(debug=True))
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT_Developments'
	FLASK_ENV = 'development'
	FLASK_DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/pythonflaskcontactos'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class Production(Config):
	DEBUG = False	# Se detecta el debug justo así (no hay necesidad de hacer después app.run(debug=True))
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT_Production'
	FLASK_ENV = 'production'
	FLASK_DEBUG = False
	pass

config = {
	'development': Development,
	'production': Production
}
