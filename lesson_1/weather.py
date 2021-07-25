import requests
from pprint import pprint
# 9325e14ad6e59ed105e538aef71bb2d9

city = 'Rim'
my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/91.0.4472.164 Safari/537.36'}
my_params = {'q': city, 'appid': '9325e14ad6e59ed105e538aef71bb2d9'}
url = 'http://api.openweathermap.org/data/2.5/weather'

response = requests.get(url, params=my_params, headers=my_headers)
data = response.json()
j_city = data['name']
j_temp = int(data['main']['temp'] - 273.15)
# pprint(data)
print(f"На данный момент в городе {j_city} температура воздуха {j_temp:.0f} градусов")
