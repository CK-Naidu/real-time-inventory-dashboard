import os
import psycopg2

def run_sql_file(filename, conn_str):
    with open(filename, 'r') as file:
        sql = file.read()

    conn = psycopg2.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    conn_url = os.getenv('DATABASE_URL')
    if not conn_url:
        raise Exception("Set the DATABASE_URL environment variable first")
    run_sql_file('sql_schema.sql', conn_url)
    print("Executed sql_schema.sql successfully.")
