import logging

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions, serializers

from ..models import Order

logger = logging.getLogger(__name__)


def get_all_attendee_without_signer(order_id):
    """
    Collect all employee_id of attendee in the order(excluding signer)

    Args:
        order_id (integer): Order ID

    Returns:
        attendees (list): All attendees in the order (no duplicate)
    """
    attendees = []

    order = Order.objects.get(pk=order_id)
    attendees.append(order.initiator)
    attendees.append(order.assigner)

    if 'contactor' in order.developers:
        attendees.append(order.developers['contactor'])
    if 'member' in order.developers:
        attendees.extend(order.developers['member'])

    return set(attendees)


def get_all_attendee_with_signer(order_id):
    """
    Collect all employee_id of attendee and in the order(including signer)

    Args:
        order_id (integer): Order ID

    Returns:
        attendees (list): All attendees in the order (no duplicate)
    """
    attendees = []

    order = Order.objects.get(pk=order_id)
    attendees.append(order.initiator)
    attendees.append(order.assigner)

    if 'contactor' in order.developers:
        attendees.append(order.developers['contactor'])
    if 'member' in order.developers:
        attendees.extend(order.developers['member'])

    attendees.extend(
        list(order.signature_set.values_list('signer', flat=True))
    )

    return set(attendees)


class OrderPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update']:
            attendees = get_all_attendee_without_signer(order_id=obj.id)
            if request.user.username not in attendees:
                return False
        return True


class DocumentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            if 'order' not in request.data:
                raise serializers.ValidationError({'order': 'This field is required.'})
            try:
                order = Order.objects.get(pk=request.data['order'])
            except ObjectDoesNotExist as err:
                logger.warn(err)
                raise serializers.ValidationError({'order': 'There is no such order'})
            if request.user.username != order.initiator:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        attendee = get_all_attendee_without_signer(obj.order.id)
        if view.action in ['update', 'partial_update', 'destroy'] and request.user.username in attendee:
            return True
        return False


class SchedulePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            if 'order' not in request.data:
                raise serializers.ValidationError({'order': 'This field is required.'})
            try:
                order = Order.objects.get(pk=request.data['order'])
            except ObjectDoesNotExist as err:
                logger.warn(err)
                raise serializers.ValidationError({'order': 'There is no such order'})
            if request.user.username != order.assigner:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy'] and request.user.username != obj.order.assigner:
            return False
        return True


class ProgressPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            if 'order' not in request.data:
                raise serializers.ValidationError({'order': 'This field is required.'})
            try:
                order = Order.objects.get(pk=request.data['order'])
            except ObjectDoesNotExist as err:
                logger.warn(err)
                raise serializers.ValidationError({'order': 'There is no such order'})
            developers_list = []
            if 'contactor' in order.developers:
                developers_list.append(order.developers['contactor'])
            if 'member' in order.developers:
                developers_list.extend(order.developers['member'])
            if request.user.username not in set(developers_list):
                return False
        return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update', 'destroy']:
            order = obj.order
            developers_list = []
            if 'contactor' in order.developers:
                developers_list.append(order.developers['contactor'])
            if 'member' in order.developers:
                developers_list.extend(order.developers['member'])
            if request.user.username not in set(developers_list):
                return False
        return True


class NotificationPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update'] and request.user.username != obj.recipient:
            return False
        return True


class SignaturePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update'] and request.user.username != obj.signer:
            return False
        return True


class CommentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            if 'order' not in request.data:
                raise serializers.ValidationError({'order': 'This field is required.'})
            try:
                order = Order.objects.get(pk=request.data['order'])
            except ObjectDoesNotExist as err:
                logger.warn(err)
                raise serializers.ValidationError({'order': 'There is no such order'})
            attendees = get_all_attendee_with_signer(order_id=order.id)
            if request.user.username not in attendees:
                return False
        return True
