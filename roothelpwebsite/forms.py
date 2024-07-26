from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class DataForm(FlaskForm):
    cropType = StringField('cropType', validators= [DataRequired()])
    area = StringField('area', validators= [DataRequired()])
    soilMoisture = StringField('soilMoisture', validators= [DataRequired()])
    submit = SubmitField('Search')