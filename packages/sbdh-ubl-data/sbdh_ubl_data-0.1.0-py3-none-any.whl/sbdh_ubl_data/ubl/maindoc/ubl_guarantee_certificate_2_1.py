from dataclasses import dataclass, field
from typing import Optional

from generated.ubl.common.ubl_common_aggregate_components_2_1 import (
    ApplicablePeriod,
    ApplicableRegulation,
    BeneficiaryParty,
    GuaranteeDocumentReference,
    GuarantorParty,
    ImmobilizedSecurity,
    InterestedParty,
    Signature,
)
from generated.ubl.common.ubl_common_basic_components_2_1 import (
    ConstitutionCode,
    ContractFolderId,
    CopyIndicator,
    CustomizationId,
    GuaranteeTypeCode,
    Id,
    IssueDate,
    IssueTime,
    LiabilityAmount,
    Note,
    ProfileExecutionId,
    ProfileId,
    Purpose,
    UblversionId,
    Uuid,
)
from generated.ubl.common.ubl_common_extension_components_2_1 import (
    Ublextensions,
)

__NAMESPACE__ = (
    "urn:oasis:names:specification:ubl:schema:xsd:GuaranteeCertificate-2"
)


@dataclass
class GuaranteeCertificateType:
    """<ns1:Component xmlns:ns1="urn:un:unece:uncefact:documentation:2">
    <ns1:ComponentType>ABIE</ns1:ComponentType> <ns1:DictionaryEntryName>Guarantee
    Certificate.

    Details</ns1:DictionaryEntryName> <ns1:Definition>A document to
    notify the deposit of a bid bond guarantee.</ns1:Definition>
    <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
    </ns1:Component>

    :ivar ublextensions: A container for all extensions present in the
        document.
    :ivar ublversion_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. UBL Version
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies the earliest version of the UBL 2
        schema for this document type that defines all of the elements
        that might be encountered in the current
        instance.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>UBL Version Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>2.0.5</ns1:Examples> </ns1:Component>
    :ivar customization_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Customization
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies a user-defined customization of UBL
        for a specific use.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Customization Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>NES</ns1:Examples> </ns1:Component>
    :ivar profile_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Profile
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies a user-defined profile of the
        customization of UBL being used.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Profile Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BasicProcurementProcess</ns1:Examples>
        </ns1:Component>
    :ivar profile_execution_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Profile
        Execution Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>Identifies an instance of executing a profile,
        to associate all transactions in a
        collaboration.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Profile Execution
        Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType>
        <ns1:Examples>BPP-1001</ns1:Examples> </ns1:Component>
    :ivar id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>An
        identifier for this document, assigned by the
        sender.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar copy_indicator: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Copy_ Indicator.
        Indicator</ns1:DictionaryEntryName> <ns1:Definition>Indicates
        whether this document is a copy (true) or not
        (false).</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Copy</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Indicator</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Indicator</ns1:RepresentationTerm>
        <ns1:DataType>Indicator. Type</ns1:DataType> </ns1:Component>
    :ivar uuid: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. UUID.
        Identifier</ns1:DictionaryEntryName> <ns1:Definition>A
        universally unique identifier for an instance of this
        document.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>UUID</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar contract_folder_id: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Contract Folder
        Identifier. Identifier</ns1:DictionaryEntryName>
        <ns1:Definition>An identifier, assigned by the sender, for the
        process file (i.e., record) to which this document
        belongs.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Contract Folder Identifier</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Identifier</ns1:RepresentationTerm>
        <ns1:DataType>Identifier. Type</ns1:DataType> </ns1:Component>
    :ivar issue_date: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Issue Date.
        Date</ns1:DictionaryEntryName> <ns1:Definition>The date,
        assigned by the sender, on which this document was
        issued.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Date</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Date</ns1:RepresentationTerm>
        <ns1:DataType>Date. Type</ns1:DataType> </ns1:Component>
    :ivar issue_time: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Issue Time.
        Time</ns1:DictionaryEntryName> <ns1:Definition>The time,
        assigned by the sender, at which this document was
        issued.</ns1:Definition> <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Issue Time</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Time</ns1:RepresentationTerm>
        <ns1:DataType>Time. Type</ns1:DataType> </ns1:Component>
    :ivar guarantee_type_code: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Guarantee Type
        Code. Code</ns1:DictionaryEntryName> <ns1:Definition>A code
        signifying the type of the guarantee.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Guarantee Type Code</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Code</ns1:RepresentationTerm>
        <ns1:DataType>Code. Type</ns1:DataType> </ns1:Component>
    :ivar purpose: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Purpose.
        Text</ns1:DictionaryEntryName> <ns1:Definition>A textual
        description of the purpose of the bid bond
        guarantee.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Purpose</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar liability_amount: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Liability.
        Amount</ns1:DictionaryEntryName> <ns1:Definition>The liability
        amount (a monetary value) in the bid bond
        guarantee.</ns1:Definition> <ns1:Cardinality>1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Liability</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Amount</ns1:RepresentationTerm>
        <ns1:DataType>Amount. Type</ns1:DataType> </ns1:Component>
    :ivar constitution_code: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Constitution
        Code. Code</ns1:DictionaryEntryName> <ns1:Definition>The code
        stating the constitution means of the
        guarantee.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Constitution Code</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Code</ns1:RepresentationTerm>
        <ns1:DataType>Code. Type</ns1:DataType> </ns1:Component>
    :ivar note: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>BBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Note.
        Text</ns1:DictionaryEntryName> <ns1:Definition>Free-form text
        pertinent to this document, conveying information that is not
        contained explicitly in other structures.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Note</ns1:PropertyTerm>
        <ns1:RepresentationTerm>Text</ns1:RepresentationTerm>
        <ns1:DataType>Text. Type</ns1:DataType> </ns1:Component>
    :ivar applicable_period: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Applicable_
        Period. Period</ns1:DictionaryEntryName> <ns1:Definition>The
        specified period in the tendering process for which this bid
        bond guarantee is effective</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Applicable</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Period</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Period</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Period</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar applicable_regulation: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Applicable_
        Regulation. Regulation</ns1:DictionaryEntryName>
        <ns1:Definition>A reference to an applicable
        regulation.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Applicable</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Regulation</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Regulation</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Regulation</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar guarantee_document_reference: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Guarantee_
        Document Reference. Document Reference</ns1:DictionaryEntryName>
        <ns1:Definition>A reference to a legal
        document.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Guarantee</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Document Reference</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Document
        Reference</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Document
        Reference</ns1:RepresentationTerm> </ns1:Component>
    :ivar immobilized_security: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Immobilized
        Security</ns1:DictionaryEntryName> <ns1:Definition>Details of an
        immobilized security.</ns1:Definition>
        <ns1:Cardinality>0..n</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Immobilized Security</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Immobilized
        Security</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Immobilized
        Security</ns1:RepresentationTerm> </ns1:Component>
    :ivar signature: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate.
        Signature</ns1:DictionaryEntryName> <ns1:Definition>A signature
        applied to this document.</ns1:Definition>
        <ns1:Cardinality>1..n</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTerm>Signature</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Signature</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Signature</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar guarantor_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Guarantor_
        Party. Party</ns1:DictionaryEntryName> <ns1:Definition>The
        guarantee creditor organization that has the authority to charge
        bid bond guarantee credit.</ns1:Definition>
        <ns1:Cardinality>1</ns1:Cardinality> <ns1:ObjectClass>Guarantee
        Certificate</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Guarantor</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar interested_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Interested_
        Party. Party</ns1:DictionaryEntryName> <ns1:Definition>The party
        depositing the bid bond guarantee.</ns1:Definition>
        <ns1:Cardinality>1</ns1:Cardinality> <ns1:ObjectClass>Guarantee
        Certificate</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Interested</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
        </ns1:Component>
    :ivar beneficiary_party: <ns1:Component
        xmlns:ns1="urn:un:unece:uncefact:documentation:2">
        <ns1:ComponentType>ASBIE</ns1:ComponentType>
        <ns1:DictionaryEntryName>Guarantee Certificate. Beneficiary_
        Party. Party</ns1:DictionaryEntryName> <ns1:Definition>The
        beneficiary of the bid bond guarantee.</ns1:Definition>
        <ns1:Cardinality>0..1</ns1:Cardinality>
        <ns1:ObjectClass>Guarantee Certificate</ns1:ObjectClass>
        <ns1:PropertyTermQualifier>Beneficiary</ns1:PropertyTermQualifier>
        <ns1:PropertyTerm>Party</ns1:PropertyTerm>
        <ns1:AssociatedObjectClass>Party</ns1:AssociatedObjectClass>
        <ns1:RepresentationTerm>Party</ns1:RepresentationTerm>
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
    contract_folder_id: Optional[ContractFolderId] = field(
        default=None,
        metadata={
            "name": "ContractFolderID",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            "required": True,
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
    guarantee_type_code: Optional[GuaranteeTypeCode] = field(
        default=None,
        metadata={
            "name": "GuaranteeTypeCode",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    purpose: list[Purpose] = field(
        default_factory=list,
        metadata={
            "name": "Purpose",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        },
    )
    liability_amount: Optional[LiabilityAmount] = field(
        default=None,
        metadata={
            "name": "LiabilityAmount",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            "required": True,
        },
    )
    constitution_code: Optional[ConstitutionCode] = field(
        default=None,
        metadata={
            "name": "ConstitutionCode",
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
    applicable_period: Optional[ApplicablePeriod] = field(
        default=None,
        metadata={
            "name": "ApplicablePeriod",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    applicable_regulation: list[ApplicableRegulation] = field(
        default_factory=list,
        metadata={
            "name": "ApplicableRegulation",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    guarantee_document_reference: list[GuaranteeDocumentReference] = field(
        default_factory=list,
        metadata={
            "name": "GuaranteeDocumentReference",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )
    immobilized_security: list[ImmobilizedSecurity] = field(
        default_factory=list,
        metadata={
            "name": "ImmobilizedSecurity",
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
            "min_occurs": 1,
        },
    )
    guarantor_party: Optional[GuarantorParty] = field(
        default=None,
        metadata={
            "name": "GuarantorParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "required": True,
        },
    )
    interested_party: Optional[InterestedParty] = field(
        default=None,
        metadata={
            "name": "InterestedParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
            "required": True,
        },
    )
    beneficiary_party: Optional[BeneficiaryParty] = field(
        default=None,
        metadata={
            "name": "BeneficiaryParty",
            "type": "Element",
            "namespace": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        },
    )


@dataclass
class GuaranteeCertificate(GuaranteeCertificateType):
    """
    This element MUST be conveyed as the root element in any instance document
    based on this Schema expression.
    """

    class Meta:
        namespace = "urn:oasis:names:specification:ubl:schema:xsd:GuaranteeCertificate-2"
