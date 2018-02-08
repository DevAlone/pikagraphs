class RestyCornException(BaseException):
    pass


class ResourceException(RestyCornException):
    pass


class ResourceDoesNotExistException(ResourceException):
    pass


class ResourceItemDoesNotExistException(ResourceException):
    pass


class MethodIsNotAllowedException(RestyCornException):
    pass


class ParamsValidationException(RestyCornException):
    pass


class SerializationError(RestyCornException):
    pass


class SQLRequestConstructorException(RestyCornException):
    pass
