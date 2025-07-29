from dataclasses import dataclass, field
from typing import Optional

from generated.sbdh.business_scope import BusinessScope
from generated.sbdh.document_identification import DocumentIdentification
from generated.sbdh.manifest import Manifest
from generated.sbdh.partner import Partner

__NAMESPACE__ = (
    "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader"
)


@dataclass
class StandardBusinessDocumentHeader:
    class Meta:
        namespace = "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader"

    header_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "HeaderVersion",
            "type": "Element",
            "required": True,
        },
    )
    sender: list[Partner] = field(
        default_factory=list,
        metadata={
            "name": "Sender",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    receiver: list[Partner] = field(
        default_factory=list,
        metadata={
            "name": "Receiver",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    document_identification: Optional[DocumentIdentification] = field(
        default=None,
        metadata={
            "name": "DocumentIdentification",
            "type": "Element",
            "required": True,
        },
    )
    manifest: Optional[Manifest] = field(
        default=None,
        metadata={
            "name": "Manifest",
            "type": "Element",
        },
    )
    business_scope: Optional[BusinessScope] = field(
        default=None,
        metadata={
            "name": "BusinessScope",
            "type": "Element",
        },
    )


@dataclass
class StandardBusinessDocument:
    class Meta:
        namespace = "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader"

    standard_business_document_header: Optional[
        StandardBusinessDocumentHeader
    ] = field(
        default=None,
        metadata={
            "name": "StandardBusinessDocumentHeader",
            "type": "Element",
        },
    )
    other_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##other",
        },
    )
