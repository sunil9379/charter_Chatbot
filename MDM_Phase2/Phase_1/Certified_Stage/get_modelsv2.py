from Phase_1.getv2_devices import get_call
import os
req_dir_path = os.environ.get("P1_CERTIFY_LOG_PATH")

def certify_get_call():
    get_call(req_dir_path,"get_v2_devices")

#certify_get_call()