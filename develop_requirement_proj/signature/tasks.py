from celery import shared_task
from develop_requirement_proj.utils.mixins import QueryDataMixin

from django.core.cache import cache


@shared_task()
def update_accounts_cache():


@shared_task()
def update_project_cache():


@shared_task()
def update_employees_cache():


@shared_task()
def update_department_categorys_cache()




@shared_task()
def find_next_signer(current_signer):
    pass


@shared_task
def step_into_signature(next_signer, next_order_status, order_id):
    pass


@shared_task
def send_email(receivers):
    pass


@shared_task
def send_notification(receivers):
    pass
