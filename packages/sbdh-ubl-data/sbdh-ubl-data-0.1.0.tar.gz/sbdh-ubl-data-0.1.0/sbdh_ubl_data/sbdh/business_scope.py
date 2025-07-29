from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = (
    "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader"
)


@dataclass
class CorrelationInformation:
    class Meta:
        namespace = "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader"

    requesting_document_creation_date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "RequestingDocumentCreationDateTime",
            "type": "Element",
        },
    )
    requesting_document_instance_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "RequestingDocumentInstanceIdentifier",
            "type": "Element",
        },
    )
    expected_response_date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ExpectedResponseDateTime",
            "type": "Element",
        },
    )


@dataclass
class ScopeInformation:
    class Meta:
        namespace = "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader"

    any_element: Optional[object] = field(
        default=None,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        },
    )


class TypeOfServiceTransaction(Enum):
    REQUESTING_SERVICE_TRANSACTION = "RequestingServiceTransaction"
    RESPONDING_SERVICE_TRANSACTION = "RespondingServiceTransaction"


@dataclass
class ServiceTransaction:
    type_of_service_transaction: Optional[TypeOfServiceTransaction] = field(
        default=None,
        metadata={
            "name": "TypeOfServiceTransaction",
            "type": "Attribute",
        },
    )
    is_non_repudiation_required: Optional[str] = field(
        default=None,
        metadata={
            "name": "IsNonRepudiationRequired",
            "type": "Attribute",
        },
    )
    is_authentication_required: Optional[str] = field(
        default=None,
        metadata={
            "name": "IsAuthenticationRequired",
            "type": "Attribute",
        },
    )
    is_non_repudiation_of_receipt_required: Optional[str] = field(
        default=None,
        metadata={
            "name": "IsNonRepudiationOfReceiptRequired",
            "type": "Attribute",
        },
    )
    is_intelligible_check_required: Optional[str] = field(
        default=None,
        metadata={
            "name": "IsIntelligibleCheckRequired",
            "type": "Attribute",
        },
    )
    is_application_error_response_requested: Optional[str] = field(
        default=None,
        metadata={
            "name": "IsApplicationErrorResponseRequested",
            "type": "Attribute",
        },
    )
    time_to_acknowledge_receipt: Optional[str] = field(
        default=None,
        metadata={
            "name": "TimeToAcknowledgeReceipt",
            "type": "Attribute",
        },
    )
    time_to_acknowledge_acceptance: Optional[str] = field(
        default=None,
        metadata={
            "name": "TimeToAcknowledgeAcceptance",
            "type": "Attribute",
        },
    )
    time_to_perform: Optional[str] = field(
        default=None,
        metadata={
            "name": "TimeToPerform",
            "type": "Attribute",
        },
    )
    recurrence: Optional[str] = field(
        default=None,
        metadata={
            "name": "Recurrence",
            "type": "Attribute",
        },
    )


@dataclass
class BusinessService:
    class Meta:
        namespace = "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader"

    business_service_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "BusinessServiceName",
            "type": "Element",
        },
    )
    service_transaction: Optional[ServiceTransaction] = field(
        default=None,
        metadata={
            "name": "ServiceTransaction",
            "type": "Element",
        },
    )


@dataclass
class Scope:
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Type",
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
    identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "Identifier",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
        },
    )
    business_service: list[BusinessService] = field(
        default_factory=list,
        metadata={
            "name": "BusinessService",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
        },
    )
    correlation_information: list[CorrelationInformation] = field(
        default_factory=list,
        metadata={
            "name": "CorrelationInformation",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
        },
    )


@dataclass
class BusinessScope:
    scope: list[Scope] = field(
        default_factory=list,
        metadata={
            "name": "Scope",
            "type": "Element",
            "namespace": "http://www.unece.org/cefact/namespaces/StandardBusinessDocumentHeader",
        },
    )
