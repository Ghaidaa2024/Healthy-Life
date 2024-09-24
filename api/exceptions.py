from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler

import logging
logger = logging.getLogger('dwLogger')


class ApplicationError(Exception):
    """Base Exception, extend this

    """
    message = 'Error'
    status = 500
    errorCode = None
    extra = {}
    detail = None
    def __init__(self):
        self.extra = {"detail": self.detail}
        if self.errorCode is not None:
            self.extra['errorCode'] = self.errorCode
        #logger.debug(str(self.extra))
            

    

class InputException(ApplicationError):
    def __init__(self, detail='Missing Parameters', errorCode=None):
        self.message = 'Invalid Input'
        self.status = 400
        self.errorCode = errorCode
        self.detail = detail
        super().__init__()
        
        
class InternalException(ApplicationError):
    def __init__(self, detail='Internal Server Error', errorCode=None):
        self.message = 'Internal Exception'
        self.status = 500
        self.errorCode = errorCode
        self.detail = detail
        super().__init__()

class PMSException(ApplicationError):
    def __init__(self, detail='Upstream Server Error', errorCode=None):
        self.message = 'Upstream Server Error'
        self.status = 503
        self.errorCode = errorCode
        self.detail = detail
        super().__init__()

class NotFoundException(ApplicationError):
    def __init__(self, detail='Not Found', errorCode=None):
        self.message = 'Not Found'
        self.status = 404
        self.errorCode = errorCode
        self.detail = detail
        super().__init__()

class AuthenticationException(ApplicationError):
    def __init__(self, detail='Invalid Credentials', errorCode=None):
        self.message = 'Invalid Credentials'
        self.status = 401
        self.errorCode = errorCode
        self.detail = detail
        super().__init__()


class LicenseException(ApplicationError):
    def __init__(self, detail='License Error', errorCode=None):
        self.message = 'License Error'
        self.status = 403
        self.errorCode = errorCode
        self.detail = detail
        super().__init__()        


        
def dw_exception_handler(exc, ctx):
    """
    {
        "message": "Error message",
        "extra": {}
    }
    """
    
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
        
    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        if isinstance(exc, ApplicationError):
            data = {"message": exc.message, "extra": exc.extra}
            return Response(data, status=exc.status)

        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {"detail": response.data}

    if isinstance(exc, exceptions.ValidationError):
        response.data["message"] = "Validation error"
        response.data["extra"] = {"fields": response.data["detail"]}
    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}

    del response.data["detail"]

    return response

