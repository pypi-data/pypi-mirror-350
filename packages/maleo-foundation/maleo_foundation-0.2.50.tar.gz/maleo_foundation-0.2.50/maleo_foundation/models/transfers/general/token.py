from __future__ import annotations
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field, model_validator
from uuid import UUID
from maleo_foundation.types import BaseTypes
from maleo_foundation.models.schemas.token import MaleoFoundationTokenSchemas

class MaleoFoundationTokenGeneralTransfers:
    class BasePayload(BaseModel):
        iss:BaseTypes.OptionalString = Field(None, description="Token's issuer")
        sub:str = Field(..., description="Token's subject")
        sr:str = Field(..., description="System role")
        u_i:int = Field(..., description="user's id")
        u_uu:UUID = Field(..., description="user's uuid")
        u_u:str = Field(..., description="user's username")
        u_e:str = Field(..., description="user's email")
        u_ut:str = Field(..., description="user's type")
        o_i:BaseTypes.OptionalInteger = Field(None, description="Organization's id")
        o_uu:BaseTypes.OptionalUUID = Field(None, description="Organization's uuid")
        o_k:BaseTypes.OptionalString = Field(None, description="Organization's key")
        o_ot:BaseTypes.OptionalString = Field(None, description="Organization's type")
        uor:BaseTypes.OptionalListOfStrings = Field(None, description="User Organization Role")

    class DecodePayload(BasePayload):
        iat_dt:datetime = Field(..., description="Issued at (datetime)")
        iat:int = Field(..., description="Issued at (integer)")
        exp_dt:datetime = Field(..., description="Expired at (datetime)")
        exp:int = Field(..., description="Expired at (integer)")

    class BaseEncodePayload(MaleoFoundationTokenSchemas.ExpIn, BasePayload): pass

    class EncodePayload(DecodePayload):
        iat_dt:datetime = Field(datetime.now(timezone.utc), description="Issued at (datetime)")
        exp_in:int = Field(15, ge=1, description="Expires in (integer, minutes)", exclude=True)

        @model_validator(mode="before")
        @classmethod
        def set_iat_and_exp(cls, values:dict):
            iat_dt = values.get("iat_dt", None)
            if not iat_dt:
                iat_dt = datetime.now(timezone.utc)
            else:
                if not isinstance(iat_dt, datetime):
                    iat_dt = datetime.fromisoformat(iat_dt)
            values["iat_dt"] = iat_dt
            #* Convert `iat` to timestamp (int)
            values["iat"] = int(iat_dt.timestamp())
            exp_in = values.get("exp_in")
            exp_dt = values.get("exp_dt", None)
            if not exp_dt:
                exp_dt = iat_dt + timedelta(minutes=exp_in)
            else:
                if not isinstance(exp_dt, datetime):
                    exp_dt = datetime.fromisoformat(exp_dt)
            values["exp_dt"] = exp_dt
            #* Convert `exp_dt` to timestamp (int)
            values["exp"] = int(exp_dt.timestamp())
            return values