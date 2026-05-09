import os 
from dotenv import load_dotenv
import pandas as pd
import psycopg2 
from psycopg2 import sql 
from psycopg2 import extras
from binance.client import Client

load_dotenv()

#API key and secret
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Initialize the client
client = Client(api_key, api_secret)

# Check account status
account_info = client.get_account()
#print(account_info['balances'])

raw_data = account_info['balances']

df_data = pd.DataFrame(raw_data)

#display(df_data)

HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
TARGET_TABLE = os.getenv("TARGET_TABLE")
PORT = os.getenv("PORT")


conn = psycopg2.connect(
    host = HOST,
    dbname = DB_NAME,
    user = USERNAME,
    password = PASSWORD,
    port = PORT
)

cur = conn.cursor()

try:
    print(f"Successfully connected to database: {DB_NAME} with user: {USERNAME}")

except psycopg2.Error as e:
    print(f"Error in connection {e}")

display(df_data)

create_table = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {table} (
    asset VARCHAR(50),
    free NUMERIC(50,50),
    locked NUMERIC(50,50),
    load_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
""").format(table = sql.Identifier(TARGET_TABLE))

try:
    cur.execute(create_table)
    conn.commit()
    print(f"Successfully created table: {TARGET_TABLE}")

except psycopg2.Error as e:
    conn.rollback()
    print(f"Check connection details / syntax Error: {e}")

#df_data.columns.to_list

columns_to_load = ['asset', 'free', 'locked']

values_to_load = [tuple(row) for row in df_data.values]

insert_query = sql.SQL("""
    INSERT INTO {table} ({columns})
    VALUES %s
""").format(table = sql.Identifier(TARGET_TABLE),
columns = sql.SQL(' ,').join(map(sql.Identifier, columns_to_load)))

try:
    extras.execute_values(cur,insert_query,values_to_load)
    conn.commit()
    print(f"Successfully loaded {len(values_to_load)} rows into table: {TARGET_TABLE}")

except psycopg2.Error as e:
    conn.rollback()
    print(f"Check connection details / syntax Error: {e}")
