from Phase_1.Deploy_Stage.kafka_info import read_kafka
from Phase_1.delete_device import delete_devices
import os
import requests
from dotenv import load_dotenv
load_dotenv()
req_dir_path = os.environ.get("P1_DEPLOY_LOG_PATH")

#delete_devices(req_dir_path,"xyz")
#read_kafka("deviceopedia-authoritative-full-device-model-qa")
'''
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkZXZpY2VvcGVkaWEtdG9rZW4gc2NyaXB0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiREVWSUNFT1BFRElBX2NsaWVudCIsInJvbGVzIjpbIlNEX0NBVEFMT0dfQURNSU4iLCJTRF9GQVNfQURNSU4iLCJTRF9SRFVfQURNSU4iLCJTRF9NT05HT19BRE1JTiIsIlNEX1NVUEVSQURNSU4iXSwibmFtZSI6Im1lIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibWUiLCJnaXZlbl9uYW1lIjoibWUiLCJmYW1pbHlfbmFtZSI6Im1lIn0.9zVJY_R1HY-4OfL25loOAd_OS_E5su7nAgXCtmXONqA"
    }

response = requests.delete(
    url="https://east-deviceopedia-qa-mdm.caas.charterlab.com/v2/catalog/models/Test_mta001?referenceId=dsf987&userId=p3289462",
    headers=headers,
    verify=False
)
print(response.status_code)
print(response.text)

'''
present = read_kafka("deviceopedia-authoritative-incremental-device-model-qa","Test_mta102")
if present:
    print("Kafka published")
else:
    print("Kafka not published")