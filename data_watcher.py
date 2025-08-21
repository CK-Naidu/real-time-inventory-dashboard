import os
import time
import pandas as pd
import psycopg2

CSV_FILE = os.getenv("CSV_FILE", "data/inventory_forecasting.csv")

def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def run_update_check():
    print("--- Starting CSV data sync ---")
    if not os.path.exists(CSV_FILE):
        print(f"Error: CSV file {CSV_FILE} not found.")
        return
    
    df = pd.read_csv(CSV_FILE)
    
    # Normalize column names: replace spaces and slashes with underscores
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace("/", "_")
    print("CSV columns loaded after normalization:", df.columns.tolist())

    # Convert Date column to proper datetime with day-first format
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True).dt.date

    if df.empty:
        print("No data found in CSV.")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("TRUNCATE TABLE InventoryTransactions, Stores, Products, Categories, Regions RESTART IDENTITY CASCADE;")
        
        # Insert unique regions
        regions = {name: i+1 for i, name in enumerate(df['Region'].unique())}
        cursor.executemany("""
            INSERT INTO Regions (RegionName) VALUES (%s)
            ON CONFLICT (RegionName) DO NOTHING;
        """, [(r,) for r in regions.keys()])
        
        # Insert categories
        categories = {name: i+1 for i, name in enumerate(df['Category'].unique())}
        cursor.executemany("""
            INSERT INTO Categories (CategoryName) VALUES (%s)
            ON CONFLICT (CategoryName) DO NOTHING;
        """, [(c,) for c in categories.keys()])
        
        # Insert stores
        stores_df = df[['Store_ID', 'Region']].drop_duplicates()
        cursor.executemany("""
            INSERT INTO Stores (StoreID, RegionID) VALUES (%s, %s)
            ON CONFLICT (StoreID) DO NOTHING;
        """, [(row.Store_ID, regions[row.Region]) for row in stores_df.itertuples()])
        
        # Insert products
        products_df = df[['Product_ID', 'Category']].drop_duplicates()
        cursor.executemany("""
            INSERT INTO Products (ProductID, CategoryID) VALUES (%s, %s)
            ON CONFLICT (ProductID) DO NOTHING;
        """, [(row.Product_ID, categories[row.Category]) for row in products_df.itertuples()])
        
        # Insert inventory transactions
        data = [tuple(row) for row in df[['Date','Store_ID','Product_ID','Inventory_Level',
                                          'Units_Sold','Units_Ordered','Demand_Forecast','Price',
                                          'Discount','Weather_Condition','Holiday_Promotion',
                                          'Competitor_Pricing','Seasonality']].itertuples(index=False)]
        
        query = """
            INSERT INTO InventoryTransactions (
                Date, StoreID, ProductID, InventoryLevel, UnitsSold, UnitsOrdered,
                DemandForecast, Price, Discount, WeatherCondition, HolidayPromotion,
                CompetitorPricing, Seasonality
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """
        cursor.executemany(query, data)
        conn.commit()
        print("--- Database updated successfully from CSV ---")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    while True:
        run_update_check()
        print("Sleeping 15 minutes...")
        time.sleep(900)
