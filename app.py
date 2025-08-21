import os
import psycopg2
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import traceback

load_dotenv()
print("Loaded DATABASE_URL:", os.getenv('DATABASE_URL'))

app = Flask(__name__)

import os
import psycopg2
from urllib.parse import urlparse

def get_db_connection():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set")

    result = urlparse(DATABASE_URL)
    
    conn = psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port,
        sslmode='require'
    )
    return conn


@app.route("/")
def dashboard():
    return render_template('index.html')

@app.route("/api/kpi/weather-impact")
def get_weather_impact():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT weathercondition AS WeatherCondition, AVG(unitssold) AS AvgUnitsSold
            FROM InventoryTransactions
            GROUP BY weathercondition;
        """
        cur.execute(query)
        colnames = [desc[0] for desc in cur.description]
        result = [dict(zip(colnames, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception:
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/kpi/sales-by-region")
def get_sales_by_region():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT region, SUM(unitssold) AS TotalUnitsSold
            FROM InventoryTransactions
            GROUP BY region;
        """
        cur.execute(query)
        colnames = [desc[0] for desc in cur.description]
        result = [dict(zip(colnames, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception:
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/kpi/sales-by-category")
def get_sales_by_category():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT category, SUM(unitssold) AS TotalUnitsSold
            FROM InventoryTransactions
            GROUP BY category;
        """
        cur.execute(query)
        colnames = [desc[0] for desc in cur.description]
        result = [dict(zip(colnames, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception:
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/kpi/sales-trend")
def get_sales_trend():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT date AS SaleDate, SUM(unitssold) AS TotalUnitsSold
            FROM InventoryTransactions
            GROUP BY date
            ORDER BY date;
        """
        cur.execute(query)
        colnames = [desc[0] for desc in cur.description]
        result = [dict(zip(colnames, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception:
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

