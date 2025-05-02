import os
import pandas as pd
import psycopg2
import gspread
import logging
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_to_csv(df, filename="products.csv"):
    try:
        df.to_csv(filename, index=False)
        logging.info(f"Data successfully saved to CSV: {filename}")
    
    except Exception as e:
        logging.error(f"Failed to save data to CSV: {e}")

def load_to_gsheet(df, worksheet_name='Sheet1'):
    try:
        # Link tetap langsung ditulis di dalam fungsi
        spreadsheet_link = "https://docs.google.com/spreadsheets/d/1HnSvhV3K-wA2QaSdGMGMJ6-uMtC_zru9Dhj-Clibsgo/edit#gid=0"
        spreadsheet_id = spreadsheet_link.split('/d/')[1].split('/')[0]

        # Setup kredensial dan client
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("google-sheets-api.json", scope)
        client = gspread.authorize(creds)

        spreadsheet = client.open_by_key(spreadsheet_id)

        try:
            sheet = spreadsheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title=worksheet_name, rows="100", cols="20")

        # Clear and update
        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())

        logging.info(f"Data successfully uploaded to Google Sheets.")
        logging.info(f"Google Sheet link: {spreadsheet.url}")

    except Exception as e:
        logging.error(f"Failed to upload data to Google Sheets: {e}")

def load_to_postgres(df):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                title TEXT,
                price BIGINT,
                rating FLOAT,
                colors INTEGER,
                size TEXT,
                gender TEXT,
                timestamp TIMESTAMP
            );
        """)

        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO products (title, price, rating, colors, size, gender, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                row["Title"],
                int(row["Price"]),
                float(row["Rating"]),
                int(row["Colors"]),
                row["Size"],
                row["Gender"],
                row["Timestamp"]
            ))
        conn.commit()
        cur.close()
        conn.close()
        logging.info("Data successfully loaded into PostgreSQL.")

    except Exception as e:
        logging.error(f"Failed to load data to PostgreSQL: {e}")
