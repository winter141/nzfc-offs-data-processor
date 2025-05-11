"""
Unabridged contains same data as in standard but alot more fields. (not shortened)
Probably ok with just using Standard
"""
import csv
import requests
from base_processor import Processor


def safe_float(value):
    return float(value) if value != "" else 0.0


class ProcessNZFoodCompData(Processor):
    def __init__(self, standard_file_path, csm_file_path, request_url):
        self.food_data = self.__process_ft_to_dict(standard_file_path, True)
        self.csm_data = self.__process_ft_to_dict(csm_file_path, False)

        self.all_data = self.__get_all_data()

        self.request_url = request_url


    def __process_ft_to_dict(self, file_path, use_units: bool):
        with open(file_path, encoding="utf-8") as file:
            reader = csv.reader(file, delimiter="~")
            rows = list(reader)

        # Separate parts
        column_names = rows[1]
        units = rows[2] if use_units else ['-' for _ in range(len(rows[2]))]
        data = rows[3:] if use_units else rows[2:]

        # Convert to dicts
        dict_data = []
        for row in data:
            d = dict()
            for col, un, val in zip(column_names, units, row):
                d[col] = (val, un)
            dict_data.append(d)
        return dict_data

    def __reformat_food_entry(self, food):
        try:
            return {
                "NZCompId": food["FoodID"][0],
                "name": food["Food Name"][0],
                "kilocalories": safe_float(food["Energy, total metabolisable (kcal, including dietary fibre)"][0]),
                "carbohydrates": safe_float(food["Available carbohydrate, FSANZ"][0]),
                "sugars": safe_float(food["Sugars, total"][0]),
                "fat": safe_float(food["Fat, total"][0]),
                "fibre": safe_float(food["Fibre, total dietary"][0]),
                "protein": safe_float(food["Protein, total; calculated from total nitrogen"][0]),

                "alcohol": safe_float(food["Alcohol"][0]),
                "alphaCarotene": safe_float(food["Alpha-carotene"][0]),
                "alphaTocopherol": safe_float(food["Alpha-tocopherol"][0]),
                "ash": safe_float(food["Ash"][0]),
                "betaCarotene": safe_float(food["Beta-carotene"][0]),
                "betaTocopherol": safe_float(food["Beta-tocopherol"][0]),
                "caffeine": safe_float(food["Caffeine"][0]),
                "calcium": safe_float(food["Calcium"][0]),
                "cholesterol": safe_float(food["Cholesterol"][0]),
                "copper": safe_float(food["Copper"][0]),
                "deltaTocopherol": safe_float(food["Delta-tocopherol"][0]),
                "dietaryFolateEquivalents": safe_float(food["Dietary folate equivalents"][0]),
                "dryMatter": safe_float(food["Dry matter"][0]),
                "fattyAcidsOmega3": safe_float(food["Fatty acids, total polyunsaturated omega-3"][0]),
                "fattyAcidsMono": safe_float(food["Fatty acids, total monounsaturated"][0]),
                "fattyAcidsPoly": safe_float(food["Fatty acids, total polyunsaturated"][0]),
                "fattyAcidsSaturated": safe_float(food["Fatty acids, total saturated"][0]),
                "fattyAcidsTrans": safe_float(food["Fatty acids, total trans"][0]),
                "fibreInsoluble": safe_float(food["Fibre, water-insoluble"][0]),
                "fibreSoluble": safe_float(food["Fibre, water-soluble"][0]),
                "folateTotal": safe_float(food["Folate, total"][0]),
                "fructose": safe_float(food["Fructose"][0]),
                "galactose": safe_float(food["Galactose"][0]),
                "gammaTocopherol": safe_float(food["Gamma-tocopherol"][0]),
                "glucose": safe_float(food["Glucose"][0]),
                "iodide": safe_float(food["Iodide"][0]),
                "iron": safe_float(food["Iron"][0]),
                "lactose": safe_float(food["Lactose"][0]),
                "magnesium": safe_float(food["Magnesium"][0]),
                "maltose": safe_float(food["Maltose"][0]),
                "manganese": safe_float(food["Manganese"][0]),
                "niacinTotal": safe_float(food["Niacin equivalents, total"][0]),
                "nitrogen": safe_float(food["Nitrogen, total"][0]),
                "phosphorus": safe_float(food["Phosphorus"][0]),
                "potassium": safe_float(food["Potassium"][0]),
                "retinol": safe_float(food["Retinol"][0]),
                "riboflavin": safe_float(food["Riboflavin"][0]),
                "selenium": safe_float(food["Selenium"][0]),
                "sodium": safe_float(food["Sodium"][0]),
                "starch": safe_float(food["Starch, total"][0]),
                "sucrose": safe_float(food["Sucrose"][0]),
                "sugarAdded": safe_float(food["Sugar, added"][0]),
                "sugarFree": safe_float(food["Sugar, free"][0]),
                "thiamin": safe_float(food["Thiamin"][0]),
                "tryptophan": safe_float(food["Tryptophan"][0]),
                "vitaminA": safe_float(food["Vitamin A, retinol activity equivalents"][0]),
                "vitaminB12": safe_float(food["Vitamin B12"][0]),
                "vitaminB6": safe_float(food["Vitamin B6"][0]),
                "vitaminC": safe_float(food["Vitamin C"][0]),
                "vitaminD": safe_float(food["Vitamin D; calculated by summation"][0]),
                "vitaminE": safe_float(food["Vitamin E, alpha-tocopherol equivalents"][0]),
                "water": safe_float(food["Water"][0]),
                "zinc": safe_float(food["Zinc"][0])
            }
        except KeyError as e:
            print(f"Missing key: {e}")
            return None
        except ValueError as e:
            print(f"Value error: {e}")
            return None

    def __reformat_csm_entry(self, csm):
        try:
            return {
                "NZCompId": csm["FoodID"][0],
                "csmDescription": csm["CSM"][0],
                "amount": safe_float(csm["Measure"][0]),
                "density": safe_float(csm["Density (g/cm3)"][0])
            }
        except KeyError as e:
            print(f"Missing key: {e}")
            return None
        except ValueError as e:
            print(f"Value error: {e}")
            return None

    def __get_all_data(self):
        """"""
        all_data = []
        csm_f_data = [self.__reformat_csm_entry(csm) for csm in self.csm_data]

        for food in self.food_data:
            food = self.__reformat_food_entry(food)
            csms = []
            for csm in csm_f_data:
                if csm["NZCompId"] == food["NZCompId"]:
                    csms.append(csm)
            food["foodCsms"] = csms
            all_data.append(food)

        return all_data

    def send_post_requests(self):
        for data in self.all_data:
            if data:
                response = requests.post(self.request_url, json=data)
                print(f"Sent {data['name']}: {response.status_code} - {response.text}")
            else:
                print(f"Skipped FOOD")
