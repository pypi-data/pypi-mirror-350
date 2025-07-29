from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.ean-ucc.org/schemas/1.3/eanucc"


@dataclass
class OrderResponseType:
    order_response_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "orderResponseIdentification",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )


@dataclass
class OrderResponse(OrderResponseType):
    class Meta:
        name = "orderResponse"
        namespace = "http://www.ean-ucc.org/schemas/1.3/eanucc"
