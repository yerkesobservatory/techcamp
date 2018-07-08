from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, IntegerField

class servoSubmit(FlaskForm):
	submit = SubmitField(label= 'Submit')

class positionForm(FlaskForm):
	position = IntegerField("position",default=0)

class servoForm(FlaskForm):
	servo = RadioField(
		'servo',
		choices=[(0,'Servo 1'),(1,'Servo 2'),(2,'Servo 3'),(3,'Servo 4')]
	)
