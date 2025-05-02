import requests
from bs4 import BeautifulSoup
import re
import logging

def extract_products():
    base_url = "https://fashion-studio.dicoding.dev"
    page = 1
    products = []

    while True:
        try:
            url = base_url if page == 1 else f"{base_url}/page{page}"
            logging.info(f"Fetching page {page} from URL: {url}")
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            cards = soup.find_all("div", class_="collection-card")
            if not cards:
                logging.info("No more products found. Ending extraction.")
                break

            for idx, card in enumerate(cards):
                try:
                    title = (card.find("h3", class_="product-title").text.strip()
                            if card.find("h3", class_="product-title") else "unknown product")

                    price_elem = card.find("span", class_="price")
                    price_text = price_elem.text.strip() if price_elem else ""
                    price = price_text.replace("$", "").replace(",", "") if price_text else ""

                    details = card.find_all("p")
                    rating_raw = details[0].text.strip() if len(details) > 0 else "not rated"
                    match = re.search(r"([\d.]+)", rating_raw)
                    rating = match.group(1) if match else "not rated"

                    colors = details[1].text.strip().replace("Colors", "").strip("> ") if len(details) > 1 else "0"
                    size = details[2].text.strip().replace("Size: ", "") if len(details) > 2 else "N/A"
                    gender = details[3].text.strip().replace("Gender: ", "") if len(details) > 3 else "Unisex"

                    products.append({
                        "title": title,
                        "price": price,
                        "rating": rating,
                        "colors": colors,
                        "size": size,
                        "gender": gender
                    })

                except Exception as e:
                    logging.warning(f"Skipping product at page {page}, index {idx} due to error: {e}")
                    continue

            page += 1

        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching page {page}: {e}")
            break

        except Exception as e:
            logging.error(f"Unexpected error on page {page}: {e}")
            break

    return products
