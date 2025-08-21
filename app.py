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
    try:
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
    except Exception as e:
        print("Error in /api/kpi/weather-impact:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/kpi/sales-by-region")
def get_sales_by_region():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT Region, SUM(UnitsSold) AS TotalUnitsSold
            FROM InventoryTransactions
            GROUP BY Region;
        """
        cur.execute(query)
        colnames = [desc[0] for desc in cur.description]
        result = [dict(zip(colnames, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        print("Error in /api/kpi/sales-by-region:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/kpi/sales-by-category")
def get_sales_by_category():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT Category, SUM(UnitsSold) AS TotalUnitsSold
            FROM InventoryTransactions
            GROUP BY Category;
        """
        cur.execute(query)
        colnames = [desc[0] for desc in cur.description]
        result = [dict(zip(colnames, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        print("Error in /api/kpi/sales-by-category:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/kpi/sales-trend")
def get_sales_trend():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT SaleDate, SUM(UnitsSold) AS TotalUnitsSold
            FROM InventoryTransactions
            GROUP BY SaleDate
            ORDER BY SaleDate;
        """
        cur.execute(query)
        colnames = [desc[0] for desc in cur.description]
        result = [dict(zip(colnames, row)) for row in cur.fetchall()]
        cur.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        print("Error in /api/kpi/sales-trend:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
