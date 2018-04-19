from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class commandForm(FlaskForm):
	command = StringField('Enter Command', validators=[DataRequired()])
	submit = SubmitField('Send Command')

