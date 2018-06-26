from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, IntegerField

class submitForm(FlaskForm):
	submit = SubmitField(label= 'Submit')

class positionForm(FlaskForm):
	position = IntegerField("Position",default=0)

class servoForm(FlaskForm):
	servo = RadioField(
		'servo',
		choices=[(1,'Servo 1'),(2,'Servo 2'),(3,'Servo 3'),(4,'Servo 4')]
	)
