from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.ean-ucc.org/schemas/1.3/eanucc"


@dataclass
class OrderType:
    order_identification: Optional[str] = field(
        default=None,
        metadata={
            "name": "orderIdentification",
            "type": "Element",
            "namespace": "",
            "required": True,
        },
    )


@dataclass
class Order(OrderType):
    class Meta:
        name = "order"
        namespace = "http://www.ean-ucc.org/schemas/1.3/eanucc"
