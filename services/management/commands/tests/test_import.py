import unittest

from ..import_recipe import parse_items, check_response
from recipes.models import Recipe


class TestParsingService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.good_response = {
            'response': {
                'count': 1111,
                'items': [
                    {'text': 'Пицца\n Поставить в духовку'},
                    {'text': 'Пирог\n Поставить в духовку.\n Поджечь\n'}
                    ]}}

        cls.bad_items = [{'text': 'Случайный текст рецепта без названия'},
                         {'text': ''}]

    def test_response_type(self):
        result = check_response(self.good_response)
        self.assertIsInstance(result, list)

    def test_items_contents(self):
        result = parse_items(self.good_response['response']['items'])
        self.assertTrue(result)

    def test_items_type(self):
        result = parse_items(self.good_response['response']['items'])
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], Recipe)

    def test_items_no_contents(self):
        result = parse_items(self.bad_items)
        self.assertFalse(result)

    def test_items_raises_contents(self):
        with self.assertRaises(TypeError,
                               msg='Ожидалась ошибка формата'):
            check_response(self.bad_items)

        with self.assertRaises(KeyError,
                               msg='Ожидалась ошибка ключа'):
            check_response(self.bad_items[0])
