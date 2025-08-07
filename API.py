import requests
import json
import logging
from datetime import datetime
import time
start_time = time.time()
logging.basicConfig(
filename='app.log',
level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s'
)

# reading the json file conetnts
file_path = "C:\\Users\P3205066\PycharmProjects\pythonProject\Config.json"

with open(file_path, 'r') as file:
	get_v2URL = str(json.load(file)["Get_model_info_v2_url"])

model = "ABE-040G-B1234AB"
referenceId = str(datetime.now())
API_URL = "https://east-deviceopedia-qa-mdm.caas.charterlab.com/v2/catalog/models/"
# Define the API endpoint
url = API_URL + model + "?" + "referenceId=" + referenceId
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkZXZpY2VvcGVkaWEtdG9rZW4gc2NyaXB0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiREVWSUNFT1BFRElBX2NsaWVudCIsInJvbGVzIjpbIlNEX0NBVEFMT0dfQURNSU4iLCJTRF9GQVNfQURNSU4iLCJTRF9SRFVfQURNSU4iLCJTRF9NT05HT19BRE1JTiIsIlNEX1NVUEVSQURNSU4iXSwibmFtZSI6Im1lIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibWUiLCJnaXZlbl9uYW1lIjoibWUiLCJmYW1pbHlfbmFtZSI6Im1lIn0.9zVJY_R1HY-4OfL25loOAd_OS_E5su7nAgXCtmXONqA"
# Optional: Define headers if needed (e.g., for authentication)
headers = {
'Authorization': f'Bearer {token}'
}
# parameters to be passed to the API

# Send the GET request
response = requests.get(url, headers=headers,verify=False)

# Check the status code and print the response
if response.status_code == 200:
    Model_Name = str((json.loads(response.text))["modelName"])
    Vendor_Name = str((json.loads(response.text))["vendorName"])
    Status = str((json.loads(response.text))["status"])
    DType = str((json.loads(response.text))["modelDesc"])
    print(DType)
    if Model_Name == model and Vendor_Name == "ALCATEL" and Status == "Test" and "'deviceTypeName': 'onu'" in DType:
        print("Test Case is passed")
        logging.info("All The attributes are matching")
        logging.info("Test case passed")
        logging.info(response.url)
    else:
        print("Test Case is failed")
        logging.error("One or more attributes are not matching")
        logging.error("Test case is failed")

    print("Success!")
    logging.info(f'response code:{response.status_code}')
    print(response.json())  # or response.text for raw output
    logging.info(response.json())


else:
    #error_msg = str((json.loads(response.text))["exc_message"])
    #assert error_msg == "500: database schema migration is required, see logs", "environment issue"
    print(f"Failed with status code: {response.status_code}")
    print(response.text)
    logging.error(f'Failed with Status code: {response.status_code}')
    logging.error(response.json())
    logging.info(response.url)


for i in range(1000000):
    _ = i * i

# End the timer
end_time = time.time()

total_time = end_time - start_time
print(f"Total execution time: {total_time:.6f} seconds")






