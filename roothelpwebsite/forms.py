from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired

class DataForm(FlaskForm):
    cropType = StringField('Crop Type', validators=[DataRequired()])
    area = FloatField('Area', validators=[DataRequired()])
    soilMoisture = FloatField('Soil Moisture', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        self.latitude = kwargs.pop('latitude', None)
        self.longitude = kwargs.pop('longitude', None)
        super(DataForm, self).__init__(*args, **kwargs)
