from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class ContactoFormPost(FlaskForm):
	# Cada variable representa un campo de formulario
	nombre = StringField("Nombre", validators=[
		DataRequired(),
		Length(min=2)
	])
	telefono = StringField("Teléfono", validators=[
		DataRequired(),
		NumberRange(min=8, max=12)
	])
	email = StringField("Email", validators=[
		DataRequired(),
		Email()
	])
	submit = SubmitField("Agregar contacto")

class ContactoFormUpdate(FlaskForm):
	# Cada variable representa un campo de formulario
	nombre = StringField("Nombre", validators=[
		DataRequired(),
		Length(min=2)
	])
	telefono = StringField("Teléfono", validators=[
		DataRequired(),
		NumberRange(min=8, max=12)
	])
	email = StringField("Email", validators=[
		DataRequired(),
		Email()
	])
	submit = SubmitField("Actualizar contacto")
