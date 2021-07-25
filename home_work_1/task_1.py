import requests
import json

USERNAME = 'IlyaMuralha'
MY_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/91.0.4472.164 Safari/537.36'}

url = f'https://api.github.com/users/{USERNAME}/repos'

response = requests.get(url, headers=MY_HEADERS)
data = response.json()
# извлекаем только url репозиториев
url_generator = (item['html_url'] for item in data)

# записываем всю инфу по репозиториям пользователя в файл
with open('repos.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

# записываем только список ссылок на репозитории пользователя в файл
with open('url_repos.json', 'w', encoding='utf-8') as f:
    result = []
    for i in url_generator:
        result.append(i)
    json.dump(result, f, ensure_ascii=False)
