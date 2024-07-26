from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class DataForm(FlaskForm):
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    cropType = StringField('cropType', validators= [DataRequired()])
    area = FloatField('area', validators= [DataRequired()])
    soilMoisture = FloatField('soilMoisture', validators= [DataRequired()])