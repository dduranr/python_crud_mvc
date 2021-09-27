from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
import phonenumbers

class ContactoFormPost(FlaskForm):
	# Cada variable representa un campo de formulario
	nombre = StringField("Nombre", validators=[
		DataRequired(),
		Length(min=2)
	])
	telefono = StringField("Teléfono", validators=[
		DataRequired()
	])
	email = StringField("Email", validators=[
		DataRequired(),
		Email()
	])
	submit = SubmitField("Agregar")

	# Desde aquí mismo se hace la validación del campo
	def validate_telefono(self, telefono):
		try:
			p = phonenumbers.parse(telefono.data)
			if not phonenumbers.is_valid_number(p):
				raise ValueError()
		except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
			raise ValidationError('Número de teléfono inválido')



class ContactoFormUpdate(FlaskForm):
	# Cada variable representa un campo de formulario
	nombre = StringField("Nombre", validators=[
		DataRequired(),
		Length(min=2)
	])
	telefono = StringField("Teléfono", validators=[
		DataRequired()
	])
	email = StringField("Email", validators=[
		DataRequired(),
		Email()
	])
	submit = SubmitField("Actualizar")

	# Desde aquí mismo se hace la validación del campo
	def validate_telefono(self, telefono):
		try:
			p = phonenumbers.parse(telefono.data)
			if not phonenumbers.is_valid_number(p):
				raise ValueError()
		except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
			raise ValidationError('Número de teléfono inválido')