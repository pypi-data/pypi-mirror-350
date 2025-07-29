from __future__ import annotations
from pydantic import BaseModel, Field
from maleo_foundation.enums import BaseEnums
from maleo_foundation.types import BaseTypes

class BaseGeneralSchemas:
    class DateFilter(BaseModel):
        name:str = Field(..., description="Column name.")
        from_date:BaseTypes.OptionalDatetime = Field(None, description="From date.")
        to_date:BaseTypes.OptionalDatetime = Field(None, description="To date.")

    class SortColumn(BaseModel):
        name:str = Field(..., description="Column name.")
        order:BaseEnums.SortOrder = Field(..., description="Sort order.")

    class SimplePagination(BaseModel):
        page:int = Field(1, ge=1, description="Page number, must be >= 1.")
        limit:int = Field(10, ge=1, le=100, description="Page size, must be 1 <= limit <= 100.")

    class PrivateKey(BaseModel):
        private_key:str = Field(..., description="Private key in str format.")

    class PublicKey(BaseModel):
        public_key:str = Field(..., description="Public key in str format.")

    class KeyPair(PublicKey, PrivateKey): pass

    class Status(BaseModel):
        status:BaseEnums.StatusType = Field(..., description="Data's status")

    class RSAKeys(BaseModel):
        password:str = Field(..., description="Key's password")
        private:str = Field(..., description="Private key")
        public:str = Field(..., description="Public key")