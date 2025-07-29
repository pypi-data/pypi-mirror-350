from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Optional, Union, Any
from uuid import UUID
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.types import BaseTypes

class FieldExpansionMetadata(BaseModel):
    success:bool = Field(..., description="Field expansion's success status")
    code:BaseTypes.OptionalString = Field(None, description="Optional result code")
    message:BaseTypes.OptionalString = Field(None, description="Optional message")
    description:BaseTypes.OptionalString = Field(None, description="Optional description")
    other:BaseTypes.OptionalAny = Field(None, description="Optional other information")

class ResultMetadata(BaseModel):
    field_expansion:Optional[Union[str, Dict[str, FieldExpansionMetadata]]] = Field(None, description="Field expansion metadata")

class BaseResultSchemas:
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

    class ExtendedPagination(BaseGeneralSchemas.SimplePagination):
        data_count:int = Field(..., description="Fetched data count")
        total_data:int = Field(..., description="Total data count")
        total_pages:int = Field(..., description="Total pages count")

    #* ----- ----- ----- Base ----- ----- ----- *#
    class Base(BaseModel):
        success:bool = Field(..., description="Success status")
        code:BaseTypes.OptionalString = Field(None, description="Optional result code")
        message:BaseTypes.OptionalString = Field(None, description="Optional message")
        description:BaseTypes.OptionalString = Field(None, description="Optional description")
        data:Any = Field(..., description="Data")
        metadata:Optional[ResultMetadata] = Field(None, description="Optional metadata")
        other:BaseTypes.OptionalAny = Field(None, description="Optional other information")

    #* ----- ----- ----- Intermediary ----- ----- ----- *#
    class Fail(Base):
        code:str = "MAL-FAI-001"
        message:str = "Fail result"
        description:str = "Operation failed."
        success:BaseTypes.LiteralFalse = Field(False, description="Success status")
        data:None = Field(None, description="No data")

    class Success(Base):
        success:BaseTypes.LiteralTrue = Field(True, description="Success status")
        code:str = "MAL-SCS-001"
        message:str = "Success result"
        description:str = "Operation succeeded."
        data:Any = Field(..., description="Data")

    #* ----- ----- ----- Derived ----- ----- ----- *#
    class NotFound(Fail):
        code:str = "MAL-NTF-001"
        message:str = "Resource not found"
        description:str = "The requested resource can not be found."
        data:None = Field(None, description="No data")

    class NoData(Success):
        code:str = "MAL-NDT-001"
        message:str = "No data found"
        description:str = "No data found in the requested resource."
        data:None = Field(None, description="No data")

    class SingleData(Success):
        code:str = "MAL-SGD-001"
        message:str = "Single data found"
        description:str = "Requested data found in database."
        data:Any = Field(..., description="Fetched single data")

    class UnpaginatedMultipleData(Success):
        code:str = "MAL-MTD-001"
        message:str = "Multiple unpaginated data found"
        description:str = "Requested unpaginated data found in database."
        data:BaseTypes.ListOfAny = Field(..., description="Unpaginated multiple data")

    class PaginatedMultipleData(
        UnpaginatedMultipleData,
        BaseGeneralSchemas.SimplePagination
    ):
        code:str = "MAL-MTD-002"
        message:str = "Multiple paginated data found"
        description:str = "Requested paginated data found in database."
        total_data:int = Field(..., ge=0, description="Total data count")
        pagination:"BaseResultSchemas.ExtendedPagination" = Field(..., description="Pagination metadata")

BaseResultSchemas.PaginatedMultipleData.model_rebuild()