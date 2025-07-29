from dataclasses import dataclass, field
from typing import Optional

from sbdh_ubl_data.ubl.common.ubl_common_aggregate_components_2_1 import (
    AdditionalDocumentReference,
    AdditionalTransportationService,
    AtLocation,
    Consignment,
    FromLocation,
    MainTransportationService,
    PayeeParty,
    ReceiverParty,
    SenderParty,
    ServiceEndTimePeriod,
    ServiceStartTimePeriod,
    Signature,
    ToLocation,
    TransportContract,
    TransportExecutionPlanDocumentReference,
    TransportExecutionTerms,
    TransportServiceDescriptionDocumentReference,
    TransportServiceProviderParty,
    TransportServiceProviderResponseDeadlinePeriod,
    TransportUserParty,
)
from sbdh_ubl_data.ubl.common.ubl_common_basic_components_2_1 import (
    CopyIndicator,
    CustomizationId,
    DocumentStatusCode,
    DocumentStatusReasonCode,
    DocumentStatusReasonDescription,
    Id,
    IssueDate,
    IssueTime,
    Note,
    ProfileExecutionId,
    ProfileId,
    TransportUserRemarks,
    UblversionId,
    Uuid,
    VersionId,
)
from sbdh_ubl_data.ubl.common.ubl_common_extension_components_2_1 import (
    Ublextensions,
)

__NAMESPACE__ = "urn:oasis:names:specification:ubl:schema:xsd:TransportExecutionPlanRequest-2"


@dataclass
class TransportExecutionPlanRequestType:
    """<ns1:Component xmlns:ns1="urn:un:unece:uncefact:documentation:2">
    <ns1:ComponentType>ABIE</ns1:ComponentType> <ns1:DictionaryEntryName>Transport
    Execution Plan Request.

    Details</ns1:DictionaryEntryName> <ns1:Definition>A document sent by
    a transport user to request a transport service from a transport
    service provider.</ns1:Definition> <ns1:ObjectClass>Transport
    Execution Plan Request</ns1:ObjectClass> </ns1:Component>

    :ivar ublextensions: A container for all extensions present in the
        document.
    :ivar ublversion_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request. UBL
        Version Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies the earliest version of the UBL 2
        schema for this document type that defines all of the elements
        that might be encountered in the current
        instance.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTerm>UBL Version
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar customization_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Customization Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies a user-defined customization of UBL
        for a specific use.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTerm>Customization
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar profile_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Profile Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies a user-defined profile of the
        customization of UBL being used.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTerm>Profile
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar profile_execution_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Profile Execution Identifier.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>Identifies
        an instance of executing a profile, to associate all
        transactions in a collaboration.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTerm>Profile Execution
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>An
        identifier for this document, assigned by the
        sender.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTerm>Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar version_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Version. Identifier</ns1:DictionaryEntryName> <ns1:Definition>An
        identifier for the current version of the Transport Execution
        Plan Request.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTerm>Version</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> <ns1:Examples>1.1
        </ns1:Examples> </ns1:Component>
    :ivar copy_indicator: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request. Copy_
        Indicator. Indicator</ns1:DictionaryEntryName>
        <ns1:Definition>Indicates whether this document is a copy (true)
        or not (false).</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Copy</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Indicator</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Indicator</ns1:RepresentationTerm>
        <ns1:DataType>Indicator. Type</ns1:DataType> </ns1:Component>
    :ivar uuid: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request. UUID.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>A
        universally unique identifier for an instance of this
        document.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTerm>UUID</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar issue_date: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request. Issue
        Date. Date</ns1:DictionaryEntryName> <ns1:Definition>The date,
        assigned by the sender, on which this document was
        issued.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTerm>Issue
        Date</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Date</ns1:RepresentationTerm>
        <ns1:DataType>Date. Type</ns1:DataType>
        <ns1:AlternativeBusinessTerms>Transport Document
        Date</ns1:AlternativeBusinessTerms> </ns1:Component>
    :ivar issue_time: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request. Issue
        Time. Time</ns1:DictionaryEntryName> <ns1:Definition>The time,
        assigned by the sender, at which this document was
        issued.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTerm>Issue
        Time</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Time</ns1:RepresentationTerm>
        <ns1:DataType>Time. Type</ns1:DataType> </ns1:Component>
    :ivar document_status_code: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Document Status Code. Code</ns1:DictionaryEntryName>
        <ns1:Definition>A code signifying the status of the Transport
        Execution Plan Request.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTerm>Document Status
        Code</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Code</ns1:RepresentationTerm>
        <ns1:DataTypeQualifier>Document Status</ns1:DataTypeQualifier>
        <ns1:DataType>Document Status_ Code. Type</ns1:DataType>
        </ns1:Component>
    :ivar document_status_reason_code: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Document Status Reason Code. Code</ns1:DictionaryEntryName>
        <ns1:Definition>A code signifying a reason associated with the
        status of the Transport Execution Plan Request.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTerm>Document Status
        Reason Code</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Code</ns1:RepresentationTerm>
        <ns1:DataType>Code. Type</ns1:DataType> </ns1:Component>
    :ivar document_status_reason_description: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Document Status Reason Description.
        Text</ns1:DictionaryEntryName> <ns1:Definition>A reason
        associated with the status of the Transport Execution Plan
        Request.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTerm>Document Status
        Reason Description</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> <ns1:Examples>123
        Standard Chartered Tower </ns1:Examples> </ns1:Component>
    :ivar note: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request. Note.
        Text</ns1:DictionaryEntryName> <ns1:Definition>Free-form text
        pertinent to this document, conveying information that is not
        contained explicitly in other structures.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTerm>Note</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar transport_user_remarks: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Transport User_ Remarks. Text</ns1:DictionaryEntryName>
        <ns1:Definition>Remarks from the transport user regarding the
        transport operations referenced in the Transport Execution Plan
        Request.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTermQualifier>Transport
        User</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Remarks</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar sender_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Sender_ Party. Party</ns1:DictionaryEntryName>
        <ns1:Definition>The party sending the Transport Execution Plan
        Request.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Sender</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar receiver_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Receiver_ Party. Party</ns1:DictionaryEntryName>
        <ns1:Definition>The party receiving the Transport Execution Plan
        Request.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Receiver</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar transport_user_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Transport User_ Party. Party</ns1:DictionaryEntryName>
        <ns1:Definition>The party requesting the transport services
        referenced in the Transport Execution Plan
        Request.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTermQualifier>Transport
        User</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar transport_service_provider_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Transport Service Provider_ Party.
        Party</ns1:DictionaryEntryName> <ns1:Definition>The party
        providing the transport services referenced in the Transport
        Execution Plan Request.</ns1:Definition>
        <ns1:Cardinality>1</ns1:Cardinality> <ns1:ObjectClass>Transport
        Execution Plan Request</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Transport Service
        Provider</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar payee_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Payee_ Party. Party</ns1:DictionaryEntryName>
        <ns1:Definition>The party that will pay for the transport
        service(s) referred to in a Transport Execution
        Plan.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Payee</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar signature: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Signature</ns1:DictionaryEntryName> <ns1:Definition>A signature
        applied to this document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTerm>Signature</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Signature</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Signature</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar transport_execution_plan_document_reference: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Transport Execution Plan_ Document Reference. Document
        Reference</ns1:DictionaryEntryName> <ns1:Definition>A reference
        to an original Transport Execution Plan
        Document.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTermQualifier>Transport
        Execution Plan</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Document Reference</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Document
        Reference</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Document
        Reference</ns1:RepresentationTerm> </ns1:Component>
    :ivar transport_service_description_document_reference:
        <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Transport Service Description_ Document Reference. Document
        Reference</ns1:DictionaryEntryName> <ns1:Definition>A reference
        to the Transport Service Description, which is used by a
        transport service provider to announce transport services to
        transport users (buyers).</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTermQualifier>Transport
        Service Description</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Document Reference</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Document
        Reference</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Document
        Reference</ns1:RepresentationTerm> </ns1:Component>
    :ivar additional_document_reference: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Additional_ Document Reference. Document
        Reference</ns1:DictionaryEntryName> <ns1:Definition>A reference
        to an additional document associated with this
        document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Additional</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Document Reference</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Document
        Reference</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Document
        Reference</ns1:RepresentationTerm> </ns1:Component>
    :ivar transport_contract: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Transport_ Contract. Contract</ns1:DictionaryEntryName>
        <ns1:Definition>A potential contract related to the Transport
        Execution Plan Request.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Transport</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Contract</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Contract</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Contract</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar transport_service_provider_response_deadline_period:
        <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Transport Service Provider Response Deadline_ Period.
        Period</ns1:DictionaryEntryName> <ns1:Definition>A deadline for
        a response from the Transport Service Provider to this Transport
        Execution Plan Request.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTermQualifier>Transport
        Service Provider Response Deadline</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Period</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Period</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Period</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar main_transportation_service: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request. Main_
        Transportation Service. Transportation
        Service</ns1:DictionaryEntryName> <ns1:Definition>A description
        of the main transportation service referenced in the Transport
        Execution Plan Request.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Main</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Transportation Service</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Transportation
        Service</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Transportation
        Service</ns1:RepresentationTerm> </ns1:Component>
    :ivar additional_transportation_service: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Additional_ Transportation Service. Transportation
        Service</ns1:DictionaryEntryName> <ns1:Definition>A description
        of an additional transportation service referenced in the
        Transport Execution Plan Request.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Additional</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Transportation Service</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Transportation
        Service</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Transportation
        Service</ns1:RepresentationTerm> </ns1:Component>
    :ivar service_start_time_period: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Service Start Time_ Period. Period</ns1:DictionaryEntryName>
        <ns1:Definition>The period within which the services referred to
        in the Transport Execution Plan Request must
        begin.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTermQualifier>Service
        Start Time</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Period</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Period</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Period</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar service_end_time_period: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Service End Time_ Period. Period</ns1:DictionaryEntryName>
        <ns1:Definition>The period during which the services referred to
        in the Transport Execution Plan Request must be
        completed.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTermQualifier>Service End
        Time</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Period</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Period</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Period</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar from_location: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request. From_
        Location. Location</ns1:DictionaryEntryName> <ns1:Definition>The
        location of origin of the transport service referenced in the
        Transport Execution Plan Request.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>From</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Location</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Location</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Location</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar to_location: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request. To_
        Location. Location</ns1:DictionaryEntryName> <ns1:Definition>The
        destination location for the transport service referenced in the
        Transport Execution Plan Request.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>To</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Location</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Location</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Location</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar at_location: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request. At_
        Location. Location</ns1:DictionaryEntryName> <ns1:Definition>The
        location of a transport service (e.g., terminal handling
        service) that does not require transport
        movement.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>At</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Location</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Location</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Location</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar transport_execution_terms: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Transport Execution Terms</ns1:DictionaryEntryName>
        <ns1:Definition>A description of terms and conditions related to
        the Transport Execution Plan Request.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass> <ns1:PropertyTerm>Transport Execution
        Terms</ns1:PropertyTerm> <ns1:AssociatedObjectClass>Transport
        Execution Terms</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Transport Execution
        Terms</ns1:RepresentationTerm> </ns1:Component>
    :ivar consignment: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Transport Execution Plan Request.
        Consignment</ns1:DictionaryEntryName> <ns1:Definition>A
        description of an identifiable collection of goods items to be
        transported between the consignor and the consignee. This
        information may be defined within a transport contract. A
        consignment may comprise more than one shipment (e.g., when
        consolidated by a freight forwarder).</ns1:Definition>
        <ns1:Cardinality>1..n</ns1:Cardinality>
        <ns1:ObjectClass>Transport Execution Plan
        Request</ns1:ObjectClass>
        <ns1:PropertyTerm>Consignment</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Consignment</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Consignment</ns1:RepresentationTerm>
        </ns1:Component>
    """

    ublextensions: Optional[Ublextensions] = field(
        default=None,
        metadata={
            "name": "UBLExtensions",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
        },
    )
    ublversion_id: Optional[UblversionId] = field(
        default=None,
        metadata={
            "name": "UBLVersionID",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    customization_id: Optional[CustomizationId] = field(
        default=None,
        metadata={
            "name": "CustomizationID",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    profile_id: Optional[ProfileId] = field(
        default=None,
        metadata={
            "name": "ProfileID",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    profile_execution_id: Optional[ProfileExecutionId] = field(
        default=None,
        metadata={
            "name": "ProfileExecutionID",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    id: Optional[Id] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            "required": True,
        },
    )
    version_id: Optional[VersionId] = field(
        default=None,
        metadata={
            "name": "VersionID",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    copy_indicator: Optional[CopyIndicator] = field(
        default=None,
        metadata={
            "name": "CopyIndicator",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={
            "name": "UUID",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    issue_date: Optional[IssueDate] = field(
        default=None,
        metadata={
            "name": "IssueDate",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    issue_time: Optional[IssueTime] = field(
        default=None,
        metadata={
            "name": "IssueTime",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    document_status_code: Optional[DocumentStatusCode] = field(
        default=None,
        metadata={
            "name": "DocumentStatusCode",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    document_status_reason_code: Optional[DocumentStatusReasonCode] = field(
        default=None,
        metadata={
            "name": "DocumentStatusReasonCode",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    document_status_reason_description: list[
        DocumentStatusReasonDescription
    ] = field(
        default_factory=list,
        metadata={
            "name": "DocumentStatusReasonDescription",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    note: list[Note] = field(
        default_factory=list,
        metadata={
            "name": "Note",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    transport_user_remarks: list[TransportUserRemarks] = field(
        default_factory=list,
        metadata={
            "name": "TransportUserRemarks",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    sender_party: Optional[SenderParty] = field(
        default=None,
        metadata={
            "name": "SenderParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    receiver_party: Optional[ReceiverParty] = field(
        default=None,
        metadata={
            "name": "ReceiverParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    transport_user_party: Optional[TransportUserParty] = field(
        default=None,
        metadata={
            "name": "TransportUserParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "required": True,
        },
    )
    transport_service_provider_party: Optional[
        TransportServiceProviderParty
    ] = field(
        default=None,
        metadata={
            "name": "TransportServiceProviderParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "required": True,
        },
    )
    payee_party: Optional[PayeeParty] = field(
        default=None,
        metadata={
            "name": "PayeeParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    signature: list[Signature] = field(
        default_factory=list,
        metadata={
            "name": "Signature",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    transport_execution_plan_document_reference: Optional[
        TransportExecutionPlanDocumentReference
    ] = field(
        default=None,
        metadata={
            "name": "TransportExecutionPlanDocumentReference",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    transport_service_description_document_reference: Optional[
        TransportServiceDescriptionDocumentReference
    ] = field(
        default=None,
        metadata={
            "name": "TransportServiceDescriptionDocumentReference",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    additional_document_reference: list[AdditionalDocumentReference] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalDocumentReference",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    transport_contract: Optional[TransportContract] = field(
        default=None,
        metadata={
            "name": "TransportContract",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    transport_service_provider_response_deadline_period: list[
        TransportServiceProviderResponseDeadlinePeriod
    ] = field(
        default_factory=list,
        metadata={
            "name": "TransportServiceProviderResponseDeadlinePeriod",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    main_transportation_service: Optional[MainTransportationService] = field(
        default=None,
        metadata={
            "name": "MainTransportationService",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    additional_transportation_service: list[
        AdditionalTransportationService
    ] = field(
        default_factory=list,
        metadata={
            "name": "AdditionalTransportationService",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    service_start_time_period: Optional[ServiceStartTimePeriod] = field(
        default=None,
        metadata={
            "name": "ServiceStartTimePeriod",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    service_end_time_period: Optional[ServiceEndTimePeriod] = field(
        default=None,
        metadata={
            "name": "ServiceEndTimePeriod",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    from_location: Optional[FromLocation] = field(
        default=None,
        metadata={
            "name": "FromLocation",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    to_location: Optional[ToLocation] = field(
        default=None,
        metadata={
            "name": "ToLocation",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    at_location: Optional[AtLocation] = field(
        default=None,
        metadata={
            "name": "AtLocation",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    transport_execution_terms: Optional[TransportExecutionTerms] = field(
        default=None,
        metadata={
            "name": "TransportExecutionTerms",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    consignment: list[Consignment] = field(
        default_factory=list,
        metadata={
            "name": "Consignment",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "min_occurs": 1,
        },
    )


@dataclass
class TransportExecutionPlanRequest(TransportExecutionPlanRequestType):
    """
    This element MUST be conveyed as the root element in any instance document
    based on this Schema expression.
    """

    class Meta:
        namespace = "urn:oasis:names:specification:ubl:schema:xsd:TransportExecutionPlanRequest-2"
