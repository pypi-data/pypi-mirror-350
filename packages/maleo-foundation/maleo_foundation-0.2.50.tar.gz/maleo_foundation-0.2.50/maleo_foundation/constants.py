import re
from uuid import UUID
from maleo_foundation.enums import BaseEnums
from maleo_foundation.types import BaseTypes

EMAIL_REGEX:str = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
TOKEN_COOKIE_KEY_NAME="token"
REFRESH_TOKEN_DURATION_DAYS:int = 7
ACCESS_TOKEN_DURATION_MINUTES:int = 5
SORT_COLUMN_PATTERN = re.compile(r'^[a-z_]+\.(asc|desc)$')
DATE_FILTER_PATTERN = re.compile(r'^[a-z_]+(?:\|from::\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))?(?:\|to::\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2}))?$')
STATUS_UPDATE_CRITERIAS:dict[
    BaseEnums.StatusUpdateAction,
    BaseTypes.OptionalListOfStatuses
] = {
    BaseEnums.StatusUpdateAction.DELETE: None,
    BaseEnums.StatusUpdateAction.RESTORE: None,
    BaseEnums.StatusUpdateAction.DEACTIVATE: [
        BaseEnums.StatusType.INACTIVE,
        BaseEnums.StatusType.ACTIVE,
    ],
    BaseEnums.StatusUpdateAction.ACTIVATE: [
        BaseEnums.StatusType.INACTIVE,
        BaseEnums.StatusType.ACTIVE,
    ]
}
IDENTIFIER_TYPE_VALUE_TYPE_MAP:dict[
    BaseEnums.IdentifierTypes,
    object
] = {
    BaseEnums.IdentifierTypes.ID: int,
    BaseEnums.IdentifierTypes.UUID: UUID
}