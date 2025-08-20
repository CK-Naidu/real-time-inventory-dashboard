# app.py (Temporary Debug Version)
import os
import psycopg2
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(_name_)

def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

@app.route("/")
def dashboard():
    return render_template('index.html')

@app.route("/api/kpi/weather-impact")
def get_weather_impact():
    # This will return FAKE data for now, to test the frontend
    fake_data = [
        {"weathercondition": "Sunny", "avgunitsold": 150},
        {"weathercondition": "Rainy", "avgunitsold": 120},
        {"weathercondition": "Cloudy", "avgunitsold": 135}
    ]
    return jsonify(fake_data)

# The /run-check endpoint is temporarily removed

if _name_ == "_main_":
    app.run(debug=True, port=int(os.environ.get("PORT", 8080)))
