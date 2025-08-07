import json
import random

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_call(stage_type):
    with open("config.json") as f:
        config = json.load(f)

    url = config["url"]
    token = config["token"]
    payload = config[stage_type]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    results = {}
    for m in config['models_v2']:

        device = payload[m]
        ref_id = str(random.randint(1000,9999))
        model_url = f"{url}v2/catalog/models/{device}?referenceId={ref_id}"
        #print("get url: ",model_url)

        response = requests.get(url=model_url, headers=headers,verify=False)
        rcode = response.status_code
        rbody = response.text


        results[device] = rcode
    return results

'''
re=get_call("imported_devices")

for r in re:
    print(r)
'''