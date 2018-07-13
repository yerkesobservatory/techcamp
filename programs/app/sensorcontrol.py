from flask_wtf import FlaskForm
from wtforms import SelectField

class sensorForm(FlaskForm):
	sensor = SelectField(
		'Sensor',
		choices=[('time','Time'),('test','Test'),('analog1','Analog 1'),('analog2','Analog 2'),('analog3','Analog 3'),('analog4','Analog 4'),('heading','Heading'),('pitch','Pitch'),('roll','Roll')]
	)
