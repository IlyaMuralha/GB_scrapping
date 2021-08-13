from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/92.0.4515.131 Safari/537.36'}
url = 'https://hh.ru'


# clusters=true&no_magic=true&ored_clusters=true&enable_snippets=true&st=searchVacancy&text=Django&from=suggest_post&area=113&page=0


def get_salary(salary: str) -> tuple:
    try:
        if salary:
            temp1 = salary.split('–')
            if len(temp1) == 2:
                min_salary = ''.join(temp1[0].split('\u202f'))
                temp2 = temp1[1].split('\u202f')
                max_salary = f'{temp2[0]}{temp2[1].split(" ")[0]}'
                currency = temp2[1].split(' ')[1]
                return int(min_salary), int(max_salary), currency
            if len(temp1) == 1:
                temp2 = temp1[0].split(' ')
                if temp2[0] == 'до':
                    min_salary = None
                    max_salary = int(''.join(temp2[1].split('\u202f')))
                    currency = temp2[2]
                    return min_salary, max_salary, currency
                elif temp2[0] == 'от':
                    min_salary = int(''.join(temp2[1].split('\u202f')))
                    max_salary = None
                    currency = temp2[2]
                    return min_salary, max_salary, currency
    except Exception as err:
        print(f'{type(err)}:\n{err}')
    return None, None, None


page = 0
vacancies = []
while True:
    params = {
        'clusters': 'true',
        'no_magic': 'true',
        'ored_clusters': 'true',
        'enable_snippets': 'true',
        'st': 'searchVacancy',
        'text': 'Django',
        'from': 'suggest_post',
        'area': '113',
        'page': page,
    }
    response = requests.get(url + '/search/vacancy', params=params, headers=my_headers)

    soup = bs(response.text, 'html.parser')

    vacancy_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
    next_page = soup.find('a', attrs={'class': 'bloko-button', 'data-qa': 'pager-next', 'rel': 'nofollow'})
    if next_page:
        for vacancy in vacancy_list:
            vacancy_data = {}
            vacancy_name = vacancy.find('a', attrs={'class': 'bloko-link'}).text
            vacancy_link = vacancy.find('a', attrs={'class': 'bloko-link'}).get('href')
            try:
                vacancy_descrip = vacancy.findAll('div',
                                                  attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'})[0].getText()
            except Exception as err:
                print(f'{type(err)}:\n{err}')
                vacancy_descrip = ''
            try:
                vacancy_stack = vacancy.findAll('div',
                                                attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'})[0].getText()
            except Exception as err:
                print(f'{type(err)}:\n{err}')
                vacancy_stack = ''
            vacancy_salary = vacancy.findAll('div', attrs={'class': 'vacancy-serp-item__sidebar'})[0].text
            min_salary, max_salary, currency = get_salary(vacancy_salary)

            vacancy_data['link'] = vacancy_link
            vacancy_data['name'] = vacancy_name
            vacancy_data['description'] = vacancy_descrip
            vacancy_data['stack'] = vacancy_stack
            vacancy_data['min_salary'] = min_salary
            vacancy_data['max_salary'] = max_salary
            vacancy_data['currency'] = currency

            vacancies.append(vacancy_data)
    else:
        break
    page += 1


pprint(vacancies)
print(len(vacancies))
