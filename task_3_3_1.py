import pandas as pd
from _datetime import datetime
from xml.etree import ElementTree
import numpy as np
import grequests


def create_chunks(file_name):
    """
    Читает и разделяет данные по годам в отдельные csv файлы
    :return: None
    """
    pd.set_option("display.max_columns", None)
    df = pd.read_csv(file_name)
    df["years"] = df["published_at"].apply(lambda x: datetime(int(x[:4]), int(x[5:7]), int(x[8:10])).year)
    years = df["years"].unique()
    for year in years:
        data = df[df["years"] == year]
        data.iloc[:, :6].to_csv(rf"data/vacancies_{year}.csv", index=False)


file_name = "vacancies_dif_currencies.csv"
create_chunks(file_name)

'''
Считывет и фильтрует файл. 
'''
df = pd.read_csv(file_name)
print(df["salary_currency"].value_counts())
df["count"] = df.groupby("salary_currency")["salary_currency"].transform("count")
df = df[(df["count"] > 5000)]
df["published_at"] = df["published_at"].apply(lambda x: datetime(int(x[:4]), int(x[5:7]), 1))
headers = df["salary_currency"].unique()
min_date = df["published_at"].min()
max_date = df["published_at"].max()
'''
список валют
'''
headers = np.delete(headers, 1)
'''
Словарь для сбора данных из запроса
'''
data_dict = {item: [] for item in np.insert(headers, 0, "date")}
'''
список с датами
'''
dates_lst = pd.date_range(min_date.strftime("%Y-%m"), max_date.strftime("%Y-%m"), freq="MS")


'''
Создает файл о валютах за определенный период
'''
sites = []
for date in dates_lst:
    t = pd.to_datetime(str(date))
    timestring = t.strftime('%d/%m/%Y')
    data_dict["date"].append(t.strftime('%Y-%m'))
    sites.append(rf"http://www.cbr.ru/scripts/XML_daily.asp?date_req={timestring}")


response = (grequests.get(url) for url in sites)
'''
Проходимся по дереву в цикле
'''
for res in grequests.map(response):
    data = {}
    root = ElementTree.fromstring(res.content)
    for element in root.iter('Valute'):
        args = []
        '''
        Получаем нужные значения
        '''
        for child in element:
            args.append(child.text)
        if headers.__contains__(args[1]):
            data[args[1]] = round(float(args[4].replace(',', '.')) / int(args[2]), 6)
    '''
    Заполняем пустые значения BYR
    '''
    for key in headers:
        if data.__contains__(key):
            data_dict[key].append(data[key])
        else:
            data_dict[key].append(None)

df = pd.DataFrame(data_dict)
df.to_csv("dataframe.csv", index=False)
