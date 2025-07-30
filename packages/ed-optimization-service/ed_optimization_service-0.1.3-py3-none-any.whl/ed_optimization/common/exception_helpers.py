from enum import StrEnum


class Exceptions(StrEnum):
    BadRequestException = "BadRequestException"
    InternalServerException = "InternalServerException"
    NotFoundException = "NotFoundException"
    SearchNotFoundException = "SearchNotFoundException"
    ValidationException = "ValidationException"
    UnauthorizedException = "UnauthorizedException"
    ForbiddenException = "ForbiddenException"
    ConflictException = "ConflictException"
    TooManyRequestsException = "TooManyRequestsException"
    ServiceUnavailableException = "ServiceUnavailableException"
    GatewayTimeoutException = "GatewayTimeoutException"
    UnprocessableEntityException = "UnprocessableEntityException"
    PreconditionFailedException = "PreconditionFailedException"
    RequestTimeoutException = "RequestTimeoutException"


ERROR_CODES: dict[Exceptions, int] = {
    Exceptions.BadRequestException: 400,
    Exceptions.InternalServerException: 500,
    Exceptions.NotFoundException: 404,
    Exceptions.SearchNotFoundException: 404,
    Exceptions.ValidationException: 400,
    Exceptions.UnauthorizedException: 401,
    Exceptions.ForbiddenException: 403,
    Exceptions.ConflictException: 409,
    Exceptions.TooManyRequestsException: 429,
    Exceptions.ServiceUnavailableException: 503,
    Exceptions.GatewayTimeoutException: 504,
    Exceptions.UnprocessableEntityException: 422,
    Exceptions.PreconditionFailedException: 412,
    Exceptions.RequestTimeoutException: 408,
}


class ApplicationException(Exception):
    def __init__(
        self, exception_type: Exceptions, message: str, errors: list[str]
    ) -> None:
        self._message = message
        self._errors = errors
        self._error_code = ERROR_CODES[exception_type]
        super().__init__(self._message)

    @property
    def message(self) -> str:
        return self._message

    @property
    def errors(self) -> list[str]:
        return self._errors

    @property
    def error_code(self) -> int:
        return self._error_code

    def __str__(self) -> str:
        return str(self._message)
