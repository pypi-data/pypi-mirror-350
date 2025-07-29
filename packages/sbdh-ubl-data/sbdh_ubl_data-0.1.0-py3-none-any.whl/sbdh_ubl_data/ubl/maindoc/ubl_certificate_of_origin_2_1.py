from dataclasses import dataclass, field
from typing import Optional

from generated.ubl.common.ubl_common_aggregate_components_2_1 import (
    CertificateOfOriginApplication,
    EmbassyEndorsement,
    EndorserParty,
    ExporterParty,
    ImporterParty,
    InsuranceEndorsement,
    IssuerEndorsement,
    Signature,
)
from generated.ubl.common.ubl_common_basic_components_2_1 import (
    CustomizationId,
    Description,
    Id,
    IssueDate,
    IssueTime,
    Note,
    ProfileExecutionId,
    ProfileId,
    UblversionId,
    Uuid,
    VersionId,
)
from generated.ubl.common.ubl_common_extension_components_2_1 import (
    Ublextensions,
)

__NAMESPACE__ = (
    "urn:oasis:names:specification:ubl:schema:xsd:CertificateOfOrigin-2"
)


@dataclass
class CertificateOfOriginType:
    """<ns1:Component xmlns:ns1="urn:un:unece:uncefact:documentation:2">
    <ns1:ComponentType>ABIE</ns1:ComponentType>
    <ns1:DictionaryEntryName>Certificate Of Origin.

    Details</ns1:DictionaryEntryName> <ns1:Definition>A document that
    describes the Certificate of Origin.</ns1:Definition>
    <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
    </ns1:Component>

    :ivar ublextensions: A container for all extensions present in the
        document.
    :ivar ublversion_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. UBL Version
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies the earliest version of the UBL 2
        schema for this document type that defines all of the elements
        that might be encountered in the current
        instance.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>UBL Version Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>2.0.5</ns1:Examples> </ns1:Component>
    :ivar customization_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Customization
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies a user-defined customization of UBL
        for a specific use.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>Customization Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>NES</ns1:Examples> </ns1:Component>
    :ivar profile_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Profile
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies a user-defined profile of the
        customization of UBL being used.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>Profile Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BasicProcurementProcess</ns1:Examples>
        </ns1:Component>
    :ivar profile_execution_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Profile
        Execution Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies an instance of executing a profile,
        to associate all transactions in a
        collaboration.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>Profile Execution
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BPP-1001</ns1:Examples> </ns1:Component>
    :ivar id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>An
        identifier for this document, assigned by the
        sender.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar uuid: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. UUID.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>A
        universally unique identifier for an instance of this
        document.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>UUID</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar issue_date: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Issue Date.
        Date</ns1:DictionaryEntryName> <ns1:Definition>The date,
        assigned by the sender, on which this document was
        issued.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Date</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Date</ns1:RepresentationTerm>
        <ns1:DataType>Date. Type</ns1:DataType> </ns1:Component>
    :ivar issue_time: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Issue Time.
        Time</ns1:DictionaryEntryName> <ns1:Definition>The time,
        assigned by the sender, at which this document was
        issued.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Time</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Time</ns1:RepresentationTerm>
        <ns1:DataType>Time. Type</ns1:DataType> </ns1:Component>
    :ivar description: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Description.
        Text</ns1:DictionaryEntryName> <ns1:Definition>Textual
        description of the document instance.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>Description</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar note: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Note.
        Text</ns1:DictionaryEntryName> <ns1:Definition>Free-form text
        pertinent to this document, conveying information that is not
        contained explicitly in other structures.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>Note</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar version_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Version.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>Identifies
        the version of this Certificate of Origin.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>Version</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar signature: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin.
        Signature</ns1:DictionaryEntryName> <ns1:Definition>A signature
        applied to this document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>Signature</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Signature</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Signature</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar exporter_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Exporter_ Party.
        Party</ns1:DictionaryEntryName> <ns1:Definition>The Party who
        makes the export declaration, or on whose behalf the export
        declaration is made, and who is the owner of the goods or has
        similar right of disposal over them at the time when the
        declaration is accepted.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Exporter</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        <ns1:AlternativeBusinessTerms>Exporter (WCO ID 41 and
        42)</ns1:AlternativeBusinessTerms> </ns1:Component>
    :ivar importer_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Importer_ Party.
        Party</ns1:DictionaryEntryName> <ns1:Definition>The Party who
        makes an import declaration, or on whose behalf a Customs
        clearing agent or other authorized person makes an import
        declaration. This may include a person who has possession of the
        goods or to whom the goods are consigned.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Importer</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        <ns1:AlternativeBusinessTerms>Importer (WCO ID 39 and
        40)</ns1:AlternativeBusinessTerms> </ns1:Component>
    :ivar endorser_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Endorser
        Party</ns1:DictionaryEntryName> <ns1:Definition>The Party
        providing the endorsement.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>Endorser Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Endorser
        Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Endorser Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar certificate_of_origin_application: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Certificate Of
        Origin Application</ns1:DictionaryEntryName>
        <ns1:Definition>Details of the application for a Certificate of
        Origin.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTerm>Certificate Of Origin
        Application</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Certificate Of Origin
        Application</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Certificate Of Origin
        Application</ns1:RepresentationTerm> </ns1:Component>
    :ivar issuer_endorsement: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Issuer_
        Endorsement. Endorsement</ns1:DictionaryEntryName>
        <ns1:Definition>Issuer Endorsement details.</ns1:Definition>
        <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Issuer</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Endorsement</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Endorsement</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Endorsement</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar embassy_endorsement: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Embassy_
        Endorsement. Endorsement</ns1:DictionaryEntryName>
        <ns1:Definition>Embassy Endorsement details.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Embassy</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Endorsement</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Endorsement</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Endorsement</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar insurance_endorsement: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Certificate Of Origin. Insurance_
        Endorsement. Endorsement</ns1:DictionaryEntryName>
        <ns1:Definition>Insurance Endorsement details.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Certificate Of Origin</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Insurance</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Endorsement</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Endorsement</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Endorsement</ns1:RepresentationTerm>
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
    version_id: Optional[VersionId] = field(
        default=None,
        metadata={
            "name": "VersionID",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
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
    exporter_party: Optional[ExporterParty] = field(
        default=None,
        metadata={
            "name": "ExporterParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    importer_party: Optional[ImporterParty] = field(
        default=None,
        metadata={
            "name": "ImporterParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    endorser_party: list[EndorserParty] = field(
        default_factory=list,
        metadata={
            "name": "EndorserParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    certificate_of_origin_application: Optional[
        CertificateOfOriginApplication
    ] = field(
        default=None,
        metadata={
            "name": "CertificateOfOriginApplication",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "required": True,
        },
    )
    issuer_endorsement: Optional[IssuerEndorsement] = field(
        default=None,
        metadata={
            "name": "IssuerEndorsement",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "required": True,
        },
    )
    embassy_endorsement: Optional[EmbassyEndorsement] = field(
        default=None,
        metadata={
            "name": "EmbassyEndorsement",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    insurance_endorsement: Optional[InsuranceEndorsement] = field(
        default=None,
        metadata={
            "name": "InsuranceEndorsement",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )


@dataclass
class CertificateOfOrigin(CertificateOfOriginType):
    """
    This element MUST be conveyed as the root element in any instance document
    based on this Schema expression.
    """

    class Meta:
        namespace = "urn:oasis:names:specification:ubl:schema:xsd:CertificateOfOrigin-2"
