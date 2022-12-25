from datetime import datetime

import pandas as pd

'''
разделение csv-файла на чанки по годам публикации вакансии
'''
file = 'vacancies.csv'
df = pd.read_csv(file)

'''
Создаем новую колонку
'''
df['years'] = df['published_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z').year)

years = df['years'].unique()

'''
Создает csv-файл с данными по году
'''
for year in years:
    data = df[df['years'] == year]
    data.iloc[:, :6].to_csv(rf'data/vacancies_{year}.csv', index=False)