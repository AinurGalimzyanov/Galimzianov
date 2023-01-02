import csv, math
import sqlite3
import pandas as pd


class SQLReport:
    """Класс создающий запросы в бд
    """
    def __init__(self, dbName: str, prof: str):
        """Инициализация и создание всех запросов и вывод результатов.
        """
        self.connect = sqlite3.connect(dbName)
        self.print_salary_by_year_query()
        self.print_salary_count_query()
        self.print_salary_by_name_query(prof)
        self.print_salary_count_by_name_query(prof)
        self.print_salary_by_city_query()
        self.print_vacancy_count_by_city_query()

    def print_salary_by_year_query(self):
        """Sql запрос для подсчета динамики уровня зарплаты по годам"""
        print("Динамика уровня зарплат по годам")
        sqlQuery = f"""SELECT SUBSTRING(published_at, 1, 4) AS 'Год', ROUND(AVG(salary), 2) AS 'Средняя з/п' 
        FROM task_3_5_2
        GROUP BY SUBSTRING(published_at, 1, 4)
        """
        df = pd.read_sql(sqlQuery, self.connect)
        print(df)
        print()

    def print_salary_count_query(self):
        """Создает запрос по количеству всех вакансий по годам"""
        print("Динамика количества вакансий по годам")
        sqlQuery = f"""SELECT SUBSTRING(published_at, 1, 4) AS 'Год', COUNT(salary) AS 'Количество вакансий' 
        FROM task_3_5_2
        GROUP BY SUBSTRING(published_at, 1, 4)
        """
        df = pd.read_sql(sqlQuery, self.connect)
        print(df)
        print()

    def print_salary_by_name_query(self, prof: str):
        """Sql запрос для подсчета динамики уровня зарплат по выбранной профессии"""
        print("Динамика уровня зарплат по годам для выбранной профессии")
        sqlQuery = (f"""SELECT SUBSTRING(published_at, 1, 4) AS 'Год', ROUND(AVG(salary), 2) 
        AS 'Средняя з/п - {prof}'
        FROM task_3_5_2
        WHERE name LIKE '%{prof}%'
        GROUP BY SUBSTRING(published_at, 1, 4)
        """)
        df = pd.read_sql(sqlQuery, self.connect)
        print(df)
        print()

    def print_salary_count_by_name_query(self, prof: str):
        """Создает запрос по количеству нужных вакансий по годам"""
        print("Динамика количества вакансий по годам для выбранной профессии")
        sqlQuery = f"""SELECT SUBSTRING(published_at, 1, 4) AS 'Год', COUNT(salary) 
        AS 'Количетсво вакансий - {prof}'
        FROM task_3_5_2
        WHERE name LIKE '%{prof}%'
        GROUP BY SUBSTRING(published_at, 1, 4)
        """
        df = pd.read_sql(sqlQuery, self.connect)
        print(df)
        print()

    def print_salary_by_city_query(self):
        """Sql запрос для подсчета уровня зарплат по городам"""
        print("Уровень зарплат по городам")
        sqlQuery = """
            SELECT area_name, COUNT(*) as count, CAST(ROUND(AVG(salary)) AS INTEGER) as avg_salary
            FROM task_3_5_2 
            GROUP BY area_name 
            HAVING count > (SELECT COUNT(*) FROM task_3_5_2) / 100
            ORDER BY avg_salary DESC
            LIMIT 10;
        """
        df = pd.read_sql(sqlQuery, self.connect)
        print(df)
        print()

    def print_vacancy_count_by_city_query(self):
        """Sql запрос для подсчета доли вакансии по городам"""
        print("Доля вакансий по городам")
        sqlQuery = """
            SELECT area_name, COUNT(*) as count, 
                CAST(ROUND(CAST(COUNT(*) AS REAL) / (SELECT COUNT(*) FROM task_3_5_2) * 100, 4) AS VARCHAR) || '%' AS piece
            FROM task_3_5_2 
            GROUP BY area_name 
            HAVING count > (SELECT COUNT(*) FROM task_3_5_2) / 100
            ORDER BY COUNT(*) DESC
            LIMIT 10;
        """
        df = pd.read_sql(sqlQuery, self.connect)
        print(df)
        print()


def setPandasOptions():
    """Устанавливает настройки pandas, чтобы корректно отображать класс DataFrame в консоли."""
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.expand_frame_repr', False)


if __name__ == '__main__':
    setPandasOptions()
    fileName = "Database_3_5_2.db"
    professionName = "Программист"
    input_values = SQLReport(fileName, professionName)