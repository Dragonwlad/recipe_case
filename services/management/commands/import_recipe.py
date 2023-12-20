import os
from http import HTTPStatus

from django.core.management import BaseCommand
import requests
from dotenv import load_dotenv

from recipes.models import Recipe
from .exceptions import TokensNotAvailable, UnexpectedResponseStatus

load_dotenv()


VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')
VK_OWNER_ID = os.getenv('VK_OWNER_ID')

VERSION = 5.199
COUNT = 5
METHOD = 'wall.get?'
ENDPOINT = f'https://api.vk.com/method/{METHOD}'

RETRY_PERIOD = 600


def check_token():
    tokens = ('VK_ACCESS_TOKEN',
              'VK_OWNER_ID', )
    missing_tokens = []
    missing_tokens = [token for token in tokens if not globals()[token]]
    if missing_tokens:
        message = (f'{",".join(missing_tokens)} is not available,'
                   'programm stoped')
        raise TokensNotAvailable(message)


def get_api_answer():
    '''Request to api YP for the status of work.'''
    payload = {'owner_id': VK_OWNER_ID,
               'count': COUNT,
               'v': VERSION}
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain',
               'Authorization': f'Bearer {VK_ACCESS_TOKEN}'}
    try:
        api_answer = requests.get(ENDPOINT,
                                  headers=headers,
                                  params=payload)
    except requests.RequestException as error:
        raise ConnectionError('Response from endpoint not received, '
                              f'{error}') from error

    if api_answer.status_code != HTTPStatus.OK:
        raise UnexpectedResponseStatus('Unexpected response status'
                                       f'code from the server: {api_answer}'
                                       f', url:{ENDPOINT}, payload:{payload}')
    return api_answer.json()


def check_response(response):
    '''Checking variables from answer.'''
    if not isinstance(response, dict):
        raise TypeError('uncorrect answer from server')
    if 'response' not in response:
        raise KeyError('no key response')
    response = response['response']

    if 'items' not in response:
        raise KeyError('no key items')
    if not isinstance(response['items'], list):
        raise TypeError('uncorrect answer from server')

    return response['items']


def parse_items(items):
    '''Parsing request.'''
    recipes = []
    for item in items:
        text = item.get('text')
        if text and '\n' in text:
            name_idx_slice = text.find('\n')
            name = text[:name_idx_slice]
            text = text[name_idx_slice:]

            recipes.append(Recipe(name=name, text=text, author_id=1))

    return recipes


def create_objects(recipes):
    '''Create new objects in DB.'''
    Recipe.objects.bulk_create(recipes, ignore_conflicts=True)


class Command(BaseCommand):
    help = 'Import recipes from VK community to DB'

    def handle(self, *args, **options):
        check_token()
        response = get_api_answer()
        items = check_response(response)
        recipes = parse_items(items)
        create_objects(recipes)
