from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = (
    "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader"
)


@dataclass
class ContactInformation:
    contact: Optional[str] = field(
        default=None,
        metadata={
            "name": "Contact",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
            "required": True,
        },
    )
    email_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "EmailAddress",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
        },
    )
    fax_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "FaxNumber",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
        },
    )
    telephone_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "TelephoneNumber",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
        },
    )
    contact_type_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "ContactTypeIdentifier",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
        },
    )


@dataclass
class PartnerIdentification:
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    authority: Optional[str] = field(
        default=None,
        metadata={
            "name": "Authority",
            "type": "Attribute",
        },
    )


@dataclass
class Partner:
    identifier: Optional[PartnerIdentification] = field(
        default=None,
        metadata={
            "name": "Identifier",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
            "required": True,
        },
    )
    contact_information: list[ContactInformation] = field(
        default_factory=list,
        metadata={
            "name": "ContactInformation",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
        },
    )
