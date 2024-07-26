from roothelpwebsite import app
from flask import  render_template, url_for, request, flash, redirect
import geocoder
from roothelpwebsite.forms import DataForm
import requests

def get_weather(lat, lon, api_key):
    base_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=alerts&appid={api_key}&units=metric"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, )
    data = response.json()
    
    if response.status_code == 200:
        return {
            'temperature': data['main']['temp'],
            'weather': data['weather'][0]['description']
        }
    else:
        return {'error': data.get('message', 'An error occurred')}

@app.route("/")
@app.route("/home")
def home():
    # Automatically determine latitude and longitude
    g = geocoder.ip('me')
    form = DataForm(latitude=g.latlng[0], longitude=g.latlng[1])
    return render_template('Layout.html', form = form)

@app.route('/calculate', methods=['POST'])
def calculate():
    # g = geocoder.ip('me')
    # form = DataForm(latitude=g.latlng[0], longitude=g.latlng[1])
    # crop_type = form['cropType']
    # area = (form['area'])
    # soil_moisture = (form['soilMoisture'])
    # latitude = float(form['latitude'])
    # longitude = float(form['longitude'])
    # api_key = "6d9d8a496b4cbad80299f18349888065"

    return render_template('calculate.html')