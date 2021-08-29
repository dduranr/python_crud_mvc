# Un modelo en Python es la clase que representa la tabla de la base de datos y su mapa de atributos por columna
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

# Base.metadata.drop_all(engine) Se eliminan las tablas de la BD
# Base.metadata.create_all(engine) Se generans las tablas de la BD



from app import app  # El 1er app es el nombre del archivo app.py. El 2do "app" es la instancia de Flask() declarada en app.py
from config import *
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Para establecer conexión entre "sqlalchemy import create_engine" y los modelos se hace mediante sesiones. A través de esta sesión se va a gestionar las BD
Session = sessionmaker(engine)
sessionDB = Session()



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)
    created_at = Column(DateTime(255), default=datetime.now())
    updated_at = Column(DateTime(255), default=datetime.now(), onupdate=datetime.now())

    def __str__(self):
        return self.email



class Contacto(Base):
    __tablename__ = 'contactos'
    id = Column(Integer(), primary_key=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime(255), default=datetime.now())
    updated_at = Column(DateTime(255), default=datetime.now(), onupdate=datetime.now())

    def __str__(self):
        return self.email

