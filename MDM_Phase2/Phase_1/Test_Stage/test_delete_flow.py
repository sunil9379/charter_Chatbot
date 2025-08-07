'''
1] Get call - code 200
2] Delete call - code 204
3] Get call - code 404
4] Delete call - code 404
'''

import datetime
import json
import os
import random
import requests

from Phase_1.log_setup import setup_log
from Phase_1.getv2_devices import get_call
from Phase_1.delete_device import delete_devices
from dotenv import load_dotenv

load_dotenv()
req_dir_path = os.environ.get("P1_TEST_LOG_PATH")
config_file_path = os.environ.get("P1_CONFIG_PATH")

def test_delete_flow():
    print("Delete Flow initiated for Test Stage")

    #get call 1
    print(f"GET CALL 1")
    get_call(req_dir_path, "test_delete_get_v2_devices_call1")

    #delete call 1
    print("DELETE MODEL 1")
    delete_devices(req_dir_path=req_dir_path, log_name="test_delete_model_call1")

    #get call2
    print("GET CALL 2")
    get_call(req_dir_path, "test_delete_get_v2_devices_call1","call2")

    #delete call 2
    print("DELETE MODEL 2")
    delete_devices(req_dir_path=req_dir_path, log_name="test_delete_model_call1",flow="call2")




