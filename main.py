from dotenv import load_dotenv
import os

from NZFC_processing import ProcessNZFoodCompData
from Open_Food_Facts_processing import ProcessOpenFoodFactsData

load_dotenv()

REQUEST_URL = os.getenv("REQUEST_URL")

NZFC_STANDARD_FILE_PATH = "NZFC Data/Principal files/ASCII Text Files/Standard/Standard DATA.AP"
NZFC_CSM_FILE_PATH = "NZFC Data/Principal files/ASCII Text Files/CSM.FT"
NZ_OPEN_FOOD_FACTS_DATA_PATH = "Open Food Facts Data/nz_food_data"
AUSTRALIA_OPEN_FOOD_FACTS_DATA_PATH = "Open Food Facts Data/australia_food_data"

if __name__ == "__main__":
    # NZFC DATA
    nzfc_processor = ProcessNZFoodCompData(NZFC_STANDARD_FILE_PATH, NZFC_CSM_FILE_PATH, REQUEST_URL)
    nzfc_processor.send_post_requests()

    # OPEN FOOD FACTS DATA
    # Sends 7464 records out of 10936
    oofsnz_processor = ProcessOpenFoodFactsData(NZ_OPEN_FOOD_FACTS_DATA_PATH, REQUEST_URL, foodDbSource="OFFNZ", add_display_name_as_name=True)
    oofsnz_processor.send_post_requests()

    # Sends 37648 records out of 50235
    oofsau_processor = ProcessOpenFoodFactsData(AUSTRALIA_OPEN_FOOD_FACTS_DATA_PATH, REQUEST_URL, foodDbSource="OFFAU", add_display_name_as_name=True)
    oofsau_processor.send_post_requests()

