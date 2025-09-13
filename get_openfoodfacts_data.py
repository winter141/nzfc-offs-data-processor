import os
import requests
import json
import time

# Folder path where you want to save the data
FOLDER_PATH = "Open Food Facts Data"
FILE_NAME = "australia_food_data.json"
FILE_PATH = os.path.join(FOLDER_PATH, FILE_NAME)

FIELDS = [
    "product_name",
    "nutriments",
    "code",  # Barcode
    "serving_size",
    "serving_quantity",
    "serving_quantity_unit",
]

BASE_URL = "https://world.openfoodfacts.net/api/v2/search"
PARAMS = {
    "countries_tags_en": "australia",
    "fields": ",".join(FIELDS),
    "page": 1,
    "page_size": 100
}

all_products = []
MAX_PAGES = 1_000  # just a failsafe
print("Starting download...")

# Ensure the folder exists
os.makedirs(FOLDER_PATH, exist_ok=True)

for page in range(1, MAX_PAGES + 1):
    PARAMS["page"] = page
    response = requests.get(BASE_URL, params=PARAMS)

    if response.status_code != 200:
        print(f"Failed at page {page}, status: {response.status_code}")
        break

    data = response.json()
    products = data.get("products", [])

    if not products:
        print(f"No more products found at page {page}. Ending.")
        break

    all_products.extend(products)
    print(f"Fetched page {page}: {len(products)} products, total so far: {len(all_products)}")

    # Avoid hitting rate limits
    time.sleep(1.5)

# Save to JSON in the specified folder
with open(FILE_PATH, "w", encoding="utf-8") as f:
    json.dump(all_products, f, ensure_ascii=False, indent=2)

print(f"Saved {len(all_products)} products to '{FILE_PATH}'")
