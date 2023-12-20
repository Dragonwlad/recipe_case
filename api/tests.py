import json
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token

from recipes.models import Ingredient, Recipe, RecipeIngredient

User = get_user_model()


class ApiRoutesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email='a@a.com',
                                       username='username',
                                       first_name='firstname',
                                       last_name='lastname',
                                       password='passWord',
                                       )
        cls.token, _ = Token.objects.get_or_create(user=cls.user)
        cls.auth_headers = {'Authorization': f'Token {cls.token.key}'}
        cls.recipe = Recipe.objects.create(name='Рецепт 1',
                                           text='Текст рецепта',
                                           author=cls.user)
        Recipe.objects.bulk_create(
            Recipe(name=f'Рецепт {index}',
                   text='Просто рецепт.',
                   author=cls.user)
            for index in range(settings.PAGE_SIZE + 1))

        cls.ingredient = Ingredient.objects.create(name='ингредиент 1')
        cls.ingredient_2 = Ingredient.objects.create(name='ингредиент 2')
        cls.recipeingredient = RecipeIngredient.objects.create(
            recipe=cls.recipe,
            ingredient=cls.ingredient_2,
            amount=10)
        cls.urls_for_all = (
            ('api:recipes-list', None),
            ('api:recipes-detail', (1, )),
            ('api:ingredients-list', None),
            ('api:ingredients-detail', (1, )), )
        cls.urls_for_auth_users = (
            ('api:user-list', None),
            ('api:user-detail', (1, )), )
        cls.recipe_data = {'ingredients': [{'id': 1, 'amount': 1}],
                           'name': 'Рецепт пользователя',
                           'text': 'Просто рецепт пользователя.', }

    def test_pages_no_availability(self):
        '''Отсутствие доступа к url для неавторизованного
         пользователя.'''
        for name, args in self.urls_for_auth_users:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_auth_pages_availability(self):
        '''Доступ авторизованного пользователя к url для авторизованных
         пользователей.'''
        for name, args in self.urls_for_auth_users:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url, headers=self.auth_headers)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_recipe_detail_page(self):
        '''Доступна страница отдельного рецепта'''
        url = reverse('api:recipes-detail', args=(1, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_contains_ten_records(self):
        '''Paginator выдал 5 постов в рецептах.'''
        recipe_url = reverse('api:recipes-list')
        response = self.client.get(recipe_url)
        dict_response = json.loads(response.content)

        self.assertEqual(len(dict_response['results']),
                         settings.PAGE_SIZE)

    def test_create_recipe(self):
        '''Авторизированный пользователь создал рецепт.'''
        recipe_count = Recipe.objects.count()
        url = reverse('api:recipes-list')
        response = self.client.post(url, headers=self.auth_headers,
                                    data=json.dumps(self.recipe_data),
                                    content_type='application/json')
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Recipe.objects.count(), recipe_count + 1)
        self.assertEqual(self.recipe_data['name'], response_json['name'])
        self.assertEqual(self.recipe_data['text'], response_json['text'])
        self.assertEqual(self.recipe_data['ingredients'][0]['id'],
                         response_json['ingredients'][0]['id'])
        self.assertEqual(self.recipe_data['ingredients'][0]['amount'],
                         response_json['ingredients'][0]['amount'])

    def test_update_recipe(self):
        '''Авторизированный пользователь изменил рецепт.'''
        url = reverse('api:recipes-detail', args=(1, ))
        response_old_recipe = self.client.get(url, headers=self.auth_headers)
        old_recipe = json.loads(response_old_recipe.content)

        response = self.client.patch(url, headers=self.auth_headers,
                                     data=json.dumps(self.recipe_data),
                                     content_type='application/json')
        response_json = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(self.recipe_data['name'], response_json['name'])
        self.assertEqual(self.recipe_data['text'], response_json['text'])
        self.assertEqual(self.recipe_data['ingredients'][0]['id'],
                         response_json['ingredients'][0]['id'])
        self.assertEqual(self.recipe_data['ingredients'][0]['amount'],
                         response_json['ingredients'][0]['amount'])

        self.assertNotEqual(old_recipe['name'], response_json['name'])
        self.assertNotEqual(old_recipe['text'], response_json['text'])
        self.assertNotEqual(old_recipe['ingredients'][0]['id'],
                            response_json['ingredients'][0]['id'])

    def test_delete_recipe(self):
        '''Авторизированный пользователь удалил рецепт.'''
        url = reverse('api:recipes-detail', args=(1, ))
        recipe_count = Recipe.objects.count()
        response = self.client.delete(url, headers=self.auth_headers)

        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), recipe_count - 1)
