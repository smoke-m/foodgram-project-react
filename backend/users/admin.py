from django.conf import settings
from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name',
                    'is_staff', 'is_superuser', 'password')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = settings.EMPTY_VALUE
    list_editable = ('username', 'email', 'first_name', 'last_name',
                     'is_superuser', 'is_staff')
