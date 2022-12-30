import sqlite3
import pandas as pd


def converter(x, cursor):
    """
    Конвертатор валют
    :param x: Строка для конвертации
    :param cursor: Объект класса Cursor
    :return: Сконвертированную валюту в рубли
    """
    if pd.isnull(x):
        return x
    values = x.split()
    if values[1] in ["RUR", "AZN", "UZS", "KGS", "GEL"]:
        return values[0]
    cursor.execute(f"""SELECT date, {values[1]} FROM exchange_rates WHERE date = '{values[2]}'""")
    course = cursor.fetchone()
    if course[1] != None:
        return round(float(values[0]) * course[1])
    return values[0]


"""
Скрипт для создания БД vacancies.csv
:return: None
"""
try:
    connect = sqlite3.connect('Database_3_5_2.db')
    cursor = connect.cursor()

    df = pd.read_csv("vacancies.csv")
    df.insert(1, "salary", None)
    df["salary"] = df[["salary_from", "salary_to"]].mean(axis=1)
    df["published_at"] = df["published_at"].apply(lambda d: d[:7])
    df["salary"] = df["salary"].astype(str) + " " + + df["salary_currency"] + " " + df["published_at"]
    df["salary"] = df["salary"].apply(lambda x: converter(x, cursor))
    df = df.drop(columns=['salary_from', 'salary_to', 'salary_currency'])
    df.to_sql('task_3_5_2', connect, if_exists='replace', index=False)
    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)

finally:
    if (connect):
        connect.close()
        print("Соединение с SQLite закрыто")


