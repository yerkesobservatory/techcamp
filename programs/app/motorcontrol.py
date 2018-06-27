from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, IntegerField, FloatField

class motorSubmit(FlaskForm):
	submit = SubmitField(label= 'Submit')

class mpForm(FlaskForm):
	power = IntegerField("Power",default=0)

class mtForm(FlaskForm):
	time = FloatField("Time",default=0)

class motorForm(FlaskForm):
	motor = RadioField(
		'motor',
		choices=[(1,'Motor 1'),(2,'Motor 2'),(3,'Motor 3'),(4,'Motor 4')]
	)
