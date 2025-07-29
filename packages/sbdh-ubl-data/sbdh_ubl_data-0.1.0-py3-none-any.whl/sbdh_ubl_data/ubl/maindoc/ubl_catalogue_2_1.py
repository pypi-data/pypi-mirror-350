from dataclasses import dataclass, field
from typing import Optional

from generated.ubl.common.ubl_common_aggregate_components_2_1 import (
    CatalogueLine,
    ContractorCustomerParty,
    DocumentReference,
    ProviderParty,
    ReceiverParty,
    ReferencedContract,
    SellerSupplierParty,
    Signature,
    SourceCatalogueReference,
    TradingTerms,
    ValidityPeriod,
)
from generated.ubl.common.ubl_common_basic_components_2_1 import (
    ActionCode,
    CustomizationId,
    Description,
    Id,
    IssueDate,
    IssueTime,
    LineCountNumeric,
    Name,
    Note,
    PreviousVersionId,
    ProfileExecutionId,
    ProfileId,
    RevisionDate,
    RevisionTime,
    UblversionId,
    Uuid,
    VersionId,
)
from generated.ubl.common.ubl_common_extension_components_2_1 import (
    Ublextensions,
)

__NAMESPACE__ = "urn:oasis:names:specification:ubl:schema:xsd:Catalogue-2"


@dataclass
class CatalogueType:
    """<ns1:Component xmlns:ns1="urn:un:unece:uncefact:documentation:2">
    <ns1:ComponentType>ABIE</ns1:ComponentType> <ns1:DictionaryEntryName>Catalogue.

    Details</ns1:DictionaryEntryName> <ns1:Definition>A document that
    describes items, prices, and price validity.</ns1:Definition>
    <ns1:ObjectClass>Catalogue</ns1:ObjectClass> </ns1:Component>

    :ivar ublextensions: A container for all extensions present in the
        document.
    :ivar ublversion_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. UBL Version Identifier.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>Identifies
        the earliest version of the UBL 2 schema for this document type
        that defines all of the elements that might be encountered in
        the current instance.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>UBL Version Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>2.0.5</ns1:Examples> </ns1:Component>
    :ivar customization_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Customization Identifier.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>Identifies
        a user-defined customization of UBL for a specific
        use.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Customization Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>NES</ns1:Examples> </ns1:Component>
    :ivar profile_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Profile Identifier.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>Identifies
        a user-defined profile of the customization of UBL being
        used.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Profile Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BasicProcurementProcess</ns1:Examples>
        </ns1:Component>
    :ivar profile_execution_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Profile Execution
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies an instance of executing a profile,
        to associate all transactions in a
        collaboration.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Profile Execution
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BPP-1001</ns1:Examples> </ns1:Component>
    :ivar id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>An
        identifier for this document, assigned by the
        sender.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar uuid: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. UUID.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>A
        universally unique identifier for an instance of this
        document.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>UUID</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar action_code: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Action Code.
        Code</ns1:DictionaryEntryName> <ns1:Definition>A code signifying
        whether the transaction is a replacement or an
        update.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Action Code</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Code</ns1:RepresentationTerm>
        <ns1:DataType>Code. Type</ns1:DataType> <ns1:Examples>Replace ,
        Update .</ns1:Examples> </ns1:Component>
    :ivar name: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue.
        Name</ns1:DictionaryEntryName> <ns1:Definition>Text, assigned by
        the sender, that identifies this document to business
        users.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Name</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Name</ns1:RepresentationTerm>
        <ns1:DataType>Name. Type</ns1:DataType> <ns1:Examples>winter
        2005 collection </ns1:Examples> </ns1:Component>
    :ivar issue_date: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Issue Date.
        Date</ns1:DictionaryEntryName> <ns1:Definition>The date,
        assigned by the sender, on which this document was
        issued.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Date</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Date</ns1:RepresentationTerm>
        <ns1:DataType>Date. Type</ns1:DataType> </ns1:Component>
    :ivar issue_time: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Issue Time.
        Time</ns1:DictionaryEntryName> <ns1:Definition>The time,
        assigned by the sender, at which this document was
        issued.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Time</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Time</ns1:RepresentationTerm>
        <ns1:DataType>Time. Type</ns1:DataType> </ns1:Component>
    :ivar revision_date: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Revision Date.
        Date</ns1:DictionaryEntryName> <ns1:Definition>The date,
        assigned by the seller party, on which the information in the
        Catalogue was last revised.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Revision Date</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Date</ns1:RepresentationTerm>
        <ns1:DataType>Date. Type</ns1:DataType> </ns1:Component>
    :ivar revision_time: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Revision Time.
        Time</ns1:DictionaryEntryName> <ns1:Definition>The time,
        assigned by the Seller party, at which the information in the
        Catalogue was last revised.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Revision Time</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Time</ns1:RepresentationTerm>
        <ns1:DataType>Time. Type</ns1:DataType> </ns1:Component>
    :ivar note: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Note.
        Text</ns1:DictionaryEntryName> <ns1:Definition>Free-form text
        pertinent to this document, conveying information that is not
        contained explicitly in other structures.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Note</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar description: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Description.
        Text</ns1:DictionaryEntryName> <ns1:Definition>Textual
        description of the document instance.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Description</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> <ns1:Examples>computer
        accessories for laptops </ns1:Examples> </ns1:Component>
    :ivar version_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Version.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>An
        identifier for the current version of the
        Catalogue.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Version</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> <ns1:Examples>1.1
        </ns1:Examples> </ns1:Component>
    :ivar previous_version_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Previous_ Version.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>An
        identifier for the previous version of the Catalogue that is
        superseded by this version.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Previous</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Version</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> <ns1:Examples>1.0
        </ns1:Examples> </ns1:Component>
    :ivar line_count_numeric: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Line Count.
        Numeric</ns1:DictionaryEntryName> <ns1:Definition>The number of
        Catalogue Lines in the document.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Line Count</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Numeric</ns1:RepresentationTerm>
        <ns1:DataType>Numeric. Type</ns1:DataType> </ns1:Component>
    :ivar validity_period: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Validity_ Period.
        Period</ns1:DictionaryEntryName> <ns1:Definition>A period,
        assigned by the seller, during which the information in the
        Catalogue is effective. This may be given as start and end dates
        or as a duration.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Validity</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Period</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Period</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Period</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar referenced_contract: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Referenced_ Contract.
        Contract</ns1:DictionaryEntryName> <ns1:Definition>A contract or
        framework agreement with which this Catalogue is
        associated.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Referenced</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Contract</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Contract</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Contract</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar source_catalogue_reference: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Source_ Catalogue Reference.
        Catalogue Reference</ns1:DictionaryEntryName> <ns1:Definition>A
        reference to the source catalogue.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Source</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Catalogue Reference</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Catalogue
        Reference</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Catalogue
        Reference</ns1:RepresentationTerm> </ns1:Component>
    :ivar document_reference: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Document
        Reference</ns1:DictionaryEntryName> <ns1:Definition>A reference
        to another document associated with this
        document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Document Reference</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Document
        Reference</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Document
        Reference</ns1:RepresentationTerm> </ns1:Component>
    :ivar signature: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue.
        Signature</ns1:DictionaryEntryName> <ns1:Definition>A signature
        applied to this document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Signature</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Signature</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Signature</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar provider_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Provider_ Party.
        Party</ns1:DictionaryEntryName> <ns1:Definition>The party
        providing the Catalogue.</ns1:Definition>
        <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Provider</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar receiver_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Receiver_ Party.
        Party</ns1:DictionaryEntryName> <ns1:Definition>The party
        receiving the Catalogue.</ns1:Definition>
        <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Receiver</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar seller_supplier_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Seller_ Supplier Party.
        Supplier Party</ns1:DictionaryEntryName> <ns1:Definition>The
        seller.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Seller</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Supplier Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Supplier
        Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Supplier Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar contractor_customer_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Contractor_ Customer Party.
        Customer Party</ns1:DictionaryEntryName> <ns1:Definition>The
        customer party responsible for the contracts with which the
        Catalogue is associated.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Contractor</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Customer Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Customer
        Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Customer Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar trading_terms: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Trading
        Terms</ns1:DictionaryEntryName> <ns1:Definition>The trading
        terms associated with this Catalogue.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Trading Terms</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Trading
        Terms</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Trading Terms</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar catalogue_line: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Catalogue. Catalogue
        Line</ns1:DictionaryEntryName> <ns1:Definition>A line in a
        Catalogue describing an item of sale.</ns1:Definition>
        <ns1:Cardinality>1..n</ns1:Cardinality>
        <ns1:ObjectClass>Catalogue</ns1:ObjectClass>
        <ns1:PropertyTerm>Catalogue Line</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Catalogue
        Line</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Catalogue Line</ns1:RepresentationTerm>
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
    uuid: Optional[Uuid] = field(
        default=None,
        metadata={
            "name": "UUID",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    action_code: Optional[ActionCode] = field(
        default=None,
        metadata={
            "name": "ActionCode",
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
    revision_date: Optional[RevisionDate] = field(
        default=None,
        metadata={
            "name": "RevisionDate",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    revision_time: Optional[RevisionTime] = field(
        default=None,
        metadata={
            "name": "RevisionTime",
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
    description: list[Description] = field(
        default_factory=list,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
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
    previous_version_id: Optional[PreviousVersionId] = field(
        default=None,
        metadata={
            "name": "PreviousVersionID",
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
    validity_period: list[ValidityPeriod] = field(
        default_factory=list,
        metadata={
            "name": "ValidityPeriod",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    referenced_contract: list[ReferencedContract] = field(
        default_factory=list,
        metadata={
            "name": "ReferencedContract",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    source_catalogue_reference: Optional[SourceCatalogueReference] = field(
        default=None,
        metadata={
            "name": "SourceCatalogueReference",
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
    provider_party: Optional[ProviderParty] = field(
        default=None,
        metadata={
            "name": "ProviderParty",
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
    seller_supplier_party: Optional[SellerSupplierParty] = field(
        default=None,
        metadata={
            "name": "SellerSupplierParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    contractor_customer_party: Optional[ContractorCustomerParty] = field(
        default=None,
        metadata={
            "name": "ContractorCustomerParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    trading_terms: list[TradingTerms] = field(
        default_factory=list,
        metadata={
            "name": "TradingTerms",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    catalogue_line: list[CatalogueLine] = field(
        default_factory=list,
        metadata={
            "name": "CatalogueLine",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "min_occurs": 1,
        },
    )


@dataclass
class Catalogue(CatalogueType):
    """
    This element MUST be conveyed as the root element in any instance document
    based on this Schema expression.
    """

    class Meta:
        namespace = "urn:oasis:names:specification:ubl:schema:xsd:Catalogue-2"
