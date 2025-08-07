'''
1] Get call - code 200
2] Delete Firmware - code 204
3] Delete firmware - code - 404
4] Delete call - code 204
5] Get call - code 404
6] Delete call - code 404
'''

import datetime
import json
import os
import random
import requests

from Phase_1.log_setup import setup_log
from Phase_1.getv2_devices import get_call
from Phase_1.delete_device import delete_devices
from Phase_1.frimware_delete import delete_firmware
from dotenv import load_dotenv

load_dotenv()
req_dir_path = os.environ.get("P1_TEST_LOG_PATH")
config_file_path = os.environ.get("P1_CONFIG_PATH")

def certified_delete_flow():
    # get call call1
    print(f"GET CALL 1")
    get_call(req_dir_path, "certify_delete_get_v2_devices_call1")

    # delete firmware call1
    print("DELETE FIRMWARE 1")
    delete_firmware(req_dir_path=req_dir_path,log_name="certify__delete_firmware_call1", stage="certify")

    # delete firmware call2
    print("DELETE FIRMWARE 2")
    delete_firmware(req_dir_path=req_dir_path, log_name="certify_delete_firmware_call2", stage="certify",call="call2")

    # deleting the model call1
    print("DELETE MODEL 1")
    delete_devices(req_dir_path=req_dir_path, log_name="certify_delete_model_call1")

    print("DELETE MODEL 2")
    delete_devices(req_dir_path=req_dir_path, log_name="certify_delete_model_call2",flow="call2")

    # get call call2
    print("GET CALL 2")
    get_call(req_dir_path, "certify_delete_get_v2_devices_call2","call2")
