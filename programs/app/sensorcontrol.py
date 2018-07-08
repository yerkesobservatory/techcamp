from flask_wtf import FlaskForm
from wtforms import SelectField

class sensorForm(FlaskForm):
	sensor = SelectField(
		'Sensor',
		choices=[('time','Time'),('test','Test'),('dist1','Distance Sensor 1'),('dist2','Distance Sensor 2'),('dist3','Distance Sensor 3'),('dist4','Distance Sensor 4'),('head','Heading'),('pitch','Pitch'),('roll','Roll')]
	)
