import logging
from utils.extract import extract_products
from utils.transform import transform
from utils.load import load_to_csv, load_to_gsheet, load_to_postgres

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        logging.info("Starting extraction...")
        raw_data = extract_products()

        logging.info(f"Extraction completed. {len(raw_data)} records fetched.")

        logging.info("Starting transformation...")
        transformed_data = transform(raw_data)

        logging.info(f"Transformation completed. {len(transformed_data)} valid records.")

        if transformed_data.empty:
            logging.warning("No valid data to load. Aborting load process.")
            return

        logging.info("Loading to CSV...")
        load_to_csv(transformed_data)

        logging.info("Loading to Google Sheets...")
        load_to_gsheet(transformed_data)

        logging.info("Loading to PostgreSQL...")
        load_to_postgres(transformed_data)

        logging.info("ETL process completed successfully!")

    except Exception as e:
        logging.error(f"ETL process failed: {e}")

if __name__ == "__main__":
    main()

