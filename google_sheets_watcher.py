import os
import io
import pandas as pd
import psycopg2
import gspread

# --- Configuration ---
GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'InventoryDataSource')

def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def run_update_check():
    print("--- Starting Google Sheets data sync ---")
    try:
        # This uses the application's default credentials in the cloud
        gc = gspread.service_account()
        spreadsheet = gc.open(GOOGLE_SHEET_NAME)
        worksheet = spreadsheet.sheet1

        print("Fetching all records from the sheet...")
        records = worksheet.get_all_records()
        df = pd.DataFrame(records)

        if df.empty:
            return "No data found in Google Sheet."

        df.columns = [col.replace(' ', '').replace('/', '') for col in df.columns]

        conn = get_db_connection()
        cursor = conn.cursor()

        print("Clearing all old data...")
        cursor.execute("TRUNCATE TABLE InventoryTransactions, Stores, Products, Categories, Regions RESTART IDENTITY CASCADE;")

        print("Populating dimension tables...")
        regions = {name: i + 1 for i, name in enumerate(df['Region'].unique())}
        cursor.executemany("INSERT INTO Regions (RegionName) VALUES (%s);", [(name,) for name in regions.keys()])

        categories = {name: i + 1 for i, name in enumerate(df['Category'].unique())}
        cursor.executemany("INSERT INTO Categories (CategoryName) VALUES (%s);", [(name,) for name in categories.keys()])

        stores_df = df[['Store_ID', 'Region']].drop_duplicates()
        cursor.executemany("INSERT INTO Stores (StoreID, RegionID) VALUES (%s, %s);", [(row.Store_ID, regions[row.Region]) for row in stores_df.itertuples()])

        products_df = df[['Product_ID', 'Category']].drop_duplicates()
        cursor.executemany("INSERT INTO Products (ProductID, CategoryID) VALUES (%s, %s);", [(row.Product_ID, categories[row.Category]) for row in products_df.itertuples()])

        print(f"Populating InventoryTransactions with {len(df)} records...")
        transaction_data = [tuple(row) for row in df[['Date', 'Store_ID', 'Product_ID', 'Inventory_Level', 'Units_Sold', 'Units_Ordered', 'Demand_Forecast', 'Price', 'Discount', 'Weather_Condition', 'Holiday_Promotion', 'Competitor_Pricing', 'Seasonality']].itertuples(index=False)]

        insert_query = """
            INSERT INTO InventoryTransactions (
                Date, StoreID, ProductID, InventoryLevel, UnitsSold, UnitsOrdered,
                DemandForecast, Price, Discount, WeatherCondition, HolidayPromotion,
                CompetitorPricing, Seasonality
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.executemany(insert_query, transaction_data)

        conn.commit()
        print("--- Database update successful! ---")
        return "Database update successful."

    except gspread.exceptions.SpreadsheetNotFound:
        return f"Error: Spreadsheet '{GOOGLE_SHEET_NAME}' not found. Make sure it's shared with your service account."
    except Exception as e:
        if 'conn' in locals() and conn: conn.rollback()
        return f"An error occurred: {e}"
    finally:
        if 'conn' in locals() and conn:
            if 'cursor' in locals(): cursor.close()
            conn.close()
