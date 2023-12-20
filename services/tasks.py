from celery import shared_task
from django.core.management import call_command


@shared_task
def import_recipe_from_vk_task():
    '''
    Периодическая загрузка новых рецептов из сообщества ВК.
    '''
    call_command('import_recipe')
