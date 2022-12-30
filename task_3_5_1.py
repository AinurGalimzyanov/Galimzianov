import sqlite3
import pandas as pd

def create_table():
    """
    Скрипт для создания БД и записи из файла dataframe.csv со всеми курсами валют с 2003-2022 год
    :return: None
    """
    try:
        sqlite_connection = sqlite3.connect('task_3_5_1.db')
        cursor = sqlite_connection.cursor()

        df = pd.read_csv("dataframe.csv")
        # Запись в созданную таблицу текущий dataframe
        df.to_sql('exchange_rates', sqlite_connection, if_exists='replace', index=False)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


if __name__ == '__main__':
    create_table()