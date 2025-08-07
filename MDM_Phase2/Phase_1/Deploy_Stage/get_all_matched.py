from Phase_1.get_all_matchedmodels_v2 import get_matched_v2
import os

req_dir_path = os.environ.get("P1_DEPLOY_LOG_PATH")

def deploy_matched_modelsv2():
    get_matched_v2(req_dir_path,"get_matched_devices_V2","Deploy")

#deploy_matched_modelsv2()