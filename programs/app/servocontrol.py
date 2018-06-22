from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, IntegerField

class submitForm(FlaskForm):
	submit = SubmitField(label= 'Submit')

class directForm(FlaskForm):
	direction = IntegerField("Direction",default=0)

class servoForm(FlaskForm):
	servo = SelectField(
		'servo',
		choices=[(0,'Select Servo'),(1,'Servo 1'),(2,'Servo 2'),(3,'Both')]
	)
