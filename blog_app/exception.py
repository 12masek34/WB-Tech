from rest_framework.exceptions import APIException as DRFAPIException


class APIException(DRFAPIException):
    status_code = 400
    subscribe_to_self = 'Do you want to subscribe to yourself.'
    readed_parameter = 'Parameter "readed" must be true on false.'
