from dotenv import load_dotenv
import os

from NZFC_processing import ProcessNZFoodCompData
from Open_Food_Facts_processing import ProcessOpenFoodFactsData

load_dotenv()

FOOD_REQUEST_URL = os.getenv("FOOD_REQUEST_URL")
CSM_REQUEST_URL = os.getenv("CSM_REQUEST_URL")

NZFC_STANDARD_FILE_PATH = "NZFC Data/Principal files/ASCII Text Files/Standard/Standard DATA.AP"
NZFC_CSM_FILE_PATH = "NZFC Data/Principal files/ASCII Text Files/CSM.FT"
OPEN_FOOD_FACTS_DATA_PATH = "Open Food Facts Data/nz_food_data"

if __name__ == "__main__":
    # NZFC DATA
    # processor = ProcessNZFoodCompData(NZFC_STANDARD_FILE_PATH, NZFC_CSM_FILE_PATH, FOOD_REQUEST_URL, CSM_REQUEST_URL)
    # processor.send_food_post_requests()
    # processor.send_csm_post_requests()

    # OPEN FOOD FACTS DATA
    processor = ProcessOpenFoodFactsData(OPEN_FOOD_FACTS_DATA_PATH, FOOD_REQUEST_URL, CSM_REQUEST_URL)
    processor.print(100)
    # processor.send_csm_post_requests()
    # processor.send_food_post_requests()