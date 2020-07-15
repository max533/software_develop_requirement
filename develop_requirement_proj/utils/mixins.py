import logging

import requests
from develop_requirement_proj.employee.models import Employee
from develop_requirement_proj.signature.models import Notification, Order

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Max

from .exceptions import Conflict, ServiceUnavailable

logger = logging.getLogger(__name__)


class QueryDataMixin:
    """
    Use 3rd-party api to get employee, department, account, project information.
    """
    def get_employee_via_query(self, employee_id):
        """
        Get employee info via employee_id from TeamRoster 2.0 System.
        employee_id : str / list
        """
        uri = settings.TEAMROSTER_URI + 'api/query/profile'
        if type(employee_id) == str:
            e_id = employee_id
        elif type(employee_id) == list:
            e_id = ','.join(employee_id)
        else:
            e_id = ''
        params = {
            'emplid': e_id,
            'avatar': True,
            'dept_category': True,
            'dept_role': True,
            'proj_all': True,
            'proj_all_role': True
        }

        headers = {'X-Authorization': settings.TEAMROSTER_TOKEN}
        r = requests.get(uri, params=params, headers=headers, timeout=3)

        if r.status_code != 200:
            error_message = (
                f"Status Code : {r.status_code}. Error Message : " +
                f"{r.text}. It can't get user information by <{r.url}>."
            )
            logger.warn(error_message)
            return False, None

        return True, r.json()

    def get_account_via_search(self, **params):
        """
        Get account info via search from Account Project System.
        """
        uri = settings.ACCOUNT_PROJECT_URI + 'api/search/accounts'
        headers = {'X-Authorization': settings.ACCOUNT_PROJECT_TOKEN}
        r = requests.get(uri, params=params, headers=headers, timeout=3)

        if r.status_code != 200:
            error_message = (
                f"Status Code : {r.status_code}. Error Message : " +
                f"{r.text}. It can't get account info by <{r.url}>."
            )
            logger.warn(error_message)
            return False, None

        return True, r.json()

    def get_project_via_search(self, **params):
        """
        Get Project info via search from Account Project 2.0 System.
        """
        uri = settings.ACCOUNT_PROJECT_URI + 'api/search/projects'
        headers = {'X-Authorization': settings.ACCOUNT_PROJECT_TOKEN}
        r = requests.get(uri, params=params, headers=headers, timeout=3)
        if r.status_code != 200:
            error_message = (
                f"Status Code : {r.status_code}. Error Message : " +
                f"{r.text}. It can't get project info by <{r.url}>."
            )
            logger.warn(error_message)
            return False, None

        return True, r.json()

    def get_option_value(self, **params):
        """
        Get options value from TeamRoster 2.0 System and Account Project System.
        """
        field = params.get('field', None)
        teamroster_options = [
            'dept_category',
            'dept_role'
        ]
        account_project_options = [
            'business_unit',
            'project_type',
            'project_status',
            'product_line',
            'business_model'
        ]
        # Choose the uri what will send request
        if field in teamroster_options:
            uri = settings.TEAMROSTER_URI + 'api/get/options'
            headers = {'X-Authorization': settings.TEAMROSTER_TOKEN}
        elif field in account_project_options:
            uri = settings.ACCOUNT_PROJECT_URI + 'api/get/options'
            headers = {'X-Authorization': settings.ACCOUNT_PROJECT_TOKEN}
        else:
            return False, None

        r = requests.get(uri, params=params, headers=headers, timeout=3)

        if r.status_code != 200:
            error_message = (
                f"Status Code : {r.status_code}. Error Message : " +
                f"{r.text}. It can't get options info by <{r.url}>."
            )
            logger.warn(error_message)
            return False, None

        return True, r.json()

    def get_department_via_search(self, *args, **kwargs):
        """
        Get department value from TeamRoster 2.0 System

        bg (str) : bussiness group Ex/ 'EBG'

        fn_lvl1 (str) : funnction Ex/ 'QT'

        fn_lvl2 (str) : sub_function Ex/ 'DQMS'
        """

        uri = settings.TEAMROSTER_URI + 'api/search/department'
        headers = {'X-Authorization': settings.TEAMROSTER_TOKEN}

        r = requests.get(uri, params=kwargs, headers=headers, timeout=3)

        if r.status_code != 200:
            error_message = (
                f"Status Code : {r.status_code}. Error Message : " +
                f"{r.text}. It can't get department info by <{r.url}>."
            )
            logger.warn(error_message)

            return False, None

        return True, r.json()

    def get_department_via_query(self, department_id=None, *args, **kwargs):
        """
        Get department information from TeamRoster 2.0 System

        department_id (str) Ex/ 'Z8502456'

        args (list) :  department_id Ex/ ['Z10612805', 'A123456']

        kwargs (dict) : other params. if no kwargs will uese deault_params.
        """
        params = dict()
        default_params = {
            'category': True,
            'dm': True,
            'proj_all': True,
            'proj_own': True,
            'proj_support': True,
            'acct_all': True,
            'acct_own': True,
            'acct_support': True,
        }
        # Add department id to params
        if department_id:
            params['deptid'] = department_id
        elif args:
            params['deptid'] = ','.join(args)
        else:
            params['deptid'] = ''
        # Add other information to params
        if kwargs:
            params.update(kwargs)
        else:
            params.update(default_params)

        uri = settings.TEAMROSTER_URI + 'api/query/department'
        headers = {'X-Authorization': settings.TEAMROSTER_TOKEN}
        r = requests.get(uri, params=params, headers=headers, timeout=3)

        if r.status_code != 200:
            error_message = (
                f"Status Code : {r.status_code}. Error Message : " +
                f"{r.text}. It can't get department info by <{r.url}>."
            )
            logger.warn(error_message)
            return False, None

        return True, r.json()

    def get_project_via_teamroaster_project_serach(self, **kwargs):
        """
        Get project information from TeamRoster 2.0 System

        kwargs (dict) : other params. if no kwargs will uese deault_params.

        kwarg key can contain `bg`, `fn_lvl1`, `fnlvl2`, `projid`, `lead`,

        `lead_dept`, `supv`, `supv_dept_list`, `member`, `member_dept_list`
        """
        params = {}
        if kwargs:
            params = kwargs

        uri = settings.TEAMROSTER_URI + 'api/search/project'
        headers = {'X-Authorization': settings.TEAMROSTER_TOKEN}

        r = requests.get(uri, params=params, headers=headers, timeout=3)

        if r.status_code != 200:
            error_message = (
                f"Status Code : {r.status_code}. Error Message : " +
                f"{r.text}. It can't get department info by <{r.url}>."
            )
            logger.warn(error_message)
            return False, None

        return True, r.json()

    def get_project_via_query(self, project_id, field=None):
        """
        Get project info via project_id from Account Project System.
        project_id : str / list
        """
        uri = settings.ACCOUNT_PROJECT_URI + 'api/query/projects'
        if type(project_id) == str:
            p_id = project_id
        elif type(project_id) == list:
            p_id = ','.join(list(map(str, project_id)))
        else:
            p_id = ''

        params = {'id': p_id}

        if field is None:
            params.update(
                {
                    'type': True,
                    'name': True,
                    'status': True,
                    'wistron_name': True,
                    'customer_name': True,
                    'wistron_code': True,
                    'plm_code_1': True,
                    'plm_code_2': True,
                    'product_line': True,
                    'business_model': True,
                    'acct': True,
                    'deleted_at': True,
                }
            )
        else:
            params.update(field)

        headers = {'X-Authorization': settings.ACCOUNT_PROJECT_TOKEN}
        r = requests.get(uri, params=params, headers=headers, timeout=3)

        if r.status_code != 200:
            error_message = (
                f"Status Code : {r.status_code}. Error Message : " +
                f"{r.text}. It can't get project info by Account Project System."
            )
            logger.warn(error_message)
            return False, None

        return True, r.json()

    def get_profile_via_query(self, employee_id, field=None):
        """
        Get profile information from TeamRoster 2.0 System
        employee_id : str
        """
        uri = settings.TEAMROSTER_URI + 'api/query/profile'
        if type(employee_id) == str:
            emplid = employee_id
        elif type(employee_id) == list:
            emplid = ','.join(list(map(str, employee_id)))
        else:
            emplid = ''

        params = {'emplid': emplid}

        if field is None:
            params.update(
                {
                    'wee': True,
                    'avatar': True,
                    'dept_category': True,
                    'dept_role': True,
                    'dept_proxy': True,
                    'proj_all': True,
                    'proj_all_role': True,
                    'acct_all': True,
                    'proj_own': True,
                    'proj_own_role': True,
                    'acct_own': True,
                    'proj_support': True,
                    'proj_support_role': True,
                    'acct_support': True
                }
            )
        else:
            params.update(field)

        headers = {'X-Authorization': settings.TEAMROSTER_TOKEN}
        r = requests.get(uri, params=params, headers=headers, timeout=3)

        if r.status_code != 200:
            error_message = (
                f"Status Code : {r.status_code}. Error Message : " +
                f"{r.text}. It can't get project info by Account Project System."
            )
            logger.warn(error_message)
            return False, None

        return True, r.json()


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
            result = self.check_identity(order.initiator)
            if result:
                skip_signature_flag, create_new_signaure_flag = True, False
                return skip_signature_flag
        elif signature_phase in 'P4':
            result = self.check_identity(order.assigner)
            if result:
                skip_signature_flag, create_new_signaure_flag = True, False
                return skip_signature_flag
        # Rule 2
        if signature_phase in 'P1':
            role_group = 'initiator'
        elif signature_phase in 'P4':
            role_group = 'assigner'

        # Check whether next phase signautre exist or not
        max_sequence = order.signature_set.filter(role_group=role_group).aggregate(Max('sequence'))['sequence__max']
        if max_sequence is None:
            skip_signature_flag, create_new_signaure_flag = False, True
            return skip_signature_flag, create_new_signaure_flag

        # Check next phase latest signature's status and singer identity
        last_signature = order.signature_set.get(sequence=max_sequence)
        if last_signature.status == 'Approve':
            result = self.check_identity(last_signature.signer)
            if result:
                skip_signature_flag, create_new_signaure_flag = True, False
            else:
                skip_signature_flag, create_new_signaure_flag = False, True
        elif last_signature.status == 'Return':
            skip_signature_flag, create_new_signaure_flag = False, True
        elif last_signature.status == '':
            skip_signature_flag, create_new_signaure_flag = False, False
        elif last_signature.status == 'Close':
            warn_message = "This is a conflict operation."
            logger.warning(warn_message)
            raise Conflict
        else:
            warn_message = "This is a wrong operation."
            logger.warning(warn_message)
            raise Conflict
        return skip_signature_flag, create_new_signaure_flag

    def check_identity(self, employee_id):
        """
        Check identity whether reach function head leader or not
        Return True  -> It present that identity is higer/equal than function head leader
        Return False -> It present that identity is below than function head leader
        """
        department_id = Employee.objects.using('hr').get(employee_id=employee_id).department_id

        count = self.count_zero_occurence(department_id)

        status, result = self.get_department_via_query(department_id)
        if not (status and result):
            warn_message = 'TeamRoster 2.0 System is not available'
            logger.warning(warn_message)
            raise ServiceUnavailable

        if department_id in result:
            function_head_employee_id = result[department_id].get('dm', None)

        if count > 4:
            identitiy_flag = True
        elif count == 4 and function_head_employee_id == employee_id:
            identitiy_flag = True
        elif count == 4 and function_head_employee_id != employee_id:
            identitiy_flag = False
        else:
            identitiy_flag = False
        return identitiy_flag

    def count_zero_occurence(self, department_id):
        """ count zero occurence time """
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
        status, result = self.get_department_via_query(department_id=signer_department_id)
        if not (status and result):
            warn_message = 'TeamRoster 2.0 System is not available'
            logger.warning(warn_message)
            raise ServiceUnavailable

        if signer_department_id in result:
            next_signer = result[signer_department_id].get('dm', None)
        # If assigner is equal to next_signer
        count = self.count_zero_occurence(signer_department_id)
        next_signer_department_id = signer_department_id
        while (signer == next_signer and count < 5):
            non_zero_part = len(signer_department_id) - count - 1
            print(non_zero_part)
            print(next_signer_department_id)
            next_signer_department_id = signer_department_id[:non_zero_part] + '0' * (count + 1)
            status, result = self.get_department_via_query(department_id=next_signer_department_id)
            if not (status and result):
                warn_message = 'TeamRoster 2.0 System is not available'
                logger.warning(warn_message)
                raise ServiceUnavailable

            print(signer, next_signer)
            if next_signer_department_id in result:
                next_signer = result[next_signer_department_id].get('dm', None)
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
            f"There is a software developement {status} order.\n" +
            "You can click below link to check the order detail.\n" +
            f"{link} \n" +
            "\n" +
            "Don't reply this mail as it is automatically sent by the system.\n" +
            "If you have any question, welcome to contact DQMS Team.\n" +
            "\n" +
            "Best Regard\n" +
            "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
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
            f"There is a software developement {status} order that is waiting for your {action}.\n" +
            "You can click below link to check the order detail.\n" +
            f"{link} \n"
            "\n" +
            "Don't reply this mail as it is automatically sent by the system.\n" +
            "If you have any question, welcome to contact DQMS Team.\n" +
            "\n" +
            "Best Regard\n" +
            "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
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
            employee_id__in=recipient_employee_id_list).values_list('mail'))
        email_subject = f"<{category.title()}> There is a software development order waiting your {action}"
        email_message = (
            "Dear all,\n" +
            "\n" +
            f"There is a software developement {status} order that is waiting for your {action}.\n" +
            "You can click below link to check the order detail.\n" +
            f"{link} \n"
            "\n" +
            "Don't reply this mail as it is automatically sent by the system.\n" +
            "If you have any question, welcome to contact DQMS Team.\n" +
            "\n" +
            "Best Regard\n" +
            "DQMS Software Developement Requirement System Administrator <dqms_admin@wistron.com>"
        )
        sender = ""
        send_mail(email_subject, email_message, sender, recipient_list)

    def send_notification(self, order_id, link, category, actor, verb, action_object='', target=''):
        """ Send notification for all order attendent"""
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
