import pandas as pd
import requests
import json
from pandas import json_normalize

'''
задаем основные настройки и переменные
'''
pd.set_option("display.max_columns", None)
data = {'name': [], 'salary_from': [], 'salary_to': [], 'salary_currency': [], 'area_name': [], 'published_at': []}
date = ['2022-12-16T00:00:00', '2022-12-16T06:00:00',
        '2022-12-16T12:00:00', '2022-12-16T18:00:00', '2022-12-17T00:00:00']

'''
цикл для прохода по часам
'''
vacancies = []
for i in range(len(date) - 1):
    date_from = date[i]
    date_to = date[i+1]
    '''
    проходимся по страницам
    '''
    for j in range(1, 20):
        '''
        данные с запроса
        '''
        request = requests.get(
           f'https://api.hh.ru/vacancies?date_from={date_from}&date_to={date_to}&&specialization=1&per_page=100&page={j}')
        jsonText = request.text
        jsonData = json.loads(jsonText)
        '''
        сохраняем данные из запроса
        '''
        vacancies.extend(jsonData['items'])

'''
сохраняем в csv
'''
df = json_normalize(vacancies)
df1 = df[["name", "salary.from", "salary.to", "salary.currency", "area.name", "published_at"]]
df1.to_csv("hh.csv", index=False)