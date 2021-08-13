from bs4 import BeautifulSoup as bs
import requests

from pprint import pprint

url = 'http://localhost:63342/parsing_python/lesson_2/example.html?_ijt=1cg8v0i96n63j681g70p0pr151'

response = requests.get(url)
html =response.text

soup = bs(html, 'html.parser')
print()
