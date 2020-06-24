import json

from celery import shared_task

from django.forms.models import model_to_dict

from .models import History, Order, OrderTracker


@shared_task
def save_order_tarcker(order_id):
    order = Order.objects.get(order_id)
    order_dict = model_to_dict(order)
    del order_dict['parent']
    order_dict['order'] = order
    OrderTracker.objects.save(**order_dict)


@shared_task
def save_order_history(order_id, update_content):
    comment = {
        'last_order': '',
        'update_content': update_content
    }

    try:
        last_order = OrderTracker.objects.filter(order=order_id).latest('created_time')
    except:
        last_order = None

    if last_order is not None:
        comment['last_order'] = model_to_dict(OrderTracker)

    history = {
        'editor': 'system',
        'comment': json.dumps(comment),
        'order': Order.objects.get(pk=order_id)
    }

    History.objects.create(**history)


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
