import os
import psycopg2

def run_sql_file(filename, conn_str):
    with open(filename, 'r') as f:
        sql = f.read()
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    print(f"Executed {filename} successfully.")

if __name__ == "__main__":
    connection_url = os.getenv('DATABASE_URL')
    if not connection_url:
        print("DATABASE_URL environment variable not set.")
    else:
        run_sql_file('sql_schema.sql', connection_url)
