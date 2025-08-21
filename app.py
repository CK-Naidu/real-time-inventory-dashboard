import os
import psycopg2
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

@app.route("/")
def dashboard():
    return render_template('index.html')

@app.route("/api/kpi/weather-impact")
def get_weather_impact():
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT WeatherCondition, AVG(UnitsSold) AS AvgUnitsSold
        FROM InventoryTransactions
        GROUP BY WeatherCondition;
    """
    cur.execute(query)
    colnames = [desc[0] for desc in cur.description]
    result = [dict(zip(colnames, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
