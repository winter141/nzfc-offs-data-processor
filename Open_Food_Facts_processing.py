from base_processor import Processor
import json
import requests
import time


def kj_to_kcal(kj):
    return round(kj / 4.184, 2)


class ProcessOpenFoodFactsData(Processor):
    def __init__(self, data_file_path, request_url):
        with open(f'{data_file_path}.json', encoding="utf-8") as file:
            data = json.load(file)
        self.all_data = [self.__format_data(product) for product in data]
        self.request_url = request_url

        c = 0
        for data in self.all_data:
            if data:
                c += 1
        print(c)
        print(len(self.all_data))

        self.i = 0

    def __format_data(self, product):
        try:
            nutriments = product["nutriments"]
            d = {
                "barcode": product["code"],
                "kilocalories": nutriments["energy-kcal_100g"] if "energy-kcal_100g" in nutriments else kj_to_kcal(nutriments["energy-kj_100g"]),
                "name": product["product_name"],
                "carbohydrates": nutriments["carbohydrates_100g"],
                "sugars": nutriments["sugars_100g"],
                "fat": nutriments["fat_100g"],
                "protein": nutriments["proteins_100g"]
            }

            if "serving_size" in product and "serving_quantity" in product:
                d["foodCsms"] = [
                    {"csmDescription": product["serving_size"], "amount": float(product["serving_quantity"])}
                    ]

            d_keys = [
                "fibre", "alcohol", "betaCarotene", "caffeine", "calcium", "cholesterol", "copper",
                "galactose", "iodide", "iron", "lactose", "magnesium", "manganese",
                "phosphorus", "potassium", "selenium", "sodium", "starch", "sucrose",
                "sugarAdded", "vitaminA", "vitaminB12", "vitaminB6", "vitaminC", "vitaminD",
                "vitaminE", "water", "zinc"
            ]
            nutrients_keys = [
                "fiber_100g", "alcohol_100g", "beta-carotene_100g", "caffeine_100g", "calcium_100g", "cholesterol_100g",
                "copper_100g", "galactose_100g", "iodine_100g", "iron_100g", "lactose_100g",
                "magnesium_100g", "manganese_100g", "phosphorus_100g", "potassium_100g",
                "selenium_100g", "sodium_100g", "sugars_100g", "sugars_100g", "added-sugars_100g",
                "vitamin-a_100g", "vitamin-b12_100g", "vitamin-b6_100g", "vitamin-c_100g",
                "vitamin-d_100g", "vitamin-e_100g", "en-water_100g", "zinc_100g"
            ]
            for key, nutrient_key in zip(d_keys, nutrients_keys):
                if nutrient_key in nutriments:
                    d[key] = nutriments[nutrient_key]
            return d

        except KeyError as e:
            if "code" in product:
                print(f"Missing key: {e} with barcode: {product['code']}")
            else:
                print(f"Missing key: {e} no barcode")
            return None
        except ValueError as e:
            print(f"Value error: {e}")
            return None

    def send_post_requests(self):
        for data in self.all_data:
            if data:
                response = requests.post(self.request_url, json=data)
                print(f"Sent {data['name']}: {response.status_code} - {response.text}")
            else:
                print(f"Skipped FOOD")
