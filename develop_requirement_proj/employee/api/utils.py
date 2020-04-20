import logging

import requests

from django.conf import settings

logger = logging.getLogger(__name__)


class QueryDataMixin:
    """
    Use 3rd-party api to get employee, customer, project information.
    """
    def get_employee_via_query(self, employee_id):
        """
        Get avatar via employee_id from TeamRoster.
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
            error_message = [
                f"Status Code : {r.status_code}. Error Message : " +
                f"{r.text}. It can't get user information by TeamRoster."
            ]
            logger.warn(error_message)
            return False, None

        return True, r.json()
