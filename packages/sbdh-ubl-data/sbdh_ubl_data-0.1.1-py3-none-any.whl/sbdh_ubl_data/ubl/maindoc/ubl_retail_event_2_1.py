from dataclasses import dataclass, field
from typing import Optional

from sbdh_ubl_data.ubl.common.ubl_common_aggregate_components_2_1 import (
    BuyerCustomerParty,
    EventComment,
    MiscellaneousEvent,
    OriginalDocumentReference,
    Period,
    PromotionalEvent,
    ReceiverParty,
    SellerSupplierParty,
    SenderParty,
    Signature,
)
from sbdh_ubl_data.ubl.common.ubl_common_basic_components_2_1 import (
    BuyerEventId,
    CopyIndicator,
    CustomizationId,
    Description,
    Id,
    IssueDate,
    IssueTime,
    Note,
    ProfileExecutionId,
    ProfileId,
    RetailEventName,
    RetailEventStatusCode,
    SellerEventId,
    UblversionId,
    Uuid,
)
from sbdh_ubl_data.ubl.common.ubl_common_extension_components_2_1 import (
    Ublextensions,
)

__NAMESPACE__ = "urn:oasis:names:specification:ubl:schema:xsd:RetailEvent-2"


@dataclass
class RetailEventType:
    """<ns1:Component xmlns:ns1="urn:un:unece:uncefact:documentation:2">
    <ns1:ComponentType>ABIE</ns1:ComponentType> <ns1:DictionaryEntryName>Retail
    Event.

    Details</ns1:DictionaryEntryName>
    <ns1:Definition>A document used to specify basic information about retail events (such as promotions, product introductions, and community or environmental events) that affect supply or demand.</ns1:Definition>
    <ns1:ObjectClass>Retail Event</ns1:ObjectClass>
    <ns1:AlternativeBusinessTerms>Event</ns1:AlternativeBusinessTerms>
    </ns1:Component>

    :ivar ublextensions: A container for all extensions present in the
        document.
    :ivar ublversion_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. UBL Version Identifier.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>Identifies
        the earliest version of the UBL 2 schema for this document type
        that defines all of the elements that might be encountered in
        the current instance.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass> <ns1:PropertyTerm>UBL Version
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>2.0.5</ns1:Examples> </ns1:Component>
    :ivar customization_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Customization Identifier.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>Identifies
        a user-defined customization of UBL for a specific
        use.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Retail Event</ns1:ObjectClass>
        <ns1:PropertyTerm>Customization Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>NES</ns1:Examples> </ns1:Component>
    :ivar profile_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Profile Identifier.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>Identifies
        a user-defined profile of the customization of UBL being
        used.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Retail Event</ns1:ObjectClass>
        <ns1:PropertyTerm>Profile Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BasicProcurementProcess</ns1:Examples>
        </ns1:Component>
    :ivar profile_execution_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Profile Execution
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies an instance of executing a profile,
        to associate all transactions in a
        collaboration.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass> <ns1:PropertyTerm>Profile Execution
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BPP-1001</ns1:Examples> </ns1:Component>
    :ivar id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>An
        identifier for this document, assigned by the
        sender.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Retail Event</ns1:ObjectClass>
        <ns1:PropertyTerm>Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:AlternativeBusinessTerms>Retail Event
        Number</ns1:AlternativeBusinessTerms> </ns1:Component>
    :ivar copy_indicator: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Copy_ Indicator.
        Indicator</ns1:DictionaryEntryName> <ns1:Definition>Indicates
        whether this document is a copy (true) or not
        (false).</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Copy</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Indicator</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Indicator</ns1:RepresentationTerm>
        <ns1:DataType>Indicator. Type</ns1:DataType> </ns1:Component>
    :ivar uuid: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. UUID.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>A
        universally unique identifier for an instance of this
        document.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass>
        <ns1:PropertyTerm>UUID</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar issue_date: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Issue Date.
        Date</ns1:DictionaryEntryName> <ns1:Definition>The date,
        assigned by the sender, on which this document was
        issued.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Retail Event</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Date</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Date</ns1:RepresentationTerm>
        <ns1:DataType>Date. Type</ns1:DataType>
        <ns1:AlternativeBusinessTerms>Retail Event
        Date</ns1:AlternativeBusinessTerms> </ns1:Component>
    :ivar issue_time: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Issue Time.
        Time</ns1:DictionaryEntryName> <ns1:Definition>The time,
        assigned by the sender, at which this document was
        issued.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Retail Event</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Time</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Time</ns1:RepresentationTerm>
        <ns1:DataType>Time. Type</ns1:DataType> </ns1:Component>
    :ivar note: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Note.
        Text</ns1:DictionaryEntryName> <ns1:Definition>Free-form text
        pertinent to this document, conveying information that is not
        contained explicitly in other structures.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass>
        <ns1:PropertyTerm>Note</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar retail_event_name: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Retail Event Name.
        Name</ns1:DictionaryEntryName> <ns1:Definition>A title, theme,
        slogan, or other identifier for the event for use by trading
        partners.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass> <ns1:PropertyTerm>Retail Event
        Name</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Name</ns1:RepresentationTerm>
        <ns1:DataType>Name. Type</ns1:DataType> </ns1:Component>
    :ivar retail_event_status_code: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Retail Event Status Code.
        Code</ns1:DictionaryEntryName> <ns1:Definition>Describes the
        logical state of the discrete activity affecting supply or
        demand in the supply chain</ns1:Definition>
        <ns1:Cardinality>1</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass> <ns1:PropertyTerm>Retail Event Status
        Code</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Code</ns1:RepresentationTerm>
        <ns1:DataType>Code. Type</ns1:DataType> </ns1:Component>
    :ivar seller_event_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Seller Event Identifier.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>An event
        tracking identifier assigned by the seller.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass> <ns1:PropertyTerm>Seller Event
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar buyer_event_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Buyer Event Identifier.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>An event
        tracking identifier assigned by the buyer.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass> <ns1:PropertyTerm>Buyer Event
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar description: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Description.
        Text</ns1:DictionaryEntryName> <ns1:Definition>Definition of the
        discrete activity affecting supply or demand in the supply
        chain</ns1:Definition> <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Retail Event</ns1:ObjectClass>
        <ns1:PropertyTerm>Description</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar period: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event.
        Period</ns1:DictionaryEntryName> <ns1:Definition>The period
        during which the event takes place.</ns1:Definition>
        <ns1:Cardinality>1</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass>
        <ns1:PropertyTerm>Period</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Period</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Period</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar original_document_reference: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Original_ Document
        Reference. Document Reference</ns1:DictionaryEntryName>
        <ns1:Definition>A reference to a Forecast document associated
        with this event.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Original</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Document Reference</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Document
        Reference</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Document
        Reference</ns1:RepresentationTerm> </ns1:Component>
    :ivar signature: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event.
        Signature</ns1:DictionaryEntryName> <ns1:Definition>A signature
        applied to this document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass>
        <ns1:PropertyTerm>Signature</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Signature</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Signature</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar sender_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Sender_ Party.
        Party</ns1:DictionaryEntryName> <ns1:Definition>The party
        sending this document.</ns1:Definition>
        <ns1:Cardinality>1</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Sender</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar receiver_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Receiver_ Party.
        Party</ns1:DictionaryEntryName> <ns1:Definition>The party
        receiving this document.</ns1:Definition>
        <ns1:Cardinality>1</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Receiver</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar buyer_customer_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Buyer_ Customer Party.
        Customer Party</ns1:DictionaryEntryName> <ns1:Definition>The
        buyer.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Retail Event</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Buyer</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Customer Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Customer
        Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Customer Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar seller_supplier_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Seller_ Supplier Party.
        Supplier Party</ns1:DictionaryEntryName> <ns1:Definition>The
        seller.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Retail Event</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Seller</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Supplier Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Supplier
        Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Supplier Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar event_comment: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Event
        Comment</ns1:DictionaryEntryName> <ns1:Definition>A comment
        regarding the event.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass> <ns1:PropertyTerm>Event
        Comment</ns1:PropertyTerm> <ns1:AssociatedObjectClass>Event
        Comment</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Event Comment</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar promotional_event: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Promotional
        Event</ns1:DictionaryEntryName> <ns1:Definition>The description
        of a promotional event associated with this
        event.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Retail Event</ns1:ObjectClass>
        <ns1:PropertyTerm>Promotional Event</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Promotional
        Event</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Promotional
        Event</ns1:RepresentationTerm> </ns1:Component>
    :ivar miscellaneous_event: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Retail Event. Miscellaneous
        Event</ns1:DictionaryEntryName> <ns1:Definition>A miscellaneous
        event associated with this event.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Retail
        Event</ns1:ObjectClass> <ns1:PropertyTerm>Miscellaneous
        Event</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Miscellaneous
        Event</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Miscellaneous
        Event</ns1:RepresentationTerm> </ns1:Component>
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
    note: list[Note] = field(
        default_factory=list,
        metadata={
            "name": "Note",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    retail_event_name: Optional[RetailEventName] = field(
        default=None,
        metadata={
            "name": "RetailEventName",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    retail_event_status_code: Optional[RetailEventStatusCode] = field(
        default=None,
        metadata={
            "name": "RetailEventStatusCode",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            "required": True,
        },
    )
    seller_event_id: Optional[SellerEventId] = field(
        default=None,
        metadata={
            "name": "SellerEventID",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    buyer_event_id: Optional[BuyerEventId] = field(
        default=None,
        metadata={
            "name": "BuyerEventID",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    description: list[Description] = field(
        default_factory=list,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    period: Optional[Period] = field(
        default=None,
        metadata={
            "name": "Period",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "required": True,
        },
    )
    original_document_reference: list[OriginalDocumentReference] = field(
        default_factory=list,
        metadata={
            "name": "OriginalDocumentReference",
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
    sender_party: Optional[SenderParty] = field(
        default=None,
        metadata={
            "name": "SenderParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "required": True,
        },
    )
    receiver_party: Optional[ReceiverParty] = field(
        default=None,
        metadata={
            "name": "ReceiverParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "required": True,
        },
    )
    buyer_customer_party: Optional[BuyerCustomerParty] = field(
        default=None,
        metadata={
            "name": "BuyerCustomerParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    seller_supplier_party: Optional[SellerSupplierParty] = field(
        default=None,
        metadata={
            "name": "SellerSupplierParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    event_comment: list[EventComment] = field(
        default_factory=list,
        metadata={
            "name": "EventComment",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    promotional_event: Optional[PromotionalEvent] = field(
        default=None,
        metadata={
            "name": "PromotionalEvent",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    miscellaneous_event: Optional[MiscellaneousEvent] = field(
        default=None,
        metadata={
            "name": "MiscellaneousEvent",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )


@dataclass
class RetailEvent(RetailEventType):
    """
    This element MUST be conveyed as the root element in any instance document
    based on this Schema expression.
    """

    class Meta:
        namespace = (
            "urn:oasis:names:specification:ubl:schema:xsd:RetailEvent-2"
        )
