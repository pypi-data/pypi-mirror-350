from typing import Callable, List, Optional
from maleo_foundation.types import BaseTypes
from maleo_foundation.models.transfers.parameters.general \
    import BaseGeneralParametersTransfers

class BaseGeneralExpandedTypes:
    #* Expansion processor related types
    FieldExpansionProcessor = Callable[
        [BaseGeneralParametersTransfers.FieldExpansionProcessor],
        BaseTypes.ListOrDictOfAny
    ]

    ListOfFieldExpansionProcessor = List[
        Callable[
            [BaseGeneralParametersTransfers.FieldExpansionProcessor],
            BaseTypes.ListOrDictOfAny
        ]
    ]

    OptionalListOfFieldExpansionProcessor = Optional[
        List[
            Callable[
                [BaseGeneralParametersTransfers.FieldExpansionProcessor],
                BaseTypes.ListOrDictOfAny
            ]
        ]
    ]