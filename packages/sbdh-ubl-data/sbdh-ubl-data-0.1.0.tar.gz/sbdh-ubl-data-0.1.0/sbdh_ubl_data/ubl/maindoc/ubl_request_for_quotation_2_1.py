from dataclasses import dataclass, field
from typing import Optional

from generated.ubl.common.ubl_common_aggregate_components_2_1 import (
    AdditionalDocumentReference,
    BuyerCustomerParty,
    CatalogueDocumentReference,
    Contract,
    Delivery,
    DeliveryTerms,
    DestinationCountry,
    OriginatorCustomerParty,
    RequestedValidityPeriod,
    RequestForQuotationLine,
    SellerSupplierParty,
    Signature,
)
from generated.ubl.common.ubl_common_basic_components_2_1 import (
    CopyIndicator,
    CustomizationId,
    Id,
    IssueDate,
    IssueTime,
    LineCountNumeric,
    Note,
    PricingCurrencyCode,
    ProfileExecutionId,
    ProfileId,
    SubmissionDueDate,
    UblversionId,
    Uuid,
)
from generated.ubl.common.ubl_common_extension_components_2_1 import (
    Ublextensions,
)

__NAMESPACE__ = (
    "urn:oasis:names:specification:ubl:schema:xsd:RequestForQuotation-2"
)


@dataclass
class RequestForQuotationType:
    """<ns1:Component xmlns:ns1="urn:un:unece:uncefact:documentation:2">
    <ns1:ComponentType>ABIE</ns1:ComponentType> <ns1:DictionaryEntryName>Request
    For Quotation.

    Details</ns1:DictionaryEntryName> <ns1:Definition>A document used to
    request a Quotation for goods and services from a
    Seller.</ns1:Definition> <ns1:ObjectClass>Request For
    Quotation</ns1:ObjectClass> <ns1:AlternativeBusinessTerms>Purchase
    Order</ns1:AlternativeBusinessTerms> </ns1:Component>

    :ivar ublextensions: A container for all extensions present in the
        document.
    :ivar ublversion_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. UBL Version
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies the earliest version of the UBL 2
        schema for this document type that defines all of the elements
        that might be encountered in the current
        instance.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass> <ns1:PropertyTerm>UBL Version
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>2.0.5</ns1:Examples> </ns1:Component>
    :ivar customization_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Customization
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies a user-defined customization of UBL
        for a specific use.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass> <ns1:PropertyTerm>Customization
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>NES</ns1:Examples> </ns1:Component>
    :ivar profile_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Profile
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies a user-defined profile of the
        customization of UBL being used.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass> <ns1:PropertyTerm>Profile
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BasicProcurementProcess</ns1:Examples>
        </ns1:Component>
    :ivar profile_execution_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Profile
        Execution Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies an instance of executing a profile,
        to associate all transactions in a
        collaboration.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass> <ns1:PropertyTerm>Profile
        Execution Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BPP-1001</ns1:Examples> </ns1:Component>
    :ivar id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>An
        identifier for this document, assigned by the
        sender.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Request For Quotation</ns1:ObjectClass>
        <ns1:PropertyTerm>Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar copy_indicator: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Copy_ Indicator.
        Indicator</ns1:DictionaryEntryName> <ns1:Definition>Indicates
        whether this document is a copy (true) or not
        (false).</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Copy</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Indicator</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Indicator</ns1:RepresentationTerm>
        <ns1:DataType>Indicator. Type</ns1:DataType> </ns1:Component>
    :ivar uuid: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. UUID.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>A
        universally unique identifier for an instance of this
        document.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTerm>UUID</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar issue_date: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Issue Date.
        Date</ns1:DictionaryEntryName> <ns1:Definition>The date,
        assigned by the sender, on which this document was
        issued.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Request For Quotation</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Date</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Date</ns1:RepresentationTerm>
        <ns1:DataType>Date. Type</ns1:DataType> </ns1:Component>
    :ivar issue_time: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Issue Time.
        Time</ns1:DictionaryEntryName> <ns1:Definition>The time,
        assigned by the sender, at which this document was
        issued.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Request For Quotation</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Time</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Time</ns1:RepresentationTerm>
        <ns1:DataType>Time. Type</ns1:DataType> </ns1:Component>
    :ivar submission_due_date: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Submission Due
        Date. Date</ns1:DictionaryEntryName> <ns1:Definition>The due
        date for submission of the Quotation.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass> <ns1:PropertyTerm>Submission Due
        Date</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Date</ns1:RepresentationTerm>
        <ns1:DataType>Date. Type</ns1:DataType> </ns1:Component>
    :ivar note: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Note.
        Text</ns1:DictionaryEntryName> <ns1:Definition>Free-form text
        pertinent to this document, conveying information that is not
        contained explicitly in other structures.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTerm>Note</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar pricing_currency_code: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Pricing_
        Currency Code. Code</ns1:DictionaryEntryName>
        <ns1:Definition>The currency that the Seller should use to price
        the Quotation.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Pricing</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Currency Code</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Code</ns1:RepresentationTerm>
        <ns1:DataTypeQualifier>Currency</ns1:DataTypeQualifier>
        <ns1:DataType>Currency_ Code. Type</ns1:DataType>
        </ns1:Component>
    :ivar line_count_numeric: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Line Count.
        Numeric</ns1:DictionaryEntryName> <ns1:Definition>The number of
        Request For Quotation Lines in this document.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass> <ns1:PropertyTerm>Line
        Count</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Numeric</ns1:RepresentationTerm>
        <ns1:DataType>Numeric. Type</ns1:DataType> </ns1:Component>
    :ivar requested_validity_period: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Requested
        Validity_ Period. Period</ns1:DictionaryEntryName>
        <ns1:Definition>The validity period requested for this
        Quotation.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Requested
        Validity</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Period</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Period</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Period</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar catalogue_document_reference: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Catalogue_
        Document Reference. Document Reference</ns1:DictionaryEntryName>
        <ns1:Definition>The Catalogue on which this Request for
        Quotation is based.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Catalogue</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Document Reference</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Document
        Reference</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Document
        Reference</ns1:RepresentationTerm> </ns1:Component>
    :ivar additional_document_reference: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Additional_
        Document Reference. Document Reference</ns1:DictionaryEntryName>
        <ns1:Definition>A reference to an additional document associated
        with this document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Additional</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Document Reference</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Document
        Reference</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Document
        Reference</ns1:RepresentationTerm> </ns1:Component>
    :ivar signature: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation.
        Signature</ns1:DictionaryEntryName> <ns1:Definition>A signature
        applied to this document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTerm>Signature</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Signature</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Signature</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar originator_customer_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Originator_
        Customer Party. Customer Party</ns1:DictionaryEntryName>
        <ns1:Definition>The originator.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Originator</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Customer Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Customer
        Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Customer Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar seller_supplier_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Seller_ Supplier
        Party. Supplier Party</ns1:DictionaryEntryName>
        <ns1:Definition>The seller.</ns1:Definition>
        <ns1:Cardinality>1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Seller</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Supplier Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Supplier
        Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Supplier Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar buyer_customer_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Buyer_ Customer
        Party. Customer Party</ns1:DictionaryEntryName>
        <ns1:Definition>The buyer.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Buyer</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Customer Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Customer
        Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Customer Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar delivery: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation.
        Delivery</ns1:DictionaryEntryName> <ns1:Definition>A delivery
        associated with this document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTerm>Delivery</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Delivery</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Delivery</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar delivery_terms: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Delivery
        Terms</ns1:DictionaryEntryName> <ns1:Definition>A set of
        delivery terms associated with this document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass> <ns1:PropertyTerm>Delivery
        Terms</ns1:PropertyTerm> <ns1:AssociatedObjectClass>Delivery
        Terms</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Delivery Terms</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar destination_country: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Destination_
        Country. Country</ns1:DictionaryEntryName> <ns1:Definition>The
        country of destination of potential orders (for customs
        purposes).</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Destination</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Country</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Country</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Country</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar contract: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation.
        Contract</ns1:DictionaryEntryName> <ns1:Definition>A contract
        associated with this Request for Quotation..</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass>
        <ns1:PropertyTerm>Contract</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Contract</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Contract</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar request_for_quotation_line: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Request For Quotation. Request For
        Quotation Line</ns1:DictionaryEntryName> <ns1:Definition>A line
        specifying a kind of item of sale.</ns1:Definition>
        <ns1:Cardinality>1..n</ns1:Cardinality> <ns1:ObjectClass>Request
        For Quotation</ns1:ObjectClass> <ns1:PropertyTerm>Request For
        Quotation Line</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Request For Quotation
        Line</ns1:AssociatedObjectClass> <ns1:RepresentationTerm>Request
        For Quotation Line</ns1:RepresentationTerm> </ns1:Component>
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
            "required": True,
        },
    )
    issue_time: Optional[IssueTime] = field(
        default=None,
        metadata={
            "name": "IssueTime",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            "required": True,
        },
    )
    submission_due_date: Optional[SubmissionDueDate] = field(
        default=None,
        metadata={
            "name": "SubmissionDueDate",
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
    pricing_currency_code: Optional[PricingCurrencyCode] = field(
        default=None,
        metadata={
            "name": "PricingCurrencyCode",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    line_count_numeric: Optional[LineCountNumeric] = field(
        default=None,
        metadata={
            "name": "LineCountNumeric",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    requested_validity_period: Optional[RequestedValidityPeriod] = field(
        default=None,
        metadata={
            "name": "RequestedValidityPeriod",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    catalogue_document_reference: Optional[CatalogueDocumentReference] = field(
        default=None,
        metadata={
            "name": "CatalogueDocumentReference",
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
    signature: list[Signature] = field(
        default_factory=list,
        metadata={
            "name": "Signature",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    originator_customer_party: Optional[OriginatorCustomerParty] = field(
        default=None,
        metadata={
            "name": "OriginatorCustomerParty",
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
    delivery: list[Delivery] = field(
        default_factory=list,
        metadata={
            "name": "Delivery",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    delivery_terms: list[DeliveryTerms] = field(
        default_factory=list,
        metadata={
            "name": "DeliveryTerms",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    destination_country: Optional[DestinationCountry] = field(
        default=None,
        metadata={
            "name": "DestinationCountry",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    contract: list[Contract] = field(
        default_factory=list,
        metadata={
            "name": "Contract",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    request_for_quotation_line: list[RequestForQuotationLine] = field(
        default_factory=list,
        metadata={
            "name": "RequestForQuotationLine",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "min_occurs": 1,
        },
    )


@dataclass
class RequestForQuotation(RequestForQuotationType):
    """
    This element MUST be conveyed as the root element in any instance document
    based on this Schema expression.
    """

    class Meta:
        namespace = "urn:oasis:names:specification:ubl:schema:xsd:RequestForQuotation-2"
