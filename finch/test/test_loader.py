import os
import unittest

from finch import loader


class TestLoader(unittest.TestCase):

    def test_load_csv_file(self):
        csv_file_path = os.path.join(os.getcwd(), 'data.csv')
        print(csv_file_path)
        csv_content = loader.load_csv_file(csv_file_path)
        self.assertEqual(
            csv_content,
            [
                {'environment': 'ci', 'host': 'localhost', 'port': '27017'},
                {'environment': 'e2e', 'host': 'localhost', 'port': '27018'}
            ]
        )

    def test_load_xlsx_file(self):
        xlsx_file_path = os.path.join(os.getcwd(), 'data.xlsx')
        print(xlsx_file_path)
        xlsx_content = loader.load_xlsx_file(xlsx_file_path)
        self.assertEqual(
            xlsx_content,
            [
                {'environment': 'ci', 'host': 'localhost', 'port': '27017'},
                {'environment': 'e2e', 'host': 'localhost', 'port': '27018'}
            ]
        )
