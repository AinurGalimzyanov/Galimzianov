import re
import prettytable
from prettytable import PrettyTable
import csv

currency_to_rub = {"Манаты": 35.68,
                   "Белорусские рубли": 23.91,
                   "Евро": 59.90,
                   "Грузинский лари": 21.74,
                   "Киргизский сом": 0.76,
                   "Тенге": 0.13,
                   "Рубли": 1,
                   "Гривны": 1.64,
                   "Доллары": 60.66,
                   "Узбекский сум": 0.0055, }


class DataSet:
    def __init__(self, file):
        self.file = file
        self.translator = {"noExperience": "Нет опыта",
                           "between1And3": "От 1 года до 3 лет",
                           "between3And6": "От 3 до 6 лет",
                           "moreThan6": "Более 6 лет",
                           "AZN": "Манаты",
                           "BYR": "Белорусские рубли",
                           "EUR": "Евро",
                           "GEL": "Грузинский лари",
                           "KGS": "Киргизский сом",
                           "KZT": "Тенге",
                           "RUR": "Рубли",
                           "UAH": "Гривны",
                           "USD": "Доллары",
                           "UZS": "Узбекский сум",
                           "True": "Да",
                           "False": "Нет",
                           "FALSE": "Нет",
                           "TRUE": "Да"}
        heading, variable = self.csv_reader()
        dictionaries = self.csv_filer(variable, heading)
        self.vacancies_objects = [Vacancy(dict) for dict in dictionaries]

    def csv_reader(self):
        list = []
        l = 0
        with open(self.file, encoding="utf-8-sig") as test:
            unpacker = csv.reader(test)
            for row in unpacker:
                if l < len(row):
                    l = len(row)
                if '' not in row and l == len(row):
                    list.append(row)
        self.check_content(list)
        return list[0], list[1:]

    def check_content(self, list):
        if len(list) == 0:
            print("Пустой файл")
            exit()
        elif len(list) == 1:
            print("Нет данных")
            exit()

    def csv_filer(self, reader, list_naming):
        dictionaries_list = []
        for vacancy in reader:
            dict = {}
            for i in range(len(list_naming)):
                dict[list_naming[i]] = self.delete_tags_space(vacancy[i])
            dictionaries_list.append(dict)
        return dictionaries_list

    def delete_tags_space(self, string):
        new_string = re \
            .compile(r'<[^>]+>') \
            .sub('', string) \
            .replace(" ", " ") \
            .replace(" ", " ") \
            .replace("  ", " ") \
            .replace("  ", " ") \
            .strip()
        if new_string in self.translator:
            new_string = self.translator[new_string]
        return new_string


class Vacancy:
    def __init__(self, dict):
        self.name = dict["name"]
        self.description = dict["description"]
        self.key_skills = dict["key_skills"]
        self.experience_id = dict["experience_id"]
        self.premium = dict["premium"]
        self.employer_name = dict["employer_name"]
        self.salary = Salary(dict["salary_from"], dict["salary_to"], dict["salary_gross"],
                             dict["salary_currency"])
        self.area_name = dict["area_name"]
        self.published_at = dict["published_at"]

    def get_variables(self):
        return {"Название": self.name,
                "Описание": self.description,
                "Навыки": self.key_skills,
                "Опыт работы": self.experience_id,
                "Премиум-вакансия": self.premium,
                "Компания": self.employer_name,
                "Оклад": self.salary,
                "Название региона": self.area_name,
                "Дата публикации вакансии": self.published_at}

    def get_copy(self):
        return Vacancy({"name": self.name, "description": self.description,
                        "key_skills": self.key_skills,
                        "experience_id": self.experience_id,
                        "premium": self.premium,
                        "employer_name": self.employer_name,
                        "salary_from": self.salary.salary_from,
                        "salary_to": self.salary.salary_to,
                        "salary_gross": self.salary.salary_gross,
                        "salary_currency": self.salary.salary_currency,
                        "area_name": self.area_name,
                        "published_at": self.published_at})


class Salary:
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency

    def get_salary_rub(self):
        return (int(float(self.salary_from)) + int(float(self.salary_to))) / 2 * currency_to_rub[self.salary_currency]


class InputCorrect:
    def __init__(self, filters, sorting_parameter, sort_order, numbers, fields):
        self.filters = filters.split(": ")
        self.sorting_parameter = sorting_parameter
        self.sort_order = sort_order
        self.numbers = numbers
        self.fields = fields

    def check_filters(self):
        if len(self.filters) == 1 and self.filters[0] != "":
            print("Формат ввода некорректен")
            exit()
        elif self.filters[0] not in ["Навыки", "Оклад", "Дата публикации вакансии", "Опыт работы",
                                     "Премиум-вакансия",
                                     "Идентификатор валюты оклада", "Название", "Название региона", "Компания",
                                     ""]:
            print("Параметр поиска некорректен")
            exit()
        elif self.sorting_parameter not in ["Навыки", "Оклад", "Дата публикации вакансии", "Опыт работы",
                                            "Премиум-вакансия",
                                            "Идентификатор валюты оклада", "Название", "Название региона", "Компания",
                                            ""]:
            print("Параметр сортировки некорректен")
            exit()
        elif self.sort_order != "Да" and self.sort_order != "Нет" and self.sort_order != "":
            print("Порядок сортировки задан некорректно")
            exit()

    def sort_data_vacancies(self, data_vacancies):
        if self.sort_order == "Да":
            self.sort_order = True
        else:
            self.sort_order = False
        if self.sorting_parameter == "":
            sorted_vacancies = data_vacancies
        elif self.sorting_parameter == "Оклад":
            sorted_vacancies = sorted(data_vacancies,
                                      key=lambda vacancy: vacancy.salary.get_salary_rub(),
                                      reverse=self.sort_order)

        elif self.sorting_parameter == "Навыки":
            sorted_vacancies = sorted(data_vacancies,
                                      key=lambda vacancy: len(
                                          vacancy.key_skills.split("\n")), reverse=self.sort_order)
        elif self.sorting_parameter == "Опыт работы":
            experience_dictionary = {"Нет опыта": 0, "От 1 года до 3 лет": 1, "От 3 до 6 лет": 2, "Более 6 лет": 3}
            sorted_vacancies = sorted(data_vacancies,
                                      key=lambda vacancy:
                                      experience_dictionary[vacancy.experience_id],
                                      reverse=self.sort_order)

        else:
            sorted_vacancies = sorted(data_vacancies,
                                      key=lambda vacancy: vacancy.get_variables()[self.sorting_parameter],
                                      reverse=self.sort_order)
        return sorted_vacancies

    def filter_vacancy(self, vacancy):
        if self.filters[0] == "Оклад":
            if int(float(self.filters[1])) < int(float(vacancy.salary.salary_from)):
                return False
            elif int(float(self.filters[1])) > int(float(vacancy.salary.salary_to)):
                return False
        elif self.filters[0] == "Дата публикации вакансии":
            if self.filters[1] != self.date_processing(vacancy.published_at):
                return False
        elif self.filters[0] == "Навыки":
            for element in self.filters[1].split(", "):
                if element not in vacancy.key_skills.split("\n"):
                    return False
        elif self.filters[0] == "Идентификатор валюты оклада":
            if self.filters[1] != vacancy.salary.salary_currency:
                return False
        elif self.filters[0] in vacancy.get_variables():
            if self.filters[1] != vacancy.get_variables()[self.filters[0]]:
                return False
        return True

    def get_new_table(self, result_table, count):
        start = 0
        end = count
        self.numbers = self.numbers.split(" ")
        if self.numbers[0] == "":
            pass
        elif len(self.numbers) == 1:
            start = int(self.numbers[0]) - 1
        elif len(self.numbers) == 2:
            start = int(self.numbers[0]) - 1
            end = int(self.numbers[1]) - 1
        self.fields = self.fields.split(", ")
        if self.fields[0] == "":
            return result_table.get_string(start=start, end=end)
        self.fields.insert(0, "№")
        return result_table.get_string(start=start, end=end, ﬁelds=self.fields)

    def print_vacancies(self, variable):
        result_table = PrettyTable(hrules=prettytable.ALL, align='l')
        number = 1
        new_data_vacancies = self.sort_data_vacancies(variable)
        correct_sequence = ["Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад",
                     "Название региона", "Дата публикации вакансии"]
        result_table.field_names = ['№'] + correct_sequence
        result_table, number = self.run_table(new_data_vacancies, number, result_table)
        result_table.max_width = 20
        result_table = self.get_new_table(result_table, number - 1)
        print(result_table)

    def run_table(self, new_data_vacancies, number, result_table):
        for new_vacancy in new_data_vacancies:
            formatted_new_vacancy = self.formatter(new_vacancy)
            if not self.filter_vacancy(new_vacancy):
                continue
            row = [value if len(value) <= 100 else value[:100] + "..." for value in
                   formatted_new_vacancy.get_variables().values()]
            row.insert(0, number)
            result_table.add_row(row)
            number += 1
        if number == 1:
            print("Ничего не найдено")
            exit()
        return result_table, number


    def formatter(self, vacancy):
        minSalary = self.add_space(vacancy.salary.salary_from)
        maxSalary = self.add_space(vacancy.salary.salary_to)
        if vacancy.salary.salary_gross == "Да":
            beforeTaxes = "Без вычета налогов"
        else:
            beforeTaxes = "С вычетом налогов"
        new_vacancy = vacancy.get_copy()
        new_vacancy.salary = f"{minSalary} - {maxSalary} ({vacancy.salary.salary_currency}) ({beforeTaxes})"
        new_vacancy.published_at = self.date_processing(vacancy.published_at)
        return new_vacancy

    def add_space(self, number):
        number = str(int(float(number)))
        new_number = ""
        new_number += number[:len(number) % 3]
        for i in range(len(number) // 3):
            if new_number != "":
                new_number += " "
            new_number += number[len(number) % 3 + i * 3: len(number) % 3 + (i + 1) * 3]
        return new_number

    def date_processing(self, date):
        newDate = date[8: 10] + "." + date[5: 7] + "." + date[: 4]
        return newDate


def GetPrettyTable():
    file = input("Введите название файла: ")
    filters = input("Введите параметр фильтрации: ")
    sorting_parameter = input("Введите параметр сортировки: ")
    sort_order = input("Обратный порядок сортировки (Да / Нет): ")
    numbers = input("Введите диапазон вывода: ")
    fields = input("Введите требуемые столбцы: ")
    input_correct = InputCorrect(filters, sorting_parameter, sort_order, numbers, fields)
    input_correct.check_filters()
    dataset = DataSet(file)
    input_correct.print_vacancies(dataset.vacancies_objects)
