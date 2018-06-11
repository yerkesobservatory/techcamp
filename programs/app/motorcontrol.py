from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import DecimalRangeField
from wtforms.validators import DataRequired

class submitForm(FlaskForm):
	submit = SubmitField(label= 'Execute')

class mpForm(FlaskForm):
	power = DecimalRangeField('power', default =0)
class mtForm(FlaskForm):
	time = SelectField(
		'Time',
		[('-1','Back 1 sec),('1','Forward 1 sec')]
	)
class servoForm(FlaskForm):
	time = SelectField(
		'Servo',
		[('0','Servo 0),('1','Servo 1')]
	)
