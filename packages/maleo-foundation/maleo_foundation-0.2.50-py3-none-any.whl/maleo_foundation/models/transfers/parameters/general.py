from __future__ import annotations
from maleo_foundation.models.schemas.general import BaseGeneralSchemas

class BaseGeneralParametersTransfers:
    class FieldExpansionProcessor(
        BaseGeneralSchemas.Expand,
        BaseGeneralSchemas.Data
    ): pass

    class GetSingleQuery(BaseGeneralSchemas.Statuses): pass

    class BaseGetSingle(
        BaseGeneralSchemas.IdentifierValue,
        BaseGeneralSchemas.IdentifierType
    ):
        pass

    class GetSingle(BaseGeneralSchemas.Statuses, BaseGetSingle): pass

    class StatusUpdate(BaseGeneralSchemas.Status): pass