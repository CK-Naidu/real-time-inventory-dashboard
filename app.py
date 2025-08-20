import os
import psycopg2
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
from google_sheets_watcher import run_update_check

load_dotenv()
app = Flask(__name__)

def get_db_connection():
    # In the cloud, the DATABASE_URL is provided automatically by the environment
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

# This special endpoint will be called by our automated scheduler
@app.route("/run-check", methods=["POST"])
def run_check_endpoint():
    message = run_update_check()
    return message, 200

if _name_ == "_main_":
    app.run(debug=True, port=int(os.environ.get("PORT", 8080)))
  
