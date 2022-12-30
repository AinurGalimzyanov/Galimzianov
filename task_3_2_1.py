from datetime import datetime

import pandas as pd

'''
Разделение csv-файла на чанки по годам публикации вакансии
'''
file_name = 'vacancies.csv'
data_csv = pd.read_csv(file_name)

'''
Создаем новую колонку
'''
data_csv['years'] = data_csv['published_at'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z').year)

years = data_csv['years'].unique()

'''
Создает csv-файл с данными по году
'''
for year in years:
    data = data_csv[data_csv['years'] == year]
    data.iloc[:, :6].to_csv(rf'data/vacancies_{year}.csv', index=False)