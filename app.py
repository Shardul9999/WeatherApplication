import requests
import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
app = Flask(__name__)


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

if not API_KEY:
    print("Error! API key Not found please check .env file again")

def get_weather_data(city):
    params = {
        'q' : city,
        'appid' : API_KEY,
        'units' : 'metric'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None
    

@app.route("/", methods=["GET","POST"])
def index():
    weather = None
    error = None
    
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            data = get_weather_data(city)
            if data:
                weather = {
                    'city': data['name'],
                    'temperature': round(data['main']['temp']),
                    'feels_like': round(data['main']['feels_like']), # NEW
                    'description': data['weather'][0]['description'].capitalize(),
                    'icon': data['weather'][0]['icon'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],             # NEW
                    'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p'), # NEW
                    'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p'),   # NEW
                }
            else:
                error = "City not found. Please try again."

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
                
