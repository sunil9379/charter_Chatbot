from Phase_1.getv2_devices import get_call
import os
from dotenv import load_dotenv
load_dotenv()

req_dir_path = os.environ.get("P1_TEST_LOG_PATH")

def test_get_devices():
    get_call(req_dir_path,"get_devices_V2")


#test_get_devices()