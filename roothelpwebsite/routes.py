from roothelpwebsite import app
from flask import render_template, request, redirect
import geocoder
from roothelpwebsite.forms import DataForm
import requests
import http.client


def get_weather(lat, lon):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    query_string = {"q":f"{lat},{lon}"}

    headers = {
	"x-rapidapi-key": "8291a087b6msha1baa6a898cfc2ep18e54ajsn16cd191a0aab",
	"x-rapidapi-host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=query_string)
    data = response.json()

    if response.status_code == 200:
        return {
            'city': data['location']['name'],
            'weather': data['current']['temp_c']
        }
    else:
        return {'error': data.get('message', 'An error occurred')}

@app.route("/")
@app.route("/home")
def home():
    geo_code = geocoder.ip('me')
    form = DataForm(latitude=geo_code.latlng[0], longitude=geo_code.latlng[1])
    return render_template('Layout.html', form=form)

@app.route('/calculate', methods=['POST'])
def calculate():
    geo_code = geocoder.ip('me')
    form = DataForm(request.form, latitude=geo_code.latlng[0], longitude=geo_code.latlng[1])
    
    crop_type = form.cropType.data
    area = form.area.data
    soil_moisture = form.soilMoisture.data
    
    # Fetch weather data using the latitude and longitude
    weather_data = get_weather(form.latitude, form.longitude)
    print(weather_data)
    
    if 'error' in weather_data:
        return render_template('calculate.html', error=weather_data['error'])
    
    return render_template('calculate.html', crop_type=crop_type, area=area, soil_moisture=soil_moisture, weather_data=weather_data)
