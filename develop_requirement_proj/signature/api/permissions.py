import logging

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions, serializers

from ..models import Order

logger = logging.getLogger(__name__)


class OrderPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update']:
            attendents = self.get_all_attendent_without_signer(order_id=obj.id)
            if request.user.username not in attendents:
                return False
        return True

    def get_all_attendent_without_signer(self, order_id):
        """
        Collect all employee_id of attendent in the order(excluding signer)

        Args:
            order_id (integer): Order ID

        Returns:
            attendents (list): All attendents in the order (no duplicate)
        """
        attendents = []

        order = Order.objects.get(pk=order_id)
        attendents.append(order.initiator)
        attendents.append(order.assigner)

        if 'contactor' in order.developers:
            attendents.append(order.developers['contactor'])
        if 'member' in order.developers:
            attendents.extend(order.developers['member'])

        return set(attendents)


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
        if view.action in ['update', 'partial_update', 'destroy']:
            if request.user.username != obj.order.initiator:
                return False
        return True


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
        if view.action in ['update', 'partial_update', 'destroy']:
            if request.user.username != obj.order.assigner:
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
        if view.action in ['update', 'partial_update']:
            if request.user.username != obj.recipient:
                return False
        return True


class SignaturePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update']:
            if request.user.username != obj.signer:
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
            attendents = self.get_all_attendent_with_signer(order_id=order.id)
            if request.user.username not in attendents:
                return False
        return True

    def get_all_attendent_with_signer(self, order_id):
        """
        Collect all employee_id of attendent and in the order(including signer)

        Args:
            order_id (integer): Order ID

        Returns:
            attendents (list): All attendents in the order (no duplicate)
        """
        attendents = []

        order = Order.objects.get(pk=order_id)
        attendents.append(order.initiator)
        attendents.append(order.assigner)

        if 'contactor' in order.developers:
            attendents.append(order.developers['contactor'])
        if 'member' in order.developers:
            attendents.extend(order.developers['member'])

        attendents.extend(
            list(order.signature_set.values_list('signer', flat=True))
        )

        return set(attendents)
