from roothelpwebsite import app
from flask import render_template, request, redirect
import geocoder
from roothelpwebsite.forms import DataForm
import requests
from bs4 import BeautifulSoup


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

def scrape_fao_crop_data(crop_type):
    base_url = 'https://www.fao.org/land-water/databases-and-software/crop-information/'
    crop_url = f'{base_url}{crop_type}/en/'
    response = requests.get(crop_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for div in soup.find_all('div', class_='rgaccord1-content'):
        header = div.find_previous_sibling('h3')
        if header and 'Water Requirements' in header.text:
            water_section = div
            break

    if water_section:
        water_recommendations = {}
        h1_tag = water_section.find('h1')
        p_tags = water_section.find_all('p', class_='bodytext')
        
        if h1_tag:
            water_recommendations['Title'] = h1_tag.text.strip()
        
        for p in p_tags:
            if 'water requirements' in p.text.lower():
                water_recommendations['Details'] = p.text.strip()
                
        return water_recommendations
    else:
        return None
    
def generate_recomendation(foa_guidelines, crop_type, temperature, area, soil_moisture):
    url = "https://chat-gtp-free.p.rapidapi.com/v1/chat/completions"

    payload = {
        "model": "92d97036-3e25-442b-9a25-096ab45b0525",
        "messages": [
            {
                "role": "user",
                "content": f"My crop_type is {crop_type} and I am trying to grow it in {temperature} degree celcius, in an area of {area} sq.mt \
                            with soil moisture content at {soil_moisture}%, use the below FAO guideline to generate a good recomendation recomendation \
                            for this crop: {foa_guidelines} and what quantity of irrigation water will it require (in litres). Make it short and on point with one paragraph or two"
            }
        ]
    }

    payload_2 = {
        "model": "92d97036-3e25-442b-9a25-096ab45b0525",
        "messages": [
            {
                "role": "user",
                "content": f"Give me a one liner following last response on how much water it will requires, in litres based on {crop_type}, {soil_moisture}%, {temperature}, {area}, and these guidelines: {foa_guidelines}"
            }
        ]
    }
    headers = {
        "x-rapidapi-key": "8291a087b6msha1baa6a898cfc2ep18e54ajsn16cd191a0aab",
        "x-rapidapi-host": "chat-gtp-free.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response_one = requests.post(url, json=payload, headers=headers)

    response_two = requests.post(url, json=payload_2, headers=headers)

    return response_one.json(), response_two.json()
    
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
    
    fao_data = scrape_fao_crop_data(crop_type)
    
    recomendation, water_required = generate_recomendation(fao_data, crop_type, weather_data["weather"], area, soil_moisture)
    
    if 'error' in weather_data:
        return render_template('calculate.html', error=weather_data['error'])
    
    return render_template('calculate.html', 
                           crop_type=crop_type, 
                           area=area, 
                           soil_moisture=soil_moisture, 
                           weather_data=weather_data, 
                           recomendation = recomendation['text'],
                           water_required = water_required['text'])
