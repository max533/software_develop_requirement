from django.contrib import admin

from .models import (
    Comment, Document, Notification, Order, OrderTracker, Progress, Schedule,
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
        'update_staff',
        'update_time',
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
        'update_staff',
        'update_time',
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
        'update_time',
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
        'timestamp',
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
        'timestamp',
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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'editor',
        'content',
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
