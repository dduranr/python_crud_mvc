# Un modelo en Python es la clase que representa la tabla de la base de datos y su mapa de atributos por columna
# Una clase modelo hereda de db.Model y define las columnas como una instancia de la clase db.Column.

from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

# Parámetros disponibles SQLAlchemy
# 	Tipos de columna
# 	-----------------------------------------------
# 	SQLAlchemy	Python			SQL
# 	-----------------------------------------------
# 	BigInteger	int				BIGINT
# 	Boolean		bool			BOOLEAN or SMALLINT
# 	Date		datetime.date	DATE
# 	DateTime	datetime.date	DATETIME
# 	Integer		int				INTEGER
# 	Float		float			FLOAT or REAL
# 	Numeric		decimal.Decimal	NUMERIC
# 	Text		str				TEXT

# 	Constraints
# 	-----------------------------------------------
# 	Constraint		Description
# 	-----------------------------------------------
# 	nullable		When set to False makes the column required. Its default value is True.
# 	default			It provides a default value for the column.
# 	index			A boolean attribute. If set to True creates an indexed column.
# 	onupdate		It provides a default value for the column while updating a record.
# 	primary_key		A boolean attribute. If set to True marks the column as the primary key of the table.
# 	unique			A boolean attribute. If set to True each value in the column must be unique.

class Contactos(db.Model):
    __tablename__ = 'contactos'
    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
