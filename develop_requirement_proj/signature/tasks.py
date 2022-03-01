from celery import shared_task

from develop_requirement_proj.employee.models import Employee
from develop_requirement_proj.signature.api.mixins import MessageMixin
from develop_requirement_proj.signature.models import Signature

from django.conf import settings
from django.core.cache import cache

from .api.serializers import EmployeeSimpleSerializer


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 5})
def update_simple_employees_cache():
    simple_employees = cache.delete('simple_employees')
    instance = Employee.objects.using('hr').all().values()
    serializer = EmployeeSimpleSerializer(instance, many=True)
    simple_employees = {}
    for simple_employee in serializer.data:
        employee_id = simple_employee['employee_id']
        if employee_id not in simple_employees:
            simple_employees[employee_id] = simple_employee
    cache.set('simple_employees', simple_employees, 60 * 60)


@shared_task(retry_kwargs={'max_retries': 3})
def send_no_sign_signature():
    querysets = Signature.objects.filter(status='', signed_time__isnull=True)
    for lazy_queryset in list(querysets):
        order_id = str(lazy_queryset.order.id)
        signer = lazy_queryset.signer
        domain = settings.SITE_ADDRESS
        link = domain + '?orders=' + order_id
        MessageMixin().send_mail_2_single_user(recipient_employee_id=signer, link=link, category='signing')


@shared_task()
def find_next_signer(current_signer):
    pass


@shared_task
def send_email(receivers):
    pass


@shared_task
def send_notification(receivers):
    pass
