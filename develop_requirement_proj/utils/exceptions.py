from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class Conflict(APIException):
    status_code = 409
    default_detail = (
        'The request could not be completed due to a conflict with the current state of the target resource.'
    )
    default_code = 'conflict'
