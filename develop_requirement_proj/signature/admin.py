from django.contrib import admin

from .models import (
    Document, History, Notification, Order, OrderTracker, Progress, Schedule,
    ScheduleTracker, Signature,
)


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


@admin.register(OrderTracker)
class OrderTrackerAdmin(admin.ModelAdmin):
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
        'order',
        'parent'
    )


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'path',
        'name',
        'description',
        'size',
        'created_time',
        'uploader',
        'order'
    )


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'event_name',
        'description',
        'confirm_status',
        'expected_time',
        'actual_time',
        'complete_rate',
        'version',
        'created_time',
        'update_time',
        'order'
    )


@admin.register(ScheduleTracker)
class ScheduleTrackerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'event_name',
        'description',
        'confirm_status',
        'expected_time',
        'actual_time',
        'complete_rate',
        'version',
        'created_time',
        'update_time',
        'order'
    )


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'complete_rate',
        'start_time',
        'end_time',
        'editor',
        'update_time',
        'order',
    )


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'editor',
        'comment',
        'created_time',
        'order',
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'link',
        'read_status',
        'category',
        'recipient',
        'actor',
        'verb',
        'action_object',
        'target',
        'created_time',
        'deleted_time'
    )


@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "sequence",
        "signer",
        "sign_unit",
        "status",
        "comment",
        "signed_time",
        "role_group",
        "order"
    )
