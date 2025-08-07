import json
import requests
from datetime import datetime

ref_id = "TestModel" + str(datetime.now().second)
ext_id = "TestModel" + str(datetime.now().second)
url = "https://east-deviceopedia-qa-mdm.caas.charterlab.com/v2/catalog/models"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkZXZpY2VvcGVkaWEtdG9rZW4gc2NyaXB0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiREVWSUNFT1BFRElBX2NsaWVudCIsInJvbGVzIjpbIlNEX0NBVEFMT0dfQURNSU4iLCJTRF9GQVNfQURNSU4iLCJTRF9SRFVfQURNSU4iLCJTRF9NT05HT19BRE1JTiIsIlNEX1NVUEVSQURNSU4iXSwibmFtZSI6Im1lIiwicHJlZmVycmVkX3VzZXJuYW1lIjoibWUiLCJnaXZlbl9uYW1lIjoibWUiLCJmYW1pbHlfbmFtZSI6Im1lIn0.9zVJY_R1HY-4OfL25loOAd_OS_E5su7nAgXCtmXONqA"
# headers for the API
headers = {
"Content-Type": "application/json",
'Authorization': f'Bearer {token}'
}