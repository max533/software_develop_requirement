import logging

import requests

from django.conf import settings

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

        try:
            field_value = field['field']
        except KeyError as err:
            logger.warn(f"There is not correct input argument. Error Message : {err}")
            raise KeyError

        # Choose the which uri will send request

        if field_value in teamroster_options:
            uri = settings.TEAMROSTER_URI + 'api/get/options'
            headers = {'X-Authorization': settings.TEAMROSTER_TOKEN}
        elif field_value in account_project_options:
            uri = settings.ACCOUNT_PROJECT_URI + 'api/get/options'
            headers = {'X-Authorization': settings.ACCOUNT_PROJECT_TOKEN}
        else:
            logger.warn("There is not correct input with field.")
            raise ValueError

        payload = field

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
        - departments [dict(dict) / empty_list]: This is the dictionary that contain department dictionary.
        Key is the department_id and value is department property.
        If TR2 can't find the data or the query is not valid, it will return empty list.

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
