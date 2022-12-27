import math
import pandas as pd


def converter(value, currency):
    '''
    Конвретируетор волют
    '''
    if pd.isnull(value):
        return value
    values = value.split()
    '''
    Получаем коэффициент для перевода 
    '''
    if currency.columns.__contains__(values[1]):
        d = values[2]
        course = currency[currency["date"] == d[:7]][values[1]].values
        if not math.isnan(course[0]):
            return round(float(values[0]) * course[0])
    return value

'''
Задаем основные настройки и считываем файлы
'''
file_name = "vacancies_dif_currencies.csv"
currencyFile_name = "dataframe.csv"
data = pd.read_csv(file_name)
currency = pd.read_csv(currencyFile_name)
'''
Выделяем основные переменные
'''
data.insert(1, "salary", None)
data["salary"] = data[["salary_from", "salary_to"]].mean(axis=1)
data["salary"] = data["salary"].astype(str) + " " + + data["salary_currency"] + " " + data["published_at"]
data["salary"] = data["salary"].apply(lambda value: converter(value, currency))

'''
Сохраняем в csv первые 100 результатов
'''
data = data.drop(columns=['salary_from', 'salary_to', 'salary_currency'])
df100 = data.head(100)
df100.to_csv("currency_conversion.csv", index=False)



