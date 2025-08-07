# importing all the required libraries
import requests
import json
import logging
from datetime import datetime

# Creating the log file to store the logs
logging.basicConfig(

filename='app.log',
level=logging.INFO,
format='%(asctime)s - %(levelname)s - %(message)s'
)

# reading the json file conetnts
file_path = "C://Users//P3205066//PycharmProjects//pythonProject//Config.json"

with open(file_path, 'r') as file:

   get_v2URL = str(json.load(file)["Get_model_info_v2_url"])

model = "ABE-040G-B1234AB"
referenceId = str(datetime.now())

# Define the API endpoint
url = get_v2URL + model + "?" + "referenceId=" + referenceId
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkZXZpY2VvcGVkaWEtdG9rZW4gc2NyaXB0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiREVWSUNFT1BFRElBX2NsaWVudCIsInJvbGVzIjpbIlNEX0NBVEFMT0dfQURNSU4iLCJTRF9GQVNfQURNSU4iLCJTRF9SRFVfQURNSU4iLCJTRF9NT05HT19BRE1JTiIsIlNEX1NVUEVSQURNSU4iXSwibmFtZSI6Im1lIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibWUiLCJnaXZlbl9uYW1lIjoibWUiLCJmYW1pbHlfbmFtZSI6Im1lIn0.9zVJY_R1HY-4OfL25loOAd_OS_E5su7nAgXCtmXONqA"
# Optional: Define headers if needed (e.g., for authentication)
headers = {
'Authorization': f'Bearer {token}'
}

# Executing the GET API
response = requests.get(url, headers=headers,verify=False)

# Check the status code and print the response
if response.status_code == 200:
    data = str(json.load(file)["onuModel"])
    if response.json() == data:
        print("Test Case is passed")
        logging.info("All The attributes are matching")
        logging.info("Test case passed for model:",model)
    else:
        print("Test Case is failed")
        logging.error("One or more attributes are not matching")
        logging.error("Test case is failed")

    print("Success!")
    logging.info(response.status_code)
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




