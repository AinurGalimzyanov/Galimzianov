import sqlite3
import pandas as pd

def create_table():
    """
    Создаем БД из файла dataframe.csv
    :return: None
    """
    try:
        conect = sqlite3.connect('Database_3_5_1.db')
        cursor = conect.cursor()

        df = pd.read_csv("dataframe.csv")
        df.to_sql('task_3_5_1', conect, if_exists='replace', index=False)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

    finally:
        if (conect):
            conect.close()
            print("Соединение с SQLite закрыто")


if __name__ == '__main__':
    create_table()