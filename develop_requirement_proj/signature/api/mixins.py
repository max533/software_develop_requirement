import logging

from develop_requirement_proj.employee.models import Employee
from develop_requirement_proj.utils.exceptions import (
    Conflict, ServiceUnavailable,
)
from develop_requirement_proj.utils.mixins import QueryDataMixin

from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import Max

from ..models import Notification, Order
from .serializers import (
    AccountSimpleSerializer, EmployeeSimpleSerializer, ProjectSimpleSerializer,
)

logger = logging.getLogger(__name__)


class CacheMixin(QueryDataMixin):
    def fetch_simple_employees_from_cache(self):
        simple_employees = cache.get('simple_employees')
        if simple_employees is None:
            instance = Employee.objects.using('hr').all().values()
            serializer = EmployeeSimpleSerializer(instance, many=True)
            simple_employees = {}
            for simple_employee in serializer.data:
                employee_id = simple_employee['employee_id']
                if employee_id not in simple_employees:
                    simple_employees[employee_id] = simple_employee
            cache.set('simple_employees', simple_employees, 60 * 60)
        return simple_employees

    def fetch_simple_accounts_from_cache(self):
        simple_accounts = cache.get('simple_accounts', None)
        if simple_accounts is None:
            simple_accounts = {}
            try:
                accounts = self.get_account_via_search()
            except Exception as err:
                logger.error(err)
                raise ServiceUnavailable

            serializer = AccountSimpleSerializer(accounts, many=True)

            for simple_account in serializer.data:
                account_id = simple_account['id']
                if account_id not in simple_accounts:
                    simple_accounts[account_id] = simple_account
            cache.set('simple_accounts', simple_accounts, 60 * 60)
        return simple_accounts

    def fetch_simple_projects_from_cache(self):
        simple_projects = cache.get('simple_projects', None)
        if simple_projects is None:
            simple_projects = {}
            try:
                projects = self.get_project_via_search()
            except Exception as err:
                logger.error(err)
                raise ServiceUnavailable

            serializer = ProjectSimpleSerializer(projects, many=True)
            for simple_project in serializer.data:
                project_id = simple_project['id']
                if project_id not in simple_projects:
                    simple_projects[project_id] = simple_project
            cache.set('simple_projects', simple_projects, 60 * 60)
        return simple_projects


class SignatureMixin(QueryDataMixin):

    def calculate_signature_flag(self, order_id, signature_phase):
        """
        1. Check initiator/assigner job position reach function head leader. (Rule 1)
        2. Check whether signature stage is finished or not. (Rule 2)
            Finished condition:
                (1) There are no any signature in signature_phase.
                (2) The last signature's signer reach function head leader.
                    and last signature's status is "Approve".
                (3) The last signature's signer didn't reach function head leader.
        """
        if signature_phase not in ['P1', 'P4']:
            return None, None

        order = Order.objects.get(pk=order_id)

        # Rule 1
        if signature_phase in 'P1':
            result = self.is_position_higher_function_head(order.initiator)
            if result:
                skip_signature_flag, create_new_signature_flag = True, False
                return skip_signature_flag
        elif signature_phase in 'P4':
            result = self.is_position_higher_function_head(order.assigner)
            if result:
                skip_signature_flag, create_new_signature_flag = True, False
                return skip_signature_flag
        # Rule 2
        if signature_phase in 'P1':
            role_group = 'initiator'
        elif signature_phase in 'P4':
            role_group = 'assigner'

        # Check whether next phase signautre exist or not
        max_sequence = order.signature_set.filter(role_group=role_group).aggregate(Max('sequence'))['sequence__max']
        if max_sequence is None:
            skip_signature_flag, create_new_signature_flag = False, True
            return skip_signature_flag, create_new_signature_flag

        # Check next phase latest signature's status and singer identity
        last_signature = order.signature_set.get(sequence=max_sequence)
        if last_signature.status == 'Approve':
            result = self.is_position_higher_function_head(last_signature.signer)
            if result:
                skip_signature_flag, create_new_signature_flag = True, False
            else:
                skip_signature_flag, create_new_signature_flag = False, True
        elif last_signature.status == 'Return':
            skip_signature_flag, create_new_signature_flag = False, True
        elif last_signature.status == '':
            skip_signature_flag, create_new_signature_flag = False, False
        elif last_signature.status == 'Close':
            warn_message = "This is a conflict operation."
            logger.warning(warn_message)
            raise Conflict
        else:
            warn_message = "This is a wrong operation."
            logger.warning(warn_message)
            raise Conflict
        return skip_signature_flag, create_new_signature_flag

    def is_position_higher_function_head(self, employee_id):
        """
        Check employee identity whether is position higher than function head or not
        Return True  -> It present that employee identity is higher than function head
        Return False -> It present that employee identity is equal/below than function head
        """

        self_department_id = Employee.objects.using('hr').get(employee_id=employee_id).department_id

        zero_count = self.count_zero_occurrence_times(self_department_id)

        return True if zero_count > 4 else False

    def count_zero_occurrence_times(self, department_id):
        """ count zero number occurrence times in department id """
        count = 0
        for char in department_id[::-1]:
            if char == '0':
                count += 1
            elif char != '0':
                break
        return count

    def find_next_signer(self, order_id, signer):
        """ Find next signer until the signer isn't equal next_signer """
        # Find next Singer
        signer_department_id = Employee.objects.using('hr').get(employee_id__iexact=signer).department_id
        try:
            departments = self.get_department_via_query(department_id=signer_department_id)
        except Exception as err:
            logger.warning(err)
            raise ServiceUnavailable

        if signer_department_id in departments:
            next_signer = departments[signer_department_id].get('dm', None)
        # If signer is equal to next_signer
        count = self.count_zero_occurrence_times(signer_department_id)
        next_signer_department_id = signer_department_id
        while (signer == next_signer and count < 5):
            non_zero_part = len(signer_department_id) - count - 1
            next_signer_department_id = signer_department_id[:non_zero_part] + '0' * (count + 1)

            try:
                departments = self.get_department_via_query(department_id=next_signer_department_id)
            except Exception as err:
                logger.warning(err)
                raise ServiceUnavailable

            if next_signer_department_id in departments:
                next_signer = departments[next_signer_department_id].get('dm', None)
            count += 1
        return next_signer, next_signer_department_id


class MessageMixin:
    def send_mail_2_all(self, order_id, link, category):
        """ Send email to all user """
        if category == 'complete':
            status = 'complete'
        elif category == 'close':
            status = 'closed'

        # Collect all member mail in recipient_list
        order = Order.objects.get(pk=order_id)
        signer_id_list = list(order.signature_set.order_by(
            'signer').distinct('signer').values_list('signer', flat=True))
        signer_mail_list = list(Employee.objects.using('hr').filter(
            employee_id__in=signer_id_list).values_list('mail', flat=True))

        developers = order.developers
        developer_list = []
        if 'contactor' in developers:
            developer_list.append(developers['contactor'])
        if 'member' in developers:
            developer_list.extend(developers['member'])
        developer_mail_list = list(Employee.objects.using('hr').filter(
            employee_id__in=developer_list).values_list('mail', flat=True))

        recipient_list = [
            Employee.objects.using('hr').get(employee_id=order.assigner).mail,
            Employee.objects.using('hr').get(employee_id=order.initiator).mail,
        ]
        recipient_list.extend(
            [mail for mail in signer_mail_list if mail not in recipient_list]
        )
        recipient_list.extend(
            [mail for mail in developer_mail_list if mail not in recipient_list]
        )

        email_subject = f"<{category.title()}> There is a software development {status} order"
        email_message = (
            "Dear all,\n" +
            "\n" +
            f"There is a software development {status} order.\n" +
            "You can click below link to check the order detail.\n" +
            f"{link} \n" +
            "\n" +
            "Don't reply this mail as it is automatically sent by the system.\n" +
            "If you have any question, welcome to contact DQMS Team.\n" +
            "\n" +
            "Best Regard\n" +
            "DQMS Software Development Requirement System Service <dqms_service@wistron.com>"
        )
        sender = ""
        send_mail(email_subject, email_message, sender, recipient_list)

    def send_mail_2_single_user(self, recipient_employee_id, link, category):
        """ Send email to specific user """
        if category == 'confirm':
            status, action = 'pending', 'response'
        elif category == 'signing':
            status, action = 'pending', 'signing'
        elif category == 'return':
            status, action = 'return', 'response'
        elif category == 'reschedule':
            status, action = 'return', 'reschedule'
        elif category == 'schedule':
            status, action = 'pending', 'schedule'

        recipient_name = Employee.objects.using('hr').get(employee_id=recipient_employee_id).english_name

        recipient_list = [Employee.objects.using('hr').get(employee_id=recipient_employee_id).mail]
        email_subject = f"<{category.title()}> There is a software development order waiting your {action}"
        email_message = (
            f"Dear {recipient_name},\n" +
            "\n" +
            f"There is a software development {status} order that is waiting for your {action}.\n" +
            "You can click below link to check the order detail.\n" +
            f"{link} \n"
            "\n" +
            "Don't reply this mail as it is automatically sent by the system.\n" +
            "If you have any question, welcome to contact DQMS Team.\n" +
            "\n" +
            "Best Regard\n" +
            "DQMS Software Development Requirement System Service <dqms_service@wistron.com>"
        )
        sender = ""
        send_mail(email_subject, email_message, sender, recipient_list)

    def send_mail_2_multiple_user(self, recipient_employee_id_list, link, category):
        """ Send email to specific user """
        recipient_employee_id_list = list(set(recipient_employee_id_list))

        if category == 'confirm':
            status, action = 'pending', 'response'
        elif category == 'signing':
            status, action = 'pending', 'signing'
        elif category == 'return':
            status, action = 'return', 'response'
        elif category == 'reschedule':
            status, action = 'return', 'reschedule'
        elif category == 'schedule':
            status, action = 'pending', 'schedule'

        recipient_list = list(Employee.objects.using('hr').filter(
            employee_id__in=recipient_employee_id_list).values_list('mail', flat=True)
        )
        email_subject = f"<{category.title()}> There is a software development order waiting your {action}"
        email_message = (
            "Dear all,\n" +
            "\n" +
            f"There is a software development {status} order that is waiting for your {action}.\n" +
            "You can click below link to check the order detail.\n" +
            f"{link} \n"
            "\n" +
            "Don't reply this mail as it is automatically sent by the system.\n" +
            "If you have any question, welcome to contact DQMS Team.\n" +
            "\n" +
            "Best Regard\n" +
            "DQMS Software Development Requirement System Service <dqms_service@wistron.com>"
        )
        sender = ""
        send_mail(email_subject, email_message, sender, recipient_list)

    def send_notification(self, order_id, link, category, actor, verb, action_object='', target=''):
        """ Send notification for all order attendant"""
        # Find all recipient
        order = Order.objects.get(pk=order_id)
        signer_id_list = list(order.signature_set.order_by('signer').distinct(
            'signer').values_list('signer', flat=True))

        developer_list = []
        if 'contactor' in order.developers:
            developer_list.append(order.developers['contactor'])
        if 'member' in order.developers:
            developer_list.extend(order.developers['member'])

        recipient_list = [
            Employee.objects.using('hr').get(employee_id=order.assigner).employee_id,
            Employee.objects.using('hr').get(employee_id=order.initiator).employee_id,
        ]
        recipient_list.extend(developer_list)
        recipient_list.extend(signer_id_list)

        objs = []
        for recipient in set(recipient_list):
            data = {
                "link": link,
                "category": category,
                "recipient": recipient,
                "actor": actor,
                "verb": verb,
                "action_object": action_object,
                "target": target,
            }
            objs.append(Notification(**data))
        Notification.objects.bulk_create(objs)
