import json

from API import file_path

file_path = "C:\\Users\P3205066\PycharmProjects\pythonProject\Putpayload_AT_onu.json"
with open(file_path, 'r') as file:
    data = json.load(file)
