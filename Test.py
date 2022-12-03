from unittest import TestCase
from task_2_1_3 import DataSet

field = ['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at', 'is_needed']
vac_row1 = ['Программист', 1, 11, 'EUR', 'Москва', '2010-12-03T18:44:25+0300']
vac_row2 = ['Дизайнер', 100000, 500000, 'KZT', 'Екатеринбург', '2012-10-22T18:44:25+0500']
dataSet = DataSet()
dataSet.lines = [vac_row1, vac_row2]


class AreasDictsTests(TestCase):
    dataSet.get_key_and_count(dataSet.lines, 'area_name', True)

    def test_area_list(self):
        self.assertEqual(dataSet.price_area.keys(), ['Москва', 'Екатеринбург'])

    def test_count_list(self):
        self.assertEqual(dataSet.count_area.keys(), ['Москва', 'Екатеринбург'])

    def test_count_list_values(self):
        self.assertEqual(dataSet.count_area.values(), [0.5, 0.5])

    def test_area_list_values(self):
        self.assertEqual(dataSet.price_area.values(), [359.4, 39000])


class YearsDictsTest(TestCase):
    dataSet.get_key_and_count(dataSet.lines, 'published_at', False)

    def test_year_list(self):
        self.assertEqual(dataSet.wages_year.keys(), [2010, 2012])

    def test_year_count_list(self):
        self.assertEqual(dataSet.count_year.keys(), [2010, 2012])

    def test_wages_year_values(self):
        self.assertEqual(dataSet.wages_year.values(), [359.4, 39000])

    def test_year_count_values(self):
        self.assertEqual(dataSet.count_year.values(), [1, 1])