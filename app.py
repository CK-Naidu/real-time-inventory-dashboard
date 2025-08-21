import os
import psycopg2
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(_name_)

def get_db_connection():
    # Railway provides the database URL as an environment variable
    return psycopg2.connect(os.getenv('DATABASE_URL'))

@app.route("/")
def dashboard():
    return render_template('index.html')

@app.route("/api/kpi/weather-impact")
def get_weather_impact():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT WeatherCondition, AVG(UnitsSold) AS AvgUnitsSold FROM InventoryTransactions GROUP BY WeatherCondition;"
    cursor.execute(query)

    colnames = [desc[0] for desc in cursor.description]
    result = [dict(zip(colnames, row)) for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return jsonify(result)

if _name_ == "_main_":
    # The port is set by Railway's PORT environment variable
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
