import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def transform(products: list) -> pd.DataFrame:
    cleaned_data = []
    extraction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for idx, product in enumerate(products):
        try:
            title = (product.get("title") or "").strip()
            price = (product.get("price") or "").strip()
            rating = (product.get("rating") or "").strip()
            colors = (product.get("colors") or "").strip()
            size = (product.get("size") or "").strip()
            gender = (product.get("gender") or "").strip()

            if "unknown product" in title.lower() or "not rated" in rating.lower() or "invalid rating" in rating.lower() or not price:
                logging.warning(f"Skipping product at index {idx}: Invalid data detected.")
                continue

            price_rp = float(price) * 16000
            rating_float = float(rating)
            colors_int = int("".join(filter(str.isdigit, colors)))

            cleaned_data.append({
                "Title": title,
                "Price": price_rp,
                "Rating": rating_float,
                "Colors": colors_int,
                "Size": size,
                "Gender": gender,
                "Timestamp": extraction_time
            })

        except (ValueError, AttributeError) as e:
            logging.error(f"Error transforming product at index {idx}: {e}")
            continue

    df = pd.DataFrame(cleaned_data)

    if df.empty:
        logging.warning("Transform result is empty. Check input data validity.")

    return df