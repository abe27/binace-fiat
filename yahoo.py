import requests
from bs4 import BeautifulSoup

# Replace BASE_CURRENCY and TARGET_CURRENCY with the desired currency codes
base_currency = 'THB'

# Construct the URL for the exchange rate
url = f'https://api.exchangerate-api.com/v4/latest/THB'
response = requests.request("GET", url)
obj = response.json()
data = obj["rates"]
print(data["TRY"])
