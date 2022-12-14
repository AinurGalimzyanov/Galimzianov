import csv, math, re
from _datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }


class Salary:
    def __init__(self, dictionary):
        self.salary_in_rur = currency_to_rub[dictionary["salary_currency"]] * \
                        (math.floor(float(dictionary["salary_to"])) + math.floor(float(dictionary["salary_from"])))/2


class Vacancy:
    def __init__(self, dictionary: dict):
        self.dic = dictionary
        self.salary = Salary(dictionary)
        self.dic["year"] = int(dictionary["published_at"][:4])
        self.is_needed = dictionary["is_needed"]


class InputConect:
    def __init__(self):
        self.file = input("Введите название файла: ")
        self.prof = input("Введите название профессии: ")
        with open(self.file, "r", encoding='utf-8-sig', newline='') as test:
            unpacker = iter(csv.reader(test))
            if next(unpacker, "none") == "none":
                print("Пустой файл")
                exit(0)
            if next(unpacker, "none") == "none":
                print("Нет данных")
                exit(0)

class DataSet:
    def __init__(self):
        self.input_values = InputConect()
        self.csv_reader()
        self.csv_filter()
        self.years = []
        for i in self.filt_vac:
            self.years.append(i.dic["year"])
        self.years.sort()
        conut_vacs = len(self.filt_vac)
        self.wages_year, self.count_year = self.get_key_and_count(self.filt_vac, "year", False)
        self.year_required_wages, self.year_required_count = self.get_key_and_count(self.required_vac, "year", False)
        self.wages_area, self.count_area = self.get_key_and_count(self.filt_vac, "area_name", True)
        self.wages_area = dict(list(sorted(self.wages_area.items(), key=lambda x: x[1], reverse=True))[:10])
        self.price_area = {x: round(y / conut_vacs, 4) for x, y in self.count_area.items()}
        self.price_area = dict(list(sorted(self.price_area.items(), key=lambda x: x[1], reverse=True))[:10])
        self.project_list = self.creat_list()
        self.write_data()

    def csv_reader(self):
        with open(self.input_values.file, "r", encoding='utf-8-sig', newline='') as test:
            csv_file = csv.reader(test)
            self.first = next(csv_file)
            self.lines = []
            lenght = 0
            for row in csv_file:
                if lenght < len(row):
                    lenght = len(row)
                if not "" in row and lenght == len(row):
                    self.lines.append(row)

    def csv_filter(self):
        self.filt_vac = []
        for i in self.lines:
            new_dict = dict(zip(self.first, i))
            new_dict["is_needed"] = new_dict["name"].find(self.input_values.prof) > -1
            self.filt_vac.append(Vacancy(new_dict))
        self.required_vac = list(filter(lambda x: x.is_needed, self.filt_vac))

    def try_add(self, dic: dict, key, x):
        try: dic[key] += x
        except: dic[key] = x
        return dic

    def upgrad_keys(self, count_key):
        for i in self.years:
            if i in count_key.keys():
                continue
            count_key[i] = 0
        return count_key

    def get_key_and_count(self, list_vacs: list, str_key: str, is_area: bool):
        sum_key, count_key = {}, {}
        for x in list_vacs:
            sum_key = self.try_add(sum_key, x.dic[str_key], x.salary.salary_in_rur)
            count_key = self.try_add(count_key, x.dic[str_key], 1)
        if not is_area:
            sum_key = self.upgrad_keys(sum_key)
            count_key = self.upgrad_keys(count_key)
        else:
            count_key = dict(filter(lambda y: y[1] / len(list_vacs) > 0.01, count_key.items()))
        salary_key = {}
        for key, x in count_key.items():
            salary_key[key] = 0 if x == 0 else math.floor(sum_key[key] / x)
        key_to_middle_salary = salary_key
        return key_to_middle_salary, count_key
    def write_data(self):
        print("Динамика уровня зарплат по годам:", self.wages_year)
        print("Динамика количества вакансий по годам:", self.count_year)
        print("Динамика уровня зарплат по годам для выбранной профессии:", self.year_required_wages)
        print("Динамика количества вакансий по годам для выбранной профессии:", self.year_required_count)
        print("Уровень зарплат по городам (в порядке убывания):", self.wages_area)
        print("Доля вакансий по городам (в порядке убывания):", self.price_area)

    def creat_list(self):
        return [self.wages_year, self.year_required_wages, self.count_year,
                self.year_required_count, self.wages_area, self.price_area]

class Report:
    def __init__(self):
        self.dataSet_list = DataSet().project_list

    def generate_image(self):
        def creator_graph(number, value_1, value_2, name, bar_name_first, bar_name_second):
            ax = fig.add_subplot(number)
            ax.set_title(name)
            ax.bar(x - 0.4 / 2, value_1.values(), 0.4, label=bar_name_first)
            ax.bar(x + 0.4 / 2, value_2.values(), 0.4, label=bar_name_second)
            ax.set_xticks(x, value_1.keys(), rotation="vertical")
            ax.legend(loc='best')
            ax.grid(True, axis='y')
            ax.legend(fontsize=8)

        fig = plt.figure()
        x = np.arange(len(self.dataSet_list[0].keys()))
        creator_graph(221, self.dataSet_list[0], self.dataSet_list[1],
                      "Уровень зарплат по годам", "средняя з/п", "з/п программист")
        creator_graph(222, self.dataSet_list[2], self.dataSet_list[3],
                      "Количество вакансии по годам", "Количество вакансии", "Количество вакансии\nпрограммист")

        ax = fig.add_subplot(223)
        ax.set_title("Уровень зарплат по городам")
        y_pos = np.arange(len(self.dataSet_list[4].keys()))
        ax.barh(y_pos, list(self.dataSet_list[4].values()), align='center')
        ax.set_yticks(y_pos, labels=self.dataSet_list[4].keys())
        ax.invert_yaxis()
        ax.grid(True, axis='x')

        ax = fig.add_subplot(224)
        ax.set_title("Доля вакансии по годам")
        keys = list(self.dataSet_list[5].keys())
        keys.append("Другие")
        values = list(self.dataSet_list[5].values())
        sum_values = sum(list(self.dataSet_list[5].values()))
        values.append(1 - sum_values)
        ax.pie(values, labels=keys, startangle=-5)

        fig.set_size_inches(9, 7)
        plt.tight_layout()
        plt.savefig("graph.png")


Report().generate_image()
