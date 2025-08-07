from logsetup import *
import json
import requests
from datetime import datetime
from deepdiff import DeepDiff
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def get_model_info(url,headers,model):
    def extract_keys(original_dict, keys_to_extract):
        # Use dictionary comprehension to extract the desired keys
        expected_response = {key: original_dict[key] for key in keys_to_extract if key in original_dict}
        return expected_response
    keys_to_extract = ['modelName', 'vendorName', 'modelDesc', 'status']
    expected_response = extract_keys(model, keys_to_extract)
    response = requests.get(url, headers=headers, verify=False)
    # Check the status code and print the response
    if response.status_code == 200:
        logging.info("Success!")
        logging.info(f"response code: {response.status_code}")
        logging.info(f'response messge:{response.json()}')
        diff_json = DeepDiff(expected_response, response.json())
        if  diff_json== {}:
            logging.info("all the attributes are matching")
        else:
            logging.info("missmatch in the attributes")
            logging.info(f"difference: {diff_json}")



    else:
        logging.error(f'Failed with Status code: {response.status_code}')
        logging.error(response.json())
        logging.info(response.url)
