import logging
from enum import IntEnum, StrEnum, Enum
from fastapi import responses

class BaseEnums:
    class EnvironmentType(StrEnum):
        LOCAL = "local"
        STAGING = "staging"
        PRODUCTION = "production"

    class StatusType(StrEnum):
        DELETED = "deleted"
        INACTIVE = "inactive"
        ACTIVE = "active"

    class UserType(StrEnum):
        REGULAR = "regular"
        PROXY = "proxy"

    class SortOrder(StrEnum):
        ASC = "asc"
        DESC = "desc"

    class StatusUpdateAction(StrEnum):
        ACTIVATE = "activate"
        DEACTIVATE = "deactivate"
        RESTORE = "restore"
        DELETE = "delete"

    class TokenType(StrEnum):
        REFRESH = "refresh"
        ACCESS = "access"

    class OperationType(StrEnum):
        CREATE = "create"
        UPDATE = "update"

    class IdentifierTypes(StrEnum):
        ID = "id"
        UUID = "uuid"

    class ServiceControllerType(StrEnum):
        REST = "rest"

    class ClientControllerType(StrEnum):
        HTTP = "http"

    class ClientCategory(StrEnum):
        GOOGLE = "google"
        MALEO = "maleo"

    class KeyType(StrEnum):
        PRIVATE = "private"
        PUBLIC = "public"

    class KeyFormatType(Enum):
        BYTES = bytes
        STRING = str

    class RESTControllerResponseType(StrEnum):
        NONE = "none"
        HTML = "html"
        TEXT = "text"
        JSON = "json"
        REDIRECT = "redirect"
        STREAMING = "streaming"
        FILE = "file"

        def get_response_type(self) -> type[responses.Response]:
            """Returns the corresponding FastAPI Response type."""
            return {
                BaseEnums.RESTControllerResponseType.NONE: responses.Response,
                BaseEnums.RESTControllerResponseType.HTML: responses.HTMLResponse,
                BaseEnums.RESTControllerResponseType.TEXT: responses.PlainTextResponse,
                BaseEnums.RESTControllerResponseType.JSON: responses.JSONResponse,
                BaseEnums.RESTControllerResponseType.REDIRECT: responses.RedirectResponse,
                BaseEnums.RESTControllerResponseType.STREAMING: responses.StreamingResponse,
                BaseEnums.RESTControllerResponseType.FILE: responses.FileResponse,
            }.get(self, responses.Response)

    class MiddlewareLoggerType(StrEnum):
        BASE = "base"
        AUTHENTICATION = "authentication"

    class ServiceLoggerType(StrEnum):
        REPOSITORY = "repository"
        DATABASE = "database"
        APPLICATION = "application"

    class LoggerType(StrEnum):
        MIDDLEWARE = "middleware"
        REPOSITORY = "repository"
        DATABASE = "database"
        APPLICATION = "application"
        CLIENT = "client"

    class LoggerLevel(IntEnum):
        CRITICAL = logging.CRITICAL
        FATAL = logging.FATAL
        ERROR = logging.ERROR
        WARNING = logging.WARNING
        WARN = logging.WARN
        INFO = logging.INFO
        DEBUG = logging.DEBUG
        NOTSET = logging.NOTSET

    class CacheType(StrEnum):
        REPOSITORY = "repository"
        ROUTER = "router"
        CLIENT = "client"

    class CacheTTL(IntEnum):
        TTL_15SC = int(15)
        TTL_30SC = int(30)
        TTL_1MN = int(1*60)
        TTL_5MN = int(5*60)
        TTL_10MN = int(10*60)
        TTL_30MN = int(30*60)
        TTL_1HR = int(1*60*60)
        TTL_6HR = int(6*60*60)
        TTL_12HR = int(12*60*60)
        TTL_1DY = int(1*24*60*60)
        TTL_3DY = int(3*24*60*60)
        TTL_1WK = int(1*24*60*60)
        TTL_2WK = int(2*24*60*60)
        TTL_1MO = int(1*30*24*60*60)