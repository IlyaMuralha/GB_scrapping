import requests
from pprint import pprint

url = 'https://www.google.ru'
response = requests.get(url)
print()

# response.status_code
# response.ok
# response.headers
# response.content
# pprint(dict(response.headers))
