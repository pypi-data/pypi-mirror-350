from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = (
    "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader"
)


@dataclass
class ManifestItem:
    mime_type_qualifier_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "MimeTypeQualifierCode",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
            "required": True,
        },
    )
    uniform_resource_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "UniformResourceIdentifier",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
        },
    )
    language_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "LanguageCode",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
        },
    )


@dataclass
class Manifest:
    number_of_items: Optional[int] = field(
        default=None,
        metadata={
            "name": "NumberOfItems",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
            "required": True,
        },
    )
    manifest_item: list[ManifestItem] = field(
        default_factory=list,
        metadata={
            "name": "ManifestItem",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
            "min_occurs": 1,
        },
    )
