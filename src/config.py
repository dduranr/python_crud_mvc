import os

DEBUG = True
PUERTO = 3000

secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
PWD = os.path.abspath(os.curdir)

SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/pythonflaskcontactos'
# SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/pythonflaskcontactos'.format(
#     PWD)
SQLALCHEMY_TRACK_MODIFICATIONS = False
