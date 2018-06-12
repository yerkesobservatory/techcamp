from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, IntegerField, validators

class submitForm(FlaskForm):
	submit = SubmitField(label= 'Submit')

class mpForm(FlaskForm):
	power = IntegerField("Power",[validators.NumberRange(min=-255,max=255,message="Must be between -255 and 255")])

class mtForm(FlaskForm):
	time = SelectField(
		'Time',
		choices=[('-1','Back 1 sec'),('1','Forward 1 sec')]
	)
class servoForm(FlaskForm):
	time = SelectField(
		'Time',
		choices=[('0','Servo 0'),('1','Servo 1')]
	)
