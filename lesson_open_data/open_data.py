import csv
from requests import get
import pandas as pd

url = 'https://data.gov.ru/opendata/5503079310-reestr-nark/data-20210928T0554-structure-20210928T0554.csv'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
}

# data = get(url, headers=headers)
#
# with open('data.csv', 'wb') as f:
#     f.write(data.content)

# with open('data.csv', 'r', encoding='utf-8') as f:
#     reader = csv.DictReader(f, delimiter=',')
#     fields_name = reader.fieldnames
#     print(fields_name)
#     for row in reader:
#         print(row['INN'], row['license'], row['work/services'])

# # open data with pandas
# data_frame = pd.read_csv('data.csv', sep=',')
data_frame = pd.read_csv(url, sep=',')
result = data_frame[data_frame['INN'] == 5503007178]
print(result)
pass
