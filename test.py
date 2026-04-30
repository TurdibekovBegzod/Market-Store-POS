import requests
from pprint import pprint

# The URL of the API endpoint
url = "http://localhost:8000/product-templates/"

# 1. Send the GET request
response = requests.get(url).json()

pprint(response)
for template in response['templates']:
    print(template['id'])


