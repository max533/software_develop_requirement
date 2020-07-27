from celery import chain, shared_task
from celery.schedules import crontab
from develop_requirement_proj.employee.models import Employee

from django.core import cache

from .api.mixins import QueryDataMixin
from .api.serializers import (
    AccountSimpleSerializer, EmployeeSimpleSerializer, ProjectSimpleSerializer,
)

# @shared_task.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         schedule=crontab(minute=0, hour='*'),
#         sig=update_simple_accounts_cache.s(),
#         name='Update simple accounts cache'
#     )

#     sender.add_periodic_task(
#         schedule=crontab(minute=0, hour='*'),
#         sig=update_simple_projects_cache.s(),
#         name='Update simple projects cache'
#     )

#     sender.add_periodic_task(
#         schedule=crontab(minute=0, hour='*'),
#         sig=update_simple_employees_cache.s(),
#         name='Update simple employees cache'
#     )


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def update_simple_accounts_cache(self):
    t1 = fetch_simple_accounts_data.s()
    t2 = store_simple_accounts_data.s()
    chain(t1, t2).delay()


@shared_task(autoretry_for=(Exception,), retry_backoff=True)
def fetch_simple_accounts_data():
    accounts = QueryDataMixin().get_account_via_search()
    return accounts


@shared_task(retry_kwargs={'max_retries': 3})
def store_simple_accounts_data(accounts):
    cache.delete('simple_accounts', None)
    simple_accounts = {}
    serializer = AccountSimpleSerializer(accounts, many=True)
    for simple_account in serializer.data:
        account_id = simple_account['id']
        if account_id not in simple_accounts:
            simple_accounts[account_id] = simple_account
    cache.set('simple_accounts', simple_accounts, 60 * 60)


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def update_simple_projects_cache(self):
    t1 = fetch_simple_projects_data.s()
    t2 = store_simple_projects_data.s()
    chain(t1, t2).delay()


@shared_task(autoretry_for=(Exception,), retry_backoff=True)
def fetch_simple_projects_data(self):
    projects = QueryDataMixin().get_project_via_search()
    return projects


@shared_task(retry_kwargs={'max_retries': 3})
def store_simple_projects_data(projects):
    cache.delete('simple_projects', None)
    simple_projects = {}
    serializer = ProjectSimpleSerializer(projects, many=True)
    for simple_account in serializer.data:
        account_id = simple_account['id']
        if account_id not in simple_projects:
            simple_projects[account_id] = simple_account
    cache.set('simple_projects', simple_projects, 60 * 60)


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


@shared_task()
def find_next_signer(current_signer):
    pass


@shared_task
def send_email(receivers):
    pass


@shared_task
def send_notification(receivers):
    pass
