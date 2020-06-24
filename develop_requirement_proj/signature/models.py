""" signature database model """
from mptt.models import MPTTModel, TreeForeignKey

from django.conf import settings
from django.contrib.postgres import fields
from django.db import models
from django.utils.translation import gettext_lazy as _


class Account:
    """ OEM Accounts Model """
    def __init__(self, **kwargs):
        fields = [
            'id',
            'name',
            'code',
            'business_unit',
            'project_count'
        ]
        for field in fields:
            setattr(self, field, kwargs.get(field, None))

    def __str__(self):
        return f'<{self.__class__.__name__} {self.id} : {self.name}>'

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"("
            f"{self.id}, "
            f"{self.name}, "
            f"{self.code}, "
            f"{self.business_unit}, "
            f"{self.project_count}"
            f")"
        )


class Project:
    """ OEM Project Model """
    def __init__(self, **kwargs):
        fields = [
            'id',
            'wistron_name',
            'customer_name',
            'wistron_code',
            'plm_code_1',
            'plm_code_2',
            'deleted_at',
            'type',
            'name',
            'plm_code',
            'status',
            'product_line',
            'business_model',
            'account'
        ]
        for field in fields:
            setattr(self, field, kwargs.get(field, None))

    def __str__(self):
        return f'<{self.__class__.__name__} {self.id} : {self.name}>'

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"("
            f"{self.id}, "
            f"{self.wistron_name}, "
            f"{self.customer_name}, "
            f"{self.wistron_code}, "
            f"{self.plm_code_1}, "
            f"{self.plm_code_2}, "
            f"{self.deleted_at}, "
            f"{self.type}, "
            f"{self.name}, "
            f"{self.plm_code}, "
            f"{self.status}, "
            f"{self.product_line}, "
            f"{self.business_model}, "
            f"{self.account}"
            f")"
        )


class Order(MPTTModel):
    """ Order Model """
    account = models.IntegerField(_("order's account"), null=True)
    project = models.IntegerField(_("order's project"), null=True)
    develop_team_function = models.CharField(_("developer's function team"), max_length=20)
    develop_team_sub_function = models.CharField(_("developer's sub function team"), max_length=20)
    status = fields.JSONField(_("order's current status"), default=dict)
    initiator = models.CharField(_("initiator's employee_id"), max_length=50)
    assigner = models.CharField(_("assigner's employee_id (PO/PM)"), max_length=50)
    developers = fields.JSONField(_("employee_ids of the developer's contactor and member"), default=dict)
    title = models.CharField(max_length=500)
    description = models.TextField()
    form_begin_time = models.DateTimeField(_("order's begin time"), auto_now_add=True)
    form_end_time = models.DateTimeField(_("order's end time"), null=True)
    expected_develop_duration_day = models.FloatField(_("expected development duration (days)"), null=True, blank=True)
    actual_develop_duration_day = models.FloatField(_("actual development duration (days)"), null=True, blank=True)
    repository_url = models.URLField(_("repository url of source code"), max_length=1000, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        ordering = ['form_begin_time']
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return f'Id: {self.id}, Title: {self.title}'


class Document(models.Model):
    """ Order's Document Model """
    path = models.FileField(_("document's relative path"), max_length=200, upload_to=settings.MEDIA_ROOT)
    name = models.CharField(_("docuemnt's name"), max_length=200)
    description = models.CharField(_("document's description"), max_length=1000)
    size = models.PositiveIntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    uploader = models.CharField(max_length=20)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order', 'created_time']
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    def __str__(self):
        return f'Id: {self.id}, Filename:{self.name}, Order_id:{self.order}'


class Schedule(models.Model):
    """ Order's Current Schedule Model """
    event_name = models.CharField(max_length=100)
    description = models.TextField()
    expected_time = models.DateTimeField(null=True)
    actual_time = models.DateField(null=True)
    complete_rate = models.PositiveIntegerField(_('the complete rate of schedule event'))
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    version = models.IntegerField(_('current version'), null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order', 'created_time']
        verbose_name = _('schedule')
        verbose_name_plural = _('schedules')

    def __str__(self):
        return f'Id: {self.id}, Name:{self.event_name}, Order:{self.order.id}'


class ScheduleTracker(models.Model):
    """ Order's Schedule Tracker Model"""
    event_name = models.CharField(max_length=100)
    description = models.TextField()
    expected_time = models.DateTimeField(null=True)
    actual_time = models.DateField(null=True)
    complete_rate = models.PositiveIntegerField(_('the complete rate of schedule event'), null=True)
    created_time = models.DateTimeField(null=True)
    update_time = models.DateTimeField(null=True)
    version = models.IntegerField(null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order', 'version']
        verbose_name = _('schedule tracker')
        verbose_name_plural = _('schedule trackers')

    def __str__(self):
        return f'Id: {self.id}, Name:{self.event_name}, Order:{self.order.id}, Version:{self.version}'


class ProgressTracker(models.Model):
    """ Order's Development Progress Model """
    editor = models.CharField(max_length=20)
    develop_time = models.DateTimeField(null=True)
    comment = models.TextField()
    complete_rate = models.PositiveIntegerField(null=True)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order', 'created_time']
        verbose_name = _('progress tracker')
        verbose_name_plural = _('progress tarckers')

    def __str__(self):
        return f'Id: {self.id}, Order: {self.order.id}, Compelete Rate:{self.complete_rate}'


class History(models.Model):
    """ Order's History Model """
    editor = models.CharField(max_length=20)
    comment = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order', 'created_time']
        verbose_name = _('history')
        verbose_name_plural = _('histories')

    def __str__(self):
        return f'Id: {self.id}, Order: {self.order.id}, Editor: {self.editor}, Comment: {self.comment}'


class Notification(models.Model):
    """ Order's Notificaiton model """
    link = models.URLField(max_length=1000)
    read = models.BooleanField(_('the read status of the notification'), default=False)
    category = models.CharField(max_length=20)
    initiator = models.CharField('the initiator of the notification', max_length=20)
    created_time = models.DateTimeField(auto_now_add=True)
    owner = models.CharField('the owner of the notification', max_length=20)

    class Meta:
        ordering = ['owner', 'read', 'created_time']
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')

    def __str__(self):
        return f'Id: {self.id}, Read: {self.read}, Create_at: {self.created_time}'


class Signature(models.Model):
    """ Order's Signature Model """
    sequence = models.PositiveIntegerField(null=True)
    signer = models.CharField(max_length=20)
    sign_unit = models.CharField(_('the department of signing'), max_length=20)
    status = models.CharField(max_length=20)
    comment = models.TextField()
    signed_time = models.DateTimeField(auto_now=True, null=True)
    role_group = models.CharField(max_length=20)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order', 'sequence']
        verbose_name = _('signature')
        verbose_name_plural = _('signatures')

    def __str__(self):
        return f'Id: {self.id}, Order: {self.order.id}, Sequence: {self.sequence}, Signer: {self.signer}'


class OrderTracker(models.Model):
    """ Order Tracker Model """
    account = models.IntegerField(_("order's account"), null=True)
    project = models.IntegerField(_("order's project"), null=True)
    develop_team_function = models.CharField(_("developer's function team"), max_length=20)
    develop_team_sub_function = models.CharField(_("developer's sub function team"), max_length=20)
    status = fields.JSONField(_("order's current status"), default=dict)
    initiator = models.CharField(_("initiator's employee_id"), max_length=50)
    assigner = models.CharField(_("assigner's employee_id (PO/PM)"), max_length=50)
    developers = fields.JSONField(_("employee_ids of the developer's contactor and member"), default=dict)
    title = models.CharField(max_length=500)
    description = models.TextField()
    form_begin_time = models.DateTimeField(_("order's begin time"))
    form_end_time = models.DateTimeField(_("order's end time"), null=True)
    expected_develop_duration_day = models.FloatField(_("expected development duration (days)"), null=True, blank=True)
    actual_develop_duration_day = models.FloatField(_("actual development duration (days)"), null=True, blank=True)
    repository_url = models.URLField(_("repository url of source code"), max_length=1000, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    parent = models.PositiveIntegerField(null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order', 'created_time']
        verbose_name = _('order tracker')
        verbose_name_plural = _('order trackers')

    def __str__(self):
        return f'Id: {self.id}, Title: {self.title}, Order: {self.order.id}, Create_at: {self.created_time}'
