from celery import shared_task


@shared_task()
def update_simple_accounts_cache():
    pass


@shared_task()
def update_simple_projects_cache():
    pass


@shared_task()
def update_simple_employees_cache():
    pass


@shared_task()
def update_department_categorys_cache():
    pass


@shared_task()
def find_next_signer(current_signer):
    pass


@shared_task
def send_email(receivers):
    pass


@shared_task
def send_notification(receivers):
    pass
