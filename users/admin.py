from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
    )
    search_fields = ('username',)
    list_filter = ('username', 'email')
    empty_value_display = '-empty-'
