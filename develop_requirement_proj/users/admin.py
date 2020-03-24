from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'display_name', 'english_name', 'chinese_name',
        'email', 'location', 'extension', 'joined_time', 'last_login'
    )
    list_filter = ('location', 'joined_time', 'last_login')
