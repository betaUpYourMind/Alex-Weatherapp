# app/main.py
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "8a1f7393bac2fe14036859c942bacf13"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = []
    if request.method == "POST":
        city1 = request.form.get("city1")
        city2 = request.form.get("city2")

        cities = [city1, city2]

        for city in cities:
            if city:
                weather = get_weather(city)
                if weather:
                    weather_data.append(weather)
    return render_template("index.html", weather_data=weather_data)

@app.route("/weather", methods=["GET"])
def weather():
    lat = request.args.get("lat")
    lng = request.args.get("lng")

    if not lat or not lng:
        return jsonify({"error": "Latitud och longitud saknas."}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        })
    return jsonify({"error": "Kunde inte hämta väderdata."}), response.status_code

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }
    return None

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
