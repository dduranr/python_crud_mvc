from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class FormularioTestwtf(FlaskForm):
	# Declaramos los futuros campos del formulario
	nombre = StringField("Nombre", validators=[
		DataRequired(),
		Length(max=10, min=3)
	])
	email = StringField("Email", validators=[
		DataRequired(),
		Email()
	])
	submit = SubmitField("Enviar")
