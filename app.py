from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# OpenWeatherMap API key
API_KEY = 'bd5e378503939ddaee76f12ad7a97608'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    city_country = None
    winter_fact = "Did you know? The coldest temperature ever recorded on Earth was -128.6°F (-89.2°C) in Antarctica!"

    if request.method == 'POST':
        city = request.form.get('city')
        country = request.form.get('country')

        if city and country:
            city_country = f"{city}, {country}"
            # Fetch weather data from OpenWeatherMap with timeout
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric"
            try:
                response = requests.get(url, timeout=5)  # Added timeout
                if response.status_code == 200:
                    weather_data = response.json()
                else:
                    weather_data = {"error": "City not found or invalid API key."}
            except requests.exceptions.RequestException as e:
                weather_data = {"error": str(e)}

    return render_template('index.html', weather=weather_data, city_country=city_country, winter_fact=winter_fact)

if __name__ == '__main__':
    # Use environment variable to toggle debug mode
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0')
