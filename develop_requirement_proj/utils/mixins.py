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
                f"{r.text}. It can't get user information by TeamRoster 2.0 System."
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
                f"{r.text}. It can't get account info by Account Project System."
            )
            logger.warn(error_message)
            return False, None

        return True, r.json()

    def get_project_via_search(seld, **params):
        """
        Get Project info via search from Account Project System.
        """
        uri = settings.ACCOUNT_PROJECT_URI + 'api/search/projects'
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

    def get_option_value(seld, **params):
        """
        Get options value from TeamRoster 2.0 System and Account Project System.
        """
        field = params.get('field', None)
        teamroster_options = ['dept_category', 'dept_role']
        account_project_options = ['business_unit', 'project_type', 'project_status', 'product_line', 'business_model']
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
                f"{r.text}. It can't get options info by {r.url}."
            )
            logger.warn(error_message)
            return False, None

        return True, r.json()
