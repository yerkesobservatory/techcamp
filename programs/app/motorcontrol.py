from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, IntegerField, FloatField

class submitForm(FlaskForm):
	submit = SubmitField(label= 'Submit')

class mpForm(FlaskForm):
	power = IntegerField("Power",default=0)

class mtForm(FlaskForm):
	time = FloatField("Time",default=0)

class motorForm(FlaskForm):
	motor = SelectField(
		'motor',
		choices=[(0,'Select Motor'),(1,'Motor 1'),(2,'Motor 2'),(3,'Both')]
	)
