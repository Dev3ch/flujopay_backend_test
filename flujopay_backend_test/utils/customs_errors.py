from rest_framework.exceptions import APIException


class InternalServerError(APIException):
    status_code = 500
    default_detail = "Algo salió mal, contáctate con el soporte de la web."
    default_code = "internal_server_error"
