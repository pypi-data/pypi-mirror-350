from dataclasses import dataclass, field
from typing import Optional

from generated.ubl.common.ubl_common_aggregate_components_2_1 import (
    DocumentReference,
    InventoryPeriod,
    InventoryReportingParty,
    InventoryReportLine,
    RetailerCustomerParty,
    SellerSupplierParty,
    Signature,
)
from generated.ubl.common.ubl_common_basic_components_2_1 import (
    CopyIndicator,
    CustomizationId,
    DocumentCurrencyCode,
    Id,
    IssueDate,
    IssueTime,
    Note,
    ProfileExecutionId,
    ProfileId,
    UblversionId,
    Uuid,
)
from generated.ubl.common.ubl_common_extension_components_2_1 import (
    Ublextensions,
)

__NAMESPACE__ = (
    "urn:oasis:names:specification:ubl:schema:xsd:InventoryReport-2"
)


@dataclass
class InventoryReportType:
    """<ns1:Component xmlns:ns1="urn:un:unece:uncefact:documentation:2">
    <ns1:ComponentType>ABIE</ns1:ComponentType> <ns1:DictionaryEntryName>Inventory
    Report.

    Details</ns1:DictionaryEntryName> <ns1:Definition>A report on the
    quantities of each item that are, or will be, in stock. This
    document is sent by a Buyer (for example a retailer) to a Seller
    (for example a producer).</ns1:Definition>
    <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
    <ns1:AlternativeBusinessTerms>Storage status
    report.</ns1:AlternativeBusinessTerms> </ns1:Component>

    :ivar ublextensions: A container for all extensions present in the
        document.
    :ivar ublversion_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. UBL Version
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies the earliest version of the UBL 2
        schema for this document type that defines all of the elements
        that might be encountered in the current
        instance.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTerm>UBL Version Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>2.0.5</ns1:Examples> </ns1:Component>
    :ivar customization_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Customization
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies a user-defined customization of UBL
        for a specific use.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTerm>Customization Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>NES</ns1:Examples> </ns1:Component>
    :ivar profile_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Profile Identifier.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>Identifies
        a user-defined profile of the customization of UBL being
        used.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTerm>Profile Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BasicProcurementProcess</ns1:Examples>
        </ns1:Component>
    :ivar profile_execution_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Profile Execution
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies an instance of executing a profile,
        to associate all transactions in a
        collaboration.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTerm>Profile Execution
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BPP-1001</ns1:Examples> </ns1:Component>
    :ivar id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>An
        identifier for the Inventory Report, assigned by the
        Issuer.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTerm>Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:AlternativeBusinessTerms>Document Number, Inventory Report
        Number</ns1:AlternativeBusinessTerms> </ns1:Component>
    :ivar copy_indicator: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Copy_ Indicator.
        Indicator</ns1:DictionaryEntryName> <ns1:Definition>Indicates
        whether this document is a copy (true) or not
        (false).</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Copy</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Indicator</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Indicator</ns1:RepresentationTerm>
        <ns1:DataType>Indicator. Type</ns1:DataType> </ns1:Component>
    :ivar uuid: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. UUID.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>A
        universally unique identifier for an instance of this
        document.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTerm>UUID</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar issue_date: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Issue Date.
        Date</ns1:DictionaryEntryName> <ns1:Definition>The date,
        assigned by the sender, on which this document was
        issued.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Date</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Date</ns1:RepresentationTerm>
        <ns1:DataType>Date. Type</ns1:DataType> </ns1:Component>
    :ivar issue_time: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Issue Time.
        Time</ns1:DictionaryEntryName> <ns1:Definition>The time at which
        the Inventory Report was issued.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Time</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Time</ns1:RepresentationTerm>
        <ns1:DataType>Time. Type</ns1:DataType> </ns1:Component>
    :ivar note: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Note.
        Text</ns1:DictionaryEntryName> <ns1:Definition>Free-form text
        pertinent to this document, conveying information that is not
        contained explicitly in other structures.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTerm>Note</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar document_currency_code: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Document_ Currency
        Code. Code</ns1:DictionaryEntryName> <ns1:Definition>A code
        signifying the currency in which the Document is presented. This
        may be the same currency as the pricing or as the
        tax.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Document</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Currency Code</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Code</ns1:RepresentationTerm>
        <ns1:DataTypeQualifier>Currency</ns1:DataTypeQualifier>
        <ns1:DataType>Currency_ Code. Type</ns1:DataType>
        </ns1:Component>
    :ivar inventory_period: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Inventory_ Period.
        Period</ns1:DictionaryEntryName> <ns1:Definition>The period
        covered by this report.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Inventory</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Period</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Period</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Period</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar document_reference: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Document
        Reference</ns1:DictionaryEntryName> <ns1:Definition>A reference
        to another document associated with this
        document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTerm>Document Reference</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Document
        Reference</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Document
        Reference</ns1:RepresentationTerm> </ns1:Component>
    :ivar signature: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report.
        Signature</ns1:DictionaryEntryName> <ns1:Definition>A signature
        applied to this document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTerm>Signature</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Signature</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Signature</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar retailer_customer_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Retailer_ Customer
        Party. Customer Party</ns1:DictionaryEntryName>
        <ns1:Definition>The retailer, who sends this
        message.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Retailer</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Customer Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Customer
        Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Customer Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar inventory_reporting_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Inventory Reporting_
        Party. Party</ns1:DictionaryEntryName> <ns1:Definition>An
        association to the Party that will really use the Inventory
        report (normally the branch for which the stock is
        reported).</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Inventory
        Reporting</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar seller_supplier_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Seller_ Supplier
        Party. Supplier Party</ns1:DictionaryEntryName>
        <ns1:Definition>The seller.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Seller</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Supplier Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Supplier
        Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Supplier Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar inventory_report_line: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Inventory Report. Inventory Report
        Line</ns1:DictionaryEntryName> <ns1:Definition>A line
        representing a particular item of sale and associated with a
        line in the Catalogue.</ns1:Definition>
        <ns1:Cardinality>1..n</ns1:Cardinality>
        <ns1:ObjectClass>Inventory Report</ns1:ObjectClass>
        <ns1:PropertyTerm>Inventory Report Line</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Inventory Report
        Line</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Inventory Report
        Line</ns1:RepresentationTerm> </ns1:Component>
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
            "required": True,
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
    document_currency_code: Optional[DocumentCurrencyCode] = field(
        default=None,
        metadata={
            "name": "DocumentCurrencyCode",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    inventory_period: Optional[InventoryPeriod] = field(
        default=None,
        metadata={
            "name": "InventoryPeriod",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
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
    signature: list[Signature] = field(
        default_factory=list,
        metadata={
            "name": "Signature",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    retailer_customer_party: Optional[RetailerCustomerParty] = field(
        default=None,
        metadata={
            "name": "RetailerCustomerParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "required": True,
        },
    )
    inventory_reporting_party: Optional[InventoryReportingParty] = field(
        default=None,
        metadata={
            "name": "InventoryReportingParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "required": True,
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
    inventory_report_line: list[InventoryReportLine] = field(
        default_factory=list,
        metadata={
            "name": "InventoryReportLine",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "min_occurs": 1,
        },
    )


@dataclass
class InventoryReport(InventoryReportType):
    """
    This element MUST be conveyed as the root element in any instance document
    based on this Schema expression.
    """

    class Meta:
        namespace = (
            "urn:oasis:names:specification:ubl:schema:xsd:InventoryReport-2"
        )
