from base_processor import Processor
import json
import requests


def kj_to_kcal(kj):
    return round(kj / 4.184, 2)


class ProcessOpenFoodFactsData(Processor):
    def __init__(self, data_file_path, food_request_url, csm_request_url):
        with open(f'{data_file_path}.json', encoding="utf-8") as file:
            data = json.load(file)
        self.food_data = data
        self.food_request_url = food_request_url
        self.csm_request_url = csm_request_url

        self.id_mapping = []

    def __format_food(self, product):
        try:
            nutriments = product["nutriments"]
            d = {
                "barcode": int(product["code"]),
                "kilocalories": nutriments["energy-kcal_100g"] if "energy-kcal_100g" in nutriments else kj_to_kcal(nutriments["energy-kj_100g"]),
                "name": product["product_name"],
                "carbohydrates": nutriments["carbohydrates_100g"],
                "sugars": nutriments["sugars_100g"],
                "fat": nutriments["fat_100g"],
                "protein": nutriments["proteins_100g"],
            }

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
            print(f"Missing key: {e}")
            return None
        except ValueError as e:
            print(f"Value error: {e}")
            return None

    def __format_csm(self, product):
        # TODO id_mapping
        try:
            return {
                "foodId": 0,  # some valid id_mapping
                "csmDescription": product["serving_size"],
                "amount": product["serving_quantity"]
            }
        except KeyError as e:
            print(f"Missing key: {e}")
            return None
        except ValueError as e:
            print(f"Value error: {e}")
            return None

    def send_food_post_requests(self):
        i = 1
        for food in self.food_data:
            data = self.__format_food(food)
            if data:
                response = requests.post(self.food_request_url, json=data)
                print(f"Sent {data['name']}: {response.status_code} - {response.text}")
                self.id_mapping.append((data["NZCompId"], i))
                i += 1
            else:
                print(f"Skipped FOOD")

        print(self.id_mapping)

    def send_csm_post_requests(self):
        for product in self.food_data:
            data = self.__format_csm(product)
            if data:
                response = requests.post(self.csm_request_url, json=data)
                # print(f"Sent {data['name']}: {response.status_code} - {response.text}")
                print(response.status_code)
            else:
                print(f"Skipped FOOD")


    def print(self, num=1):
        for product in self.food_data[:num]:
            print(self.__format_food(product))
