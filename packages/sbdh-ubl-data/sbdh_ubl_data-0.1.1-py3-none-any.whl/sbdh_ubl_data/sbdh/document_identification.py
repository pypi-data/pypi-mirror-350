from dataclasses import dataclass, field
from typing import Optional

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = (
    "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader"
)


@dataclass
class DocumentIdentification:
    standard: Optional[str] = field(
        default=None,
        metadata={
            "name": "Standard",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
            "required": True,
        },
    )
    type_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeVersion",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
            "required": True,
        },
    )
    instance_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "InstanceIdentifier",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
            "required": True,
        },
    )
    multiple_type: Optional[bool] = field(
        default=None,
        metadata={
            "name": "MultipleType",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
        },
    )
    creation_date_and_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "CreationDateAndTime",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
            "required": True,
        },
    )
