class InvalidService(Exception):
    pass


class ServiceError(Exception):
    pass


class OrganizeChaptersToVolError(ServiceError):
    pass


class RezipChaptersToVolError(ServiceError):
    pass


class FileSystemError(ServiceError):
    pass


class CreateVolumesError(ServiceError):
    pass


class RenameMediaError(ServiceError):
    pass


class DataTypeError(ServiceError):
    pass


class BadSchemaError(ServiceError):
    pass


class ApiError(ServiceError):
    pass


class RequestError(ApiError):
    pass
