from dotenv import load_dotenv
import os

from NZFC_processing import ProcessNZFoodCompData
from Open_Food_Facts_processing import ProcessOpenFoodFactsData

load_dotenv()

REQUEST_URL = os.getenv("REQUEST_URL")

NZFC_STANDARD_FILE_PATH = "NZFC Data/Principal files/ASCII Text Files/Standard/Standard DATA.AP"
NZFC_CSM_FILE_PATH = "NZFC Data/Principal files/ASCII Text Files/CSM.FT"
OPEN_FOOD_FACTS_DATA_PATH = "Open Food Facts Data/nz_food_data"

if __name__ == "__main__":
    # NZFC DATA
    nzfc_processor = ProcessNZFoodCompData(NZFC_STANDARD_FILE_PATH, NZFC_CSM_FILE_PATH, REQUEST_URL)
    nzfc_processor.send_post_requests()

    # OPEN FOOD FACTS DATA
    oofs_processor = ProcessOpenFoodFactsData(OPEN_FOOD_FACTS_DATA_PATH, REQUEST_URL)
    oofs_processor.send_post_requests()
