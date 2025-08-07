import random
import requests
from Phase_1.getv2_devices import get_call
import os
import json
import datetime
from Phase_1.log_setup import setup_log
from dotenv import load_dotenv

load_dotenv()
req_dir_path = os.environ.get("P1_DEPLOY_LOG_PATH")
config_file_path = os.environ.get("P1_CONFIG_PATH")

def deploy_get_models():

    def deploy_get_call_v1():
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S")
        log_dir = os.path.join(os.path.dirname(__file__), f"{req_dir_path}")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{timestamp}_deploy_get_models_v1.txt")
        logger = setup_log(log_file, logger_name="file1")

        logger.info("Test initiated to get v1 devices")
        with open(config_file_path, "r") as f:
            config = json.load(f)

        url = config["url"]
        token = config["token"]
        payload = config["test_devices"]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        vendors = {
            "ata": "Ubee",
            "mta": "Technicolor",
            "cwl": "Motorola",
            "onu": "ALCATEL",
            "snu": "Humax"
        }

        results = {}
        try:
            for key,value in vendors.items():

                device = payload[key]
                ref_id = str(random.randint(1000, 9999))
                model_url = f"{url}v1/catalog/vendors/{value}/models"
                # print("get url: ",model_url)

                logger.info(f"Getting response for device {device}")
                response = requests.get(url=model_url, headers=headers, verify=False)
                rcode = response.status_code
                rbody = response.text
                if rcode == 200:
                    logger.info(f"Getting success response for device {device}")
                    logger.info(f"Success code: {rcode}\nResponse Body: {rbody}")
                    print(f"Success response for device {device}\ncode: {rcode}\nbody: {rbody}")

                    if device in response.text:
                        logger.info(f"Device {device} present in response body")
                        print(f"Device {device} present in response body")
                    else:
                        logger.error(f"Device {device} is not present in response body")
                        print(f"Device {device} is not present in response body")
                else:
                    logger.error(f"Getting failure response for device {device}")
                    logger.error(f"Error code: {rcode}\nResponse Body: {rbody}")
                    print(f"Error response for device {device}\ncode: {rcode}\nbody: {rbody}")
        except Exception as e:
            print(f"Exception occurred during request action: {e}")
            logger.error(f"Exception occurred during request action: {e}")
        finally:
            print("Test completed for get models v1")
            logger.info("Test completed for get models v1")

    deploy_get_call_v1()
    get_call(req_dir_path,"get_v2_devices")

#deploy_get_models()