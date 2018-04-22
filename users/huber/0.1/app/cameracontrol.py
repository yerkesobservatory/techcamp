from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired

class cameraForm(FlaskForm):
	takeimg = SubmitField(label= 'Take Image')

