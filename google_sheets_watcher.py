# google_sheets_watcher.py
import os
import pandas as pd
import psycopg2
import gspread

# --- Configuration ---
# The name of the Google Sheet you created
GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'InventoryDataSource')

def get_db_connection():
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def run_update_check():
    print("--- Starting Google Sheets data sync ---")
    try:
        # 1. Authenticate and fetch all data from Google Sheets
        gc = gspread.service_account()
        spreadsheet = gc.open(GOOGLE_SHEET_NAME)
        worksheet = spreadsheet.sheet1  # Get the first sheet

        print("Fetching all records from the sheet...")
        records = worksheet.get_all_records()
        df = pd.DataFrame(records)

        if df.empty:
            return "No data found in Google Sheet."

        # --- 2. The rest of the ETL logic is the same ---
        df.columns = [col.replace(' ', '').replace('/', '') for col in df.columns]

        conn = get_db_connection()
        cursor = conn.cursor()

        print("Clearing all old data...")
        cursor.execute("TRUNCATE TABLE InventoryTransactions, Stores, Products, Categories, Regions RESTART IDENTITY CASCADE;")

        # ... (The exact same code as before for populating Regions, Categories, Stores, Products) ...

        print(f"Populating InventoryTransactions with {len(df)} records...")
        # ... (The exact same code as before for inserting into the main transaction table) ...

        conn.commit()
        print("--- Database update successful! ---")
        return "Database update successful."

    except gspread.exceptions.SpreadsheetNotFound:
        return f"Error: Spreadsheet '{GOOGLE_SHEET_NAME}' not found. Make sure it's shared with your service account."
    except Exception as e:
        if 'conn' in locals() and conn: conn.rollback()
        print(f"An error occurred during the data sync: {e}")
        return f"An error occurred: {e}"
    finally:
        if 'conn' in locals() and conn:
            if 'cursor' in locals(): cursor.close()
            conn.close()
