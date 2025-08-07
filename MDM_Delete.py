import requests
import json
from datetime import datetime


# Define the API endpoint
url = "https://east-deviceopedia-qa-mdm.caas.charterlab.com/v2/catalog/models/abc?referenceId=abc&userId=abc"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkZXZpY2VvcGVkaWEtdG9rZW4gc2NyaXB0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiREVWSUNFT1BFRElBX2NsaWVudCIsInJvbGVzIjpbIlNEX0NBVEFMT0dfQURNSU4iLCJTRF9GQVNfQURNSU4iLCJTRF9SRFVfQURNSU4iLCJTRF9NT05HT19BRE1JTiIsIlNEX1NVUEVSQURNSU4iXSwibmFtZSI6Im1lIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibWUiLCJnaXZlbl9uYW1lIjoibWUiLCJmYW1pbHlfbmFtZSI6Im1lIn0.9zVJY_R1HY-4OfL25loOAd_OS_E5su7nAgXCtmXONqA"
# Optional: Define headers if needed (e.g., for authentication)
headers = {
'Authorization': f'Bearer {token}'
}

# Send the GET request
response = requests.delete(url, headers=headers,verify=False)

# Check the status code and print the response
if response.status_code == 204:
    print("Success!")
    print(response.json())  # or response.text for raw output



else:
    print(f"Failed with status code: {response.status_code}")
    print(response.text)




