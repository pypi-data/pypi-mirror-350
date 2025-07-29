from dataclasses import dataclass, field
from typing import Optional

from generated.ubl.common.ubl_common_aggregate_components_2_1 import (
    CarrierParty,
    ConsignorParty,
    DocumentReference,
    ExchangeRate,
    FreightForwarderParty,
    Shipment,
    Signature,
)
from generated.ubl.common.ubl_common_basic_components_2_1 import (
    AdValoremIndicator,
    CarrierAssignedId,
    CustomizationId,
    DeclaredCarriageValueAmount,
    Description,
    DocumentStatusCode,
    Id,
    IssueDate,
    IssueTime,
    Name,
    Note,
    OtherInstruction,
    ProfileExecutionId,
    ProfileId,
    ShippingOrderId,
    ToOrderIndicator,
    UblversionId,
    Uuid,
)
from generated.ubl.common.ubl_common_extension_components_2_1 import (
    Ublextensions,
)

__NAMESPACE__ = (
    "urn:oasis:names:specification:ubl:schema:xsd:ForwardingInstructions-2"
)


@dataclass
class ForwardingInstructionsType:
    """<ns1:Component xmlns:ns1="urn:un:unece:uncefact:documentation:2">
    <ns1:ComponentType>ABIE</ns1:ComponentType> <ns1:DictionaryEntryName>Forwarding
    Instructions.

    Details</ns1:DictionaryEntryName> <ns1:Definition>A document issued
    to a forwarder, giving instructions regarding the action to be taken
    for the forwarding of goods described therein. Forwarding
    Instructions is used by any party who gives instructions for the
    transportation services required for a consignment of goods to any
    party who is contracted to provide the transportation services. The
    parties who issue this document are commonly referred to as the
    shipper or consignor, while the parties who receive this document
    are forwarders, carriers, shipping agents, etc. This document may
    also be issued by a forwarder or shipping agent in its capacity as a
    shipper. This document can be used to arrange for the transportation
    (1) of different types of goods or cargoes; (2) whether
    containerized or non-containerized; (3) through different modes of
    transport including multi-modal; and (4) from any origin to any
    destination.</ns1:Definition> <ns1:ObjectClass>Forwarding
    Instructions</ns1:ObjectClass>
    <ns1:AlternativeBusinessTerms>Forwarding Instruction, Freight
    Forwarding Instruction, Shippers Letter of Instruction, Shipper's
    Letter of Instruction, Shipping
    Instruction</ns1:AlternativeBusinessTerms> </ns1:Component>

    :ivar ublextensions: A container for all extensions present in the
        document.
    :ivar ublversion_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. UBL Version
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies the earliest version of the UBL 2
        schema for this document type that defines all of the elements
        that might be encountered in the current
        instance.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>UBL Version Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>2.0.5</ns1:Examples> </ns1:Component>
    :ivar customization_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Customization
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies a user-defined customization of UBL
        for a specific use.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Customization Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>NES</ns1:Examples> </ns1:Component>
    :ivar profile_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Profile
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies a user-defined profile of the
        customization of UBL being used.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Profile Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BasicProcurementProcess</ns1:Examples>
        </ns1:Component>
    :ivar profile_execution_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Profile
        Execution Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies an instance of executing a profile,
        to associate all transactions in a
        collaboration.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Profile Execution
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BPP-1001</ns1:Examples> </ns1:Component>
    :ivar id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>An
        identifier for this document, assigned by the
        sender.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar carrier_assigned_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Carrier
        Assigned_ Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Reference number assigned by a carrier or its
        agent to identify a specific shipment, such as a booking
        reference number when cargo space is reserved prior to
        loading.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Carrier
        Assigned</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar uuid: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. UUID.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>A
        universally unique identifier for an instance of this
        document.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>UUID</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar issue_date: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Issue Date.
        Date</ns1:DictionaryEntryName> <ns1:Definition>The date,
        assigned by the sender, on which this document was
        issued.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Date</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Date</ns1:RepresentationTerm>
        <ns1:DataType>Date. Type</ns1:DataType> </ns1:Component>
    :ivar issue_time: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Issue Time.
        Time</ns1:DictionaryEntryName> <ns1:Definition>The time,
        assigned by the sender, at which this document was
        issued.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Time</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Time</ns1:RepresentationTerm>
        <ns1:DataType>Time. Type</ns1:DataType> </ns1:Component>
    :ivar name: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions.
        Name</ns1:DictionaryEntryName> <ns1:Definition>Text, assigned by
        the sender, that identifies this document to business
        users.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Name</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Name</ns1:RepresentationTerm>
        <ns1:DataType>Name. Type</ns1:DataType> </ns1:Component>
    :ivar description: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Description.
        Text</ns1:DictionaryEntryName> <ns1:Definition>Textual
        description of the document instance.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Description</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar note: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Note.
        Text</ns1:DictionaryEntryName> <ns1:Definition>Free-form text
        pertinent to this document, conveying information that is not
        contained explicitly in other structures.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Note</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar document_status_code: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Document
        Status Code. Code</ns1:DictionaryEntryName> <ns1:Definition>A
        code signifying the status of the Forwarding Instructions with
        respect to its original state. This code may be used if the
        document precedes the event and is subsequently found to be
        incorrect and in need of cancellation or
        revision.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Document Status Code</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Code</ns1:RepresentationTerm>
        <ns1:DataTypeQualifier>Document Status</ns1:DataTypeQualifier>
        <ns1:DataType>Document Status_ Code. Type</ns1:DataType>
        </ns1:Component>
    :ivar shipping_order_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Shipping Order
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Reference number to identify a Shipping
        Order.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Shipping Order Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar to_order_indicator: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. To Order_
        Indicator. Indicator</ns1:DictionaryEntryName>
        <ns1:Definition>Indicates whether the transport document is
        consigned to order.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>To Order</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Indicator</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Indicator</ns1:RepresentationTerm>
        <ns1:DataType>Indicator. Type</ns1:DataType> </ns1:Component>
    :ivar ad_valorem_indicator: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Ad Valorem_
        Indicator. Indicator</ns1:DictionaryEntryName> <ns1:Definition>A
        term used in commerce in reference to certain duties, called ad
        valorem duties, which are levied on commodities at certain rates
        per centum on their value.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Ad
        Valorem</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Indicator</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Indicator</ns1:RepresentationTerm>
        <ns1:DataType>Indicator. Type</ns1:DataType> </ns1:Component>
    :ivar declared_carriage_value_amount: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Declared
        Carriage_ Value. Amount</ns1:DictionaryEntryName>
        <ns1:Definition>Value declared by the shipper or his agent
        solely for the purpose of varying the carrier's level of
        liability from that provided in the contract of carriage in case
        of loss or damage to goods or delayed delivery.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Declared
        Carriage</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Value</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Amount</ns1:RepresentationTerm>
        <ns1:DataType>Amount. Type</ns1:DataType> </ns1:Component>
    :ivar other_instruction: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Other_
        Instruction. Text</ns1:DictionaryEntryName>
        <ns1:Definition>Contains other free-text instructions to the
        forwarders or carriers related to the shipment. This should only
        be used where such information cannot be represented in other
        structured information entities within the
        document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Other</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Instruction</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar consignor_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Consignor_
        Party. Party</ns1:DictionaryEntryName> <ns1:Definition>The party
        consigning goods, as stipulated in the transport contract by the
        party ordering transport.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Consignor</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        <ns1:AlternativeBusinessTerms>Consignor (WCO ID 71 and
        72)</ns1:AlternativeBusinessTerms> </ns1:Component>
    :ivar carrier_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Carrier_
        Party. Party</ns1:DictionaryEntryName> <ns1:Definition>The party
        providing the transport of goods between named
        points.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Carrier</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        <ns1:AlternativeBusinessTerms>Transport Company, Shipping Line,
        NVOCC, Airline, Haulier, Courier, Carrier (WCO ID 49 and
        50)</ns1:AlternativeBusinessTerms> </ns1:Component>
    :ivar freight_forwarder_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Freight
        Forwarder_ Party. Party</ns1:DictionaryEntryName>
        <ns1:Definition>A party combining individual smaller
        consignments into a single larger shipment (a so-called
        consolidated consignment or shipment) that is sent to a
        counterpart who mirrors the consolidator's activity by dividing
        the consolidated consignment into its original
        components.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Freight
        Forwarder</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        <ns1:AlternativeBusinessTerms>Consolidator (WCO ID 192 AND
        193)</ns1:AlternativeBusinessTerms> </ns1:Component>
    :ivar shipment: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions.
        Shipment</ns1:DictionaryEntryName> <ns1:Definition>An
        identifiable collection of one or more goods items to be
        transported between the seller party and the buyer
        party.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Shipment</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Shipment</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Shipment</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar document_reference: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Document
        Reference</ns1:DictionaryEntryName> <ns1:Definition>A reference
        to another document associated with this
        document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Document Reference</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Document
        Reference</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Document
        Reference</ns1:RepresentationTerm> </ns1:Component>
    :ivar exchange_rate: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions. Exchange
        Rate</ns1:DictionaryEntryName> <ns1:Definition>Information about
        the rate of exchange (conversion) between two
        currencies.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Exchange Rate</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Exchange
        Rate</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Exchange Rate</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar signature: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Forwarding Instructions.
        Signature</ns1:DictionaryEntryName> <ns1:Definition>A signature
        applied to this document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Forwarding Instructions</ns1:ObjectClass>
        <ns1:PropertyTerm>Signature</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Signature</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Signature</ns1:RepresentationTerm>
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
    carrier_assigned_id: Optional[CarrierAssignedId] = field(
        default=None,
        metadata={
            "name": "CarrierAssignedID",
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
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "Name",
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
    note: list[Note] = field(
        default_factory=list,
        metadata={
            "name": "Note",
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
    shipping_order_id: Optional[ShippingOrderId] = field(
        default=None,
        metadata={
            "name": "ShippingOrderID",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    to_order_indicator: Optional[ToOrderIndicator] = field(
        default=None,
        metadata={
            "name": "ToOrderIndicator",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    ad_valorem_indicator: Optional[AdValoremIndicator] = field(
        default=None,
        metadata={
            "name": "AdValoremIndicator",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    declared_carriage_value_amount: Optional[DeclaredCarriageValueAmount] = (
        field(
            default=None,
            metadata={
                "name": "DeclaredCarriageValueAmount",
                "type": "Element",
                "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            },
        )
    )
    other_instruction: list[OtherInstruction] = field(
        default_factory=list,
        metadata={
            "name": "OtherInstruction",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    consignor_party: Optional[ConsignorParty] = field(
        default=None,
        metadata={
            "name": "ConsignorParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    carrier_party: Optional[CarrierParty] = field(
        default=None,
        metadata={
            "name": "CarrierParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    freight_forwarder_party: Optional[FreightForwarderParty] = field(
        default=None,
        metadata={
            "name": "FreightForwarderParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    shipment: Optional[Shipment] = field(
        default=None,
        metadata={
            "name": "Shipment",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "required": True,
        },
    )
    document_reference: list[DocumentReference] = field(
        default_factory=list,
        metadata={
            "name": "DocumentReference",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    exchange_rate: list[ExchangeRate] = field(
        default_factory=list,
        metadata={
            "name": "ExchangeRate",
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


@dataclass
class ForwardingInstructions(ForwardingInstructionsType):
    """
    This element MUST be conveyed as the root element in any instance document
    based on this Schema expression.
    """

    class Meta:
        namespace = "urn:oasis:names:specification:ubl:schema:xsd:ForwardingInstructions-2"
