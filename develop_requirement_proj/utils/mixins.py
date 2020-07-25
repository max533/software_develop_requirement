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
    def get_account_via_search(self, *args, **kwargs):
        """
        Get account info via search from Account Project 2.0 System.

        `Args`:
        - kwargs ([dict], optional) : other params.
        - kwarg key can contain `name`, `code`, `bu`, `sort`, `order`, `offset`, `limit`.

        `Raises`:
        - requests.HTTPError: If the http status code of the response is not 200, it will be raised.
        - Other error will handle by `requests` library.

        `Returns`:
        - accounts [list(dict)]: This is the list that contain account dictionary

        `Usage Note`:
        - Please use the function with try catch.
        """
        uri = settings.ACCOUNT_PROJECT_URI + 'api/search/accounts'
        headers = {'X-Authorization': settings.ACCOUNT_PROJECT_TOKEN}

        try:
            r = requests.get(uri, params=kwargs, headers=headers, timeout=3)
        except Exception as err:
            logger.warn(err)
            raise

        if r.status_code != 200:
            message = f"Status Code : {r.status_code}. It can't get account info by <{r.url}>."
            logger.warn(message)
            raise requests.HTTPError

        try:
            accounts = r.json()
        except Exception as err:
            logger.warn(err)
            raise

        return accounts

    def get_project_via_search(self, *args, **kwargs):
        """
        Get Project info via search from Account Project 2.0 System.

        `Args`:
        - kwargs ([dict], optional) : other params.
        - kwarg key can contain `acct_id`, `acct_code`, `acct_bu`, `wistron_name`, `customer_name`,
        `wistron_code`, `plm_code`, `plm_code_1`, `plm_code_2`, `type`, `status`, `business_model`,
        `product_line`, `sort`, `order`, `offset`, `limit`.

        `Raises`:
        - requests.HTTPError: If the http status code of the response is not 200, it will be raised.
        - Other error will handle by `requests` library.

        `Returns`:
        - projects [list(dict)]: This is the list that contain project dictionary

        `Usage Note`:
        - Please use the function with try catch.
        """
        uri = settings.ACCOUNT_PROJECT_URI + 'api/search/projects'
        headers = {'X-Authorization': settings.ACCOUNT_PROJECT_TOKEN}

        try:
            r = requests.get(uri, params=kwargs, headers=headers, timeout=3)
        except Exception as err:
            logger.warn(err)
            raise

        if r.status_code != 200:
            message = f"Status Code : {r.status_code}. It can't get project info by <{r.url}>."
            logger.warn(message)
            raise requests.HTTPError

        try:
            projects = r.json()
        except Exception as err:
            logger.warn(err)
            raise

        return projects

    def get_option_value(self, field, *args, **kwargs):
        """
        Get options value from TeamRoster 2.0 System and Account Project System.

        `Args`:
        - kwargs ([dict], optional) : other params.
        - field [str] : the category of query data

        `Raises`:
        - requests.HTTPError: If the http status code of the response is not 200, it will be raised.
        - Other error will handle by `requests` library.

        `Returns`:
        - options [dict]: Constant Value

        `Usage Note`:
        - Please use the function with try catch.
        """
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
        # Choose the which uri will send request
        if field in teamroster_options:
            uri = settings.TEAMROSTER_URI + 'api/get/options'
            headers = {'X-Authorization': settings.TEAMROSTER_TOKEN}
        elif field in account_project_options:
            uri = settings.ACCOUNT_PROJECT_URI + 'api/get/options'
            headers = {'X-Authorization': settings.ACCOUNT_PROJECT_TOKEN}
        else:
            logger.warn("There is not correct input with field")
            raise ValueError

        payload = {"field": field}
        try:
            r = requests.get(uri, params=payload, headers=headers, timeout=3)
        except Exception as err:
            logger.warn(err)
            raise

        if r.status_code != 200:
            message = f"Status Code : {r.status_code}. It can't get options info by <{r.url}>."
            logger.warn(message)
            raise requests.HTTPError

        try:
            options = r.json()
        except Exception as err:
            logger.warn(err)
            raise

        return options

    def get_department_via_search(self, *args, **kwargs):
        """
        Get department information from TeamRoster 2.0 System

        `Args`:
        - kwargs ([dict], optional) : other params.
        - kwarg key can contain `bg`, `fn_lvl1`, `fnlvl2`.

        `Raises`:
        - requests.HTTPError: If the http status code of the response is not 200, it will be raised.
        - Other error will handle by `requests` library.

        `Returns`:
        - departments [list(str)]: This is the list that contains department id.
        Key is the department_id and value is department property.

        `Usage Note`:
        - Please use the function with try catch.
        """
        uri = settings.TEAMROSTER_URI + 'api/search/department'
        headers = {'X-Authorization': settings.TEAMROSTER_TOKEN}

        try:
            r = requests.get(uri, params=kwargs, headers=headers, timeout=3)
        except Exception as err:
            logger.warn(err)
            raise

        if r.status_code != 200:
            message = f"Status Code : {r.status_code}. It can't get department info by <{r.url}>."
            logger.warn(message)
            raise requests.HTTPError

        try:
            departments = r.json()
        except Exception as err:
            logger.warn(err)
            raise

        return departments

    def get_project_via_teamroaster_project_serach(self, *args, **kwargs):
        """
        Get project information from TeamRoster 2.0 System.

        `Args`:
        - kwargs ([dict], optional) : other params.
        - kwarg key can contain `bg`, `fn_lvl1`, `fnlvl2`, `projid`, `lead`,
        `lead_dept`, `supv`, `supv_dept_list`, `member`, `member_dept_list`

        `Raises`:
        - requests.HTTPError: If the http status code of the response is not 200, it will be raised.
        - Other error will handle by `requests` library.

        `Returns`:
        - projects [list(dict)]: This is the list that contain project dictionary.
        Key is the department_id and value is department property.

        `Usage Note`:
        - Please use the function with try catch.
        """
        uri = settings.TEAMROSTER_URI + 'api/search/project'
        headers = {'X-Authorization': settings.TEAMROSTER_TOKEN}

        try:
            r = requests.get(uri, params=kwargs, headers=headers, timeout=3)
        except Exception as err:
            logger.warn(err)
            raise

        if r.status_code != 200:
            message = f"Status Code : {r.status_code}. It can't get project info by <{r.url}>."
            logger.warn(message)
            raise requests.HTTPError

        try:
            projects = r.json()
        except Exception as err:
            logger.warn(err)
            raise

        return projects

    def get_department_via_query(self, department_id=None, department_list=None, field=None):
        """
        Get department information from TeamRoster 2.0 System.

        `Args`:
        - department_id ([str], optional): department id. Defaults to None.`
        - department_list ([list], optional): the list of department id. Defaults to None.
        - field ([dict], optional) : other params. if no kwargs will uese deault_params.
        The value of department_id nor department_list could not both be None.

        `Raises`:
        - requests.HTTPError: If the http status code of the response is not 200, it will be raised.
        - ValueError : If the value of department_id nor department_list both be None, it will be raised.
        - Other error will handle by `requests library.

        `Returns`:
        - departments [dict(dict)]: This is the dictionary that contain department dictionary.
        Key is the department_id and value is department property.

        `Usage Note`:
        - Please use the function with try catch.
        """
        payload = dict()
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
        # Add department id to payload
        if department_id is not None:
            payload['deptid'] = department_id
        elif department_list is not None:
            payload['deptid'] = ','.join(list(map(str, department_list)))
        elif department_id is None and department_list is None:
            raise ValueError('This is not reasonable input argument')
        # Add other information to payload
        if field is None:
            payload.update(default_params)
        else:
            payload.update(field)

        uri = settings.TEAMROSTER_URI + 'api/query/department'
        headers = {'X-Authorization': settings.TEAMROSTER_TOKEN}

        try:
            r = requests.get(uri, params=payload, headers=headers, timeout=3)
        except Exception as err:
            logger.warn(err)
            raise

        if r.status_code != 200:
            message = f"Status Code : {r.status_code}. It can't get department info by <{r.url}>."
            logger.warn(message)
            raise requests.HTTPError

        try:
            departments = r.json()
        except Exception as err:
            logger.warn(err)
            raise

        return departments

    def get_project_via_query(self, project_id=None, project_list=None, field=None):
        """
        Get project information from  Account Project 2.0 System

        `Args`:
        - project_id ([str], optional): Project id. Defaults to None.
        - project_list ([list(str)], optional): Project id list. Defaults to None.
        - field ([type], optional): Query data field. Defaults to None. It will use default_param.
        - The value of project_id nor project_list could not both be None.

        `Raises`:
        - requests.HTTPError: If the http status code of the response is not 200, it will be raised.
        - ValueError : If the value of department_id nor department_list both be None, it will be raised.
        - Other error will handle by `requests library.

        `Returns`:
        - projects [list(dict)]: This is the list that contains project dictionary.

        `Usage Note`:
        - Please use the function with try catch.
        """
        default_param = {
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
        payload = dict()
        if project_id is not None:
            payload['id'] = project_id
        elif project_list is not None:
            payload['id'] = ','.join(list(map(str, project_list)))
        elif project_id is None and project_list is None:
            raise ValueError('This is not reasonable input argument')

        if field is None:
            payload.update(default_param)
        else:
            payload.update(field)

        uri = settings.ACCOUNT_PROJECT_URI + 'api/query/projects'
        headers = {'X-Authorization': settings.ACCOUNT_PROJECT_TOKEN}
        try:
            r = requests.get(uri, params=payload, headers=headers, timeout=3)
        except Exception as err:
            logger.warn(err)
            raise

        if r.status_code != 200:
            message = f"Status Code : {r.status_code}. It can't get project info by <{r.url}>."
            logger.warn(message)
            raise requests.HTTPError

        try:
            projects = r.json()
        except Exception as err:
            logger.warn(err)
            raise

        return projects

    def get_profile_via_query(self, employee_id=None, employee_list=None, field=None):
        """
        Get profile information from TeamRoster 2.0 System

        `Args`:
        - employee_id ([str], optional): Employee id. Defaults to None.
        - employee_list ([list(str)], optional): Employee id list. Defaults to None.
        - field ([type], optional): Query data field. Defaults to None. It will use default_param.
        - The value of employee_id nor employee_list could not both be None.

        `Raises`:
        - requests.HTTPError: If the http status code of the response is not 200, it will be raised.
        - ValueError : If the value of department_id nor department_list both be None, it will be raised.
        - Other error will handle by `requests library.

        `Returns`:
        - employees [dict(dict)]: This is the dictionary that contains employees dictionary.

        `Usage Note`:
        - Please use the function with try catch.
        """
        default_param = {
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

        payload = dict()

        if employee_id is not None:
            payload['emplid'] = employee_id
        elif employee_list is not None:
            payload['emplid'] = ','.join(list(map(str, employee_list)))
        elif employee_id is None and employee_list is None:
            raise ValueError('This is not reasonable input argument')

        if field is None:
            payload.update(default_param)
        else:
            payload.update(field)

        uri = settings.TEAMROSTER_URI + 'api/query/profile'
        headers = {'X-Authorization': settings.TEAMROSTER_TOKEN}
        try:
            r = requests.get(uri, params=payload, headers=headers, timeout=3)
        except Exception as err:
            logger.warn(err)
            raise

        if r.status_code != 200:
            message = f"Status Code : {r.status_code}. It can't get employee info by <{r.url}>."
            logger.warn(message)
            raise requests.HTTPError

        try:
            employees = r.json()
        except Exception as err:
            logger.warn(err)
            raise

        return employees


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

        try:
            departments = self.get_department_via_query(department_id)
        except Exception as err:
            logger.warning(err)
            raise ServiceUnavailable

        if department_id in departments:
            function_head_employee_id = departments[department_id].get('dm', None)

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
        try:
            departments = self.get_department_via_query(department_id=signer_department_id)
        except Exception as err:
            logger.warning(err)
            raise ServiceUnavailable

        if signer_department_id in departments:
            next_signer = departments[signer_department_id].get('dm', None)
        # If signer is equal to next_signer
        count = self.count_zero_occurence(signer_department_id)
        next_signer_department_id = signer_department_id
        while (signer == next_signer and count < 5):
            non_zero_part = len(signer_department_id) - count - 1
            next_signer_department_id = signer_department_id[:non_zero_part] + '0' * (count + 1)

            try:
                departments = self.get_department_via_query(department_id=signer_department_id)
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
