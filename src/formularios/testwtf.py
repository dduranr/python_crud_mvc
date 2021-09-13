from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class FormularioTestwtf(FlaskForm):
	# Cada variable representa un campo de formulario
	nombre = StringField("Nombre", validators=[
		DataRequired(),
		Length(max=10, min=3)
	])
	email = StringField("Email", validators=[
		DataRequired(),
		Email()
	])
	submit = SubmitField("Enviar")
