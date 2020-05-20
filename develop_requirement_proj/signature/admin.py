from django.contrib import admin

from .models import Document, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'account',
        'project',
        'develop_team_function',
        'develop_team_sub_function',
        'status',
        'initiator',
        'assigner',
        'developers',
        'title',
        'description',
        'form_begin_time',
        'form_end_time',
        'expected_develop_duration_day',
        'actual_develop_duration_day',
        'repository_url',
        'parent'
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'path',
        'name',
        'description',
        'size',
        'created_time',
        'uploader',
        'order'
    )
