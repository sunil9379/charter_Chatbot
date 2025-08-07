from Phase_1.get_all_matchedmodels_v2 import get_matched_v2
import os
from load_dotenv import load_dotenv
load_dotenv()

req_dir_path = os.environ.get("P1_TEST_LOG_PATH")

def test_get_allmatched():

    get_matched_v2(req_dir_path,"get_all_matched_models","Test")

#test_get_allmatched()