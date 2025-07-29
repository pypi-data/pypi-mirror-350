from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from maleo_foundation.enums import BaseEnums
from maleo_foundation.types import BaseTypes

class BaseGeneralSchemas:
    class IdentifierType(BaseModel):
        identifier:BaseEnums.IdentifierTypes = Field(..., description="Data's identifier type")

    class IdentifierValue(BaseModel):
        value:BaseTypes.IdentifierValue = Field(..., description="Data's identifier value")

    class Ids(BaseModel):
        ids:BaseTypes.OptionalListOfIntegers = Field(None, description="Specific Ids")

    class Uuids(BaseModel):
        uuids:BaseTypes.OptionalListOfUUIDs = Field(None, description="Specific Uuids")

    class Codes(BaseModel):
        codes:BaseTypes.OptionalListOfStrings = Field(None, description="Specific Codes")

    class Keys(BaseModel):
        keys:BaseTypes.OptionalListOfStrings = Field(None, description="Specific Keys")

    class Names(BaseModel):
        names:BaseTypes.OptionalListOfStrings = Field(None, description="Specific Names")

    class Search(BaseModel):
        search:BaseTypes.OptionalString = Field(None, description="Search parameter string.")

    class DateFilter(BaseModel):
        name:str = Field(..., description="Column name.")
        from_date:BaseTypes.OptionalDatetime = Field(None, description="From date.")
        to_date:BaseTypes.OptionalDatetime = Field(None, description="To date.")

    class Statuses(BaseModel):
        statuses:BaseTypes.OptionalListOfStatuses = Field(None, description="Data's status")

    class SortColumn(BaseModel):
        name:str = Field(..., description="Column name.")
        order:BaseEnums.SortOrder = Field(..., description="Sort order.")

    class SimplePagination(BaseModel):
        page:int = Field(1, ge=1, description="Page number, must be >= 1.")
        limit:int = Field(10, ge=1, le=100, description="Page size, must be 1 <= limit <= 100.")

    class ExtendedPagination(SimplePagination):
        data_count:int = Field(..., description="Fetched data count")
        total_data:int = Field(..., description="Total data count")
        total_pages:int = Field(..., description="Total pages count")

    class Status(BaseModel):
        status:BaseEnums.StatusType = Field(..., description="Status")

    class Expand(BaseModel):
        expand:BaseTypes.OptionalListOfStrings = Field(None, description="Expanded field(s)")

    class PrivateKey(BaseModel):
        private_key:str = Field(..., description="Private key in str format.")

    class PublicKey(BaseModel):
        public_key:str = Field(..., description="Public key in str format.")

    class KeyPair(PublicKey, PrivateKey): pass

    class Identifiers(BaseModel):
        id:int = Field(..., ge=1, description="Data's ID, must be >= 1.")
        uuid:UUID = Field(..., description="Data's UUID.")

    class Timestamps(BaseModel):
        created_at:datetime = Field(..., description="Data's created_at timestamp")
        updated_at:datetime = Field(..., description="Data's updated_at timestamp")
        deleted_at:BaseTypes.OptionalDatetime = Field(..., description="Data's deleted_at timestamp")
        restored_at:BaseTypes.OptionalDatetime = Field(..., description="Data's restored_at timestamp")
        deactivated_at:BaseTypes.OptionalDatetime = Field(..., description="Data's deactivated_at timestamp")
        activated_at:datetime = Field(..., description="Data's activated_at timestamp")

    class Status(BaseModel):
        status:BaseEnums.StatusType = Field(..., description="Data's status")

    class Order(BaseModel):
        order:BaseTypes.OptionalInteger = Field(..., description="Data's order")

    class Code(BaseModel):
        code:str = Field(..., description="Data's code")

    class Key(BaseModel):
        key:str = Field(..., description="Data's key")

    class Name(BaseModel):
        name:str = Field(..., description="Data's name")

    class Secret(BaseModel):
        secret:UUID = Field(..., description="Data's secret")

    class Data(BaseModel):
        data:BaseTypes.StringToAnyDict = Field(..., description="Data")

    class RSAKeys(BaseModel):
        password:str = Field(..., description="Key's password")
        private:str = Field(..., description="Private key")
        public:str = Field(..., description="Public key")