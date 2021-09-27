from app import create_app

# Al crear la aplicación indicamos el environment que queremos usar (production, development, etc).
app = create_app('development')
app.run()