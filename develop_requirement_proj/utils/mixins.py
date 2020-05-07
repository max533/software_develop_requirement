import logging

import requests

from django.conf import settings

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
        Get Project info via search from Account Project System.
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
            print(error_message)
            return False, None

        return True, r.json()

    def get_department_via_query(self, department_id=None, *args, **kwargs):
        """
        Get department information from TeamRsoter 2.0 System

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
        Get project information from TeamRsoter 2.0 System

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
